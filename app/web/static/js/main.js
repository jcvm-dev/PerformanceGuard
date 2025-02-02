function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function getStatusClass(value, type) {
    switch(type) {
        case 'response_time':
            return value < 300 ? 'status-good' : 
                   value < 1000 ? 'status-warning' : 'status-bad';
        case 'status_code':
            return value < 400 ? 'status-good' :
                   value < 500 ? 'status-warning' : 'status-bad';
        default:
            return '';
    }
}

function formatMetricKey(key) {
    return key
        .replace(/_/g, ' ')
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}

function formatMetricValue(value) {
    if (value === null || value === undefined) return 'N/A';
    if (typeof value === 'boolean') return value ? 'Sim' : 'Não';
    if (typeof value === 'number') return value.toString();
    if (typeof value === 'string') return value;
    if (Array.isArray(value)) return value.join(', ');
    if (typeof value === 'object') return JSON.stringify(value, null, 2);
    return value.toString();
}

function createMetricsTable(title, metrics, level = 0) {
    if (!metrics || typeof metrics !== 'object') return '';

    let html = '';
    
    // Adicionar título apenas no primeiro nível
    if (level === 0) {
        html += `<div class="metrics-section">
                    <h3>${title}</h3>`;
    }

    html += `<table class="metrics-table ${level > 0 ? 'nested-table' : ''}">
                <tbody>`;

    for (const [key, value] of Object.entries(metrics)) {
        if (value === null || value === undefined) continue;

        if (typeof value === 'object' && !Array.isArray(value) && Object.keys(value).length > 0) {
            // Objeto aninhado
            html += `
                <tr class="section-header">
                    <th colspan="2">${formatMetricKey(key)}</th>
                </tr>
                <tr>
                    <td colspan="2" class="nested-content">
                        ${createMetricsTable(key, value, level + 1)}
                    </td>
                </tr>`;
        } else {
            // Valor simples
            html += `
                <tr>
                    <th>${formatMetricKey(key)}</th>
                    <td>${formatMetricValue(value)}</td>
                </tr>`;
        }
    }

    html += `</tbody></table>`;

    // Fechar a div da seção apenas no primeiro nível
    if (level === 0) {
        html += `</div>`;
    }

    return html;
}

function createHealthIndicator(health) {
    const indicators = {
        'good': '🟢',
        'warning': '🟡',
        'bad': '🔴'
    };
    
    return `
        <div class="health-indicator">
            <h3>Status de Saúde</h3>
            <div class="health-grid">
                <div class="health-item ${health.performance}">
                    ${indicators[health.performance]} Performance
                </div>
                <div class="health-item ${health.security}">
                    ${indicators[health.security]} Segurança
                </div>
                <div class="health-item ${health.seo}">
                    ${indicators[health.seo]} SEO
                </div>
                <div class="health-item ${health.overall}">
                    ${indicators[health.overall]} Geral
                </div>
            </div>
        </div>
    `;
}

