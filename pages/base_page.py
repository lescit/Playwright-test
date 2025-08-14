from typing import Optional
from playwright.sync_api import Page, expect
import re

class BasePage:
    DEFAULT_TIMEOUT = 10_000

    def __init__(self, page: Page):
        self.page = page

    def navigate_to(self, url: str, wait_until: str = "networkidle"):
        self.page.goto(url, wait_until=wait_until)
        self.accept_cookies_if_present()

    def accept_cookies_if_present(self):
        """Zentralisierte Cookie-Behandlung"""
        try:
            # Semantischer Ansatz
            btn = self.page.get_by_role(
                "button", name=re.compile(r"(akzept|accept|zustimm|einverstanden)", re.I)
            )
            if btn.count() == 0:
                # Fallback auf technische Selektoren
                btn = self.page.locator(
                    "button:has-text('Akzept'), button:has-text('Accept'), button:has-text('Einverstanden')"
                )
            if btn.count() > 0:
                self.safe_click(btn)
        except Exception:
            pass

    def wait_visible(self, locator, timeout: Optional[int] = None):
        timeout = timeout or self.DEFAULT_TIMEOUT
        expect(locator).to_be_visible(timeout=timeout)

    def safe_action(self, action_func, *args, max_retries=2, sleep_ms=300, **kwargs):
        """Führt Aktionen mit Retry-Mechanismus aus"""
        for attempt in range(max_retries + 1):
            try:
                return action_func(*args, **kwargs)
            except Exception:
                if attempt == max_retries:
                    raise
                self.page.wait_for_timeout(sleep_ms)

    def safe_click(self, locator, timeout: Optional[int] = None):
        """Wartet auf Sichtbarkeit und klickt mit Retry"""
        self.wait_visible(locator, timeout)
        return self.safe_action(locator.first.click)
