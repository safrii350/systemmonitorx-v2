#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SystemMonitorX - Disk-Widget
Desktop-Widget für Festplatten-Monitoring

Autor: SystemMonitorX Team
Version: 1.0.0
"""

from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt
import psutil
from .base_widget import BaseWidget

class DiskWidget(BaseWidget):
    """
    Disk-Monitoring Widget
    - Festplatten-Auslastung in Prozent
    - Verwendeter Speicher in GB
    - Gesamter Speicher in GB
    - Progress-Bar
    """
    
    def __init__(self):
        super().__init__(
            widget_type="disk",
            title="Festplatte",
            icon_path="assets/widgets/disk_widget.png"
        )
        
        # Widget-spezifische UI
        self.setup_disk_ui()
        
    def setup_disk_ui(self):
        """Disk-spezifische UI erstellen"""
        # Progress Bar für Disk-Auslastung
        self.disk_progress = QProgressBar()
        self.disk_progress.setMinimum(0)
        self.disk_progress.setMaximum(100)
        self.disk_progress.setValue(0)
        self.disk_progress.setFormat("Disk: %p%")
        
        # Details-Layout
        details_layout = QHBoxLayout()
        
        # Verwendeter Speicher
        self.used_label = QLabel("Verwendet: 0.0 GB")
        self.used_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # Gesamter Speicher
        self.total_label = QLabel("Gesamt: 0.0 GB")
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        details_layout.addWidget(self.used_label)
        details_layout.addStretch()
        details_layout.addWidget(self.total_label)
        
        # Layout hinzufügen
        self.content_layout.addWidget(self.disk_progress)
        self.content_layout.addLayout(details_layout)
        
    def update_data(self):
        """Disk-Daten aktualisieren"""
        try:
            # Disk-Daten (Hauptfestplatte)
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            disk_used_gb = disk.used / (1024**3)
            disk_total_gb = disk.total / (1024**3)
            
            # Progress Bar aktualisieren
            self.disk_progress.setValue(int(disk_percent))
            
            # Labels aktualisieren
            self.used_label.setText(f"Verwendet: {disk_used_gb:.1f} GB")
            self.total_label.setText(f"Gesamt: {disk_total_gb:.1f} GB")
            
        except Exception as e:
            print(f"Fehler beim Disk-Widget Update: {e}")
            self.disk_progress.setValue(0)
            self.used_label.setText("Verwendet: N/A")
            self.total_label.setText("Gesamt: N/A") 