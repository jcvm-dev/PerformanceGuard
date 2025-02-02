import pytest
import sqlite3
import json
from datetime import datetime
from app.database.db import Database
import os

@pytest.fixture
def test_db():
    db_path = "test_database.db"
    # Garantir que começamos com um banco limpo
    if os.path.exists(db_path):
        os.remove(db_path)
    db = Database(db_path)
    yield db
    # Limpeza após os testes
    if os.path.exists(db_path):
        os.remove(db_path)

@pytest.fixture
def sample_metrics():
    return {
        'basic_metrics': {
            'response_time': 200,
            'status_code': 200
        },
        'resource_metrics': {
            'images': 5,
            'scripts': 3
        }
    }

def test_database_initialization(test_db):
    """Testa se o banco de dados é inicializado corretamente"""
    assert os.path.exists(test_db.db_path)
    
    # Verifica se a tabela foi criada
    with sqlite3.connect(test_db.db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='metrics'
        """)
        assert cursor.fetchone() is not None

def test_save_metrics(test_db, sample_metrics):
    """Testa o salvamento de métricas no banco"""
    url = "https://example.com"
    test_db.save_metrics(url, sample_metrics)
    
    # Verifica se os dados foram salvos
    with sqlite3.connect(test_db.db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM metrics WHERE url = ?", (url,))
        row = cursor.fetchone()
        
        assert row is not None
        assert row[1] == url  # url
        assert row[3] == 200  # response_time
        assert row[4] == 200  # status_code
        
        # Verifica se os dados JSON foram salvos corretamente
        saved_metrics = json.loads(row[5])  # metrics_data
        assert saved_metrics == sample_metrics

def test_get_metrics_with_url(test_db, sample_metrics):
    """Testa a recuperação de métricas com filtro de URL"""
    url = "https://example.com"
    test_db.save_metrics(url, sample_metrics)
    
    # Salva uma métrica diferente para garantir o filtro
    test_db.save_metrics("https://other.com", sample_metrics)
    
    results = test_db.get_metrics(url=url)
    assert len(results) == 1
    assert results[0][1] == url  # url

def test_get_metrics_without_url(test_db, sample_metrics):
    """Testa a recuperação de todas as métricas"""
    urls = ["https://example1.com", "https://example2.com", "https://example3.com"]
    
    # Salva múltiplas métricas
    for url in urls:
        test_db.save_metrics(url, sample_metrics)
    
    results = test_db.get_metrics()
    assert len(results) == len(urls)

def test_get_metrics_with_limit(test_db, sample_metrics):
    """Testa o limite na recuperação de métricas"""
    urls = ["https://example1.com", "https://example2.com", "https://example3.com"]
    
    for url in urls:
        test_db.save_metrics(url, sample_metrics)
    
    results = test_db.get_metrics(limit=2)
    assert len(results) == 2

def test_metrics_ordering(test_db, sample_metrics):
    """Testa se as métricas são retornadas em ordem decrescente de timestamp"""
    url = "https://example.com"
    
    # Salva múltiplas métricas com pequeno intervalo
    for _ in range(3):
        test_db.save_metrics(url, sample_metrics)
    
    results = test_db.get_metrics(url=url)
    
    # Verifica se os timestamps estão em ordem decrescente
    timestamps = [datetime.fromisoformat(row[2]) for row in results]
    assert timestamps == sorted(timestamps, reverse=True)

def test_invalid_db_path():
    """Testa a criação do banco com caminho inválido"""
    with pytest.raises(sqlite3.OperationalError):
        Database("/invalid/path/to/database.db")

def test_save_metrics_with_missing_data(test_db):
    """Testa o salvamento de métricas com dados ausentes"""
    url = "https://example.com"
    incomplete_metrics = {
        'basic_metrics': {}
    }
    
    test_db.save_metrics(url, incomplete_metrics)
    
    results = test_db.get_metrics(url=url)
    assert len(results) == 1
    assert results[0][3] is None  # response_time should be NULL
    assert results[0][4] is None  # status_code should be NULL
