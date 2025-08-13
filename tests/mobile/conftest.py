# tests/mobile/conftest.py
import pytest

@pytest.fixture
def page(playwright):
    device = playwright.devices["iPhone 13 Pro Max"]
    browser = playwright.webkit.launch()                 # <= WebKit!
    context = browser.new_context(**device)
    page = context.new_page()
    yield page
    context.close()
    browser.close()

