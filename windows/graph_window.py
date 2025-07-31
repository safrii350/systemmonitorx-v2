#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SystemMonitorX - Graph-Fenster
PyQt6-Fenster für Matplotlib-Graphen

Autor: SystemMonitorX Team
Version: 1.0.0
"""

import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTabWidget, QFrame
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPalette, QColor

from utils.graphs import SystemGraphs

# Theme-Farben (Dark Mode)
THEME_COLORS = {
    'background': '#141414',
    'accent': '#4a307d',
    'text': '#f2ecfa',
    'text_secondary': '#a0a0a0',
    'card_background': '#1e1e1e'
}

class GraphWindow(QMainWindow):
    """
    Graph-Fenster für SystemMonitorX
    Zeigt Matplotlib-Graphen mit Dark Mode an
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SystemMonitorX - Graphen")
        self.setMinimumSize(1000, 700)
        
        # Graph-System initialisieren
        self.graphs = SystemGraphs()
        
        # UI Setup
        self.setup_theme()
        self.setup_ui()
        
        # Live-Updates starten
        self.graphs.start_live_updates()
        
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
        
        # Tab-Widget für Graphen
        self.setup_tab_widget(main_layout)
        
    def setup_header(self, parent_layout):
        """Header-Bereich"""
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        
        # Titel
        title_label = QLabel("📈 SystemMonitorX - Graphen")
        title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #f2ecfa;
            font-family: 'Consolas', monospace;
        """)
        
        # Untertitel
        subtitle_label = QLabel("Live-System-Monitoring Visualisierung")
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
        """Tab-Widget für verschiedene Graphen"""
        self.tab_widget = QTabWidget()
        
        # System-Übersicht Tab
        self.overview_tab = self.create_graph_tab("overview", "System-Übersicht")
        self.tab_widget.addTab(self.overview_tab, "🖥️ System-Übersicht")
        
        # CPU Tab
        self.cpu_tab = self.create_graph_tab("cpu", "CPU-Monitoring")
        self.tab_widget.addTab(self.cpu_tab, "🖥️ CPU")
        
        # RAM Tab
        self.ram_tab = self.create_graph_tab("ram", "RAM-Monitoring")
        self.tab_widget.addTab(self.ram_tab, "💾 RAM")
        
        # Disk Tab
        self.disk_tab = self.create_graph_tab("disk", "Festplatten-Monitoring")
        self.tab_widget.addTab(self.disk_tab, "💿 Festplatte")
        
        parent_layout.addWidget(self.tab_widget)
        
    def create_graph_tab(self, graph_type: str, title: str) -> QWidget:
        """Graph-Tab erstellen"""
        tab_widget = QWidget()
        layout = QVBoxLayout(tab_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Graph-Widget erstellen
        try:
            canvas, toolbar, fig = self.graphs.create_graph_widget(graph_type)
            
            # Toolbar-Layout
            toolbar_layout = QHBoxLayout()
            toolbar_layout.addWidget(toolbar)
            toolbar_layout.addStretch()
            
            # Refresh-Button
            refresh_button = QPushButton("🔄 Aktualisieren")
            refresh_button.clicked.connect(lambda: self.refresh_graph(graph_type))
            toolbar_layout.addWidget(refresh_button)
            
            layout.addLayout(toolbar_layout)
            layout.addWidget(canvas)
            
            # Referenzen speichern
            tab_widget.canvas = canvas
            tab_widget.figure = fig
            tab_widget.graph_type = graph_type
            
        except Exception as e:
            # Fehler-Label
            error_label = QLabel(f"Fehler beim Laden des Graphen: {e}")
            error_label.setStyleSheet("color: red; font-size: 14px;")
            layout.addWidget(error_label)
            
        return tab_widget
        
    def refresh_graph(self, graph_type: str):
        """Graph aktualisieren"""
        try:
            # Neuen Graph erstellen
            canvas, toolbar, fig = self.graphs.create_graph_widget(graph_type)
            
            # Tab finden und aktualisieren
            for i in range(self.tab_widget.count()):
                tab = self.tab_widget.widget(i)
                if hasattr(tab, 'graph_type') and tab.graph_type == graph_type:
                    # Alte Widgets entfernen
                    old_layout = tab.layout()
                    while old_layout.count():
                        child = old_layout.takeAt(0)
                        if child.widget():
                            child.widget().deleteLater()
                    
                    # Neue Widgets hinzufügen
                    toolbar_layout = QHBoxLayout()
                    toolbar_layout.addWidget(toolbar)
                    toolbar_layout.addStretch()
                    
                    refresh_button = QPushButton("🔄 Aktualisieren")
                    refresh_button.clicked.connect(lambda: self.refresh_graph(graph_type))
                    toolbar_layout.addWidget(refresh_button)
                    
                    old_layout.addLayout(toolbar_layout)
                    old_layout.addWidget(canvas)
                    
                    # Referenzen aktualisieren
                    tab.canvas = canvas
                    tab.figure = fig
                    break
                    
        except Exception as e:
            print(f"Fehler beim Aktualisieren des Graphen: {e}")
            
    def closeEvent(self, event):
        """Fenster schließen - Live-Updates stoppen"""
        self.graphs.stop_live_updates()
        event.accept()
        
    def update_graphs(self):
        """Alle Graphen mit Live-Daten aktualisieren"""
        try:
            # System-Daten sammeln
            data = self.graphs._collect_system_data()
            self.graphs.update_graph_data(data)
            
            # Graphen aktualisieren (falls Canvas vorhanden)
            for i in range(self.tab_widget.count()):
                tab = self.tab_widget.widget(i)
                if hasattr(tab, 'canvas') and tab.canvas:
                    tab.canvas.draw()
                    
        except Exception as e:
            print(f"Fehler beim Aktualisieren der Graphen: {e}") 