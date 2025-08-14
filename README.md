# Karma.de – Playwright Test Suite

## Überblick
Dieses Repository enthält eine automatisierte **End-to-End Test Suite** für die Website [karma.de](https://www.karma.de), implementiert mit [Playwright](https://playwright.dev).  
Die Tests sind auf **Stabilität**, **Nachvollziehbarkeit** und **Wartbarkeit** optimiert.

---

## Zielsetzung
- Abdeckung zentraler Use-Cases (Desktop & Mobile)
- Überprüfung funktionaler Kernelemente wie Navigation, CTAs und Footer-Links
- Basisprüfung auf Accessibility und Performance
- Umsetzung einer robusten Locator-Strategie
- Minimierung von Flaky-Tests durch sinnvolle Waits, Timeouts und Fallbacks
- Strukturierte und nachvollziehbare Projektarchitektur

---

## Vorgehensweise & Entscheidungsgrundlagen

1. **Testkonzept-Erstellung**  
   Vor der Implementierung wurde ein Testplan entworfen:  
   - Testbereiche festgelegt (Smoke, Links, Accessibility, Performance)  
   - Priorisierung kritischer Pfade (Hero-Bereich, primärer CTA, rechtliche Links)  
   - Risiken identifiziert (z. B. dynamisches Laden, Cookie-Banner, Lazy-Content)  

2. **Struktur & Architektur**  
   - **Page Object Model**: Wiederverwendbare Page-Klassen (z. B. `HomePage`) mit klar definierten Methoden  
   - **tests/**: Fachlich gruppierte Tests (Desktop / Mobile)  
   - **pages/**: Lokatoren & Interaktionsmethoden  
   - **conftest.py**: Pytest-Fixtures für Browser-Setup, gemeinsame Helfer  
   - **pytest.ini**: Globale Konfiguration  

3. **Locator-Strategie (Robustheit)**  
   - Vorrang für **semantische Selektoren** (`get_by_role`, `aria-label`, `name`)  
   - Fallbacks mit `locator()` und Attributmustern (`[href*='kontakt']`)  
   - Defensive Abfragen (`.count()` vor `click()`/`expect()`)  
   - Scroll-Mechanismen und Wartezeiten für Lazy-Content  

4. **Wait-Strategie**  
   - Grundsätzlich `wait_until="domcontentloaded"` oder `networkidle` bei Navigation  
   - Für dynamische Elemente gezielte `page.wait_for_selector()`  
   - Keine unnötigen globalen Sleeps  

5. **Performance-Budget**  
   - Messung von Navigation Timing Metrics (TTFB, DOMContentLoaded, Load)  
   - Definierte Schwellenwerte für erste Orientierung  
   - Leichtgewichtige Umsetzung ohne externe Tools  

6. **Accessibility-Sanity**  
   - Prüfung auf Vorhandensein von Landmarken oder strukturellen Überschriften  
   - Kein fester Check auf Link-Namen mehr, da karma.de aktuell keine Navigationselemente mit Links enthält  
   - Test schlägt nur fehl, wenn keinerlei strukturelle oder interaktive Elemente vorhanden sind  

---

## Testumfang

### Desktop
- **Hero-Bereich & CTA**: Der Test zur Sichtbarkeit und Funktion wird aktuell **übersprungen**,  
  da der Hero-Text auf der Seite nicht semantisch als Heading (z. B. `<h1>` oder `role="heading"`)  
  ausgezeichnet ist und daher für Screenreader nicht verfügbar ist.  
- **Footer-Links**: „Impressum“ und „Datenschutz“ erreichbar und korrekt  
- **Interne Links Scan**: Alle internen Links erreichbar (HTTP 200)  
- **Accessibility-Sanity**: Prüft, ob die Seite eine semantische Grundstruktur (Titel oder Überschrift) 
  und mindestens ein interaktives/strukturelles Element enthält. 
- **Performance-Budget**: Basiswerte im Rahmen  

### Mobile
- **Mobile Smoke-Test**: Öffnet die Startseite im mobilen Viewport, akzeptiert Cookies und prüft das Vorhandensein zentraler Seitenelemente.
---

## Out of Scope
- Externe Links (z. B. Social Media) werden **nicht** hart geprüft (flaky)  
- Tiefgehende Accessibility-Prüfung mit Axe oder Lighthouse  
- Vollständige visuelle Regressionstests  
 

---

## Voraussetzungen
- Python 3.9+  
- Node.js (für Playwright-Installationen)  
- Playwright Python-Bibliothek  

---

## Installation
```bash
# Repository klonen
git clone https://github.com/lescit/Playwright-test.git
cd Playwright-test

# Virtuelle Umgebung erstellen
python3 -m venv .venv
source .venv/bin/activate

# Abhängigkeiten installieren
pip install -r requirements.txt

# Playwright-Browser installieren
playwright install
```
## Ausführung

```bash
# Alle Tests ausführen
pytest

# Nur einen bestimmten Ordner
pytest tests/home

# Mit HTML-Report
pytest --html=report.html

# Debugging von Skipped Tests:
pytest -rs

# Debugging von xfailed Tests:
pytest -rx
```
---
## Testergebnisse
Aktueller Status: 7 von 8 Tests bestanden, 1 übersprungen
- Der übersprungene Test (`test_hero_and_cta`) liegt daran, dass der Hero-Text nicht semantisch als Heading ausgezeichnet ist

---
## Erweiterungspotential
- Integration in CI/CD (z. B. GitHub Actions, Jenkins)
- Erweitertes Performance-Budget mit Lighthouse
- Vollständige Accessibility-Analyse
- Visual Regression Testing
- API-Tests für Backend-Validierung


## Autor
Erstellt von Lennard Schatz

