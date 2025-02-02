# PerfomanceGuard - Plataforma de Monitoramento de Desempenho de Sites

## Objetivo
Criar uma plataforma para monitorar e otimizar o desempenho de sites, analisando o tempo de resposta, disponibilidade e segurança, com integração com Cloudflare para otimização de cache e tráfego e AWS Lambda para processamento de dados. A plataforma também vai permitir visualizar métricas em tempo real usando Grafana.

## Arquitetura Completa do Projeto

### Cloudflare Workers
O Cloudflare Workers é a camada de otimização de desempenho do projeto. Ele será responsável por melhorar o tempo de resposta dos sites monitorados, utilizando cache dinâmico e pré-carregamento de conteúdo, ao mesmo tempo que faz o primeiro nível de monitoramento de latência e disponibilidade.

**Funções principais:**

- **Cache de Conteúdo Estático:** Armazenar e entregar conteúdo estático, como imagens, CSS e JS, para diminuir o tempo de carregamento do site.
- **Monitoramento de Latência e Disponibilidade:** Coletar dados básicos sobre o tempo de resposta dos sites e o status de disponibilidade.
- **Verificação de segurança:** Verificar se há ataques ou problemas de segurança, como DDoS, e reportar ao sistema.

### AWS Lambda (Python)
O AWS Lambda será a função principal para processar e analisar os dados que vêm do Cloudflare Workers e outros pontos de monitoramento. Ele será responsável por calcular as métricas de desempenho, analisar os dados de disponibilidade e segurança, e gravar as informações no banco de dados.

**Funções principais:**

- **Coleta e Processamento de Dados:** Receber dados do Cloudflare sobre o desempenho (tempo de resposta, status do site) e realizar cálculos para identificar qualquer problema.
- **Análise de Segurança:** Analisar logs de segurança e detectar possíveis ameaças ou comportamentos suspeitos, como ataques DDoS ou acessos não autorizados.
- **Armazenamento de Métricas:** Enviar os dados coletados para o banco de dados DynamoDB para posterior consulta e análise.
- **Geração de Alertas:** Caso algum parâmetro de desempenho ou segurança esteja fora dos padrões definidos, o Lambda pode disparar alertas para os administradores do site.

### Amazon DynamoDB
DynamoDB será utilizado como banco de dados NoSQL para armazenar todos os dados de desempenho e segurança coletados. Ele proporcionará alta escalabilidade, permitindo armazenar métricas de múltiplos sites de forma eficiente e acessível.

**Funções principais:**

- **Armazenamento de Dados:** Armazenar tempos de resposta, status de disponibilidade, logs de segurança e métricas de performance.
- **Consultas Rápidas:** Suportar consultas rápidas para visualizar métricas em tempo real no Grafana.
- **Escalabilidade:** Garantir que o banco de dados possa crescer à medida que novos sites e mais métricas são adicionados.

### Grafana
Grafana será a interface de visualização de métricas. Ele vai conectar-se ao DynamoDB para mostrar dashboards dinâmicos e gráficos detalhados sobre a performance dos sites monitorados. A visualização permitirá que os administradores e desenvolvedores acompanhem os dados em tempo real e detectem rapidamente qualquer problema de desempenho ou segurança.

**Funções principais:**

- **Visualização de Métricas:** Apresentar gráficos e painéis com as métricas de desempenho, como tempo de resposta, disponibilidade e segurança.
- **Alertas e Notificações:** Configurar alertas para quando um site estiver fora dos parâmetros ideais (tempo de resposta alto, queda de disponibilidade ou problemas de segurança).
- **Análise de Tendências:** Permitir a análise de dados históricos, possibilitando que os administradores identifiquem padrões de performance ao longo do tempo.

## Fluxo de Dados

### Navegação do Usuário:

1. O usuário acessa um site monitorado, o Cloudflare é o primeiro ponto de contato.
2. O Cloudflare Worker verifica se o conteúdo está no cache. Se não estiver, solicita o conteúdo do servidor de backend.

### Monitoramento de Desempenho:

1. Durante a requisição do site, o Cloudflare Worker mede o tempo de resposta (latência) e a disponibilidade do site.
2. O Worker também verifica aspectos de segurança, como possíveis ataques DDoS.

### Processamento no AWS Lambda:

1. Quando o Cloudflare Worker captura dados, ele envia informações para a função AWS Lambda, que realiza o processamento dos dados:
   - Calcular métricas de desempenho, como tempo médio de resposta.
   - Verificar a integridade da segurança do site.
2. Se qualquer métrica estiver fora dos parâmetros desejados, o Lambda envia um alerta para os administradores.

### Armazenamento no DynamoDB:

- Todos os dados de desempenho, status e segurança são gravados no DynamoDB, permitindo consultas rápidas e eficientes.

### Visualização no Grafana:

1. O Grafana acessa o DynamoDB para buscar dados em tempo real e gerar dashboards.
2. As métricas serão apresentadas de forma visual, com gráficos de tempos de resposta, uptimes, falhas de segurança, etc.
3. Alertas são configurados para notificar os administradores caso haja algum problema no site.

## Funcionalidades Chave

### Monitoramento de Tempo de Resposta e Uptime:

- **Métrica:** Tempo médio de resposta do site, tempo de carregamento das páginas e status de disponibilidade.
- **Objetivo:** Garantir que o site esteja rápido e sempre disponível para os usuários.

### Monitoramento de Segurança:

- **Métrica:** Detecção de ataques DDoS, tentativas de acesso não autorizado e outros incidentes de segurança.
- **Objetivo:** Proteger o site contra ameaças externas e garantir que ele esteja seguro.

### Alertas e Notificações:

- **Métrica:** Definir limiares para tempo de resposta, disponibilidade e segurança.
- **Objetivo:** Enviar alertas imediatos aos administradores caso o site apresente problemas.

### Visualização em Tempo Real:

- **Métrica:** Exibição de dashboards com gráficos e relatórios de desempenho e segurança.
- **Objetivo:** Permitir aos administradores acompanharem a saúde do site de forma contínua.

## Tecnologias Utilizadas

- **Cloudflare Workers:** Cache, otimização de tráfego e monitoramento de latência.
- **AWS Lambda:** Processamento de dados e execução de funções serverless.
- **DynamoDB:** Armazenamento de dados escalável e rápido.
- **Grafana:** Visualização de métricas e geração de relatórios interativos.
- **Python:** Linguagem de programação para funções Lambda, análise e processamento de dados.
