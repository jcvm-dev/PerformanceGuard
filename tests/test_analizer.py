import pytest
from app.analyzer.performance import PerformanceAnalyzer
from unittest.mock import Mock, patch
from datetime import datetime

@pytest.fixture
def analyzer():
    return PerformanceAnalyzer()

@pytest.fixture
def mock_response():
    mock = Mock()
    mock.status_code = 200
    mock.content = b"<html><body><img src='test.jpg'><script></script></body></html>"
    mock.text = mock.content.decode()
    mock.headers = {'Content-Type': 'text/html'}
    mock.encoding = 'utf-8'
    mock.history = []
    mock.url = 'https://example.com'
    mock.cookies = []
    return mock

def test_analyzer_initialization(analyzer):
    assert isinstance(analyzer, PerformanceAnalyzer)
    assert 'response_time' in analyzer.thresholds
    assert 'size' in analyzer.thresholds
    assert 'resources' in analyzer.thresholds

@patch('requests.get')
def test_analyze_basic_metrics(mock_get, analyzer, mock_response):
    mock_get.return_value = mock_response
    
    metrics = analyzer._analyze_basic_metrics('https://example.com')
    
    assert isinstance(metrics, dict)
    assert 'response_time' in metrics
    assert 'status_code' in metrics
    assert metrics['status_code'] == 200
    assert 'content_size' in metrics
    assert 'headers' in metrics

@patch('socket.gethostbyname')
def test_analyze_dns(mock_dns, analyzer):
    mock_dns.return_value = '93.184.216.34'
    
    metrics = analyzer._analyze_dns('https://example.com')
    
    assert isinstance(metrics, dict)
    assert 'ip' in metrics
    assert 'dns_time' in metrics
    assert metrics['ip'] == '93.184.216.34'

@patch('requests.get')
def test_analyze_resources(mock_get, analyzer, mock_response):
    mock_get.return_value = mock_response
    
    metrics = analyzer._analyze_resources('https://example.com')
    
    assert isinstance(metrics, dict)
    assert 'images' in metrics
    assert metrics['images'] == 1
    assert 'scripts' in metrics
    assert metrics['scripts'] == 1

@patch('requests.get')
def test_analyze_seo(mock_get, analyzer):
    mock_response = Mock()
    mock_response.text = '''
        <html>
            <head>
                <title>Test Page</title>
                <meta name="description" content="Test description">
            </head>
            <body>
                <h1>Test Header</h1>
                <img src="test.jpg" alt="test">
            </body>
        </html>
    '''
    mock_get.return_value = mock_response
    
    metrics = analyzer._analyze_seo('https://example.com')
    
    assert isinstance(metrics, dict)
    assert 'title' in metrics
    assert metrics['title'] == 'Test Page'
    assert 'meta_description' in metrics
    assert metrics['h1_count'] == 1

@patch('requests.get')
def test_analyze_security(mock_get, analyzer):
    mock_response = Mock()
    mock_response.headers = {
        'Strict-Transport-Security': 'max-age=31536000',
        'Content-Security-Policy': "default-src 'self'"
    }
    mock_response.url = 'https://example.com'
    mock_response.cookies = []
    mock_get.return_value = mock_response
    
    metrics = analyzer._analyze_security('https://example.com')
    
    assert isinstance(metrics, dict)
    assert 'security_headers_present' in metrics
    assert 'https_redirect' in metrics
    assert metrics['https_redirect'] == True

def test_analyze_health(analyzer):
    test_metrics = {
        'basic_metrics': {'response_time': 200},
        'security_metrics': {'ssl_valid': True, 'security_headers_present': {'Strict-Transport-Security': True}},
        'seo_metrics': {'title': 'Test', 'meta_description': 'Test', 'images_without_alt': 0}
    }
    
    health = analyzer._analyze_health(test_metrics)
    
    assert isinstance(health, dict)
    assert 'performance' in health
    assert 'security' in health
    assert 'seo' in health
    assert 'overall' in health

def test_generate_recommendations(analyzer):
    test_metrics = {
        'basic_metrics': {'response_time': 2000},
        'security_metrics': {'ssl_valid': False},
        'seo_metrics': {'meta_description': None}
    }
    
    recommendations = analyzer._generate_recommendations(test_metrics)
    
    assert isinstance(recommendations, list)
    assert len(recommendations) > 0
    assert all('type' in rec for rec in recommendations)
    assert all('priority' in rec for rec in recommendations)
    assert all('message' in rec for rec in recommendations)

@patch('requests.get')
def test_analyze_url_complete(mock_get, analyzer, mock_response):
    mock_get.return_value = mock_response
    
    result = analyzer.analyze_url('https://example.com')
    
    assert isinstance(result, dict)
    assert 'timestamp' in result
    assert 'basic_metrics' in result
    assert 'dns_metrics' in result
    assert 'ssl_metrics' in result
    assert 'resource_metrics' in result
    assert 'seo_metrics' in result
    assert 'security_metrics' in result
    assert 'availability_metrics' in result
    assert 'health_check' in result
    assert 'recommendations' in result
