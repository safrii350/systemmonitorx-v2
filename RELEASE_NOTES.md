# SystemMonitorX v2.0.0 - Release Notes

## 🎉 Neue Version verfügbar!

### 📦 Download
- **SystemMonitorX.exe** (66.8 MB) - Portable Version für Windows
- Keine Installation erforderlich - läuft auf jedem Windows PC ohne Admin-Rechte

### ✨ Neue Features in v2.0.0

#### 🎨 Professionelles Design
- **Vollständige Icon-Integration**: Alle Emoji-Icons durch professionelle PNG-Icons ersetzt
- **Dark Mode**: Elegantes dunkles Design mit Farbpalette (#141414, #4a307d, #f2ecfa)
- **Glasmorphism-Effekte**: Moderne, transparente UI-Elemente
- **Abgerundete Ecken**: Konsistentes Design für Dashboard und Widgets

#### 📊 System-Monitoring
- **Echtzeit-Überwachung**: CPU, RAM, Festplatte und System-Informationen
- **Desktop-Widgets**: Frei schwebende, draggable Widgets mit individuellen Designs
- **Daten-Logging**: CSV und JSON Export mit automatischem Speichern
- **Graphen-Visualisierung**: Matplotlib-basierte Live-Graphen mit Dark Mode

#### 🔧 Erweiterte Funktionen
- **System-Tray Integration**: Dynamische Icons mit Kontext-Menü
- **JSON-Konfiguration**: Einstellungen und Widget-Positionen werden gespeichert
- **Portable .exe**: Läuft ohne Installation auf jedem Windows PC

### 🛠️ Technische Verbesserungen

#### Framework-Migration
- **PyQt6**: Vollständige Migration von CustomTkinter zu PyQt6
- **Erweiterte UI-Möglichkeiten**: Custom Window Designs, Frameless Windows
- **Bessere Performance**: Optimierte Threading-Architektur

#### Icon-System
- **PNG-Icons**: Professionelle Icons von Flaticon
- **Automatische Skalierung**: Icons werden automatisch auf die richtige Größe skaliert
- **Fallback-System**: Emoji-Fallback bei fehlenden Icon-Dateien
- **Dark Mode Optimiert**: Helle Icons für optimale Sichtbarkeit

### 📁 Asset-Struktur
```
assets/
├── icons/
│   ├── dashboard/     # Dashboard-Monitoring-Karten
│   ├── buttons/       # Haupt-Buttons
│   └── widgets/       # Widget-spezifische Icons
├── graphs/            # Graph-Icons
├── settings/          # Einstellungs-Icons
├── tray/              # System-Tray Icons
└── ui/                # UI-Aktions-Icons
```

### 🔧 Installation & Verwendung

#### Für Endbenutzer:
1. **SystemMonitorX.exe** herunterladen
2. Doppelklick zum Starten
3. Keine Installation erforderlich

#### Für Entwickler:
```bash
# Dependencies installieren
python -m pip install -r requirements.txt

# Anwendung starten
python main.py

# .exe erstellen
python -m PyInstaller systemmonitorx.spec
```

### 🐛 Bekannte Probleme
- Widgets sind derzeit "always on top" (wird in v2.1 behoben)
- Einige Icons müssen noch in Settings-Window integriert werden

### 📈 Performance
- **Startzeit**: ~2-3 Sekunden
- **Speicherverbrauch**: ~50-80 MB RAM
- **CPU-Last**: <1% im Idle-Modus

### 🔮 Geplante Features für v2.1
- Widget "Always on Top" Option
- Vollständige Icon-Integration in Settings
- Light Mode Support
- Erweiterte Graph-Optionen
- Plugin-System

### 📞 Support
Bei Problemen oder Fragen:
- GitHub Issues: https://github.com/safrii350/systemmonitorx-v2/issues
- Dokumentation: Siehe README.md

---

**SystemMonitorX v2.0.0** - Moderne System-Monitoring-Lösung für Windows 