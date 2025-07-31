#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SystemMonitorX - Konfigurations-System
JSON-basierte Einstellungen und Widget-Positionen

Autor: SystemMonitorX Team
Version: 1.0.0
"""

import json
import os
from typing import Dict, Any, Optional
from datetime import datetime

class ConfigManager:
    """
    Konfigurations-Manager für SystemMonitorX
    - JSON-basierte Einstellungen
    - Widget-Positionen speichern
    - App-Settings verwalten
    """
    
    def __init__(self):
        self.config_dir = "config"
        self.settings_file = os.path.join(self.config_dir, "settings.json")
        self.widgets_file = os.path.join(self.config_dir, "widgets.json")
        
        # Standard-Einstellungen
        self.default_settings = {
            "theme": {
                "background": "#141414",
                "accent": "#4a307d",
                "text": "#f2ecfa",
                "text_secondary": "#a0a0a0",
                "card_background": "#1e1e1e",
                "progress_background": "#2a2a2a"
            },
            "logging": {
                "enabled": False,
                "buffer_size": 60,
                "max_files": 10,
                "auto_save_interval": 60
            },
            "monitoring": {
                "update_interval": 1000,
                "widgets_enabled": True,
                "graphs_enabled": True
            },
            "system_tray": {
                "enabled": True,
                "minimize_to_tray": True,
                "start_minimized": False
            },
            "window": {
                "width": 800,
                "height": 600,
                "x": 100,
                "y": 100,
                "maximized": False
            }
        }
        
        # Standard-Widget-Positionen
        self.default_widgets = {
            "cpu": {"x": 50, "y": 50, "visible": True},
            "ram": {"x": 400, "y": 50, "visible": True},
            "disk": {"x": 50, "y": 200, "visible": True},
            "system": {"x": 400, "y": 200, "visible": True}
        }
        
        # Erstelle Config-Verzeichnis
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Lade oder erstelle Konfigurationen
        self.settings = self.load_settings()
        self.widgets = self.load_widgets()
        
    def load_settings(self) -> Dict[str, Any]:
        """Einstellungen laden oder Standard-Werte erstellen"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    # Neue Standard-Werte hinzufügen
                    self._merge_defaults(settings, self.default_settings)
                    return settings
            else:
                # Standard-Einstellungen erstellen
                self.save_settings(self.default_settings)
                return self.default_settings.copy()
                
        except Exception as e:
            print(f"Fehler beim Laden der Einstellungen: {e}")
            return self.default_settings.copy()
            
    def save_settings(self, settings: Dict[str, Any]):
        """Einstellungen speichern"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Fehler beim Speichern der Einstellungen: {e}")
            
    def load_widgets(self) -> Dict[str, Any]:
        """Widget-Positionen laden oder Standard-Werte erstellen"""
        try:
            if os.path.exists(self.widgets_file):
                with open(self.widgets_file, 'r', encoding='utf-8') as f:
                    widgets = json.load(f)
                    # Neue Standard-Werte hinzufügen
                    self._merge_defaults(widgets, self.default_widgets)
                    return widgets
            else:
                # Standard-Widget-Positionen erstellen
                self.save_widgets(self.default_widgets)
                return self.default_widgets.copy()
                
        except Exception as e:
            print(f"Fehler beim Laden der Widget-Positionen: {e}")
            return self.default_widgets.copy()
            
    def save_widgets(self, widgets: Dict[str, Any]):
        """Widget-Positionen speichern"""
        try:
            with open(self.widgets_file, 'w', encoding='utf-8') as f:
                json.dump(widgets, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Fehler beim Speichern der Widget-Positionen: {e}")
            
    def _merge_defaults(self, current: Dict[str, Any], defaults: Dict[str, Any]):
        """Standard-Werte mit bestehenden Einstellungen zusammenführen"""
        for key, value in defaults.items():
            if key not in current:
                current[key] = value
            elif isinstance(value, dict) and isinstance(current[key], dict):
                self._merge_defaults(current[key], value)
                
    def get_setting(self, category: str, key: str, default: Any = None) -> Any:
        """Einstellung abrufen"""
        try:
            return self.settings[category][key]
        except KeyError:
            return default
            
    def set_setting(self, category: str, key: str, value: Any):
        """Einstellung setzen und speichern"""
        if category not in self.settings:
            self.settings[category] = {}
        self.settings[category][key] = value
        self.save_settings(self.settings)
        
    def get_widget_position(self, widget_type: str) -> Dict[str, Any]:
        """Widget-Position abrufen"""
        try:
            return self.widgets[widget_type]
        except KeyError:
            return {"x": 50, "y": 50, "visible": True}
            
    def set_widget_position(self, widget_type: str, x: int, y: int, visible: bool = True):
        """Widget-Position setzen und speichern"""
        self.widgets[widget_type] = {
            "x": x,
            "y": y,
            "visible": visible,
            "last_updated": datetime.now().isoformat()
        }
        self.save_widgets(self.widgets)
        
    def get_theme_colors(self) -> Dict[str, str]:
        """Theme-Farben abrufen"""
        return self.settings.get("theme", self.default_settings["theme"])
        
    def set_theme_colors(self, colors: Dict[str, str]):
        """Theme-Farben setzen"""
        self.settings["theme"] = colors
        self.save_settings(self.settings)
        
    def get_logging_config(self) -> Dict[str, Any]:
        """Logging-Konfiguration abrufen"""
        return self.settings.get("logging", self.default_settings["logging"])
        
    def set_logging_config(self, config: Dict[str, Any]):
        """Logging-Konfiguration setzen"""
        self.settings["logging"] = config
        self.save_settings(self.settings)
        
    def get_monitoring_config(self) -> Dict[str, Any]:
        """Monitoring-Konfiguration abrufen"""
        return self.settings.get("monitoring", self.default_settings["monitoring"])
        
    def set_monitoring_config(self, config: Dict[str, Any]):
        """Monitoring-Konfiguration setzen"""
        self.settings["monitoring"] = config
        self.save_settings(self.settings)
        
    def get_system_tray_config(self) -> Dict[str, Any]:
        """System-Tray-Konfiguration abrufen"""
        return self.settings.get("system_tray", self.default_settings["system_tray"])
        
    def set_system_tray_config(self, config: Dict[str, Any]):
        """System-Tray-Konfiguration setzen"""
        self.settings["system_tray"] = config
        self.save_settings(self.settings)
        
    def get_window_config(self) -> Dict[str, Any]:
        """Fenster-Konfiguration abrufen"""
        return self.settings.get("window", self.default_settings["window"])
        
    def set_window_config(self, config: Dict[str, Any]):
        """Fenster-Konfiguration setzen"""
        self.settings["window"] = config
        self.save_settings(self.settings)
        
    def reset_to_defaults(self):
        """Alle Einstellungen auf Standard zurücksetzen"""
        self.settings = self.default_settings.copy()
        self.widgets = self.default_widgets.copy()
        self.save_settings(self.settings)
        self.save_widgets(self.widgets)
        print("Einstellungen auf Standard zurückgesetzt")
        
    def export_config(self, filepath: str):
        """Konfiguration exportieren"""
        try:
            export_data = {
                "settings": self.settings,
                "widgets": self.widgets,
                "exported_at": datetime.now().isoformat(),
                "version": "1.0.0"
            }
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            print(f"Konfiguration exportiert nach: {filepath}")
        except Exception as e:
            print(f"Fehler beim Exportieren der Konfiguration: {e}")
            
    def import_config(self, filepath: str):
        """Konfiguration importieren"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
                
            if "settings" in import_data:
                self.settings = import_data["settings"]
                self.save_settings(self.settings)
                
            if "widgets" in import_data:
                self.widgets = import_data["widgets"]
                self.save_widgets(self.widgets)
                
            print(f"Konfiguration importiert von: {filepath}")
        except Exception as e:
            print(f"Fehler beim Importieren der Konfiguration: {e}")
            
    def get_config_summary(self) -> Dict[str, Any]:
        """Konfigurations-Zusammenfassung"""
        return {
            "settings_file": self.settings_file,
            "widgets_file": self.widgets_file,
            "settings_count": len(self.settings),
            "widgets_count": len(self.widgets),
            "last_updated": datetime.now().isoformat()
        } 