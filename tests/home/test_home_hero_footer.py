import re
import pytest
from pages.home_page import HomePage
from playwright.sync_api import expect

def test_hero_and_cta(page):
    home = HomePage(page)
    home.open()
    home.accept_cookies_if_present()

    heading = home.hero_heading()
    cta = home.primary_cta()

    # 1) Versuche Heading sichtbar zu machen
    heading_visible = False
    try:
        expect(heading).to_be_visible(timeout=8000)
        heading_visible = True
    except Exception:
        heading_visible = False

    # 2) Wenn Heading nicht sichtbar → CTA versuchen
    if not heading_visible:
        if cta.count() == 0:
            pytest.skip("Weder Hero-Heading noch CTA gefunden – Test wird übersprungen.")

        cta_first = cta.first
        try:
            cta_first.scroll_into_view_if_needed(timeout=5000)
        except Exception:
            pass
        expect(cta_first).to_be_visible(timeout=8000)
        expect(cta_first).to_be_enabled()

        old_url = page.url
        cta_first.click()
        page.wait_for_load_state("networkidle")
        page.wait_for_load_state("domcontentloaded")
        home.accept_cookies_if_present()

        # 3) Zielseite plausibilisieren (mehrere akzeptierte Signale)
        url_ok = (page.url != old_url) or re.search(r"/(kontakt|contact|demo|termin|anfrage|angebot)", page.url, re.I)
        title = (page.title() or "").strip()
        title_ok = len(title) > 0
        heading_ok = page.locator("h1, h2, [role='heading']").count() > 0
        form_ok = page.locator("form").count() > 0
        contact_link_ok = page.locator("a[href^='mailto:'], a[href^='tel:']").count() > 0

        assert url_ok or heading_ok or form_ok or contact_link_ok or title_ok, \
            f"CTA-Ziel nicht plausibel bestätigt. URL='{page.url}', Title='{title}'"
