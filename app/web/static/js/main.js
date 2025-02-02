function analyzeUrl() {
    const url = document.getElementById('urlInput').value;
    if (!url) {
        alert('Por favor, insira uma URL válida');
        return;
    }

    // Mostrar loading
    document.getElementById('loading').style.display = 'block';
    
    // Limpar resultados anteriores
    document.getElementById('metricsCards').innerHTML = '';
    document.getElementById('responseTimeChart').innerHTML = '';
    document.getElementById('resourcesChart').innerHTML = '';
    document.getElementById('detailedMetrics').innerHTML = '';

    fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({url: url})
    })
    .then(response => response.json())
    .then(data => {
        // Esconder loading
        document.getElementById('loading').style.display = 'none';

        // Mostrar métricas básicas
        const basicMetrics = data.basic_metrics;
        document.getElementById('metricsCards').innerHTML = `
            <div class="metric-card">
                <h3>Tempo de Resposta</h3>
                <div class="metric-value">${basicMetrics.response_time}ms</div>
            </div>
            <div class="metric-card">
                <h3>Status</h3>
                <div class="metric-value">${basicMetrics.status_code}</div>
            </div>
            <div class="metric-card">
                <h3>Tamanho</h3>
                <div class="metric-value">${(basicMetrics.content_size / 1024).toFixed(2)}KB</div>
            </div>
        `;

        // Criar gráfico de tempo de resposta
        const responseTrace = {
            y: [basicMetrics.response_time],
            type: 'bar',
            name: 'Tempo de Resposta (ms)'
        };

        Plotly.newPlot('responseTimeChart', [responseTrace], {
            title: 'Tempo de Resposta',
            yaxis: {title: 'Millisegundos'}
        });

        // Mostrar métricas detalhadas
        document.getElementById('detailedMetrics').innerHTML = `
            <h2>Métricas Detalhadas</h2>
            <pre>${JSON.stringify(data, null, 2)}</pre>
        `;
    })
    .catch(error => {
        document.getElementById('loading').style.display = 'none';
        alert('Erro ao analisar o site: ' + error);
    });
}