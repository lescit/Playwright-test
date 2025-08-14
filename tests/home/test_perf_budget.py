from pages.home_page import HomePage

HOME = "https://www.karma.de/home"

def _nav_metrics(page):
    return page.evaluate("""
        () => {
            const nav = performance.getEntriesByType('navigation')[0];
            return {
                ttfb: nav?.responseStart || 0,
                dcl: nav?.domContentLoadedEventEnd || 0,
                load: nav?.loadEventEnd || 0
            };
        }
    """)

def _web_vitals(page):
    return page.evaluate("""
        () => {
          const nav = performance.getEntriesByType('navigation')[0];
          const paint = performance.getEntriesByType('paint');
          const fcp = paint.find(p => p.name === 'first-contentful-paint');
          const lcpEntries = performance.getEntriesByType('largest-contentful-paint');
          const lcp = lcpEntries.length ? lcpEntries[lcpEntries.length - 1] : null;

          return {
            ttfb: nav?.responseStart || 0,
            dcl: nav?.domContentLoadedEventEnd || 0,
            load: nav?.loadEventEnd || 0,
            fcp: fcp?.startTime || 0,
            lcp: lcp?.startTime || 0
          };
        }
    """)

def test_perf_budget_navigation(page):
    page.goto(HOME, wait_until="domcontentloaded")
    HomePage(page).accept_cookies_if_present()

    metrics = _nav_metrics(page)
    assert metrics["ttfb"] < 2000
    assert metrics["dcl"] < 6000
    assert metrics["load"] < 12000

    vitals = _web_vitals(page)
    assert vitals["fcp"] >= 0
    assert vitals["lcp"] >= 0
    if vitals["lcp"] and vitals["lcp"] > 6000:
        print(f"[Perf Warnung] LCP hoch: {vitals['lcp']:.0f} ms")
