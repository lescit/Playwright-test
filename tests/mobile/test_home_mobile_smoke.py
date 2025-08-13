from playwright.sync_api import expect
from pages.home_page import HomePage
import re

def accept_cookies_if_present(page):
    try:
        btn = page.get_by_role("button", name=lambda n: n and any(x in n.lower() for x in ["akzept", "accept", "zustimm", "einverstanden"]))
        if btn.count() > 0:
            btn.first.click()
    except Exception:
        pass

def test_home_mobile_smoke(page):
    page.goto("https://www.karma.de/home", wait_until="domcontentloaded")
    HomePage(page).accept_cookies_if_present()
    accept_cookies_if_present(page)

    # 1) Versuche: irgendeine Überschrift sichtbar
    heading = page.locator("h1, h2, [role='heading']").first
    try:
        expect(heading).to_be_visible(timeout=6000)
        return  # Smoke ok
    except Exception:
        pass  # Fallback greifen lassen

    # 2) Fallback: zum Footer scrollen und nach Impressum/Datenschutz suchen
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    legal = page.locator("a[href*='impressum'], a[href*='datenschutz']")
    if legal.count() > 0:
        expect(legal.first).to_be_visible(timeout=6000)
        return  # Smoke ok

    # 3) Letzter Fallback: Seitentitel muss sinnvoll befüllt sein
    title = page.title() or ""
    assert len(title.strip()) > 0, "Weder Heading noch Footer-Links noch brauchbarer Titel gefunden."

