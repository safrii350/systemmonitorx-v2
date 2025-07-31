#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SystemMonitorX - CPU-Widget
Desktop-Widget für CPU-Monitoring

Autor: SystemMonitorX Team
Version: 1.0.0
"""

from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt
import psutil
from .base_widget import BaseWidget

class CPUWidget(BaseWidget):
    """
    CPU-Monitoring Widget
    - CPU-Auslastung in Prozent
    - Anzahl der Kerne
    - Frequenz (GHz)
    - Progress-Bar
    """
    
    def __init__(self):
        super().__init__(
            widget_type="cpu",
            title="CPU",
            icon="🖥️"
        )
        
        # Widget-spezifische UI
        self.setup_cpu_ui()
        
    def setup_cpu_ui(self):
        """CPU-spezifische UI erstellen"""
        # Progress Bar für CPU-Auslastung
        self.cpu_progress = QProgressBar()
        self.cpu_progress.setMinimum(0)
        self.cpu_progress.setMaximum(100)
        self.cpu_progress.setValue(0)
        self.cpu_progress.setFormat("CPU: %p%")
        
        # Details-Layout
        details_layout = QHBoxLayout()
        
        # CPU-Kerne
        self.cores_label = QLabel("Kerne: 0")
        self.cores_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # CPU-Frequenz
        self.freq_label = QLabel("Freq: 0.0 GHz")
        self.freq_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        details_layout.addWidget(self.cores_label)
        details_layout.addStretch()
        details_layout.addWidget(self.freq_label)
        
        # Layout hinzufügen
        self.content_layout.addWidget(self.cpu_progress)
        self.content_layout.addLayout(details_layout)
        
    def update_data(self):
        """CPU-Daten aktualisieren"""
        try:
            # CPU-Auslastung
            cpu_percent = psutil.cpu_percent(interval=0.1)
            self.cpu_progress.setValue(int(cpu_percent))
            
            # CPU-Kerne
            cpu_count = psutil.cpu_count()
            self.cores_label.setText(f"Kerne: {cpu_count}")
            
            # CPU-Frequenz
            cpu_freq = psutil.cpu_freq()
            if cpu_freq:
                freq_ghz = cpu_freq.current / 1000  # MHz zu GHz
                self.freq_label.setText(f"Freq: {freq_ghz:.1f} GHz")
            else:
                self.freq_label.setText("Freq: N/A")
                
        except Exception as e:
            print(f"Fehler beim CPU-Widget Update: {e}")
            self.cpu_progress.setValue(0)
            self.cores_label.setText("Kerne: N/A")
            self.freq_label.setText("Freq: N/A") 