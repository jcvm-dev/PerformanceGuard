import requests
import time
from datetime import datetime
from urllib.parse import urlparse
import ssl
import socket

class PerformanceAnalyzer:
    def __init__(self):
        self.metrics = {}
    
    def analyze_url(self, url):
        """Analisa a performance completa de uma URL"""
        try:
            start_time = time.time()
            
            # Análise básica
            basic_metrics = self._analyze_basic_metrics(url)
            
            # Análise DNS
            dns_metrics = self._analyze_dns(url)
            
            # Análise SSL
            ssl_metrics = self._analyze_ssl(url)
            
            # Análise de recursos
            resource_metrics = self._analyze_resources(url)
            
            # Tempo total
            total_time = int((time.time() - start_time) * 1000)
            
            return {
                'basic_metrics': basic_metrics,
                'dns_metrics': dns_metrics,
                'ssl_metrics': ssl_metrics,
                'resource_metrics': resource_metrics,
                'total_time': total_time
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_basic_metrics(self, url):
        """Analisa métricas básicas como tempo de resposta e status"""
        start_time = time.time()
        response = requests.get(url, timeout=30)
        response_time = int((time.time() - start_time) * 1000)
        
        return {
            'response_time': response_time,
            'status_code': response.status_code,
            'content_size': len(response.content),
            'headers': dict(response.headers)
        }
    
    def _analyze_dns(self, url):
        """Analisa métricas de DNS"""
        domain = urlparse(url).netloc
        start_time = time.time()
        try:
            ip = socket.gethostbyname(domain)
            dns_time = int((time.time() - start_time) * 1000)
            return {
                'ip': ip,
                'dns_time': dns_time
            }
        except:
            return {'error': 'DNS resolution failed'}
    
    def _analyze_ssl(self, url):
        """Analisa métricas de SSL"""
        domain = urlparse(url).netloc
        try:
            start_time = time.time()
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    ssl_time = int((time.time() - start_time) * 1000)
                    return {
                        'ssl_time': ssl_time,
                        'version': ssock.version(),
                        'cipher': ssock.cipher()
                    }
        except:
            return {'error': 'SSL analysis failed'}
    
    def _analyze_resources(self, url):
        """Analisa recursos da página (imagens, scripts, etc)"""
        try:
            response = requests.get(url)
            html = response.text
            
            resources = {
                'images': html.count('<img'),
                'scripts': html.count('<script'),
                'styles': html.count('<link rel="stylesheet"'),
                'total_size': len(response.content)
            }
            
            return resources
        except:
            return {'error': 'Resource analysis failed'}
