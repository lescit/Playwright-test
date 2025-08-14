import re
from pages.home_page import HomePage

HOME = "https://www.karma.de/home"

def _parse_rgb(s):
    import re
    m = re.match(r"rgba?\\((\\d+),\\s*(\\d+),\\s*(\\d+)(?:,\\s*([\\d.]+))?\\)", s or "", re.I)
    if not m:
        return None
    r, g, b = map(int, m.group(1,2,3))
    a = float(m.group(4)) if m.group(4) else 1.0
    return (r, g, b, a)

def _rel_luminance(r,g,b):
    def srgb_to_lin(c):
        c = c/255.0
        return c/12.92 if c <= 0.04045*255 else ((c/255.0 + 0.055)/1.055)**2.4
    R = srgb_to_lin(r)
    G = srgb_to_lin(g)
    B = srgb_to_lin(b)
    return 0.2126*R + 0.7152*G + 0.0722*B

def _contrast_ratio(c1, c2):
    L1 = _rel_luminance(*c1[:3])
    L2 = _rel_luminance(*c2[:3])
    Lmax, Lmin = (max(L1, L2), min(L1, L2))
    return (Lmax + 0.05) / (Lmin + 0.05)

def test_cta_contrast_basic(page):
    page.goto(HOME, wait_until="domcontentloaded")
    HomePage(page).accept_cookies_if_present()

    cta = HomePage(page).primary_cta().first
    if cta.count() == 0:
        return

    styles = page.evaluate("""(el) => {
      const cs = window.getComputedStyle(el);
      return { bg: cs.backgroundColor, color: cs.color };
    }""", cta)

    fg = _parse_rgb(styles.get("color"))
    bg = _parse_rgb(styles.get("bg"))
    if not fg or not bg or fg[3] < 1 or bg[3] < 1:
        return

    ratio = _contrast_ratio(fg, bg)
    assert ratio >= 4.5, f"CTA-Kontrast zu niedrig: {ratio:.2f}:1 (min 4.5:1)"
