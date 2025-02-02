import sqlite3
from datetime import datetime
import json

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Inicializa o banco de dados"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabela de métricas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    response_time INTEGER,
                    status_code INTEGER,
                    metrics_data TEXT
                )
            ''')
            
            conn.commit()
    
    def save_metrics(self, url, metrics):
        """Salva métricas no banco de dados"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO metrics (url, timestamp, response_time, status_code, metrics_data)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                url,
                datetime.utcnow().isoformat(),
                metrics.get('basic_metrics', {}).get('response_time'),
                metrics.get('basic_metrics', {}).get('status_code'),
                json.dumps(metrics)
            ))
            
            conn.commit()
    
    def get_metrics(self, url=None, limit=100):
        """Recupera métricas do banco de dados"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if url:
                cursor.execute('''
                    SELECT * FROM metrics 
                    WHERE url = ? 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (url, limit))
            else:
                cursor.execute('''
                    SELECT * FROM metrics 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (limit,))
            
            return cursor.fetchall()