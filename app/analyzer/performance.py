import requests
import time
from datetime import datetime
from urllib.parse import urlparse
import ssl
import socket
import http.client
from bs4 import BeautifulSoup

class PerformanceAnalyzer:
    def __init__(self):
        self.metrics = {}
        
        # Definir thresholds
        self.thresholds = {
            'response_time': {
                'good': 300,      # ms
                'warning': 1000   # ms
            },
            'size': {
                'good': 1024 * 1024,     # 1MB
                'warning': 3 * 1024 * 1024  # 3MB
            },
            'resources': {
                'good': 50,
                'warning': 100
            }
        }
    
    def analyze_url(self, url):
        """Análise completa com recomendações"""
        try:
            metrics = {
                'timestamp': datetime.utcnow().isoformat(),
                'url': url,
                'basic_metrics': self._analyze_basic_metrics(url),
                'dns_metrics': self._analyze_dns(url),
                'ssl_metrics': self._analyze_ssl(url),
                'resource_metrics': self._analyze_resources(url),
                'seo_metrics': self._analyze_seo(url),
                'security_metrics': self._analyze_security(url),
                'availability_metrics': self._analyze_availability(url)
            }
            
            # Adicionar análise de saúde e recomendações
            metrics['health_check'] = self._analyze_health(metrics)
            metrics['recommendations'] = self._generate_recommendations(metrics)
            
            return metrics
            
        except Exception as e:
            return {'error': str(e), 'timestamp': datetime.utcnow().isoformat()}
    
    def _analyze_basic_metrics(self, url):
        """Analisa métricas básicas como tempo de resposta e status"""
        start_time = time.time()
        response = requests.get(url, timeout=30)
        response_time = int((time.time() - start_time) * 1000)
        
        return {
            'response_time': response_time,
            'status_code': response.status_code,
            'content_size': len(response.content),
            'headers': dict(response.headers),
            'encoding': response.encoding,
            'redirect_count': len(response.history),
            'is_redirect': len(response.history) > 0,
            'final_url': response.url
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
    
    def _analyze_seo(self, url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            return {
                'title': soup.title.string if soup.title else None,
                'meta_description': soup.find('meta', {'name': 'description'})['content'] if soup.find('meta', {'name': 'description'}) else None,
                'h1_count': len(soup.find_all('h1')),
                'images_without_alt': len([img for img in soup.find_all('img') if not img.get('alt')]),
                'has_robots_txt': requests.get(f"{urlparse(url).scheme}://{urlparse(url).netloc}/robots.txt").status_code == 200,
                'has_sitemap': requests.get(f"{urlparse(url).scheme}://{urlparse(url).netloc}/sitemap.xml").status_code == 200
            }
        except:
            return {'error': 'SEO analysis failed'}
    
    def _analyze_security(self, url):
        try:
            domain = urlparse(url).netloc
            ssl_info = self._analyze_ssl(url)
            
            security_headers = [
                'Strict-Transport-Security',
                'Content-Security-Policy',
                'X-Frame-Options',
                'X-Content-Type-Options',
                'X-XSS-Protection'
            ]
            
            response = requests.get(url)
            headers = response.headers
            
            return {
                'ssl_valid': not isinstance(ssl_info, dict) or 'error' not in ssl_info,
                'security_headers_present': {
                    header: header.lower() in map(str.lower, headers.keys())
                    for header in security_headers
                },
                'cookies_secure': all(cookie.secure for cookie in response.cookies),
                'https_redirect': response.url.startswith('https')
            }
        except:
            return {'error': 'Security analysis failed'}
    
    def _analyze_availability(self, url):
        locations = ['us', 'eu', 'asia']  # Simulated locations
        results = {}
        
        for location in locations:
            try:
                start_time = time.time()
                requests.get(url, timeout=5)
                response_time = int((time.time() - start_time) * 1000)
                results[location] = {
                    'available': True,
                    'response_time': response_time
                }
            except:
                results[location] = {
                    'available': False,
                    'response_time': None
                }
        
        return results
    
    def _analyze_health(self, metrics):
        health_status = {
            'performance': 'good',
            'security': 'good',
            'seo': 'good',
            'overall': 'good'
        }
        
        # Análise de Performance
        response_time = metrics['basic_metrics']['response_time']
        if response_time > self.thresholds['response_time']['warning']:
            health_status['performance'] = 'bad'
        elif response_time > self.thresholds['response_time']['good']:
            health_status['performance'] = 'warning'
        
        # Análise de Segurança
        security = metrics['security_metrics']
        if not security.get('ssl_valid', False):
            health_status['security'] = 'bad'
        elif not all(security.get('security_headers_present', {}).values()):
            health_status['security'] = 'warning'
        
        # Análise de SEO
        seo = metrics['seo_metrics']
        if not seo.get('title') or not seo.get('meta_description'):
            health_status['seo'] = 'warning'
        if seo.get('images_without_alt', 0) > 0:
            health_status['seo'] = 'warning'
        
        # Status Geral
        if 'bad' in health_status.values():
            health_status['overall'] = 'bad'
        elif 'warning' in health_status.values():
            health_status['overall'] = 'warning'
        
        return health_status
    
    def _generate_recommendations(self, metrics):
        recommendations = []
        
        # Recomendações de Performance
        if metrics['basic_metrics']['response_time'] > self.thresholds['response_time']['good']:
            recommendations.append({
                'type': 'performance',
                'priority': 'high',
                'message': 'Tempo de resposta alto. Considere usar CDN ou otimizar o servidor.'
            })
        
        # Recomendações de Segurança
        security = metrics['security_metrics']
        if not security.get('ssl_valid', False):
            recommendations.append({
                'type': 'security',
                'priority': 'critical',
                'message': 'SSL inválido ou ausente. Instale um certificado SSL válido.'
            })
        
        # Recomendações de SEO
        seo = metrics['seo_metrics']
        if not seo.get('meta_description'):
            recommendations.append({
                'type': 'seo',
                'priority': 'medium',
                'message': 'Meta description ausente. Adicione uma descrição relevante.'
            })
        
        return recommendations
