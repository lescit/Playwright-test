# Karma.de Playwright Test Suite

## 📌 Überblick
Dieses Projekt enthält eine automatisierte Test-Suite für die Webseite **karma.de**, entwickelt mit [Playwright](https://playwright.dev/).  
Der Zweck ist die **Qualitätsprüfung** der öffentlichen Homepage (`/home`) unter den Gesichtspunkten:

- Funktionalität
- Performance
- Barrierefreiheit
- Stabilität

Die Umsetzung basiert auf einem **schrittweisen Testkonzept**, das speziell für diese Aufgabe erstellt wurde, um die Tests **strukturiert, erweiterbar und robust** zu halten.

---

## 📂 Projektstruktur
karma-playwright/
│
├── pages/ # Page Object Dateien (robuste Locator-Strategie)
│ └── home_page.py
│
├── tests/ # Testfälle gruppiert nach Funktionsbereich
│ └── home/
│ ├── test_home_hero_footer.py
│ ├── test_home_links_scan.py
│ ├── test_a11y_sanity.py
│ ├── test_home_performance.py
│
├── report.html # Automatisch generierter HTML-Report (pytest-html)
├── requirements.txt # Python-Abhängigkeiten
└── README.md # Diese Datei

---

## 🧠 Vorgehensweise & Überlegungen

### 1. Testkonzept-Erstellung
- **Priorisierung:** Zuerst kritische Smoke-Tests, danach Detailprüfungen.
- **Breite Abdeckung:** Hero-Elemente, Navigation, interne Links, Performance, Accessibility.
- **Robuste Locator-Strategie:** Primär semantische Selektoren (`get_by_role`), Fallbacks für dynamische Inhalte.
- **Erweiterbarkeit:** Modular durch **Page Object Pattern**, einfache Ergänzung neuer Tests.

> Vorteil: Jeder Test kann einzeln angepasst oder erweitert werden, ohne andere Tests zu destabilisieren.

---

### 2. Umsetzung in Playwright
#### **Page Object Pattern**
- Saubere Trennung zwischen Testlogik und Element-Lokalisierung.
- Beispiel: Cookie-Banner-Handling nur einmal zentral implementiert.

#### **wait_until-Strategie**
- Standard: `domcontentloaded` für schnelle Tests.
- `networkidle` für Seiten mit Lazy Loading.

#### **Fallback-Checks**
- Alternative Selektoren oder Scroll-Mechanismen, wenn Elemente nicht gefunden werden.

---

### 3. Performance-Checks
Ein leichter Performance-Test auf Basis der **Navigation Timing API** prüft:
- **First Contentful Paint (FCP)**
- **DOMContentLoaded (DCL)**
- **Gesamtladezeit**

Es wird ein **Mini-Budget** definiert, um Ausreißer schnell zu erkennen.

---

### 4. Accessibility-Sanity
Kein vollumfänglicher WCAG-Test, sondern eine **Sanity-Prüfung**:
- Landmarken oder alternative Navigierbarkeits-Indikatoren.
- Vorhandensein von Headings oder `<title>`.
- Sichtbare Links/Buttons.

> Fehlende Landmarken führen nicht zu einem harten Fail, sondern zu informativen Hinweisen.

---

### 5. Robustheit
- Fallback-Strategien bei dynamischen Inhalten.
- Automatisches Scrollen, wenn Elemente erst später geladen werden.
- Externe Links werden **nicht hart geprüft**, um Flakiness zu vermeiden (siehe *Out of Scope*).

---

## ⚙️ Installation & Ausführung

### 1. Umgebung einrichten
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install
2. Tests ausführen
pytest --html=report.html --self-contained-html
➡ HTML-Report wird in report.html generiert.
🚫 Out of Scope
Externe Links: Nicht geprüft, um Instabilität durch externe Server zu vermeiden.
Carousels/Slider: Nicht getestet, da auf /home aktuell nicht vorhanden.
Vollständige WCAG-Prüfung: Nur Sanity-Check, vollständiger Audit könnte mit axe-core integriert werden.
🔮 Weiterentwicklung
CI-Integration: Empfohlene GitHub Actions Pipeline:
name: Playwright Tests
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: playwright install
      - run: pytest --html=report.html --self-contained-html
Browser-Matrix: Tests zusätzlich in Firefox und WebKit ausführen.
Tiefe Link-Scans: Optional Tiefe >1 zur Erkennung toter interner Links.
👤 Autor
Lennard Schatz

---

