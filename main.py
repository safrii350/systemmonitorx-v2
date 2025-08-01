#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SystemMonitorX - Hauptanwendung
Modernes System-Monitoring-Tool mit PyQt6

Autor: SystemMonitorX Team
Version: 1.0.0
"""

import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QGridLayout, QLabel, QPushButton,
    QProgressBar, QFrame, QScrollArea
)
from PyQt6.QtCore import (
    Qt, QTimer, QThread, pyqtSignal, QPropertyAnimation,
    QEasingCurve, QRect
)
from PyQt6.QtGui import (
    QPalette, QColor, QFont, QPixmap, QIcon,
    QPainter, QBrush, QPen, QLinearGradient
)
import psutil
import json
from datetime import datetime

# Theme-Farben (Dark Mode)
THEME_COLORS = {
    'background': '#141414',
    'accent': '#4a307d',
    'text': '#f2ecfa',
    'text_secondary': '#a0a0a0',
    'card_background': '#1e1e1e',
    'progress_background': '#2a2a2a'
}

class SystemMonitorX(QMainWindow):
    """
    Hauptfenster der SystemMonitorX Anwendung
    Dashboard mit System-Monitoring in Echtzeit
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SystemMonitorX")
        self.setMinimumSize(800, 600)
        
        # Konfigurations-System initialisieren
        from utils.config import ConfigManager
        self.config_manager = ConfigManager()
        
        # Logging-System initialisieren
        from utils.logging import SystemLogger
        self.logger = SystemLogger()
        self.logging_active = False
        
        # System-Tray initialisieren
        from utils.system_tray import SystemTrayIcon
        self.tray_icon = SystemTrayIcon(self.config_manager)
        
        # Theme und Styling
        self.setup_theme()
        self.setup_ui()
        self.setup_monitoring()
        self.setup_system_tray()
        
        # Fenster-Eigenschaften
        self.setWindowFlags(Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        
    def setup_theme(self):
        """Dark Mode Theme konfigurieren"""
        # Palette für Dark Mode
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(THEME_COLORS['background']))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(THEME_COLORS['text']))
        palette.setColor(QPalette.ColorRole.Base, QColor(THEME_COLORS['card_background']))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(THEME_COLORS['accent']))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(THEME_COLORS['background']))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(THEME_COLORS['text']))
        palette.setColor(QPalette.ColorRole.Text, QColor(THEME_COLORS['text']))
        palette.setColor(QPalette.ColorRole.Button, QColor(THEME_COLORS['accent']))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(THEME_COLORS['text']))
        palette.setColor(QPalette.ColorRole.Link, QColor(THEME_COLORS['accent']))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(THEME_COLORS['accent']))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(THEME_COLORS['text']))
        
        self.setPalette(palette)
        
        # Stylesheet für abgerundete Ecken und moderne Optik
        self.setStyleSheet("""
            QMainWindow {
                background-color: #141414;
                border-radius: 10px;
            }
            
            QFrame {
                background-color: #1e1e1e;
                border-radius: 8px;
                border: 1px solid #2a2a2a;
            }
            
            QLabel {
                color: #f2ecfa;
                font-family: 'Consolas', monospace;
                font-size: 12px;
            }
            
            QPushButton {
                background-color: #4a307d;
                color: #f2ecfa;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-family: 'Consolas', monospace;
                font-size: 12px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #5a408d;
            }
            
            QPushButton:pressed {
                background-color: #3a206d;
            }
            
            QProgressBar {
                border: 2px solid #2a2a2a;
                border-radius: 6px;
                text-align: center;
                background-color: #2a2a2a;
                color: #f2ecfa;
                font-family: 'Consolas', monospace;
                font-size: 11px;
            }
            
            QProgressBar::chunk {
                background-color: #4a307d;
                border-radius: 4px;
            }
        """)
        
    def setup_ui(self):
        """Benutzeroberfläche erstellen"""
        # Zentrales Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Haupt-Layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Header
        self.setup_header(main_layout)
        
        # System-Karten
        self.setup_system_cards(main_layout)
        
        # Button-Bereich
        self.setup_button_area(main_layout)
        
    def setup_header(self, parent_layout):
        """Header-Bereich mit Titel"""
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        
        # Titel
        title_label = QLabel("SystemMonitorX")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #f2ecfa;
            font-family: 'Consolas', monospace;
        """)
        
        # Untertitel
        subtitle_label = QLabel("Echtzeit-System-Monitoring")
        subtitle_label.setStyleSheet("""
            font-size: 14px;
            color: #a0a0a0;
            font-family: 'Consolas', monospace;
        """)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(subtitle_label)
        
        parent_layout.addWidget(header_frame)
        
    def setup_system_cards(self, parent_layout):
        """4 Hauptkarten für System-Monitoring"""
        cards_frame = QFrame()
        cards_layout = QGridLayout(cards_frame)
        cards_layout.setSpacing(15)
        
        # CPU-Karte
        self.cpu_card = self.create_monitoring_card("CPU", "assets/icons/dashboard/cpu.png")
        cards_layout.addWidget(self.cpu_card, 0, 0)
        
        # RAM-Karte
        self.ram_card = self.create_monitoring_card("RAM", "assets/icons/dashboard/ram.png")
        cards_layout.addWidget(self.ram_card, 0, 1)
        
        # Disk-Karte
        self.disk_card = self.create_monitoring_card("Festplatte", "assets/icons/dashboard/disk.png")
        cards_layout.addWidget(self.disk_card, 1, 0)
        
        # System-Karte
        self.system_card = self.create_monitoring_card("System", "assets/icons/dashboard/system.png")
        cards_layout.addWidget(self.system_card, 1, 1)
        
        parent_layout.addWidget(cards_frame)
        
    def create_monitoring_card(self, title, icon_path):
        """Einzelne Monitoring-Karte erstellen"""
        card = QFrame()
        card.setMinimumHeight(150)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Titel mit Icon
        title_layout = QHBoxLayout()
        icon_label = QLabel()
        icon_label.setFixedSize(32, 32)
        
        # Icon laden und skalieren
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            scaled_pixmap = pixmap.scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            icon_label.setPixmap(scaled_pixmap)
        else:
            # Fallback: Text-Icon
            icon_label.setStyleSheet("font-size: 20px;")
            icon_label.setText("📊")
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #f2ecfa;
        """)
        
        title_layout.addWidget(icon_label)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        layout.addLayout(title_layout)
        
        # Progress Bar
        progress_bar = QProgressBar()
        progress_bar.setMinimum(0)
        progress_bar.setMaximum(100)
        progress_bar.setValue(0)
        progress_bar.setFormat("%p%")
        
        layout.addWidget(progress_bar)
        
        # Details
        details_label = QLabel("Lade...")
        details_label.setStyleSheet("""
            font-size: 11px;
            color: #a0a0a0;
        """)
        
        layout.addWidget(details_label)
        layout.addStretch()
        
        # Speichere Referenzen für Updates
        card.progress_bar = progress_bar
        card.details_label = details_label
        
        return card
        
    def setup_button_area(self, parent_layout):
        """Button-Bereich für Aktionen"""
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        
        # Widget-Button
        widget_button = QPushButton("Desktop-Widgets")
        widget_button.setIcon(QIcon("assets/icons/buttons/widgets.png"))
        widget_button.clicked.connect(self.open_widgets)
        
        # Logging-Button
        logging_button = QPushButton("Daten-Logging")
        logging_button.setIcon(QIcon("assets/icons/buttons/logging.png"))
        logging_button.clicked.connect(self.toggle_logging)
        
        # Graphen-Button
        graphs_button = QPushButton("Graphen")
        graphs_button.setIcon(QIcon("assets/icons/buttons/graphs.png"))
        graphs_button.clicked.connect(self.open_graphs)
        
        # Einstellungen-Button
        settings_button = QPushButton("Einstellungen")
        settings_button.setIcon(QIcon("assets/icons/buttons/settings.png"))
        settings_button.clicked.connect(self.open_settings)
        
        button_layout.addWidget(widget_button)
        button_layout.addWidget(logging_button)
        button_layout.addWidget(graphs_button)
        button_layout.addStretch()
        button_layout.addWidget(settings_button)
        
        parent_layout.addWidget(button_frame)
        
    def setup_monitoring(self):
        """System-Monitoring Timer einrichten"""
        self.monitoring_timer = QTimer()
        self.monitoring_timer.timeout.connect(self.update_system_data)
        self.monitoring_timer.start(1000)  # Jede Sekunde
        
        # Initial Update
        self.update_system_data()
        
    def setup_system_tray(self):
        """System-Tray einrichten"""
        try:
            # Tray-Icon erstellen
            self.tray_icon.create_tray_icon()
            
            # Signals verbinden
            self.tray_icon.show_main_window.connect(self.show_main_window)
            self.tray_icon.hide_main_window.connect(self.hide_main_window)
            self.tray_icon.open_widgets.connect(self.open_widgets)
            self.tray_icon.open_graphs.connect(self.open_graphs)
            self.tray_icon.toggle_logging.connect(self.toggle_logging)
            self.tray_icon.quit_app.connect(self.quit_application)
            
            print("System-Tray eingerichtet")
            
        except Exception as e:
            print(f"Fehler beim Einrichten des System-Trays: {e}")
            
    def show_main_window(self):
        """Hauptfenster anzeigen"""
        self.show()
        self.raise_()
        self.activateWindow()
        
    def hide_main_window(self):
        """Hauptfenster ausblenden"""
        self.hide()
        
    def quit_application(self):
        """Anwendung beenden"""
        if self.tray_icon.is_tray_active():
            self.tray_icon.hide_tray_icon()
        sys.exit(0)
        
    def update_system_data(self):
        """System-Daten aktualisieren"""
        try:
            # CPU-Daten
            cpu_percent = psutil.cpu_percent(interval=0.1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            self.cpu_card.progress_bar.setValue(int(cpu_percent))
            self.cpu_card.details_label.setText(
                f"Kerne: {cpu_count} | Frequenz: {cpu_freq.current:.1f} GHz"
            )
            
            # RAM-Daten
            memory = psutil.virtual_memory()
            ram_percent = memory.percent
            ram_used_gb = memory.used / (1024**3)
            ram_total_gb = memory.total / (1024**3)
            
            self.ram_card.progress_bar.setValue(int(ram_percent))
            self.ram_card.details_label.setText(
                f"Verwendet: {ram_used_gb:.1f} GB / {ram_total_gb:.1f} GB"
            )
            
            # Disk-Daten
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            disk_used_gb = disk.used / (1024**3)
            disk_total_gb = disk.total / (1024**3)
            
            self.disk_card.progress_bar.setValue(int(disk_percent))
            self.disk_card.details_label.setText(
                f"Verwendet: {disk_used_gb:.1f} GB / {disk_total_gb:.1f} GB"
            )
            
            # System-Daten
            platform = sys.platform
            username = os.getlogin()
            
            self.system_card.progress_bar.setValue(100)  # System läuft
            self.system_card.details_label.setText(
                f"OS: {platform} | Benutzer: {username}"
            )
            
        except Exception as e:
            print(f"Fehler beim Update der System-Daten: {e}")
            
    def open_widgets(self):
        """Desktop-Widgets öffnen"""
        print("Desktop-Widgets werden geöffnet...")
        
        # Widgets importieren
        try:
            from widgets.cpu_widget import CPUWidget
            from widgets.ram_widget import RAMWidget
            from widgets.disk_widget import DiskWidget
            from widgets.system_widget import SystemWidget
            
            # Widgets erstellen und anzeigen
            self.cpu_widget = CPUWidget()
            self.ram_widget = RAMWidget()
            self.disk_widget = DiskWidget()
            self.system_widget = SystemWidget()
            
            # Widgets anzeigen
            self.cpu_widget.show()
            self.ram_widget.show()
            self.disk_widget.show()
            self.system_widget.show()
            
            # Widget-Schließung behandeln
            self.cpu_widget.widget_closed.connect(self.on_widget_closed)
            self.ram_widget.widget_closed.connect(self.on_widget_closed)
            self.disk_widget.widget_closed.connect(self.on_widget_closed)
            self.system_widget.widget_closed.connect(self.on_widget_closed)
            
            print("Alle Desktop-Widgets wurden geöffnet!")
            
        except Exception as e:
            print(f"Fehler beim Öffnen der Widgets: {e}")
            
    def on_widget_closed(self, widget_type):
        """Widget wurde geschlossen"""
        print(f"Widget {widget_type} wurde geschlossen")
        
    def toggle_logging(self):
        """Daten-Logging starten/stoppen"""
        if not self.logging_active:
            # Logging starten
            self.logger.start_logging()
            self.logging_active = True
            print("Daten-Logging gestartet")
        else:
            # Logging stoppen
            self.logger.stop_logging()
            self.logging_active = False
            print("Daten-Logging gestoppt")
        
    def open_graphs(self):
        """Graphen öffnen"""
        print("Graphen werden geöffnet...")
        try:
            from windows.graph_window import GraphWindow
            self.graph_window = GraphWindow()
            self.graph_window.show()
            print("Graph-Fenster geöffnet!")
        except Exception as e:
            print(f"Fehler beim Öffnen der Graphen: {e}")
        
    def open_settings(self):
        """Einstellungen öffnen"""
        print("Einstellungen werden geöffnet...")
        try:
            from windows.settings_window import SettingsWindow
            self.settings_window = SettingsWindow(self.config_manager)
            self.settings_window.settings_changed.connect(self.on_settings_changed)
            self.settings_window.show()
            print("Einstellungen-Fenster geöffnet!")
        except Exception as e:
            print(f"Fehler beim Öffnen der Einstellungen: {e}")
            
    def on_settings_changed(self):
        """Einstellungen wurden geändert"""
        print("Einstellungen wurden geändert - Anwendung wird aktualisiert...")
        # TODO: Theme und andere Einstellungen anwenden

def main():
    """Hauptfunktion"""
    app = QApplication(sys.argv)
    
    # App-Eigenschaften
    app.setApplicationName("SystemMonitorX")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("SystemMonitorX Team")
    
    # Hauptfenster erstellen und anzeigen
    window = SystemMonitorX()
    window.show()
    
    # Event-Loop starten
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 