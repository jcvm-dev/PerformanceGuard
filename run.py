from flask import Flask, render_template, jsonify, request
from app.analyzer.performance import PerformanceAnalyzer
from app.database.db import Database
from config import config
import os

# Inicialização
app = Flask(__name__, 
            template_folder='app/web/templates',
            static_folder='app/web/static')

# Configuração
env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Instâncias
analyzer = PerformanceAnalyzer()
db = Database(app.config['DATABASE_PATH'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        # Analisar URL
        metrics = analyzer.analyze_url(url)
        
        # Salvar métricas
        db.save_metrics(url, metrics)
        
        return jsonify(metrics)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/metrics/<path:url>')
def get_metrics(url):
    metrics = db.get_metrics(url)
    return jsonify(metrics)

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])