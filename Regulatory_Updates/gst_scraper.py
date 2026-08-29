import re
import pymupdf

from playwright.sync_api import sync_playwright


# ============================================================
# CONFIGURATION
# ============================================================

BASE_URL = "https://taxinformation.cbic.gov.in/"

HEADLESS = True

NAVIGATION_TIMEOUT = 60000
PAGE_WAIT_MS = 8000

DOWNLOAD_TIMEOUT = 10000
CLICK_TIMEOUT = 15000

MAX_NAVIGATION_RETRIES = 3
RETRY_WAIT_MS = 5000

LATEST_MAX_DOCUMENTS = 10
SECTION_MAX_DOCUMENTS = 50


# ============================================================
# RESULT STRUCTURE
# ============================================================

def empty_result(error=None):

    return {
        "tax_rate_changes": [],
        "error": error
    }


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text):

    return re.sub(
        r"\s+",
        " ",
        text or ""
    ).strip()


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_pdf_text(pdf_bytes):

    if not pdf_bytes:
        return ""

    document = None

    try:

        document = pymupdf.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        pages = []

        for page in document:

            text = page.get_text()

            if text:

                pages.append(text)

        return "\n".join(pages)

    except Exception as e:

        print(
            "PDF extraction error:",
            e
        )

        return ""

    finally:

        if document is not None:

            document.close()


# ============================================================
# TAX RATE CLASSIFICATION ONLY
# ============================================================

def is_tax_rate_change(title,pdf_text):

    content = clean_text(
        f"{title} {pdf_text}"
    ).lower()


    # --------------------------------------------------------
    # Tax-rate related keywords
    # --------------------------------------------------------

    rate_keywords = [

        "tax rate",

        "tax rates",

        "rate of tax",

        "rates of tax",

        "gst rate",

        "gst rates",

        "rate of gst",

        "central tax (rate)",

        "central tax rate",

        "integrated tax (rate)",

        "integrated tax rate",

        "union territory tax (rate)",

        "union territory tax rate",

        "compensation cess",

        "rate amendment",

        "amendment of rate",

        "amendment in rate",

        "change in rate",

        "changes in rate",

        "changes to the rate",

        "schedule i",

        "schedule ii",

        "schedule iii"
    ]


    # --------------------------------------------------------
    # Check for rate-related information
    # --------------------------------------------------------

    for keyword in rate_keywords:

        if keyword in content:

            return True


    return False


def extract_notification_number(text):

    match = re.search(
        r"Notification\s+No\.?\s*([0-9]+/\d{4}-Central Tax\s*\(Rate\))",
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1)

    return None



def extract_date_issued(text):

    match = re.search(
        r"New Delhi,\s*the\s*(\d{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+\s*,?\s*\d{4})",
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1)

    return None



def extract_effective_date(text):

    match = re.search(
        r"shall come into force from\s*(.*?)(?:\.)",
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1)

    return None



def extract_issued_by(text):

    if (
        "MINISTRY OF FINANCE" in text.upper()
        and
        "DEPARTMENT OF REVENUE" in text.upper()
    ):

        return "Ministry of Finance, Department of Revenue (CBIC)"

    return None



def extract_legal_basis(text):

    result = []

    if "sub-section (1) of section 9" in text.lower():
        result.append("Section 9(1)")

    if "sub-section (5) of section 15" in text.lower():
        result.append("Section 15(5)")


    if result:

        return (
            " and ".join(result)
            +
            " of CGST Act, 2017"
        )

    return None



def extract_status(text):

    match = re.search(
        r"Notification No\.\s*([0-9]+/\d{4}-Central Tax\s*\(Rate\))",
        text,
        re.IGNORECASE
    )


    if match:

        return (
            "Latest amendment to Notification No. "
            +
            match.group(1)
        )

    return None


# ============================================================
# GET UPDATE TITLE
# ============================================================

