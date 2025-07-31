#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SystemMonitorX - System-Widget
Desktop-Widget für System-Informationen

Autor: SystemMonitorX Team
Version: 1.0.0
"""

from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
import psutil
import os
import sys
from .base_widget import BaseWidget

class SystemWidget(BaseWidget):
    """
    System-Informationen Widget
    - Betriebssystem
    - Benutzername
    - Online-Status
    - System-Status
    """
    
    def __init__(self):
        super().__init__(
            widget_type="system",
            title="System",
            icon="⚙️"
        )
        
        # Widget-spezifische UI
        self.setup_system_ui()
        
    def setup_system_ui(self):
        """System-spezifische UI erstellen"""
        # System-Status
        self.status_label = QLabel("Status: Online")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            font-size: 12px;
            font-weight: bold;
            color: #4a307d;
        """)
        
        # Details-Layout
        details_layout = QVBoxLayout()
        
        # Betriebssystem
        self.os_label = QLabel("OS: Windows")
        self.os_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # Benutzername
        self.user_label = QLabel("Benutzer: Unknown")
        self.user_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # Online-Status
        self.online_label = QLabel("Online: Ja")
        self.online_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        details_layout.addWidget(self.os_label)
        details_layout.addWidget(self.user_label)
        details_layout.addWidget(self.online_label)
        
        # Layout hinzufügen
        self.content_layout.addWidget(self.status_label)
        self.content_layout.addLayout(details_layout)
        
    def update_data(self):
        """System-Daten aktualisieren"""
        try:
            # Betriebssystem
            platform = sys.platform
            if platform == "win32":
                os_name = "Windows"
            elif platform == "darwin":
                os_name = "macOS"
            elif platform.startswith("linux"):
                os_name = "Linux"
            else:
                os_name = platform
                
            self.os_label.setText(f"OS: {os_name}")
            
            # Benutzername
            try:
                username = os.getlogin()
                self.user_label.setText(f"Benutzer: {username}")
            except:
                self.user_label.setText("Benutzer: Unknown")
                
            # Online-Status (einfache Prüfung)
            try:
                # Prüfe ob Netzwerk verfügbar ist
                network = psutil.net_if_addrs()
                if network:
                    self.online_label.setText("Online: Ja")
                    self.status_label.setText("Status: Online")
                    self.status_label.setStyleSheet("""
                        font-size: 12px;
                        font-weight: bold;
                        color: #4a307d;
                    """)
                else:
                    self.online_label.setText("Online: Nein")
                    self.status_label.setText("Status: Offline")
                    self.status_label.setStyleSheet("""
                        font-size: 12px;
                        font-weight: bold;
                        color: #a0a0a0;
                    """)
            except:
                self.online_label.setText("Online: Unbekannt")
                self.status_label.setText("Status: Unbekannt")
                self.status_label.setStyleSheet("""
                    font-size: 12px;
                    font-weight: bold;
                    color: #a0a0a0;
                """)
                
        except Exception as e:
            print(f"Fehler beim System-Widget Update: {e}")
            self.os_label.setText("OS: N/A")
            self.user_label.setText("Benutzer: N/A")
            self.online_label.setText("Online: N/A")
            self.status_label.setText("Status: Fehler")
            self.status_label.setStyleSheet("""
                font-size: 12px;
                font-weight: bold;
                color: #ff4444;
            """) 