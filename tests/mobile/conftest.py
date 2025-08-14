import pytest
import re

@pytest.fixture
def cookie_handler():
    def _accept(page):
        btn = page.get_by_role("button", name=re.compile(r"(akzept|accept|zustimm|einverstanden)", re.I))
        if btn.count() == 0:
            btn = page.locator(
                "button:has-text('Akzept'), button:has-text('Accept'), button:has-text('Einverstanden')"
            )
        if btn.count() > 0:
            btn.first.click()
    return _accept
