import re
import json
from datetime import datetime
from urllib.parse import urljoin

import requests
import pymupdf
from bs4 import BeautifulSoup


# ============================================================
# CONFIGURATION
# ============================================================

BASE_URL = "https://www.labour.gov.in"

TIMEOUT = 30

MAX_DOCUMENTS = 30

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/139.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,"
        "application/pdf;q=0.9,*/*;q=0.8"
    ),
    "Accept-Language": "en-IN,en;q=0.9",
}


# ============================================================
# OFFICIAL LABOUR SOURCES
# ============================================================

SOURCE_PAGES = [

    # Labour Ministry home / What's New
    f"{BASE_URL}/",

    # Labour Codes
    f"{BASE_URL}/labourlaw/code-on-wages",

    f"{BASE_URL}/policies/safety-health-and-environment-work-place",

    # Official sitemap
    f"{BASE_URL}/en/site-map",

]


# ============================================================
# OFFICIAL DOCUMENT FALLBACKS
#
# These are official labour.gov.in documents.
# They are used even if the Labour website's HTML page
# is temporarily blocked.
# ============================================================

OFFICIAL_DOCUMENTS = [

    # --------------------------------------------------------
    # MINIMUM WAGES / CODE ON WAGES
    # --------------------------------------------------------

    {
        "url":
        "https://www.labour.gov.in/static/uploads/2026/01/"
        "44b4b68890bb457be71155b25fcda804.pdf",

        "title":
        "Wages (Central) Rules / Minimum Wages"
    },

    {
        "url":
        "https://www.labour.gov.in/static/uploads/2026/02/"
        "83978455025732b99b0165def80ab171.pdf",

        "title":
        "Compliance Handbook - Code on Wages, 2019"
    },

    {
        "url":
        "https://www.labour.gov.in/static/uploads/2026/03/"
        "a4ccf4c6d97c4f1f36a6d83f8c64213d.pdf",

        "title":
        "Code on Wages - FAQs"
    },


    # --------------------------------------------------------
    # SOCIAL SECURITY
    # --------------------------------------------------------

    {
        "url":
        "https://www.labour.gov.in/static/uploads/2026/03/"
        "d70bb9f7e87ec48bd64fde40329f9c09.pdf",

        "title":
        "Key Provisions under Code on Social Security, 2020"
    },


    # --------------------------------------------------------
    # WORKPLACE SAFETY
    # --------------------------------------------------------

    {
        "url":
        "https://www.labour.gov.in/static/uploads/2026/05/"
        "71e30b7362363ceb07423af6fd804b69.pdf",

        "title":
        "Occupational Safety Health and Working Conditions Notification"
    },

    {
        "url":
        "https://www.labour.gov.in/static/uploads/2026/02/"
        "dde0e6667243665c258b52d2c36db66a.pdf",

        "title":
        "Draft Occupational Safety Health and Working Conditions Regulations"
    },

]


# ============================================================
# RESULT
# ============================================================

def empty_result():

    return {

        "last_updated":
            datetime.now().isoformat(),

        "minimum_wages": [],

        "social_security_contributions": [],

        "workplace_safety": [],

        "error": None
    }


# ============================================================
# HTTP SESSION
# ============================================================

def create_session():

    session = requests.Session()

    session.headers.update(
        HEADERS
    )

    return session


# ============================================================
# CLEAN TEXT
# ============================================================

def clean_text(text):

    return re.sub(
        r"\s+",
        " ",
        text or ""
    ).strip()


# ============================================================
# DOWNLOAD URL
# ============================================================

def download_document(
    session,
    url
):

    try:

        print(
            "Downloading:",
            url
        )

        response = session.get(
            url,
            timeout=TIMEOUT
        )

        print(
            "HTTP:",
            response.status_code,
            "SIZE:",
            len(response.content)
        )

        if response.status_code != 200:

            return None

        data = response.content

        if data.startswith(b"%PDF"):

            return data

        content_type = (
            response.headers.get(
                "content-type",
                ""
            ).lower()
        )

        if "pdf" in content_type:

            return data

        return None

    except Exception as e:

        print(
            "Download error:",
            e
        )

        return None


