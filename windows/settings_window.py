#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SystemMonitorX - Einstellungen-Fenster
Tab-basierte Konfiguration für alle App-Einstellungen

Autor: SystemMonitorX Team
Version: 1.0.0
"""

import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTabWidget, QFrame, QSpinBox,
    QCheckBox, QLineEdit, QColorDialog, QGroupBox,
    QFormLayout, QDialog, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPalette, QColor

from utils.config import ConfigManager

# Theme-Farben (Dark Mode)
THEME_COLORS = {
    'background': '#141414',
    'accent': '#4a307d',
    'text': '#f2ecfa',
    'text_secondary': '#a0a0a0',
    'card_background': '#1e1e1e'
}

class SettingsWindow(QMainWindow):
    """
    Einstellungen-Fenster für SystemMonitorX
    Tab-basierte Konfiguration für alle App-Einstellungen
    """
    
    # Signals
    settings_changed = pyqtSignal()
    
    def __init__(self, config_manager: ConfigManager):
        super().__init__()
        self.config_manager = config_manager
        self.setWindowTitle("SystemMonitorX - Einstellungen")
        self.setMinimumSize(600, 500)
        
        # UI Setup
        self.setup_theme()
        self.setup_ui()
        
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
        
        # Stylesheet
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
            
            QTabWidget::pane {
                border: 1px solid #2a2a2a;
                background-color: #1e1e1e;
                border-radius: 8px;
            }
            
            QTabBar::tab {
                background-color: #2a2a2a;
                color: #f2ecfa;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-family: 'Consolas', monospace;
                font-size: 11px;
            }
            
            QTabBar::tab:selected {
                background-color: #4a307d;
            }
            
            QTabBar::tab:hover {
                background-color: #3a206d;
            }
            
            QSpinBox, QLineEdit {
                background-color: #2a2a2a;
                color: #f2ecfa;
                border: 1px solid #4a307d;
                border-radius: 4px;
                padding: 4px 8px;
                font-family: 'Consolas', monospace;
                font-size: 11px;
            }
            
            QCheckBox {
                color: #f2ecfa;
                font-family: 'Consolas', monospace;
                font-size: 11px;
            }
            
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #4a307d;
                border-radius: 3px;
                background-color: #2a2a2a;
            }
            
            QCheckBox::indicator:checked {
                background-color: #4a307d;
            }
            
            QGroupBox {
                color: #f2ecfa;
                font-family: 'Consolas', monospace;
                font-size: 12px;
                font-weight: bold;
                border: 1px solid #4a307d;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
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
        
        # Tab-Widget für Einstellungen
        self.setup_tab_widget(main_layout)
        
        # Button-Bereich
        self.setup_button_area(main_layout)
        
    def setup_header(self, parent_layout):
        """Header-Bereich"""
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        
        # Titel
        title_label = QLabel("⚙️ SystemMonitorX - Einstellungen")
        title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #f2ecfa;
            font-family: 'Consolas', monospace;
        """)
        
        # Untertitel
        subtitle_label = QLabel("App-Konfiguration und Einstellungen")
        subtitle_label.setStyleSheet("""
            font-size: 12px;
            color: #a0a0a0;
            font-family: 'Consolas', monospace;
        """)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(subtitle_label)
        
        parent_layout.addWidget(header_frame)
        
    def setup_tab_widget(self, parent_layout):
        """Tab-Widget für verschiedene Einstellungen"""
        self.tab_widget = QTabWidget()
        
        # Theme Tab
        self.theme_tab = self.create_theme_tab()
        self.tab_widget.addTab(self.theme_tab, "🎨 Theme")
        
        # Logging Tab
        self.logging_tab = self.create_logging_tab()
        self.tab_widget.addTab(self.logging_tab, "📊 Logging")
        
        # Monitoring Tab
        self.monitoring_tab = self.create_monitoring_tab()
        self.tab_widget.addTab(self.monitoring_tab, "🖥️ Monitoring")
        
        # System-Tray Tab
        self.tray_tab = self.create_tray_tab()
        self.tab_widget.addTab(self.tray_tab, "📌 System-Tray")
        
        # Konfiguration Tab
        self.config_tab = self.create_config_tab()
        self.tab_widget.addTab(self.config_tab, "⚙️ Konfiguration")
        
        parent_layout.addWidget(self.tab_widget)
        
    def create_theme_tab(self) -> QWidget:
        """Theme-Einstellungen Tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Theme-Farben
        theme_group = QGroupBox("Theme-Farben")
        theme_layout = QFormLayout(theme_group)
        
        # Farb-Buttons
        self.color_buttons = {}
        colors = self.config_manager.get_theme_colors()
        
        for color_name, color_value in colors.items():
            button = QPushButton()
            button.setFixedSize(60, 30)
            button.setStyleSheet(f"background-color: {color_value}; border: 1px solid #4a307d;")
            button.clicked.connect(lambda checked, name=color_name: self.choose_color(name))
            
            label = QLabel(color_name.replace('_', ' ').title())
            theme_layout.addRow(label, button)
            self.color_buttons[color_name] = button
            
        layout.addWidget(theme_group)
        layout.addStretch()
        
        return tab
        
    def create_logging_tab(self) -> QWidget:
        """Logging-Einstellungen Tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Logging-Konfiguration
        logging_config = self.config_manager.get_logging_config()
        
        # Allgemeine Einstellungen
        general_group = QGroupBox("Allgemeine Einstellungen")
        general_layout = QFormLayout(general_group)
        
        self.logging_enabled = QCheckBox("Logging aktiviert")
        self.logging_enabled.setChecked(logging_config.get("enabled", False))
        general_layout.addRow(self.logging_enabled)
        
        # Buffer-Einstellungen
        buffer_group = QGroupBox("Buffer-Einstellungen")
        buffer_layout = QFormLayout(buffer_group)
        
        self.buffer_size = QSpinBox()
        self.buffer_size.setRange(10, 300)
        self.buffer_size.setValue(logging_config.get("buffer_size", 60))
        buffer_layout.addRow("Buffer-Größe (Sekunden):", self.buffer_size)
        
        self.max_files = QSpinBox()
        self.max_files.setRange(1, 50)
        self.max_files.setValue(logging_config.get("max_files", 10))
        buffer_layout.addRow("Max. Log-Dateien:", self.max_files)
        
        self.auto_save_interval = QSpinBox()
        self.auto_save_interval.setRange(10, 300)
        self.auto_save_interval.setValue(logging_config.get("auto_save_interval", 60))
        buffer_layout.addRow("Auto-Save Intervall (Sekunden):", self.auto_save_interval)
        
        layout.addWidget(general_group)
        layout.addWidget(buffer_group)
        layout.addStretch()
        
        return tab
        
    def create_monitoring_tab(self) -> QWidget:
        """Monitoring-Einstellungen Tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Monitoring-Konfiguration
        monitoring_config = self.config_manager.get_monitoring_config()
        
        # Update-Einstellungen
        update_group = QGroupBox("Update-Einstellungen")
        update_layout = QFormLayout(update_group)
        
        self.update_interval = QSpinBox()
        self.update_interval.setRange(500, 5000)
        self.update_interval.setValue(monitoring_config.get("update_interval", 1000))
        self.update_interval.setSuffix(" ms")
        update_layout.addRow("Update-Intervall:", self.update_interval)
        
        # Feature-Einstellungen
        features_group = QGroupBox("Feature-Einstellungen")
        features_layout = QFormLayout(features_group)
        
        self.widgets_enabled = QCheckBox("Desktop-Widgets aktiviert")
        self.widgets_enabled.setChecked(monitoring_config.get("widgets_enabled", True))
        features_layout.addRow(self.widgets_enabled)
        
        self.graphs_enabled = QCheckBox("Graphen aktiviert")
        self.graphs_enabled.setChecked(monitoring_config.get("graphs_enabled", True))
        features_layout.addRow(self.graphs_enabled)
        
        layout.addWidget(update_group)
        layout.addWidget(features_group)
        layout.addStretch()
        
        return tab
        
    def create_tray_tab(self) -> QWidget:
        """System-Tray Einstellungen Tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # System-Tray-Konfiguration
        tray_config = self.config_manager.get_system_tray_config()
        
        # Tray-Einstellungen
        tray_group = QGroupBox("System-Tray Einstellungen")
        tray_layout = QFormLayout(tray_group)
        
        self.tray_enabled = QCheckBox("System-Tray aktiviert")
        self.tray_enabled.setChecked(tray_config.get("enabled", True))
        tray_layout.addRow(self.tray_enabled)
        
        self.minimize_to_tray = QCheckBox("Minimieren in System-Tray")
        self.minimize_to_tray.setChecked(tray_config.get("minimize_to_tray", True))
        tray_layout.addRow(self.minimize_to_tray)
        
        self.start_minimized = QCheckBox("Gestartet minimiert")
        self.start_minimized.setChecked(tray_config.get("start_minimized", False))
        tray_layout.addRow(self.start_minimized)
        
        layout.addWidget(tray_group)
        layout.addStretch()
        
        return tab
        
    def create_config_tab(self) -> QWidget:
        """Konfigurations-Management Tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Konfigurations-Aktionen
        actions_group = QGroupBox("Konfigurations-Aktionen")
        actions_layout = QVBoxLayout(actions_group)
        
        # Export-Button
        export_button = QPushButton("📤 Konfiguration exportieren")
        export_button.clicked.connect(self.export_config)
        actions_layout.addWidget(export_button)
        
        # Import-Button
        import_button = QPushButton("📥 Konfiguration importieren")
        import_button.clicked.connect(self.import_config)
        actions_layout.addWidget(import_button)
        
        # Reset-Button
        reset_button = QPushButton("🔄 Auf Standard zurücksetzen")
        reset_button.clicked.connect(self.reset_to_defaults)
        actions_layout.addWidget(reset_button)
        
        # Konfigurations-Info
        info_group = QGroupBox("Konfigurations-Informationen")
        info_layout = QFormLayout(info_group)
        
        summary = self.config_manager.get_config_summary()
        
        info_layout.addRow("Einstellungen-Datei:", QLabel(summary["settings_file"]))
        info_layout.addRow("Widgets-Datei:", QLabel(summary["widgets_file"]))
        info_layout.addRow("Einstellungen:", QLabel(str(summary["settings_count"])))
        info_layout.addRow("Widgets:", QLabel(str(summary["widgets_count"])))
        info_layout.addRow("Letzte Änderung:", QLabel(summary["last_updated"]))
        
        layout.addWidget(actions_group)
        layout.addWidget(info_group)
        layout.addStretch()
        
        return tab
        
    def setup_button_area(self, parent_layout):
        """Button-Bereich für Aktionen"""
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        
        # Speichern-Button
        save_button = QPushButton("💾 Speichern")
        save_button.clicked.connect(self.save_settings)
        
        # Abbrechen-Button
        cancel_button = QPushButton("❌ Abbrechen")
        cancel_button.clicked.connect(self.close)
        
        button_layout.addWidget(save_button)
        button_layout.addStretch()
        button_layout.addWidget(cancel_button)
        
        parent_layout.addWidget(button_frame)
        
    def choose_color(self, color_name: str):
        """Farbe auswählen"""
        current_color = self.config_manager.get_theme_colors().get(color_name, "#000000")
        color = QColorDialog.getColor(QColor(current_color), self, f"Farbe für {color_name}")
        
        if color.isValid():
            # Button-Farbe aktualisieren
            button = self.color_buttons[color_name]
            button.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #4a307d;")
            
    def save_settings(self):
        """Einstellungen speichern"""
        try:
            # Theme-Farben speichern
            theme_colors = {}
            for color_name, button in self.color_buttons.items():
                # Farbe aus Button-Stylesheet extrahieren
                style = button.styleSheet()
                if "background-color:" in style:
                    color = style.split("background-color:")[1].split(";")[0].strip()
                    theme_colors[color_name] = color
                    
            self.config_manager.set_theme_colors(theme_colors)
            
            # Logging-Konfiguration speichern
            logging_config = {
                "enabled": self.logging_enabled.isChecked(),
                "buffer_size": self.buffer_size.value(),
                "max_files": self.max_files.value(),
                "auto_save_interval": self.auto_save_interval.value()
            }
            self.config_manager.set_logging_config(logging_config)
            
            # Monitoring-Konfiguration speichern
            monitoring_config = {
                "update_interval": self.update_interval.value(),
                "widgets_enabled": self.widgets_enabled.isChecked(),
                "graphs_enabled": self.graphs_enabled.isChecked()
            }
            self.config_manager.set_monitoring_config(monitoring_config)
            
            # System-Tray-Konfiguration speichern
            tray_config = {
                "enabled": self.tray_enabled.isChecked(),
                "minimize_to_tray": self.minimize_to_tray.isChecked(),
                "start_minimized": self.start_minimized.isChecked()
            }
            self.config_manager.set_system_tray_config(tray_config)
            
            # Signal senden
            self.settings_changed.emit()
            
            QMessageBox.information(self, "Einstellungen", "Einstellungen erfolgreich gespeichert!")
            self.close()
            
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Fehler beim Speichern der Einstellungen: {e}")
            
    def export_config(self):
        """Konfiguration exportieren"""
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Konfiguration exportieren", 
            "systemmonitorx_config.json", 
            "JSON-Dateien (*.json)"
        )
        
        if filepath:
            try:
                self.config_manager.export_config(filepath)
                QMessageBox.information(self, "Export", f"Konfiguration exportiert nach:\n{filepath}")
            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"Fehler beim Exportieren: {e}")
                
    def import_config(self):
        """Konfiguration importieren"""
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Konfiguration importieren", 
            "", "JSON-Dateien (*.json)"
        )
        
        if filepath:
            try:
                self.config_manager.import_config(filepath)
                QMessageBox.information(self, "Import", f"Konfiguration importiert von:\n{filepath}")
                self.settings_changed.emit()
            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"Fehler beim Importieren: {e}")
                
    def reset_to_defaults(self):
        """Auf Standard zurücksetzen"""
        reply = QMessageBox.question(
            self, "Zurücksetzen", 
            "Möchten Sie wirklich alle Einstellungen auf Standard zurücksetzen?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.config_manager.reset_to_defaults()
                QMessageBox.information(self, "Zurücksetzen", "Einstellungen auf Standard zurückgesetzt!")
                self.settings_changed.emit()
            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"Fehler beim Zurücksetzen: {e}") 