function createRecommendations(recommendations) {
    if (!recommendations || recommendations.length === 0) {
        return '';
    }
    
    return `
        <div class="recommendations-section">
            <h3>Recomendações</h3>
            <div class="recommendations-list">
                ${recommendations.map(rec => `
                    <div class="recommendation ${rec.priority}">
                        <span class="recommendation-type">${rec.type}</span>
                        <p>${rec.message}</p>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

function analyzeUrl() {
    const url = document.getElementById('urlInput').value;
    if (!url) {
        alert('Por favor, insira uma URL válida');
        return;
    }

    // Mostrar loading e esconder resultados anteriores
    document.getElementById('loading').style.display = 'block';
    document.getElementById('results').style.display = 'none';
    
    // Limpar resultados anteriores
    document.getElementById('metricsCards').innerHTML = '';
    document.getElementById('responseTimeChart').innerHTML = '';
    document.getElementById('resourcesChart').innerHTML = '';
    document.getElementById('detailedMetrics').innerHTML = '';
    document.getElementById('healthStatus').innerHTML = '';
    document.getElementById('recommendations').innerHTML = '';

    fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({url: url})
    })
    .then(response => response.json())
    .then(data => {
        // Esconder loading e mostrar resultados
        document.getElementById('loading').style.display = 'none';
        document.getElementById('results').style.display = 'block';

        // Métricas básicas em cards
        const basicMetrics = data.basic_metrics;
        document.getElementById('metricsCards').innerHTML = `
            <div class="metric-card">
                <h3>Tempo de Resposta</h3>
                <div class="metric-value ${getStatusClass(basicMetrics.response_time, 'response_time')}">
                    ${basicMetrics.response_time}ms
                </div>
            </div>
            <div class="metric-card">
                <h3>Status</h3>
                <div class="metric-value ${getStatusClass(basicMetrics.status_code, 'status_code')}">
                    ${basicMetrics.status_code}
                </div>
            </div>
            <div class="metric-card">
                <h3>Tamanho Total</h3>
                <div class="metric-value">
                    ${formatBytes(basicMetrics.content_size)}
                </div>
            </div>
            <div class="metric-card">
                <h3>Tempo Total</h3>
                <div class="metric-value">
                    ${data.total_time}ms
                </div>
            </div>
        `;

        // Status de Saúde
        if (data.health_check) {
            document.getElementById('healthStatus').innerHTML = createHealthIndicator(data.health_check);
        }

        // Recomendações
        if (data.recommendations) {
            document.getElementById('recommendations').innerHTML = createRecommendations(data.recommendations);
        }

        // Gráficos
        const timelineData = {
            dns: data.dns_metrics?.dns_time || 0,
            ssl: data.ssl_metrics?.ssl_time || 0,
            response: basicMetrics.response_time,
            total: data.total_time
        };

        const timelineTrace = {
            x: Object.keys(timelineData),
            y: Object.values(timelineData),
            type: 'bar',
            marker: {
                color: '#2196F3'
            }
        };

        Plotly.newPlot('responseTimeChart', [timelineTrace], {
            title: 'Análise de Tempo (ms)',
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            yaxis: {title: 'Millisegundos'}
        });

        // Gráfico de recursos
        if (data.resource_metrics) {
            const resourceData = {
                labels: Object.keys(data.resource_metrics),
                values: Object.values(data.resource_metrics),
            };

            const resourceTrace = {
                values: resourceData.values,
                labels: resourceData.labels,
                type: 'pie',
                hole: 0.4,
                marker: {
                    colors: ['#2196F3', '#4CAF50', '#FFC107', '#F44336']
                }
            };

            Plotly.newPlot('resourcesChart', [resourceTrace], {
                title: 'Distribuição de Recursos',
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)'
            });
        }

        // Métricas detalhadas
        document.getElementById('detailedMetrics').innerHTML = `
            <h2>Análise Detalhada</h2>
            ${createMetricsTable('Performance', {
                'Métricas Básicas': {
                    'Tempo de Resposta': `${basicMetrics.response_time}ms`,
                    'Tempo Total': `${data.total_time}ms`,
                    'Status Code': basicMetrics.status_code,
                    'Tamanho Total': formatBytes(basicMetrics.content_size),
                    'Redirecionamentos': basicMetrics.redirect_count || 0,
                    'URL Final': basicMetrics.final_url || url
                },
                'DNS': data.dns_metrics,
                'SSL/TLS': data.ssl_metrics,
                'Recursos': data.resource_metrics,
                'SEO': data.seo_metrics,
                'Segurança': data.security_metrics,
                'Headers': basicMetrics.headers
            })}
        `;
    })
    .catch(error => {
        document.getElementById('loading').style.display = 'none';
        alert('Erro ao analisar o site: ' + error);
    });
}

// Atualizar o CSS também
const styleSheet = document.createElement('style');
styleSheet.textContent = `
    .nested-table {
        width: 100%;
        margin: 5px 0;
    }

    .nested-content {
        padding: 0 !important;
    }

    .section-header th {
        background-color: #f8f9fa !important;
        color: #2196F3;
        font-size: 1.1em;
        padding: 15px !important;
    }

    .metrics-table tr:hover {
        background-color: #f5f5f5;
    }

    .metrics-table td pre {
        margin: 0;
        white-space: pre-wrap;
        word-break: break-word;
    }
`;
document.head.appendChild(styleSheet);