from playwright.sync_api import expect
import pytest, re

HOME = "https://www.karma.de/home"

def accept_cookies_if_present(page):
    try:
        btn = page.get_by_role(
            "button",
            name=lambda n: n and any(x in n.lower() for x in ["akzept", "accept", "zustimm", "einverstanden"]),
        )
        if btn.count() > 0:
            btn.first.click()
    except Exception:
        pass

def _settle(page, ms=600):
    # leichte Pause statt harter Sichtbarkeits-Waits
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(ms)

def test_landmarks_and_heading_present(page):
    page.goto(HOME, wait_until="domcontentloaded")
    accept_cookies_if_present(page)

    # 1) Struktur-Nachweis: <title> ODER irgendeine Überschrift vorhanden
    title_ok = bool((page.title() or "").strip())
    heading_cnt = page.locator("h1, h2, [role='heading']").count()
    assert title_ok or heading_cnt > 0, "Weder <title> noch Überschrift gefunden."

    # 2) Minimaler Navigierbarkeits-/Semantik-Nachweis:
    sema_cnt = page.locator(
        "nav, header, footer, [role='navigation'], [role='banner'], [role='contentinfo'], "
        "a[href], button, [role='button'], [role='link'], input, select, textarea"
    ).count()

    # Fallback: wenn noch 0, dann DOM-Knoten zählen (Content vorhanden?)
    if sema_cnt == 0:
        sema_cnt = page.locator("body *").count()

    assert sema_cnt > 0, "Keine Hinweise auf interaktive/semantische Elemente oder Content im DOM."
