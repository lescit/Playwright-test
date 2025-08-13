# tests/home/test_perf_budget.py
HOME = "https://www.karma.de/home"

def _nav_metrics(page):
    return page.evaluate(
        """
        () => {
          const nav = performance.getEntriesByType('navigation')[0];
          if (!nav) return null;
          return {
            dcl: nav.domContentLoadedEventEnd || 0,
            load: nav.loadEventEnd || 0,
            ttfb: nav.responseStart || 0
          };
        }
        """
    )

def test_perf_budget_navigation(page):
    # Wir warten nur bis DOM bereit ist; die Messung kommt aus Performance API
    page.goto(HOME, wait_until="domcontentloaded")

    m = _nav_metrics(page)
    assert m is not None, "Navigation Timing nicht verfügbar (Performance API fehlte)."

    dcl = m["dcl"] or 0
    load = m["load"] or 0
    ttfb = m["ttfb"] or 0

    # Sanity-Schwellen (großzügig, damit stabil):
    assert dcl > 0 and dcl < 6000, f"DOMContentLoaded zu langsam: {dcl:.0f} ms"
    if load > 0:
        assert load < 12000, f"Load Event zu langsam: {load:.0f} ms"
    if ttfb > 0:
        assert ttfb < 2000, f"TTFB hoch: {ttfb:.0f} ms"
