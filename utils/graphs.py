#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SystemMonitorX - Graph-System
Matplotlib-Graphen mit Dark Mode Styling

Autor: SystemMonitorX Team
Version: 1.0.0
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any
import psutil
import threading
import time

# Dark Mode Matplotlib Styling
plt.style.use('dark_background')

class SystemGraphs:
    """
    Graph-System für SystemMonitorX
    - System-Übersicht, CPU, RAM, Disk Graphen
    - Dark Mode Styling
    - Zoom und Navigation
    - Live-Updates
    """
    
    def __init__(self):
        # Theme-Farben
        self.colors = {
            'background': '#141414',
            'accent': '#4a307d',
            'text': '#f2ecfa',
            'grid': '#2a2a2a',
            'cpu': '#ff6b6b',
            'ram': '#4ecdc4',
            'disk': '#45b7d1',
            'system': '#96ceb4'
        }
        
        # Daten-History
        self.data_history = []
        self.max_history = 300  # 5 Minuten bei 1s Updates
        
        # Threading
        self.graphing_active = False
        self.graphing_thread = None
        
    def create_system_overview_graph(self) -> Figure:
        """System-Übersicht Graph erstellen"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        fig.patch.set_facecolor(self.colors['background'])
        
        # CPU Graph
        self._setup_axis(ax1, "CPU Auslastung", "%", self.colors['cpu'])
        ax1.set_title("CPU", color=self.colors['text'], fontsize=14, fontweight='bold')
        
        # RAM Graph
        self._setup_axis(ax2, "RAM Auslastung", "%", self.colors['ram'])
        ax2.set_title("RAM", color=self.colors['text'], fontsize=14, fontweight='bold')
        
        # Disk Graph
        self._setup_axis(ax3, "Festplatten Auslastung", "%", self.colors['disk'])
        ax3.set_title("Festplatte", color=self.colors['text'], fontsize=14, fontweight='bold')
        
        # System Info
        self._setup_system_info(ax4)
        
        plt.tight_layout()
        return fig
        
    def create_cpu_graph(self) -> Figure:
        """CPU-spezifischer Graph"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        fig.patch.set_facecolor(self.colors['background'])
        
        # CPU Auslastung
        self._setup_axis(ax1, "CPU Auslastung", "%", self.colors['cpu'])
        ax1.set_title("CPU Auslastung", color=self.colors['text'], fontsize=16, fontweight='bold')
        
        # CPU Frequenz
        self._setup_axis(ax2, "CPU Frequenz", "GHz", self.colors['accent'])
        ax2.set_title("CPU Frequenz", color=self.colors['text'], fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        return fig
        
    def create_ram_graph(self) -> Figure:
        """RAM-spezifischer Graph"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        fig.patch.set_facecolor(self.colors['background'])
        
        # RAM Auslastung
        self._setup_axis(ax1, "RAM Auslastung", "%", self.colors['ram'])
        ax1.set_title("RAM Auslastung", color=self.colors['text'], fontsize=16, fontweight='bold')
        
        # RAM Verwendung
        self._setup_axis(ax2, "RAM Verwendung", "GB", self.colors['accent'])
        ax2.set_title("RAM Verwendung", color=self.colors['text'], fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        return fig
        
    def create_disk_graph(self) -> Figure:
        """Disk-spezifischer Graph"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        fig.patch.set_facecolor(self.colors['background'])
        
        # Disk Auslastung
        self._setup_axis(ax1, "Festplatten Auslastung", "%", self.colors['disk'])
        ax1.set_title("Festplatten Auslastung", color=self.colors['text'], fontsize=16, fontweight='bold')
        
        # Disk Verwendung
        self._setup_axis(ax2, "Festplatten Verwendung", "GB", self.colors['accent'])
        ax2.set_title("Festplatten Verwendung", color=self.colors['text'], fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        return fig
        
    def _setup_axis(self, ax, ylabel, unit, color):
        """Axis für Dark Mode konfigurieren"""
        ax.set_facecolor(self.colors['background'])
        ax.grid(True, color=self.colors['grid'], alpha=0.3)
        ax.set_ylabel(f"{ylabel} ({unit})", color=self.colors['text'], fontsize=12)
        ax.set_xlabel("Zeit", color=self.colors['text'], fontsize=12)
        ax.tick_params(colors=self.colors['text'])
        
        # Y-Achse Limits
        if unit == "%":
            ax.set_ylim(0, 100)
        elif unit == "GHz":
            ax.set_ylim(0, 5)  # Typische CPU-Frequenzen
        elif unit == "GB":
            ax.set_ylim(0, 50)  # Typische RAM/Storage-Größen
            
        return ax
        
    def _setup_system_info(self, ax):
        """System-Informationen anzeigen"""
        ax.set_facecolor(self.colors['background'])
        ax.axis('off')
        
        # System-Daten sammeln
        try:
            cpu_count = psutil.cpu_count()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            platform = psutil.sys.platform
            
            info_text = f"""
System-Informationen:

CPU: {cpu_count} Kerne
RAM: {memory.total / (1024**3):.1f} GB
Festplatte: {disk.total / (1024**3):.1f} GB
OS: {platform}
            """
            
            ax.text(0.1, 0.9, info_text, transform=ax.transAxes,
                   fontsize=12, color=self.colors['text'],
                   verticalalignment='top', fontfamily='monospace')
                   
        except Exception as e:
            ax.text(0.1, 0.9, f"Fehler beim Laden der System-Daten: {e}",
                   transform=ax.transAxes, fontsize=12, color='red')
                   
    def update_graph_data(self, data: Dict[str, Any]):
        """Graph-Daten aktualisieren"""
        timestamp = datetime.now()
        
        # Daten zum History hinzufügen
        data_point = {
            'timestamp': timestamp,
            'cpu_percent': data.get('cpu_percent', 0),
            'cpu_freq_ghz': data.get('cpu_freq_ghz', 0),
            'ram_percent': data.get('ram_percent', 0),
            'ram_used_gb': data.get('ram_used_gb', 0),
            'disk_percent': data.get('disk_percent', 0),
            'disk_used_gb': data.get('disk_used_gb', 0)
        }
        
        self.data_history.append(data_point)
        
        # History begrenzen
        if len(self.data_history) > self.max_history:
            self.data_history.pop(0)
            
    def get_recent_data(self, minutes: int = 5) -> List[Dict[str, Any]]:
        """Letzte Daten für Graphen zurückgeben"""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        return [d for d in self.data_history if d['timestamp'] > cutoff_time]
        
    def plot_live_data(self, ax, data_key: str, color: str, unit: str = ""):
        """Live-Daten auf Axis plotten"""
        if not self.data_history:
            return
            
        recent_data = self.get_recent_data()
        if not recent_data:
            return
            
        timestamps = [d['timestamp'] for d in recent_data]
        values = [d[data_key] for d in recent_data]
        
        ax.clear()
        self._setup_axis(ax, f"{data_key.replace('_', ' ').title()}", unit, color)
        
        ax.plot(timestamps, values, color=color, linewidth=2, marker='o', markersize=3)
        
        # X-Achse Format
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
    def start_live_updates(self):
        """Live-Updates starten"""
        if not self.graphing_active:
            self.graphing_active = True
            self.graphing_thread = threading.Thread(target=self._live_update_loop, daemon=True)
            self.graphing_thread.start()
            
    def stop_live_updates(self):
        """Live-Updates stoppen"""
        self.graphing_active = False
        
    def _live_update_loop(self):
        """Live-Update-Schleife"""
        while self.graphing_active:
            try:
                # System-Daten sammeln
                data = self._collect_system_data()
                self.update_graph_data(data)
                
            except Exception as e:
                print(f"Fehler im Live-Update-Loop: {e}")
                
            time.sleep(1)  # 1 Sekunde warten
            
    def _collect_system_data(self) -> Dict[str, Any]:
        """System-Daten für Graphen sammeln"""
        try:
            # CPU-Daten
            cpu_percent = psutil.cpu_percent(interval=0.1)
            cpu_freq = psutil.cpu_freq()
            cpu_freq_ghz = cpu_freq.current / 1000 if cpu_freq else 0
            
            # RAM-Daten
            memory = psutil.virtual_memory()
            ram_percent = memory.percent
            ram_used_gb = memory.used / (1024**3)
            
            # Disk-Daten
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            disk_used_gb = disk.used / (1024**3)
            
            return {
                'cpu_percent': cpu_percent,
                'cpu_freq_ghz': cpu_freq_ghz,
                'ram_percent': ram_percent,
                'ram_used_gb': ram_used_gb,
                'disk_percent': disk_percent,
                'disk_used_gb': disk_used_gb
            }
            
        except Exception as e:
            print(f"Fehler beim Sammeln der Graph-Daten: {e}")
            return {}
            
    def create_graph_widget(self, graph_type: str):
        """Graph-Widget mit Navigation erstellen"""
        if graph_type == "overview":
            fig = self.create_system_overview_graph()
        elif graph_type == "cpu":
            fig = self.create_cpu_graph()
        elif graph_type == "ram":
            fig = self.create_ram_graph()
        elif graph_type == "disk":
            fig = self.create_disk_graph()
        else:
            raise ValueError(f"Unbekannter Graph-Typ: {graph_type}")
            
        # Canvas erstellen
        canvas = FigureCanvas(fig)
        toolbar = NavigationToolbar(canvas, None)
        
        return canvas, toolbar, fig 