import re
from playwright.sync_api import expect
from pages.home_page import HomePage

HOME = "https://www.karma.de/home"

def test_mobile_navigation_menu(page):
    page.goto(HOME, wait_until="domcontentloaded")
    HomePage(page).accept_cookies_if_present()

    toggle = page.get_by_role("button", name=re.compile(r"(menü|menu|nav|öffnen|schließen)", re.I))
    if toggle.count() == 0:
        return

    toggle.first.click()
    menu = page.locator("[role='navigation'] ul, nav ul, .nav-menu, .mobile-menu, [class*='menu']")
    expect(menu.first).to_be_visible(timeout=3000)
