# SystemMonitorX v2.0.0

Ein modernes System-Monitoring-Tool mit Desktop-Widgets, entwickelt mit PyQt6.

![SystemMonitorX](https://img.shields.io/badge/Version-2.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.12+-green)
![PyQt6](https://img.shields.io/badge/PyQt6-6.5.0+-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎨 Design-Features

### Farbpalette (Dark Mode)
- **Hintergrund**: `#141414`
- **Accent**: `#4a307d` 
- **Text**: `#f2ecfa`
- **Karten-Hintergrund**: `#1e1e1e`
- **Progress-Hintergrund**: `#2a2a2a`

### Moderne UI-Elemente
- **Glasmorphismus-Effekte**: Transparente Karten mit Blur-Effekt
- **Abgerundete Ecken**: Moderne, sanfte Design-Sprache
- **Progress-Bars**: Visuelle Darstellung der System-Auslastung
- **Emoji-Icons**: 🎨 🖥️ 💾 📊 📈 ⚙️ für bessere UX
- **Responsive Layout**: Anpassungsfähiges Grid-System

## ✨ Features

### 🖥️ System-Monitoring
- **CPU-Auslastung**: Echtzeit-Überwachung mit Frequenz-Anzeige
- **RAM-Verbrauch**: Arbeitsspeicher-Nutzung in GB und Prozent
- **Festplatten-Auslastung**: Speicherplatz-Überwachung
- **System-Informationen**: Plattform, Version, Architektur

### 📊 Desktop-Widgets
- **Unabhängige Widgets**: CPU, RAM, Disk als separate Fenster
- **Drag & Drop**: Widgets frei positionierbar
- **Transparente Overlays**: Glasmorphismus-Design
- **Konfigurierbar**: Größe, Position, Transparenz
- **Feste Größe**: 320x110 Pixel für optimale Übersicht

### 📈 Daten-Logging
- **CSV/JSON Export**: Automatische Datenspeicherung
- **Matplotlib-Graphen**: Interaktive Visualisierungen
- **Verlaufsdaten**: System-Performance über Zeit
- **Buffer-System**: Effiziente Speicherung (60 Sekunden)

### 🎯 System-Tray
- **Tray-Integration**: Minimierung in System-Tray
- **Dynamische Icons**: CPU-Auslastung im Icon
- **Kontext-Menü**: Schnellzugriff auf Funktionen
- **Hintergrund-Betrieb**: Läuft im Hintergrund

### 🔧 Konfiguration
- **JSON-basiert**: Vollständig konfigurierbar
- **Widget-Positionen**: Automatisch gespeichert
- **Theme-Einstellungen**: Persistent gespeichert
- **Export/Import**: Konfigurationen übertragbar

## 🛠️ Technologie-Stack

- **Python 3.12+**: Core-Programmiersprache
- **PyQt6**: Moderne GUI-Bibliothek für custom Designs
- **psutil**: System-Monitoring
- **threading**: Hintergrund-Updates
- **pyinstaller**: Portable .exe-Erstellung
- **pystray**: System-Tray-Integration
- **Pillow (PIL)**: Icon-Erstellung
- **matplotlib**: Datenvisualisierung
- **JSON/CSV**: Datenpersistierung

## 📁 Projektstruktur

```
SystemMonitorX/
├── main.py                     # Hauptanwendung
├── requirements.txt            # Python-Dependencies
├── README.md                  # Dokumentation
├── LICENSE                    # MIT-Lizenz
├── .gitignore                 # Git-Ignore
├── widgets/                   # Desktop-Widgets
│   ├── __init__.py
│   ├── base_widget.py         # Basis-Widget-Klasse
│   ├── cpu_widget.py          # CPU-Widget
│   ├── ram_widget.py          # RAM-Widget
│   ├── disk_widget.py         # Disk-Widget
│   └── system_widget.py       # System-Widget
├── utils/                     # Utility-Module
│   ├── __init__.py
│   ├── logging.py             # Daten-Logging
│   ├── graphs.py              # Matplotlib-Graphen
│   ├── config.py              # Konfigurations-Manager
│   └── system_tray.py         # System-Tray
├── windows/                   # Fenster-Klassen
│   ├── __init__.py
│   ├── graph_window.py        # Graph-Fenster
│   └── settings_window.py     # Einstellungen-Fenster
├── config/                    # Konfiguration (wird erstellt)
│   ├── settings.json          # App-Einstellungen
│   └── widgets.json           # Widget-Konfiguration
└── logs/                      # Log-Dateien (wird erstellt)
```

## 🚀 Installation

### Voraussetzungen
- Python 3.12 oder höher
- Windows 10/11 (getestet)

### Installation

```bash
# Repository klonen
git clone https://github.com/safrii350/systemmonitorx-v2.git
cd systemmonitorx-v2

# Dependencies installieren
pip install -r requirements.txt

# Anwendung starten
python main.py
```

### Portable Version
1. Download der neuesten Release
2. `SystemMonitorX.exe` ausführen
3. Keine Installation erforderlich

## 📖 Verwendung

### Dashboard
- **Systemdaten**: Automatische Anzeige von CPU, RAM, Disk
- **Real-time Updates**: Alle 1 Sekunde aktualisiert
- **Progress-Bars**: Visuelle Darstellung der Auslastung

### Desktop-Widgets
- **Widget erstellen**: Klick auf "🖥️ Desktop-Widgets"
- **Positionieren**: Drag & Drop der Widgets
- **Schließen**: Klick auf runden Close-Button
- **Position speichern**: Automatisch beim Schließen

### Daten-Logging
- **Logging starten**: Klick auf "📝 Logging starten"
- **Graphen anzeigen**: Klick auf "📈 Graphen"
- **Daten exportieren**: Automatisch in `logs/` Ordner

### System-Tray
- **Minimieren**: Klick auf "📌 Minimieren"
- **Tray-Icon**: Rechtsklick für Kontext-Menü
- **Wiederherstellen**: Über Tray-Icon

## 🔧 Konfiguration

### Theme-Einstellungen
```json
{
  "theme": {
    "background": "#141414",
    "accent": "#4a307d",
    "text": "#f2ecfa",
    "text_secondary": "#a0a0a0",
    "card_background": "#1e1e1e",
    "progress_background": "#2a2a2a"
  }
}
```

### Widget-Konfiguration
```json
{
  "widgets": {
    "cpu": {"x": 50, "y": 50, "visible": true},
    "ram": {"x": 400, "y": 50, "visible": true},
    "disk": {"x": 50, "y": 200, "visible": true},
    "system": {"x": 400, "y": 200, "visible": true}
  }
}
```

## 🐛 Fehlerbehebung

### Anwendung startet nicht
- Python 3.12+ installiert?
- Dependencies installiert? (`pip install -r requirements.txt`)
- Als Administrator ausführen

### Widgets werden nicht angezeigt
- Konfigurationsdateien prüfen
- Anwendung neu starten
- Widget-Konfiguration zurücksetzen

### Logging funktioniert nicht
- Schreibrechte im `logs/` Ordner prüfen
- Speicherplatz verfügbar?
- Logging neu starten

## 🤝 Beitragen

1. Fork das Repository
2. Feature-Branch erstellen (`git checkout -b feature/AmazingFeature`)
3. Änderungen committen (`git commit -m 'Add some AmazingFeature'`)
4. Branch pushen (`git push origin feature/AmazingFeature`)
5. Pull Request erstellen

## 📝 Changelog

### v2.0.0 (2025-07-31)

#### ✨ Neue Features
- **PyQt6 Migration**: Kompletter Wechsel von CustomTkinter zu PyQt6
- **Custom Window Designs**: Abgerundete Ecken, transparente Hintergründe
- **Desktop-Widgets**: Unabhängige, draggable Widgets mit Glasmorphismus
- **System-Tray Integration**: Dynamische Icons und Context-Menü
- **Daten-Logging**: CSV/JSON Export mit Buffer-System
- **Matplotlib-Graphen**: Interaktive System-Performance-Visualisierung
- **JSON-Konfiguration**: Vollständig konfigurierbare Einstellungen

#### 🎨 Design-Verbesserungen
- **Dark Mode**: Professionelle Farbpalette (#141414, #4a307d, #f2ecfa)
- **Glasmorphismus**: Transparente Karten mit Blur-Effekt
- **Responsive Layout**: Anpassungsfähiges Grid-System
- **Emoji-Icons**: Intuitive Benutzerführung

#### 🛠️ Technische Verbesserungen
- **Modulare Architektur**: Saubere Trennung von GUI, Logik und Daten
- **Threading**: Hintergrund-Updates für flüssige Performance
- **Error Handling**: Robuste Fehlerbehandlung
- **Portable Distribution**: PyInstaller für .exe-Erstellung

#### 🔧 Konfiguration
- **Widget-Positionen**: Automatisches Speichern und Laden
- **Theme-Einstellungen**: Persistent gespeicherte Benutzereinstellungen
- **Export/Import**: Konfigurationen übertragbar

## 📄 Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe [LICENSE](LICENSE) für Details.

## 👥 Autoren

- **SystemMonitorX Team** - _Initiale Entwicklung_

## 🙏 Danksagungen

- **PyQt6** - Moderne GUI-Bibliothek
- **psutil** - System-Monitoring
- **matplotlib** - Datenvisualisierung
- **PyInstaller** - Portable Distribution

---

**SystemMonitorX v2.0.0** - Ein modernes System-Monitoring-Tool mit Desktop-Widgets 🚀 