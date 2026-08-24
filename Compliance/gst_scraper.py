import re
import fitz

from playwright.sync_api import sync_playwright


BASE_URL = "https://taxinformation.cbic.gov.in/"


# =========================================================
# RESULT STRUCTURE
# =========================================================

def empty_result(error=None):
    return {
        "return_deadlines": [],
        "tax_rate_changes": [],
        "compliance_extensions": [],
        "portal_updates": [],
        "error": error
    }


# =========================================================
# TEXT CLEANING
# =========================================================

def clean_text(text):
    return re.sub(r"\s+", " ", text or "").strip()


# =========================================================
# PDF TEXT EXTRACTION
# =========================================================

def extract_pdf_text(pdf_bytes):

    if not pdf_bytes:
        return ""

    try:

        document = fitz.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        pages = []

        for page in document:

            text = page.get_text()

            if text:
                pages.append(text)

        document.close()

        return "\n".join(pages)

    except Exception as e:

        print("PDF extraction error:", e)

        return ""


# =========================================================
# CLASSIFICATION
# =========================================================

def classify_update(title, pdf_text):

    content = clean_text(
        f"{title} {pdf_text}"
    ).lower()

    categories = []

    # =====================================================
    # 1. RETURN DEADLINES
    #
    # We require BOTH:
    #   A. GST return / filing context
    #   B. deadline/date context
    #
    # This avoids treating every document containing
    # "return" or "filing" as a deadline.
    # =====================================================

    return_context = [
        "gstr-1",
        "gstr 1",
        "gstr-3b",
        "gstr 3b",
        "gstr-4",
        "gstr 4",
        "gstr-5",
        "gstr 5",
        "gstr-6",
        "gstr 6",
        "gstr-7",
        "gstr 7",
        "gstr-8",
        "gstr 8",
        "gstr-9",
        "gstr 9",
        "gstr-9c",
        "gstr 9c",
        "gstr-10",
        "gstr 10",
        "gstr-11",
        "gstr 11",
        "gst return",
        "gst returns",
        "return filing",
        "filing of return",
        "filing returns",
        "tax return"
    ]

    deadline_context = [
        "due date",
        "due dates",
        "last date",
        "last dates",
        "date for filing",
        "date of filing",
        "filing date",
        "deadline",
        "deadlines",
        "on or before",
        "within the prescribed",
        "extended up to",
        "extended till",
        "extended to",
        "extension of due date"
    ]

    has_return_context = any(
        keyword in content
        for keyword in return_context
    )

    has_deadline_context = any(
        keyword in content
        for keyword in deadline_context
    )

    # Also detect explicit return + date combinations
    return_date_pattern = re.search(
        r"(gstr[- ]?\d+[a-z]?).{0,120}"
        r"(due date|last date|deadline|"
        r"extended|filing date)",
        content,
        re.IGNORECASE
    )

    if (
        has_return_context
        and has_deadline_context
    ) or return_date_pattern:

        categories.append(
            "return_deadlines"
        )

    # =====================================================
    # 2. TAX RATE CHANGES
    #
    # KEEPING THE WORKING LOGIC
    # =====================================================

    rate_keywords = [
        "tax rate",
        "rate of tax",
        "gst rate",
        "rate of gst",
        "central tax (rate)",
        "integrated tax (rate)",
        "union territory tax (rate)",
        "compensation cess",
        "rate amendment",
        "amendment of rate",
        "tax rates",
        "rates of tax",
        "schedule i",
        "schedule ii",
        "schedule iii"
    ]

    if any(
        keyword in content
        for keyword in rate_keywords
    ):

        categories.append(
            "tax_rate_changes"
        )

    # =====================================================
    # 3. COMPLIANCE EXTENSIONS
    #
    # Require an actual extension / waiver / relaxation
    # context rather than simply "filing".
    # =====================================================

    extension_keywords = [
        "extension",
        "extended",
        "extend the due date",
        "extension of due date",
        "extended up to",
        "extended till",
        "extended to",
        "amnesty",
        "relaxation",
        "relaxation in",
        "relaxation of",
        "waiver",
        "waive",
        "waived",
        "late fee waiver",
        "late fee waived",
        "interest waiver",
        "interest waived",
        "penalty waiver",
        "penalty waived",
        "condonation",
        "condonation of delay",
        "time limit extended",
        "period extended"
    ]

    compliance_subjects = [
        "return",
        "gstr",
        "gst",
        "filing",
        "late fee",
        "interest",
        "penalty",
        "compliance",
        "registration",
        "payment",
        "taxpayer",
        "invoice",
        "e-invoice",
        "e-way bill",
        "appeal",
        "application"
    ]

    has_extension = any(
        keyword in content
        for keyword in extension_keywords
    )

    has_compliance_subject = any(
        keyword in content
        for keyword in compliance_subjects
    )

    if (
        has_extension
        and has_compliance_subject
    ):

        categories.append(
            "compliance_extensions"
        )

    # =====================================================
    # 4. PORTAL UPDATES
    #
    # KEEPING THE WORKING LOGIC
    # =====================================================

    portal_keywords = [
        "portal",
        "gst portal",
        "common portal",
        "portal functionality",
        "portal facility",
        "filing facility",
        "online filing",
        "online facility",
        "e-invoice",
        "einvoice",
        "e-way bill",
        "eway bill"
    ]

    if any(
        keyword in content
        for keyword in portal_keywords
    ):

        categories.append(
            "portal_updates"
        )

    return categories


