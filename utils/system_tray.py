#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SystemMonitorX - System-Tray
Dynamische Icons und Context-Menü

Autor: SystemMonitorX Team
Version: 1.0.0
"""

import pystray
from PIL import Image, ImageDraw, ImageFont
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, pyqtSignal, QObject
from PyQt6.QtGui import QIcon, QPixmap
import psutil
import threading
import time
from typing import Optional, Callable
import math

class SystemTrayIcon(QObject):
    """
    System-Tray Icon für SystemMonitorX
    - Dynamische Icons basierend auf System-Auslastung
    - Context-Menü mit Aktionen
    - Minimize-to-Tray Funktionalität
    """
    
    # Signals
    show_main_window = pyqtSignal()
    hide_main_window = pyqtSignal()
    open_widgets = pyqtSignal()
    open_graphs = pyqtSignal()
    toggle_logging = pyqtSignal()
    quit_app = pyqtSignal()
    
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.icon = None
        self.tray_active = False
        
        # System-Tray Konfiguration
        self.tray_config = self.config_manager.get_system_tray_config()
        
        # Icon-Generierung
        self.icon_size = 64
        self.update_interval = 2000  # 2 Sekunden
        
        # Threading
        self.update_thread = None
        self.update_active = False
        
    def create_tray_icon(self):
        """System-Tray Icon erstellen"""
        try:
            # Initial Icon erstellen
            icon_image = self.create_dynamic_icon()
            
            # Context-Menü erstellen
            menu = self.create_context_menu()
            
            # System-Tray Icon erstellen
            self.icon = pystray.Icon(
                "SystemMonitorX",
                icon_image,
                "SystemMonitorX",
                menu
            )
            
            # Icon anzeigen
            self.icon.run_detached()
            self.tray_active = True
            
            # Update-Thread starten
            self.start_icon_updates()
            
            print("System-Tray Icon erstellt")
            
        except Exception as e:
            print(f"Fehler beim Erstellen des System-Tray Icons: {e}")
            
    def create_dynamic_icon(self, cpu_percent: float = 0.0) -> Image.Image:
        """Dynamisches Icon basierend auf CPU-Auslastung erstellen"""
        # Icon-Größe
        size = self.icon_size
        
        # Bild erstellen
        image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Hintergrund (abgerundetes Rechteck)
        bg_color = (20, 20, 20, 200)  # Dark background
        draw.rounded_rectangle([(2, 2), (size-2, size-2)], radius=8, fill=bg_color)
        
        # CPU-Auslastung als einfacher Balken statt Kreis
        center = size // 2
        bar_width = size - 20
        bar_height = 8
        bar_y = center + 10
        
        # Hintergrund-Balken
        draw.rectangle(
            [10, bar_y, 10 + bar_width, bar_y + bar_height],
            fill=(40, 40, 40, 100)
        )
        
        # CPU-Auslastung-Balken
        if cpu_percent > 0:
            # Farbe basierend auf Auslastung
            if cpu_percent < 30:
                color = (76, 175, 80, 255)  # Grün
            elif cpu_percent < 70:
                color = (255, 193, 7, 255)   # Gelb
            else:
                color = (244, 67, 54, 255)   # Rot
                
            # Balken zeichnen
            bar_fill_width = int((cpu_percent / 100) * bar_width)
            draw.rectangle(
                [10, bar_y, 10 + bar_fill_width, bar_y + bar_height],
                fill=color
            )
            
        # Text (CPU %)
        try:
            # Einfache Schriftart verwenden
            font_size = max(8, size // 8)
            font = ImageFont.load_default()
            
            text = f"{int(cpu_percent)}%"
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            text_x = center - text_width // 2
            text_y = center - 15
            
            # Text-Hintergrund
            draw.rectangle(
                [text_x - 2, text_y - 2, text_x + text_width + 2, text_y + text_height + 2],
                fill=(0, 0, 0, 150)
            )
            
            # Text zeichnen
            draw.text((text_x, text_y), text, fill=(242, 236, 250, 255), font=font)
            
        except Exception as e:
            print(f"Fehler beim Zeichnen des Texts: {e}")
            
        return image
        

            
    def create_context_menu(self):
        """Context-Menü erstellen"""
        menu_items = [
            pystray.MenuItem("🖥️ Dashboard anzeigen", self.on_show_main_window),
            pystray.MenuItem("📊 Desktop-Widgets", self.on_open_widgets),
            pystray.MenuItem("📈 Graphen", self.on_open_graphs),
            pystray.MenuItem("📝 Logging", self.on_toggle_logging),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("❌ Beenden", self.on_quit_app)
        ]
        
        return pystray.Menu(*menu_items)
        
    def start_icon_updates(self):
        """Icon-Updates starten"""
        if not self.update_active:
            self.update_active = True
            self.update_thread = threading.Thread(target=self._update_icon_loop, daemon=True)
            self.update_thread.start()
            
    def stop_icon_updates(self):
        """Icon-Updates stoppen"""
        self.update_active = False
        if self.update_thread:
            self.update_thread.join(timeout=5)
            
    def _update_icon_loop(self):
        """Icon-Update-Schleife"""
        while self.update_active:
            try:
                # CPU-Auslastung abrufen
                cpu_percent = psutil.cpu_percent(interval=0.1)
                
                # Neues Icon erstellen
                new_icon = self.create_dynamic_icon(cpu_percent)
                
                # Icon aktualisieren (falls möglich)
                if self.icon and hasattr(self.icon, '_icon'):
                    self.icon._icon = new_icon
                    
            except Exception as e:
                print(f"Fehler im Icon-Update-Loop: {e}")
                
            time.sleep(self.update_interval / 1000)  # Millisekunden zu Sekunden
            
    def on_show_main_window(self, icon, item):
        """Hauptfenster anzeigen"""
        self.show_main_window.emit()
        
    def on_open_widgets(self, icon, item):
        """Desktop-Widgets öffnen"""
        self.open_widgets.emit()
        
    def on_open_graphs(self, icon, item):
        """Graphen öffnen"""
        self.open_graphs.emit()
        
    def on_toggle_logging(self, icon, item):
        """Logging umschalten"""
        self.toggle_logging.emit()
        
    def on_quit_app(self, icon, item):
        """Anwendung beenden"""
        self.quit_app.emit()
        
    def hide_tray_icon(self):
        """System-Tray Icon ausblenden"""
        if self.icon:
            self.icon.stop()
            self.tray_active = False
            self.stop_icon_updates()
            
    def update_tray_config(self):
        """Tray-Konfiguration aktualisieren"""
        self.tray_config = self.config_manager.get_system_tray_config()
        
    def is_tray_active(self) -> bool:
        """Prüfen ob Tray aktiv ist"""
        return self.tray_active
        
    def get_cpu_usage(self) -> float:
        """Aktuelle CPU-Auslastung abrufen"""
        try:
            return psutil.cpu_percent(interval=0.1)
        except:
            return 0.0 