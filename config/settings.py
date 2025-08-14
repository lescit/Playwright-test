class TestConfig:
    BASE_URL = "https://www.karma.de"
    DEFAULT_TIMEOUT = 10_000
    PERFORMANCE_BUDGETS = {
        "ttfb": 2000,
        "dcl": 6000,
        "load": 12000,
        # optional: "fcp": 3000
    }