def get_update_title(control):

    try:

        title = control.evaluate(
            """
            (el) => {

                let node = el;

                for (let i = 0; i < 10; i++) {

                    if (
                        !node ||
                        !node.parentElement
                    ) {

                        break;

                    }

                    node =
                        node.parentElement;

                    const text =
                        node.innerText || "";

                    if (

                        (
                            text.includes(
                                "Circular"
                            )

                            ||

                            text.includes(
                                "Notification"
                            )
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

        return clean_text(
            title
        )

    except Exception:

        try:

            return clean_text(
                control.inner_text()
            )

        except Exception:

            return ""


# ============================================================
# FIND CLICKABLE DOWNLOAD ELEMENT
# ============================================================

def get_clickable_element(
    control
):

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


# ============================================================
# INSPECT DOWNLOAD ELEMENT
# ============================================================

def inspect_download_element(
    control
):

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

                        node.tagName === "A"

                        ||

                        node.tagName === "BUTTON"

                        ||

                        node.getAttribute(
                            "onclick"
                        )

                        ||

                        node.getAttribute(
                            "role"
                        ) === "button"

                    ) {

                        return node.outerHTML;

                    }

                    node =
                        node.parentElement;

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


# ============================================================
# CAPTURE PDF
# ============================================================

def capture_pdf(
    page,
    control
):

    pdf_result = {

        "data": None,

        "url": None

    }


    responses = []


    # ========================================================
    # NETWORK RESPONSE HANDLER
    # ========================================================

    def handle_response(
        response
    ):

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

                or

                "download" in url.lower()

                or

                "view-pdf" in url.lower()

                or

                "document" in url.lower()

                or

                "application/pdf"
                in content_type

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


                responses.append(
                    response
                )


        except Exception:

            pass


    page.on(
        "response",
        handle_response
    )


    clickable = (
        get_clickable_element(
            control
        )
    )


    inspect_download_element(
        clickable
    )


    try:

        # ====================================================
        # METHOD 1
        # BROWSER DOWNLOAD EVENT
        # ====================================================

        try:

            print(
                "Trying browser download..."
            )


            with page.expect_download(
                timeout=DOWNLOAD_TIMEOUT
            ) as download_info:

                clickable.click(
                    force=True,
                    timeout=CLICK_TIMEOUT
                )


            download = (
                download_info.value
            )


            print(
                "DOWNLOAD EVENT RECEIVED"
            )


            print(
                "Download URL:",
                download.url
            )


            path = download.path()


            if path:

                with open(
                    path,
                    "rb"
                ) as file:

                    data = file.read()


                print(
                    "Downloaded bytes:",
                    len(data)
                )


                if (

                    data

                    and

                    data.startswith(
                        b"%PDF"
                    )

                ):

                    pdf_result["data"] = (
                        data
                    )

                    pdf_result["url"] = (
                        download.url
                    )


                    print(
                        "PDF CAPTURED FROM DOWNLOAD"
                    )


                    return pdf_result


        except Exception as e:

            print(
                "Download event failed:",
                e
            )


        # ====================================================
        # METHOD 2
        # NORMAL CLICK
        # ====================================================

        try:

            print(
                "Trying normal click..."
            )


            clickable.click(
                force=True,
                timeout=CLICK_TIMEOUT
            )


        except Exception as e:

            print(
                "Normal click failed:",
                e
            )


            # =================================================
            # JAVASCRIPT CLICK
            # =================================================

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


        # ====================================================
        # METHOD 3
        # NETWORK RESPONSE
        # ====================================================

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


                if (

                    data

                    and

                    data.startswith(
                        b"%PDF"
                    )

                ):

                    pdf_result["data"] = (
                        data
                    )

                    pdf_result["url"] = (
                        response.url
                    )


                    print(
                        "*** PDF SUCCESSFULLY CAPTURED ***"
                    )


                    return pdf_result


            except Exception as e:

                print(
                    "Could not read response:",
                    e
                )


        # ====================================================
        # METHOD 4
        # SEARCH PAGE SOURCE
        # ====================================================

        try:

            html = page.content()


            matches = re.findall(
                r"""https?://[^"']+\.pdf[^"']*""",
                html,
                re.IGNORECASE
            )


            if matches:

                pdf_url = matches[0]


                print(
                    "PDF URL found:",
                    pdf_url
                )


                response = (
                    page.request.get(
                        pdf_url,
                        timeout=60000
                    )
                )


                data = response.body()


                if (

                    data

                    and

                    data.startswith(
                        b"%PDF"
                    )

                ):

                    pdf_result["data"] = (
                        data
                    )

                    pdf_result["url"] = (
                        pdf_url
                    )


                    return pdf_result


        except Exception as e:

            print(
                "PDF URL search failed:",
                e
            )


        return pdf_result


    finally:

        page.remove_listener(
            "response",
            handle_response
        )


