import re
from playwright.sync_api import expect
from .base_page import BasePage

class HomePage(BasePage):
    ORIGIN = "https://www.karma.de"
    URL = f"{ORIGIN}/home"

    # Einheitliche Navigation (wartet auf networkidle + Cookies)
    def open(self):
        self.navigate_to(self.URL, wait_until="networkidle")

    # Robust: warte bis ein Heading-Kandidat im DOM ist; bevorzuge <h1>, sonst role=heading
    def hero_heading(self):
        try:
            # DOM-Anwesenheit (nicht zwingend sichtbar) verhindert Race-Conditions
            self.page.wait_for_selector("h1, [role='heading']", state="attached", timeout=self.DEFAULT_TIMEOUT)
        except Exception:
            pass
        # Erst echtes H1, sonst beliebiges role=heading
        return self.page.locator("h1").first.or_(self.page.get_by_role("heading").first)

    # Primärer CTA mit Scoping, ARIA-first und Fallbacks
    def primary_cta(self):
        name_re = re.compile(r"(kontakt|kontaktieren|demo|mehr|termin|anfrage|angebot|jetzt|erfahren)", re.I)

        # Scope: Header/Hero (robuster gegen False Positives)
        scope = self.page.locator("header, [role='banner'], main, section").first

        loc = scope.get_by_role("link", name=name_re)
        if loc.count() == 0:
            loc = scope.get_by_role("button", name=name_re)

        if loc.count() == 0:
            loc = scope.locator(
                "a[href*='kontakt'], a[href*='contact'], a[href*='demo'], "
                "a[href*='termin'], a[href*='anfrage'], a[href*='angebot']"
            )

        if loc.count() == 0:
            # Letzter Fallback: irgendein sichtbarer Link/Button im Scope
            loc = scope.locator("a:visible, button:visible")

        return loc
