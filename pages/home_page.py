# pages/home_page.py
import re
from playwright.sync_api import Page, expect


class HomePage:
    ORIGIN = "https://www.karma.de"
    URL = f"{ORIGIN}/home"

    def __init__(self, page: Page):
        self.page = page

    # --- Navigation ---
    def open(self):
        self.page.goto(self.URL, wait_until="domcontentloaded")

    # --- Cookies ---
    def accept_cookies_if_present(self):
        """
        Akzeptiert ggf. den Cookie-Dialog.
        ARIA-first, mit Text-Fallback und einfachem iFrame-Scan.
        """
        # 1) ARIA-first
        btn = self.page.get_by_role(
            "button",
            name=re.compile(r"(akzept|accept|zustimm|einverstanden)", re.I),
        )
        if btn.count() == 0:
            # 2) Text-Fallback
            btn = self.page.locator(
                "button:has-text('Akzept'), button:has-text('Accept'), button:has-text('Einverstanden')"
            )

        # 3) iFrame-Fallback (z. B. Consent-Provider)
        if btn.count() == 0:
            for f in self.page.frames:
                f_url = (f.url or "").lower()
                if any(x in f_url for x in ["consent", "cookie"]):
                    fbtn = f.get_by_role(
                        "button",
                        name=re.compile(r"(akzept|accept|zustimm|einverstanden)", re.I),
                    )
                    if fbtn.count() == 0:
                        fbtn = f.locator(
                            "button:has-text('Akzept'), button:has-text('Accept'), button:has-text('Einverstanden')"
                        )
                    if fbtn.count() > 0:
                        expect(fbtn.first).to_be_visible()
                        fbtn.first.click()
                        return

        if btn.count() > 0:
            expect(btn.first).to_be_visible()
            btn.first.click()

    # --- Hero / Headings ---
    def hero_heading(self):
        """
        Liefert den ersten sinnvollen Heading-Kandidaten.
        Semantik vor Text, bevorzugt innerhalb von <main>.
        """
        self.page.wait_for_load_state("domcontentloaded")
        cand = self.page.locator(
            "main h1, main [role='heading'], h1, [role='heading'], h2"
        ).first
        return cand

    # --- Primärer CTA (mit Scoping) ---
    def primary_cta(self):
        # 1) Nach Link-Name (zugänglich)
        loc = self.page.get_by_role(
            "link",
            name=re.compile(r"(kontakt|kontaktieren|demo|mehr|termin|anfragen)", re.I),
        )

        # 2) Fallback: href-Muster
        if loc.count() == 0:
            loc = self.page.locator(
                "a[href*='kontakt'], a[href*='contact'], a[href*='demo'], a[href*='termin'], a[href*='anfrage']"
            )

        # 3) Letzter Fallback: irgendein sichtbarer Link/Button im sichtbaren Bereich
        if loc.count() == 0:
            loc = self.page.locator("a:visible, button:visible")

        return loc