# =========================================================
# GET UPDATE TITLE
# =========================================================

def get_update_title(control):

    try:

        title = control.evaluate(
            """
            (el) => {

                let node = el;

                for (let i = 0; i < 10; i++) {

                    if (!node.parentElement) {
                        break;
                    }

                    node = node.parentElement;

                    const text =
                        node.innerText || "";

                    if (
                        (
                            text.includes("Circular") ||
                            text.includes("Notification")
                        )
                        &&
                        text.length > 30
                        &&
                        text.length < 2000
                    ) {
                        return text;
                    }
                }

                return el.innerText || "";
            }
            """
        )

        return clean_text(title)

    except Exception:

        return clean_text(
            control.inner_text()
        )


# =========================================================
# INSPECT DOWNLOAD ELEMENT
# =========================================================

def inspect_download_element(control):

    try:

        html = control.evaluate(
            """
            (el) => {

                let node = el;

                for (let i = 0; i < 10; i++) {

                    if (!node) {
                        break;
                    }

                    if (
                        node.tagName === "A" ||
                        node.tagName === "BUTTON" ||
                        node.getAttribute("onclick") ||
                        node.getAttribute("role") === "button"
                    ) {
                        return node.outerHTML;
                    }

                    node = node.parentElement;
                }

                return el.outerHTML;
            }
            """
        )

        print(
            "\n===== DOWNLOAD ELEMENT ====="
        )

        print(html)

        print(
            "===== END DOWNLOAD ELEMENT =====\n"
        )

    except Exception as e:

        print(
            "Element inspection failed:",
            e
        )


# =========================================================
# FIND REAL CLICKABLE ELEMENT
# =========================================================

def get_clickable_element(control):

    try:

        clickable = control.locator(
            "xpath=ancestor-or-self::*["
            "self::a or "
            "self::button or "
            "@role='button' or "
            "@onclick"
            "]"
        ).first

        if clickable.count() > 0:
            return clickable

    except Exception:
        pass

    return control


# =========================================================
# CAPTURE PDF
# =========================================================

def capture_pdf(page, control):

    pdf_result = {
        "data": None,
        "url": None
    }

    responses = []

    def handle_response(response):

        try:

            url = response.url

            content_type = (
                response.headers.get(
                    "content-type",
                    ""
                ).lower()
            )

            interesting = (
                "pdf" in url.lower()
                or "download" in url.lower()
                or "view-pdf" in url.lower()
                or "document" in url.lower()
                or "application/pdf" in content_type
            )

            if interesting:

                print(
                    "\nNETWORK RESPONSE"
                )

                print(
                    "URL:",
                    url
                )

                print(
                    "CONTENT TYPE:",
                    content_type
                )

                responses.append(response)

        except Exception:
            pass

    page.on(
        "response",
        handle_response
    )

    clickable = get_clickable_element(
        control
    )

    inspect_download_element(
        clickable
    )

    try:

        # =================================================
        # METHOD 1: DOWNLOAD EVENT
        # =================================================

        try:
                print("Trying browser download...")

                with page.expect_download(timeout=8000) as download_info:
                    clickable.click(
                        force=True,
                        timeout=15000
                    )

                download = download_info.value

                print("DOWNLOAD EVENT RECEIVED")
                print("Download URL:", download.url)

                path = download.path()

                if path:
                        with open(path, "rb") as file:
                            data = file.read()

                        if data.startswith(b"%PDF"):
                            pdf_result["data"] = data
                            pdf_result["url"] = download.url

                            print("PDF CAPTURED FROM DOWNLOAD")

                        return pdf_result

        except Exception as e:
               print("Download failed:", e)

    

        # =================================================
        # METHOD 2: NORMAL CLICK
        # =================================================

        try:

            print(
                "Trying normal click..."
            )

            clickable.click(
                force=True,
                timeout=15000
            )

        except Exception as e:

            print(
                "Normal click failed:",
                e
            )

            try:

                clickable.evaluate(
                    "(el) => el.click()"
                )

                print(
                    "JavaScript click executed."
                )

            except Exception as js_error:

                print(
                    "JavaScript click failed:",
                    js_error
                )

        page.wait_for_timeout(
            8000
        )

        # =================================================
        # READ NETWORK RESPONSES
        # =================================================

        print(
            "\nChecking captured responses..."
        )

        for response in responses:

            try:

                data = response.body()

                print(
                    "Response size:",
                    len(data),
                    "URL:",
                    response.url
                )

                if data.startswith(
                    b"%PDF"
                ):

                    pdf_result["data"] = data
                    pdf_result["url"] = (
                        response.url
                    )

                    print(
                        "\n*** PDF SUCCESSFULLY CAPTURED ***"
                    )

                    return pdf_result

            except Exception as e:

                print(
                    "Could not read response:",
                    e
                )

        # =================================================
        # METHOD 3: CHECK PAGE HTML FOR PDF
        # =================================================

        try:

            html = page.content()

            matches = re.findall(
                r'https?://[^"\']+\.pdf[^"\']*',
                html,
                re.IGNORECASE
            )

            if matches:

                pdf_url = matches[0]

                print(
                    "PDF URL found in page:",
                    pdf_url
                )

                try:

                    response = page.request.get(
                        pdf_url,
                        timeout=60000
                    )

                    data = response.body()

                    if data.startswith(
                        b"%PDF"
                    ):

                        pdf_result["data"] = data
                        pdf_result["url"] = pdf_url

                        return pdf_result

                except Exception as e:

                    print(
                        "PDF URL request failed:",
                        e
                    )

        except Exception:
            pass

    finally:

        page.remove_listener(
            "response",
            handle_response
        )

    return pdf_result


