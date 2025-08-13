import re
from urllib.parse import urljoin, urlparse
from playwright.sync_api import expect
from pages.home_page import HomePage

ORIGIN = "https://www.karma.de"
HOME = f"{ORIGIN}/home"

def is_internal(href: str) -> bool:
    if not href:
        return False
    href = href.strip()
    if href.startswith(("#", "mailto:", "tel:", "javascript:")):
        return False
    u = urlparse(href)
    # intern: relative Pfade oder gleiche Domain
    return (not u.netloc) or u.netloc.endswith("karma.de")

def test_internal_links_depth1(page):
    page.goto(HOME, wait_until="domcontentloaded")
    HomePage(page).accept_cookies_if_present()  # zentraler Helper

    # Cookie-Banner weg
    try:
        btn = page.get_by_role("button", name=re.compile(r"akzept|accept|zustimm|einverstanden", re.I))
        if btn.count() > 0:
            btn.first.click()
    except Exception:
        pass

    # Warte, bis überhaupt Links im DOM sind (nicht zwingend sichtbar)
    page.wait_for_selector("a[href]", state="attached", timeout=10000)

    # Einmal nach unten scrollen (falls Footer/Lazy-Content)
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    # Hrefs einsammeln (robust über nth(i))
    links = page.locator("a[href]")
    count = links.count()
    hrefs = set()
    for i in range(count):
        href = links.nth(i).get_attribute("href")
        if is_internal(href):
            absolute = urljoin(ORIGIN, href)
            hrefs.add(absolute)

    assert hrefs, "Keine internen Links gefunden"

    # Tiefe-1-Check: jede URL muss 200 liefern
    for url in sorted(hrefs):
        resp = page.request.get(url, timeout=15000)
        assert resp.status == 200, f"{url} → HTTP {resp.status}"