# ============================================================
# PROCESS CURRENT PAGE
# ============================================================

def process_current_page(
    page,
    result,
    processed,
    max_documents=30
):

    controls = page.get_by_text(
        "Download file in English language",
        exact=False
    )


    count = controls.count()


    print(
        "\nEnglish download controls found:",
        count
    )


    if count == 0:

        return 0


    processed_count = 0


    limit = min(
        count,
        max_documents
    )


    for index in range(
        limit
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


        # ====================================================
        # TITLE
        # ====================================================

        title = get_update_title(
            control
        )


        print(
            "TITLE:",
            title[:500]
        )


        # ====================================================
        # CAPTURE PDF
        # ====================================================

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


        if not pdf_data:

            print(
                "PDF was not captured."
            )

            continue


        # ====================================================
        # DUPLICATE CHECK
        # ====================================================

        if (

            pdf_url

            and

            pdf_url in processed

        ):

            print(
                "Already processed."
            )

            continue


        if pdf_url:

            processed.add(
                pdf_url
            )


        # ====================================================
        # PDF EXTRACTION
        # ====================================================

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


        # ====================================================
        # TAX RATE CHECK ONLY
        # ====================================================

        tax_rate_match = (
            is_tax_rate_change(
                title,
                pdf_text
            )
        )


        print(
            "TAX RATE CHANGE:",
            tax_rate_match
        )


        if not tax_rate_match:

            print(
                "Not a tax-rate update. Skipping."
            )

            continue


        # ====================================================
        # RESULT
        # ====================================================

        item = {

            "notification_number":
                extract_notification_number(pdf_text),

            "date_issued":
                extract_date_issued(pdf_text),

            "effective_date":
                extract_effective_date(pdf_text),

            "issued_by":
                extract_issued_by(pdf_text),

            "legal_basis":
                extract_legal_basis(pdf_text),

            "status":
                extract_status(pdf_text),

            "title":
                title,

            "source_url":
                pdf_url
        }

        result[
            "tax_rate_changes"
        ].append(
            item
        )


        processed_count += 1


    return processed_count


# ============================================================
# OPEN CBIC SECTION
# ============================================================

def open_section(
    page,
    section_text
):

    print(
        f"\nLooking for: {section_text}"
    )


    locator = page.get_by_text(
        section_text,
        exact=False
    ).first


    if locator.count() == 0:

        print(
            "Section link not found."
        )

        return False


    try:

        anchor = locator.locator(
            "xpath=ancestor::a[1]"
        ).first


        if anchor.count() > 0:

            href = (
                anchor.get_attribute(
                    "href"
                )
            )


            print(
                "Section href:",
                href
            )


            if href:

                if href.startswith(
                    "/"
                ):

                    full_url = (
                        "https://taxinformation.cbic.gov.in"
                        + href
                    )

                else:

                    full_url = href


                print(
                    "Opening:",
                    full_url
                )


                page.goto(
                    full_url,
                    wait_until="commit",
                    timeout=60000
                )


            else:

                anchor.click(
                    force=True
                )


        else:

            locator.click(
                force=True
            )


        page.wait_for_timeout(
            7000
        )


        return True


    except Exception as e:

        print(
            "Section navigation failed:",
            e
        )

        return False


# ============================================================
# OPEN CBIC WITH RETRY
# ============================================================

def open_cbic_with_retry(
    page
):

    last_error = None


    for attempt in range(
        MAX_NAVIGATION_RETRIES
    ):

        try:

            print(
                f"Attempt {attempt + 1}/"
                f"{MAX_NAVIGATION_RETRIES}"
            )


            page.goto(
                BASE_URL,
                wait_until="commit",
                timeout=NAVIGATION_TIMEOUT
            )


            page.wait_for_timeout(
                PAGE_WAIT_MS
            )


            return


        except Exception as e:

            last_error = e


            print(
                "CBIC connection error:",
                e
            )


            if (
                attempt
                <
                MAX_NAVIGATION_RETRIES - 1
            ):

                page.wait_for_timeout(
                    RETRY_WAIT_MS
                )


    raise last_error


# ============================================================
# MAIN GST TAX-RATE SCRAPER
# ============================================================

def scrape_gst_updates():

    result = empty_result()


    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=HEADLESS
        )


        page = browser.new_page()


        try:

            # =================================================
            # OPEN CBIC
            # =================================================

            print(
                "\nOpening CBIC..."
            )


            open_cbic_with_retry(
                page
            )


            # =================================================
            # DEBUG PAGE TEXT
            # =================================================

            print(
                "\n===== CBIC PAGE TEXT ====="
            )


            try:

                body_text = (
                    page.locator(
                        "body"
                    ).inner_text()
                )


                print(
                    body_text[:12000]
                )


            except Exception as e:

                print(
                    "Could not read page text:",
                    e
                )


            print(
                "===== END CBIC PAGE TEXT =====\n"
            )


            processed = set()


            # =================================================
            # 1. LATEST UPDATES
            # =================================================

            print(
                "\n========== LATEST UPDATES =========="
            )


            process_current_page(
                page,
                result,
                processed,
                max_documents=
                    LATEST_MAX_DOCUMENTS
            )


            # =================================================
            # 2. GST NOTIFICATIONS
            # =================================================

            print(
                "\n========== GST NOTIFICATIONS =========="
            )


            page.goto(
                BASE_URL,
                wait_until="commit",
                timeout=NAVIGATION_TIMEOUT
            )


            page.wait_for_timeout(
                5000
            )


            opened = open_section(
                page,
                "View GST Notifications"
            )


            if opened:

                print(
                    "GST Notifications page:",
                    page.url
                )


                process_current_page(
                    page,
                    result,
                    processed,
                    max_documents=
                        SECTION_MAX_DOCUMENTS
                )


            else:

                print(
                    "Could not open GST Notifications."
                )


            # =================================================
            # 3. GST CIRCULARS
            # =================================================

            print(
                "\n========== GST CIRCULARS =========="
            )


            page.goto(
                BASE_URL,
                wait_until="commit",
                timeout=NAVIGATION_TIMEOUT
            )


            page.wait_for_timeout(
                5000
            )


            opened = open_section(
                page,
                "View GST Circulars"
            )


            if opened:

                print(
                    "GST Circulars page:",
                    page.url
                )


                process_current_page(
                    page,
                    result,
                    processed,
                    max_documents=
                        SECTION_MAX_DOCUMENTS
                )


            else:

                print(
                    "Could not open GST Circulars."
                )


            # =================================================
            # FINAL RESULT
            # =================================================

            result["error"] = None


            print(
                "\n========== FINAL RESULT =========="
            )


            print(
                "tax_rate_changes:",
                len(
                    result[
                        "tax_rate_changes"
                    ]
                )
            )


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


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    import json


    output = scrape_gst_updates()


    print(
        "\n========== JSON OUTPUT =========="
    )


    print(
        json.dumps(
            output,
            indent=2,
            ensure_ascii=False
        )
    )