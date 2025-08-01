#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SystemMonitorX - Basis-Widget-Klasse
Desktop-Widgets mit PyQt6 und abgerundeten Ecken

Autor: SystemMonitorX Team
Version: 1.0.0
"""

import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QProgressBar
)
from PyQt6.QtCore import (
    Qt, QTimer, QPropertyAnimation, QEasingCurve,
    QRect, QPoint, pyqtSignal
)
from PyQt6.QtGui import (
    QPalette, QColor, QFont, QPainter, QBrush,
    QPen, QLinearGradient, QMouseEvent
)
import psutil
import json
import os

# Theme-Farben (Dark Mode)
THEME_COLORS = {
    'background': '#141414',
    'accent': '#4a307d',
    'text': '#f2ecfa',
    'text_secondary': '#a0a0a0',
    'widget_background': '#1e1e1e',
    'close_button': '#4a307d',
    'close_button_hover': '#5a408d'
}

class BaseWidget(QWidget):
    """
    Basis-Klasse für alle Desktop-Widgets
    - Abgerundete Ecken
    - Transparenter Hintergrund
    - Eigener Close-Button
    - Drag & Drop
    - 320x110px Größe
    """
    
    # Signal für Widget-Schließung
    widget_closed = pyqtSignal(str)
    
    def __init__(self, widget_type, title, icon_path):
        super().__init__()
        self.widget_type = widget_type
        self.title = title
        self.icon_path = icon_path
        
        # Widget-Eigenschaften
        self.setFixedSize(320, 110)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |  # Keine Standard-Titelleiste
            Qt.WindowType.WindowStaysOnTopHint |  # Immer im Vordergrund
            Qt.WindowType.Tool  # Tool-Fenster (nicht in Taskbar)
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        # Drag & Drop Variablen
        self.dragging = False
        self.drag_position = QPoint()
        
        # Setup
        self.setup_ui()
        self.setup_styling()
        self.setup_monitoring()
        
        # Position aus Konfiguration laden
        self.load_position()
        
    def setup_ui(self):
        """Benutzeroberfläche erstellen"""
        # Haupt-Layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)
        
        # Header mit Titel und Close-Button
        header_layout = QHBoxLayout()
        
        # Icon und Titel
        title_layout = QHBoxLayout()
        icon_label = QLabel()
        icon_label.setFixedSize(24, 24)
        
        # Icon laden und skalieren
        if os.path.exists(self.icon_path):
            from PyQt6.QtGui import QPixmap
            pixmap = QPixmap(self.icon_path)
            scaled_pixmap = pixmap.scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            icon_label.setPixmap(scaled_pixmap)
        else:
            # Fallback: Text-Icon
            icon_label.setStyleSheet("font-size: 16px;")
            icon_label.setText("📊")
        
        title_label = QLabel(self.title)
        title_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #f2ecfa;
            font-family: 'Consolas', monospace;
        """)
        
        title_layout.addWidget(icon_label)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        header_layout.addLayout(title_layout)
        
        # Close-Button (rund, lila)
        self.close_button = QPushButton("×")
        self.close_button.setFixedSize(20, 20)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #4a307d;
                color: #f2ecfa;
                border: none;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Consolas', monospace;
            }
            QPushButton:hover {
                background-color: #5a408d;
            }
            QPushButton:pressed {
                background-color: #3a206d;
            }
        """)
        self.close_button.clicked.connect(self.close_widget)
        
        header_layout.addWidget(self.close_button)
        
        main_layout.addLayout(header_layout)
        
        # Content-Bereich (wird von Unterklassen implementiert)
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        main_layout.addWidget(self.content_widget)
        
    def setup_styling(self):
        """Styling für abgerundete Ecken und Transparenz"""
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 30, 200);
                border-radius: 10px;
                border: 1px solid rgba(74, 48, 125, 100);
            }
            
            QLabel {
                color: #f2ecfa;
                font-family: 'Consolas', monospace;
                font-size: 11px;
            }
            
            QProgressBar {
                border: 1px solid #2a2a2a;
                border-radius: 4px;
                text-align: center;
                background-color: rgba(42, 42, 42, 150);
                color: #f2ecfa;
                font-family: 'Consolas', monospace;
                font-size: 10px;
            }
            
            QProgressBar::chunk {
                background-color: #4a307d;
                border-radius: 3px;
            }
        """)
        
    def setup_monitoring(self):
        """Monitoring-Timer für Updates"""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_data)
        self.update_timer.start(1000)  # Jede Sekunde
        
    def update_data(self):
        """Daten aktualisieren (wird von Unterklassen überschrieben)"""
        pass
        
    def close_widget(self):
        """Widget schließen"""
        self.save_position()
        self.widget_closed.emit(self.widget_type)
        self.close()
        
    def mousePressEvent(self, event: QMouseEvent):
        """Maus-Druck für Drag & Drop"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
            
    def mouseMoveEvent(self, event: QMouseEvent):
        """Maus-Bewegung für Drag & Drop"""
        if event.buttons() == Qt.MouseButton.LeftButton and self.dragging:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
            
    def mouseReleaseEvent(self, event: QMouseEvent):
        """Maus-Release für Drag & Drop"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            self.save_position()
            event.accept()
            
    def save_position(self):
        """Widget-Position speichern"""
        try:
            config_file = "config/widgets.json"
            os.makedirs("config", exist_ok=True)
            
            # Bestehende Konfiguration laden
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                config = {"widgets": {}}
            
            # Position speichern
            config["widgets"][self.widget_type] = {
                "x": self.x(),
                "y": self.y(),
                "visible": True
            }
            
            # Konfiguration speichern
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Fehler beim Speichern der Widget-Position: {e}")
            
    def load_position(self):
        """Widget-Position laden"""
        try:
            config_file = "config/widgets.json"
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                if self.widget_type in config.get("widgets", {}):
                    widget_config = config["widgets"][self.widget_type]
                    x = widget_config.get("x", 100)
                    y = widget_config.get("y", 100)
                    self.move(x, y)
                    
        except Exception as e:
            print(f"Fehler beim Laden der Widget-Position: {e}")
            # Standard-Position
            self.move(100, 100)
            
    def paintEvent(self, event):
        """Custom Paint Event für Glasmorphismus-Effekt"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Abgerundetes Rechteck mit Transparenz
        rect = self.rect()
        painter.setPen(QPen(QColor(74, 48, 125, 100), 1))
        painter.setBrush(QBrush(QColor(30, 30, 30, 200)))
        painter.drawRoundedRect(rect, 10, 10)
        
    def enterEvent(self, event):
        """Hover-Effekt beim Betreten"""
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 30, 220);
                border-radius: 10px;
                border: 1px solid rgba(74, 48, 125, 150);
            }
        """)
        
    def leaveEvent(self, event):
        """Hover-Effekt beim Verlassen"""
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 30, 200);
                border-radius: 10px;
                border: 1px solid rgba(74, 48, 125, 100);
            }
        """) 