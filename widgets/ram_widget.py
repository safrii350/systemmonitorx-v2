#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SystemMonitorX - RAM-Widget
Desktop-Widget für RAM-Monitoring

Autor: SystemMonitorX Team
Version: 1.0.0
"""

from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt
import psutil
from .base_widget import BaseWidget

class RAMWidget(BaseWidget):
    """
    RAM-Monitoring Widget
    - RAM-Auslastung in Prozent
    - Verwendeter RAM in GB
    - Gesamter RAM in GB
    - Progress-Bar
    """
    
    def __init__(self):
        super().__init__(
            widget_type="ram",
            title="RAM",
            icon="💾"
        )
        
        # Widget-spezifische UI
        self.setup_ram_ui()
        
    def setup_ram_ui(self):
        """RAM-spezifische UI erstellen"""
        # Progress Bar für RAM-Auslastung
        self.ram_progress = QProgressBar()
        self.ram_progress.setMinimum(0)
        self.ram_progress.setMaximum(100)
        self.ram_progress.setValue(0)
        self.ram_progress.setFormat("RAM: %p%")
        
        # Details-Layout
        details_layout = QHBoxLayout()
        
        # Verwendeter RAM
        self.used_label = QLabel("Verwendet: 0.0 GB")
        self.used_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # Gesamter RAM
        self.total_label = QLabel("Gesamt: 0.0 GB")
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        details_layout.addWidget(self.used_label)
        details_layout.addStretch()
        details_layout.addWidget(self.total_label)
        
        # Layout hinzufügen
        self.content_layout.addWidget(self.ram_progress)
        self.content_layout.addLayout(details_layout)
        
    def update_data(self):
        """RAM-Daten aktualisieren"""
        try:
            # RAM-Daten
            memory = psutil.virtual_memory()
            ram_percent = memory.percent
            ram_used_gb = memory.used / (1024**3)
            ram_total_gb = memory.total / (1024**3)
            
            # Progress Bar aktualisieren
            self.ram_progress.setValue(int(ram_percent))
            
            # Labels aktualisieren
            self.used_label.setText(f"Verwendet: {ram_used_gb:.1f} GB")
            self.total_label.setText(f"Gesamt: {ram_total_gb:.1f} GB")
            
        except Exception as e:
            print(f"Fehler beim RAM-Widget Update: {e}")
            self.ram_progress.setValue(0)
            self.used_label.setText("Verwendet: N/A")
            self.total_label.setText("Gesamt: N/A") 