# =========================================================
# MAIN GST SCRAPER
# =========================================================

def scrape_gst_updates():

    result = empty_result()

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        try:

            # =================================================
            # OPEN CBIC
            # =================================================

            print(
                "\nOpening CBIC..."
            )

            page.goto(
                BASE_URL,
                wait_until="commit",
                timeout=30000
            )

            page.wait_for_timeout(
                8000
            )

            # =================================================
            # WAIT FOR LATEST UPDATES
            # =================================================

            try:

                page.get_by_text(
                    "Latest Updates",
                    exact=False
                ).first.wait_for(
                    state="visible",
                    timeout=15000
                )

                print(
                    "Latest Updates section detected."
                )

            except Exception:

                print(
                    "Latest Updates section "
                    "wait timed out."
                )

            page.wait_for_timeout(
                5000
            )

            # =================================================
            # DEBUG PAGE TEXT
            # =================================================

            print(
                "\n===== CBIC PAGE TEXT ====="
            )

            body_text = page.locator(
                "body"
            ).inner_text()

            print(
                body_text[:12000]
            )

            print(
                "===== END CBIC PAGE TEXT =====\n"
            )

            # =================================================
            # ENGLISH DOWNLOAD CONTROLS
            # =================================================

            controls = page.get_by_text(
                "Download file in English language",
                exact=False
            )

            count = controls.count()

            print(
                "English download controls found:",
                count
            )

            if count == 0:

                result["error"] = (
                    "CBIC page loaded, but English "
                    "download controls were not found."
                )

                return result

            # =================================================
            # PROCESS AVAILABLE UPDATES
            # =================================================

            processed = set()

            for index in range(
                min(count, 10)
            ):

                control = controls.nth(
                    index
                )

                print(
                    "\n================================"
                )

                print(
                    "UPDATE:",
                    index + 1
                )

                # =================================================
                # TITLE
                # =================================================

                title = get_update_title(
                    control
                )

                print(
                    "TITLE:",
                    title[:500]
                )

                # =================================================
                # PDF
                # =================================================

                pdf = capture_pdf(
                    page,
                    control
                )

                pdf_data = pdf[
                    "data"
                ]

                pdf_url = pdf[
                    "url"
                ]

                print(
                    "PDF URL:",
                    pdf_url
                )

                # =================================================
                # DUPLICATE CHECK
                # =================================================

                if (
                    pdf_url
                    and pdf_url in processed
                ):

                    print(
                        "Already processed."
                    )

                    continue

                if pdf_url:

                    processed.add(
                        pdf_url
                    )

                # =================================================
                # EXTRACT PDF TEXT
                # =================================================

                pdf_text = extract_pdf_text(
                    pdf_data
                )

                print(
                    "PDF TEXT LENGTH:",
                    len(pdf_text)
                )

                if not pdf_text:

                    print(
                        "No PDF text extracted."
                    )

                    continue

                # =================================================
                # CLASSIFY
                # =================================================

                categories = classify_update(
                    title,
                    pdf_text
                )

                print(
                    "CATEGORIES:",
                    categories
                )

                # =================================================
                # CREATE ITEM
                # =================================================

                item = {
                    "title": title,
                    "url": pdf_url,
                    "content_preview": clean_text(
                        pdf_text
                    )[:1200]
                }

                # =================================================
                # ADD TO CATEGORIES
                # =================================================

                for category in categories:

                    result[
                        category
                    ].append(item)

            result["error"] = None

            return result

        except Exception as e:

            print(
                "\nSCRAPER ERROR:",
                repr(e)
            )

            result["error"] = (
                f"GST scraping failed: {str(e)}"
            )

            return result

        finally:

            browser.close()