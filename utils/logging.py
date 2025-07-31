#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SystemMonitorX - Logging-System
CSV/JSON-Export mit automatischem Speichern

Autor: SystemMonitorX Team
Version: 1.0.0
"""

import csv
import json
import os
import threading
import time
from datetime import datetime
from typing import Dict, List, Any
import psutil

class SystemLogger:
    """
    System-Logging für CSV/JSON-Export
    - Automatisches Speichern alle 60 Sekunden
    - Buffer-System für effiziente Speicherung
    - Maximal 10 Log-Dateien
    - Thread-sicher
    """
    
    def __init__(self):
        self.logs_dir = "logs"
        self.buffer_size = 60  # 60 Sekunden = 1 Minute
        self.max_files = 10
        
        # Buffer für Daten
        self.csv_buffer = []
        self.json_buffer = []
        
        # Threading
        self.logging_active = False
        self.logging_thread = None
        self.lock = threading.Lock()
        
        # Erstelle Logs-Verzeichnis
        os.makedirs(self.logs_dir, exist_ok=True)
        
    def start_logging(self):
        """Logging starten"""
        if not self.logging_active:
            self.logging_active = True
            self.logging_thread = threading.Thread(target=self._logging_loop, daemon=True)
            self.logging_thread.start()
            print("System-Logging gestartet")
            
    def stop_logging(self):
        """Logging stoppen"""
        self.logging_active = False
        if self.logging_thread:
            self.logging_thread.join(timeout=5)
        print("System-Logging gestoppt")
        
    def _logging_loop(self):
        """Haupt-Logging-Schleife"""
        while self.logging_active:
            try:
                # System-Daten sammeln
                data = self._collect_system_data()
                
                # Daten zum Buffer hinzufügen
                with self.lock:
                    self.csv_buffer.append(data)
                    self.json_buffer.append(data)
                    
                    # Wenn Buffer voll, speichern
                    if len(self.csv_buffer) >= self.buffer_size:
                        self._save_data()
                        
            except Exception as e:
                print(f"Fehler im Logging-Loop: {e}")
                
            # 1 Sekunde warten
            time.sleep(1)
            
    def _collect_system_data(self) -> Dict[str, Any]:
        """System-Daten sammeln"""
        try:
            # CPU-Daten
            cpu_percent = psutil.cpu_percent(interval=0.1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            cpu_freq_ghz = cpu_freq.current / 1000 if cpu_freq else 0
            
            # RAM-Daten
            memory = psutil.virtual_memory()
            ram_percent = memory.percent
            ram_used_gb = memory.used / (1024**3)
            ram_total_gb = memory.total / (1024**3)
            
            # Disk-Daten
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            disk_used_gb = disk.used / (1024**3)
            disk_total_gb = disk.total / (1024**3)
            
            # System-Daten
            platform = os.name
            username = os.getlogin()
            
            # Timestamp
            timestamp = datetime.now().isoformat()
            
            return {
                "timestamp": timestamp,
                "cpu_percent": cpu_percent,
                "cpu_count": cpu_count,
                "cpu_freq_ghz": cpu_freq_ghz,
                "ram_percent": ram_percent,
                "ram_used_gb": ram_used_gb,
                "ram_total_gb": ram_total_gb,
                "disk_percent": disk_percent,
                "disk_used_gb": disk_used_gb,
                "disk_total_gb": disk_total_gb,
                "platform": platform,
                "username": username
            }
            
        except Exception as e:
            print(f"Fehler beim Sammeln der System-Daten: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
            
    def _save_data(self):
        """Daten in CSV und JSON speichern"""
        try:
            # CSV speichern
            self._save_csv()
            
            # JSON speichern
            self._save_json()
            
            # Buffer leeren
            self.csv_buffer.clear()
            self.json_buffer.clear()
            
            print(f"Daten gespeichert: {len(self.csv_buffer)} Einträge")
            
        except Exception as e:
            print(f"Fehler beim Speichern der Daten: {e}")
            
    def _save_csv(self):
        """CSV-Datei speichern"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"system_monitor_{timestamp}.csv"
        filepath = os.path.join(self.logs_dir, filename)
        
        # CSV-Header
        fieldnames = [
            "timestamp", "cpu_percent", "cpu_count", "cpu_freq_ghz",
            "ram_percent", "ram_used_gb", "ram_total_gb",
            "disk_percent", "disk_used_gb", "disk_total_gb",
            "platform", "username"
        ]
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.csv_buffer)
            
        # Alte Dateien löschen
        self._cleanup_old_files("csv")
        
    def _save_json(self):
        """JSON-Datei speichern"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"system_monitor_{timestamp}.json"
        filepath = os.path.join(self.logs_dir, filename)
        
        # JSON-Daten mit Metadaten
        json_data = {
            "metadata": {
                "version": "1.0.0",
                "created": datetime.now().isoformat(),
                "entries": len(self.json_buffer),
                "buffer_size": self.buffer_size
            },
            "data": self.json_buffer
        }
        
        with open(filepath, 'w', encoding='utf-8') as jsonfile:
            json.dump(json_data, jsonfile, indent=2, ensure_ascii=False)
            
        # Alte Dateien löschen
        self._cleanup_old_files("json")
        
    def _cleanup_old_files(self, file_type: str):
        """Alte Log-Dateien löschen (maximal 10 Dateien)"""
        try:
            # Alle Dateien des Typs finden
            files = []
            for filename in os.listdir(self.logs_dir):
                if filename.endswith(f".{file_type}"):
                    filepath = os.path.join(self.logs_dir, filename)
                    files.append((filepath, os.path.getmtime(filepath)))
                    
            # Nach Datum sortieren (älteste zuerst)
            files.sort(key=lambda x: x[1])
            
            # Alte Dateien löschen
            if len(files) > self.max_files:
                files_to_delete = files[:-self.max_files]
                for filepath, _ in files_to_delete:
                    os.remove(filepath)
                    print(f"Alte Log-Datei gelöscht: {filepath}")
                    
        except Exception as e:
            print(f"Fehler beim Aufräumen alter Dateien: {e}")
            
    def get_logging_status(self) -> Dict[str, Any]:
        """Logging-Status zurückgeben"""
        with self.lock:
            return {
                "active": self.logging_active,
                "buffer_size": len(self.csv_buffer),
                "max_buffer_size": self.buffer_size,
                "logs_directory": self.logs_dir,
                "max_files": self.max_files
            }
            
    def force_save(self):
        """Sofortiges Speichern erzwingen"""
        with self.lock:
            if self.csv_buffer:
                self._save_data()
                print("Sofortiges Speichern durchgeführt")
                
    def get_recent_data(self, count: int = 10) -> List[Dict[str, Any]]:
        """Letzte Daten zurückgeben"""
        with self.lock:
            return self.csv_buffer[-count:] if self.csv_buffer else [] 