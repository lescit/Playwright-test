# conftest.py
import os, pytest
from playwright.sync_api import ConsoleMessage

ENABLE_CONSOLE_FAIL = os.getenv("CONSOLE_FAIL", "0") == "1"

@pytest.fixture
def context(browser):
    ctx = browser.new_context()
    # Tracing (hilfreich bei Debug, kann im README erwähnt werden)
    ctx.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield ctx
    ctx.tracing.stop(path="trace.zip")

@pytest.fixture
def page(context):
    console_errors = []
    if ENABLE_CONSOLE_FAIL:
        def on_console(msg: ConsoleMessage):
            if msg.type == "error":
                console_errors.append(msg.text)
        context.on("console", on_console)

    p = context.new_page()
    yield p

    if console_errors:
        raise AssertionError(f"Console errors: {console_errors}")
