import re
from playwright.sync_api import expect

BASE_ORIGIN = "https://www.karma.de"
HOME = f"{BASE_ORIGIN}/home"

def accept_cookies_if_present(page):
    btn = page.get_by_role(
        "button",
        name=re.compile(r"akzept|accept|zustimm|einverstanden", re.I),
    )
    if btn.count() > 0:
        expect(btn.first).to_be_visible()
        btn.first.click()

def test_footer_legal_links(page):
    page.goto(HOME)
    accept_cookies_if_present(page)

    for link_text, expected_keyword in [
        ("Impressum", "Impressum"),
        ("Datenschutz", "Datenschutz"),
    ]:
        with page.expect_navigation():
            page.get_by_role("link", name=re.compile(link_text, re.I)).click()

        page.wait_for_load_state("networkidle")
        accept_cookies_if_present(page)

        # 1) Titel enthält Keyword?
        title = page.title() or ""
        if re.search(expected_keyword, title, re.I):
            pass
        else:
            # 2) h1/h2/role=heading
            heading = page.locator("h1, h2, [role='heading']").first
            if heading.count() > 0:
                expect(heading).to_be_visible(timeout=10000)
                text = (heading.inner_text() or "").strip()
                if re.search(expected_keyword, text, re.I):
                    pass
                else:
                    # 3) Fallback: Keyword im main/body
                    body_match = page.locator("main, body").get_by_text(expected_keyword, exact=False)
                    expect(body_match).to_be_visible(timeout=10000)
            else:
                body_match = page.locator("main, body").get_by_text(expected_keyword, exact=False)
                expect(body_match).to_be_visible(timeout=10000)

        # zurück zur Home
        page.goto(HOME)
        accept_cookies_if_present(page)


    def test_hero_heading_and_primary_cta(page):
        page.goto(BASE_URL)
        accept_cookies_if_present(page)

         # Hero-Überschrift vorhanden
        hero_heading = page.get_by_role("heading")
        expect(hero_heading).to_be_visible()

        # Primärer CTA: wir suchen generisch nach z. B. "Kontakt", "Mehr", "Demo"
        cta = page.get_by_role("link", name=re.compile(r"kontakt|demo|mehr", re.I))
        expect(cta.first).to_be_visible()

        with page.expect_navigation():
            cta.first.click()

        # Zielseite: irgendeine Überschrift sichtbar
        expect(page.get_by_role("heading")).to_be_visible()