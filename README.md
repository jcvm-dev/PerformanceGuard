# Performance Guard 🚀

Uma ferramenta web moderna para análise completa de performance, segurança e SEO de websites.

## 📋 Funcionalidades

### Análise de Performance
- Tempo de resposta
- Tempo de carregamento DNS
- Análise SSL/TLS
- Tamanho de recursos
- Métricas de redirecionamento

### Análise de Segurança
- Verificação de certificados SSL
- Headers de segurança
- Cookies seguros
- Redirecionamentos HTTPS

### Análise SEO
- Meta tags
- Estrutura de headings
- Alt text em imagens
- Robots.txt
- Sitemap.xml

### Visualização de Dados
- Gráficos interativos
- Métricas em tempo real
- Recomendações detalhadas
- Status de saúde do site

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python/Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Gráficos**: Plotly.js
- **Ícones**: Font Awesome
- **Análise**: BeautifulSoup4, Requests
- **Banco de Dados**: SQLite

## 📦 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/jcvm-dev/PerformanceGuard
cd performanceguard
```
2. Crie um ambiente virtual:
```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
.\venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 🚀 Como Usar

1. Inicie o servidor:
```bash
python run.py
```

2. Acesse no navegador:
```
http://localhost:5000
```

3. Insira a URL que deseja analisar e clique em "Analisar Site"

## 📁 Estrutura do Projeto

```
performanceguard/
├── app/
│   ├── analyzer/
│   │   ├── __init__.py
│   │   └── performance.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── db.py
│   └── web/
│       ├── static/
│       │   ├── css/
│       │   │   └── style.css
│       │   └── js/
│       │       └── main.js
│       └── templates/
│           └── index.html
├── config.py
├── requirements.txt
└── run.py
```

## 🔍 Principais Arquivos

- `run.py`: Ponto de entrada da aplicação
- `config.py`: Configurações do projeto
- `app/analyzer/performance.py`: Lógica de análise
- `app/database/db.py`: Gerenciamento do banco de dados
- `app/web/static/js/main.js`: Lógica frontend
- `app/web/static/css/style.css`: Estilos
- `app/web/templates/index.html`: Template principal

## ⚙️ Configuração

O arquivo `config.py` contém as principais configurações:

```python
class Config:
    DEBUG = False
    DATABASE_PATH = 'app/database/metrics.db'
    RESPONSE_TIME_THRESHOLD = 1000  # ms
    SECURITY_CHECK_ENABLED = True
```

## 📊 Métricas Analisadas

1. **Performance**
   - Tempo de resposta
   - Tamanho da página
   - Recursos carregados
   - Tempo DNS
   - Tempo SSL

2. **Segurança**
   - Certificado SSL
   - Headers de segurança
   - Configurações de cookies
   - Redirecionamentos seguros

3. **SEO**
   - Meta tags
   - Estrutura HTML
   - Imagens e alt text
   - Arquivos robots.txt/sitemap.xml

## 🔄 Atualizações Futuras

- [ ] Suporte a múltiplas URLs
- [ ] Histórico de análises
- [ ] Exportação de relatórios
- [ ] Análise de Web Vitals
- [ ] Integração com APIs de terceiros
- [ ] Monitoramento contínuo

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## ✨ Autor

**Jefferson Monteiro**
- GitHub: [@jcvm-dev](https://github.com/jcvm-dev)

## 🙏 Agradecimentos

- Plotly.js pela biblioteca de gráficos
- Font Awesome pelos ícones
- Comunidade Python/Flask

---
Desenvolvido com ☕ e dedicação por Jefferson Monteiro