# ============================================================
# PDF EXTRACTION
# ============================================================

def extract_pdf_text(
    pdf_bytes
):

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

        if document:

            document.close()


# ============================================================
# DATE EXTRACTION
# ============================================================

def extract_date(text):

    patterns = [

        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b",

        r"\b\d{1,2}(?:st|nd|rd|th)?\s+"
        r"(?:January|February|March|April|May|June|"
        r"July|August|September|October|November|December)"
        r"(?:,)?\s+\d{4}\b",

        r"\b(?:January|February|March|April|May|June|"
        r"July|August|September|October|November|December)"
        r"\s+\d{1,2},\s+\d{4}\b"

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return match.group(0)

    return None


# ============================================================
# NOTIFICATION NUMBER
# ============================================================

def extract_notification_number(
    text
):

    patterns = [

        r"Notification\s+No\.?\s*([A-Za-z0-9./()_-]+)",

        r"G\.S\.R\.?\s*([A-Za-z0-9./()_-]+)",

        r"S\.O\.?\s*([A-Za-z0-9./()_-]+)",

        r"No\.\s*([A-Za-z0-9./()_-]+)"

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return match.group(1)

    return None


# ============================================================
# CLASSIFICATION
# ============================================================

def classify_document(
    title,
    text
):

    content = clean_text(
        title + " " + text
    ).lower()


    categories = set()


    # ========================================================
    # MINIMUM WAGES
    # ========================================================

    wage_keywords = [

        "minimum wage",

        "minimum wages",

        "minimum rate of wages",

        "minimum rates of wages",

        "minimum wage rate",

        "minimum wages act",

        "code on wages",

        "wage rate",

        "wage rates",

        "floor wage",

        "dearness allowance",

        "variable dearness allowance",

        "wages payable",

        "wage period",

        "payment of wages"

    ]


    if any(
        keyword in content
        for keyword in wage_keywords
    ):

        categories.add(
            "minimum_wages"
        )


    # ========================================================
    # SOCIAL SECURITY
    # ========================================================

    social_keywords = [

        "code on social security",

        "social security",

        "provident fund",

        "provident funds",

        "employee provident fund",

        "employees provident fund",

        "epf",

        "epfo",

        "employee state insurance",

        "employees state insurance",

        "esic",

        "esi",

        "pension scheme",

        "employees pension scheme",

        "social security contribution",

        "social security contributions",

        "gratuity",

        "maternity benefit"

    ]


    if any(
        keyword in content
        for keyword in social_keywords
    ):

        categories.add(
            "social_security_contributions"
        )


    # ========================================================
    # WORKPLACE SAFETY
    # ========================================================

    safety_keywords = [

        "occupational safety",

        "occupational health",

        "occupational safety and health",

        "workplace safety",

        "working conditions",

        "health and working conditions",

        "industrial safety",

        "factory safety",

        "safety standards",

        "safety measures",

        "occupational health and safety",

        "code on occupational safety",

        "osh code",

        "working hours",

        "hours of work",

        "welfare facilities",

        "hazardous process",

        "hazardous processes",

        "safety regulations"

    ]


    if any(
        keyword in content
        for keyword in safety_keywords
    ):

        categories.add(
            "workplace_safety"
        )


    return categories


# ============================================================
# CREATE DOCUMENT ITEM
# ============================================================

def create_item(
    title,
    url,
    text
):

    return {

        "title":
            clean_text(title),

        "notification_number":
            extract_notification_number(
                text
            ),

        "date":
            extract_date(text),

        "summary":
            clean_text(text)[:2500],

        "official_source_url":
            url

    }


# ============================================================
# DISCOVER PDF LINKS FROM OFFICIAL HTML
# ============================================================

def discover_official_pdfs(
    session
):

    documents = []


    for source_url in SOURCE_PAGES:

        print(
            "\nChecking official page:"
        )

        print(
            source_url
        )

        try:

            response = session.get(
                source_url,
                timeout=TIMEOUT
            )

            print(
                "HTTP:",
                response.status_code
            )

            if response.status_code != 200:

                continue


            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )


            for anchor in soup.find_all(
                "a",
                href=True
            ):

                href = anchor.get(
                    "href"
                )

                text = clean_text(
                    anchor.get_text(
                        " ",
                        strip=True
                    )
                )


                if not href:

                    continue


                full_url = urljoin(
                    source_url,
                    href
                )


                if (
                    "labour.gov.in"
                    not in full_url
                ):

                    continue


                if (
                    ".pdf"
                    not in full_url.lower()
                ):

                    continue


                documents.append({

                    "url":
                        full_url,

                    "title":
                        text or "Labour Ministry Document"

                })


        except Exception as e:

            print(
                "Page discovery error:",
                e
            )


    return documents


# ============================================================
# REMOVE DUPLICATES
# ============================================================

def unique_documents(
    documents
):

    seen = set()

    result = []


    for document in documents:

        url = document["url"]


        if url in seen:

            continue


        seen.add(url)

        result.append(
            document
        )


    return result


# ============================================================
# PROCESS DOCUMENT
# ============================================================

def process_document(
    session,
    document,
    result,
    processed
):

    url = document["url"]

    title = document["title"]


    if url in processed:

        return


    processed.add(url)


    print(
        "\n----------------------------------------"
    )

    print(
        "DOCUMENT:",
        title
    )

    print(
        "URL:",
        url
    )


    pdf_bytes = download_document(
        session,
        url
    )


    if not pdf_bytes:

        print(
            "Not a PDF or download failed."
        )

        return


    text = extract_pdf_text(
        pdf_bytes
    )


    if not text:

        print(
            "No PDF text extracted."
        )

        return


    print(
        "PDF TEXT:",
        len(text),
        "characters"
    )


    categories = classify_document(
        title,
        text
    )


    print(
        "CATEGORIES:",
        categories
    )


    if not categories:

        print(
            "No target category."
        )

        return


    item = create_item(
        title,
        url,
        text
    )


    for category in categories:

        if category not in result:

            continue


        # Avoid duplicate entries
        existing_urls = {

            x["official_source_url"]

            for x in result[category]

        }


        if url not in existing_urls:

            result[
                category
            ].append(
                item.copy()
            )


# ============================================================
# MAIN SCRAPER
# ============================================================

def scrape_labour_updates():

    result = empty_result()

    session = create_session()

    processed = set()


    try:

        print(
            "\n======================================"
        )

        print(
            "LABOUR COMPLIANCE SCRAPER"
        )

        print(
            "======================================"
        )


        # ====================================================
        # 1. DISCOVER LIVE OFFICIAL PDF LINKS
        # ====================================================

        discovered = (
            discover_official_pdfs(
                session
            )
        )


        print(
            "\nLIVE PDF DOCUMENTS FOUND:",
            len(discovered)
        )


        # ====================================================
        # 2. ADD KNOWN OFFICIAL DOCUMENTS
        #
        # These guarantee that the scraper still has
        # official current documents when the Labour site's
        # HTML layer is unavailable.
        # ====================================================

        documents = (
            discovered
            +
            OFFICIAL_DOCUMENTS
        )


        documents = unique_documents(
            documents
        )


        print(
            "TOTAL DOCUMENTS:",
            len(documents)
        )


        # ====================================================
        # 3. PROCESS DOCUMENTS
        # ====================================================

        for document in documents[:
            MAX_DOCUMENTS
        ]:

            process_document(

                session,

                document,

                result,

                processed

            )


        # ====================================================
        # 4. FINAL RESULT
        # ====================================================

        result["last_updated"] = (
            datetime.now().isoformat()
        )


        result["error"] = None


        print(
            "\n======================================"
        )

        print(
            "FINAL RESULT"
        )

        print(
            "Minimum Wages:",
            len(
                result[
                    "minimum_wages"
                ]
            )
        )

        print(
            "Social Security:",
            len(
                result[
                    "social_security_contributions"
                ]
            )
        )

        print(
            "Workplace Safety:",
            len(
                result[
                    "workplace_safety"
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
            f"Labour scraping failed: {str(e)}"
        )


        return result


    finally:

        session.close()


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    output = scrape_labour_updates()


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