# ⚡ E-commerce Analytics & Logistic Performance

> Um painel interativo de Business Intelligence desenvolvido em Python para análise de faturamento, volumetria de vendas e impacto do prazo logístico na satisfação do consumidor.

---

## 🎯 Contexto e Pergunta de Negócio
Em operações modernas de e-commerce, a agilidade logística é um dos principais fatores de retenção e fidelização de clientes. Este projeto foi estruturado para responder à seguinte pergunta central de negócio:

> **"Quais categorias de produtos geram o maior faturamento total e de que forma o tempo médio de entrega impacta a satisfação dos clientes nas diferentes regiões?"**

---

## 🛠️ Stack Tecnológica & Arquitetura
O sistema foi desenvolvido utilizando uma arquitetura enxuta e robusta, tendo um arquivo CSV otimizado como núcleo (*Single Source of Truth*):
* **Python 3.10+**: Linguagem base para toda a lógica de programação.
* **Pandas & NumPy**: Motor de ETL (Extract, Transform, Load), limpeza de dados, engenharia de features e tratamento vetorial de alta performance.
* **Streamlit**: Framework para construção e deploy da interface web interativa.
* **Plotly**: Biblioteca de visualização de dados para criação de gráficos analíticos de alto contraste.

---

## 📊 Funcionalidades do Sistema
1. **Auto-Healing ETL (Auto-cura):** O script valida automaticamente a integridade do banco de dados local. Caso o arquivo de dados não esteja presente, ele gera de forma sintética uma base corporativa realista para evitar quebras de fluxo.
2. **Filtros Globais Dinâmicos:** Segmentação cruzada em tempo real por Estado (UF) e Categoria de Produto.
3. **Indicadores Executivos (KPIs):** Cartões de desempenho destacados para Faturamento Total, Volume de Pedidos, Prazo Médio de Entrega e Nota Média de Satisfação.
4. **Análise Multidimensional:** 
   * Gráfico de barras horizontais destacando o Top 10 de categorias geradoras de receita.
   * Gráfico de série temporal mensal (*Real-Time Analytics*) mapeando a evolução do faturamento corporativo.

---

## 🚀 Como Executar o Projeto Localmente

1. Clone o repositório ou baixe os arquivos para a sua máquina.
2. Instale as bibliotecas necessárias executando o comando abaixo no terminal:
   ```bash
   pip install streamlit pandas numpy plotly