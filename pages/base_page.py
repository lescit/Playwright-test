import re
from typing import Optional
from playwright.sync_api import Page, expect, TimeoutError as PWTimeout

class BasePage:
    DEFAULT_TIMEOUT = 10_000

    def __init__(self, page: Page):
        self.page = page

    def navigate_to(self, url: str, wait_until: str = "networkidle"):
        """Navigiert zu einer URL und akzeptiert Cookies."""
        self.page.goto(url, wait_until=wait_until)
        self.accept_cookies_if_present()

    def wait_visible(self, locator, timeout: Optional[int] = None):
        """Wartet, bis ein Element sichtbar ist."""
        expect(locator).to_be_visible(timeout=timeout or self.DEFAULT_TIMEOUT)

    def accept_cookies_if_present(self):
        """Zentralisierte Cookie-Behandlung mit mehreren Fallbacks."""
        try:
            self.page.wait_for_load_state("domcontentloaded")
        except Exception:
            pass  # Seite war vielleicht schon geladen

        selectors = [
            "button:has-text('Akzept')",
            "button:has-text('Accept')",
            "button:has-text('Zustimm')",
            "[data-testid='accept-cookies']"
        ]

        for selector in selectors:
            loc = self.page.locator(selector)
            if loc.count() > 0:
                try:
                    expect(loc.first).to_be_visible(timeout=3000)
                    loc.first.click()
                    break
                except PWTimeout:
                    continue
