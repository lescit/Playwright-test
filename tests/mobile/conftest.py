import pytest

@pytest.fixture
def page(playwright):
    browser = None
    context = None
    try:
        device = playwright.devices["iPhone 13 Pro Max"]
        browser = playwright.webkit.launch()   # WebKit ~ Safari
        context = browser.new_context(**device)
        page = context.new_page()
        yield page
    finally:
        # Sicher schließen – auch bei Testfehlern
        if context:
            context.close()
        if browser:
            browser.close()
