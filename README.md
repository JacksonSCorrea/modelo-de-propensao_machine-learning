
## Modelo Preditivo de Propensão à adesão de produtos bancários

Este repositório contém o código e a documentação relacionados ao projeto do modelo preditivo de propensão à subscrição de depósitos bancários a prazo para o Banco Prospex. O objetivo deste projeto é melhorar a eficácia das campanhas de marketing direcionadas a depósitos bancários a prazo, permitindo ao banco prever quais clientes têm maior probabilidade de adquirir esse produto.
O projeto foi desenvolvido co orintação ao CRISP-DM, de forma que as etapas são bem definidas eestão corretamente organizadas no código.

### Contexto
O Banco Prospex, uma instituição bancária portuguesa, enfrenta desafios na eficácia de suas campanhas de marketing para depósitos bancários a prazo. Atualmente, as abordagens de marketing são amplas e pouco personalizadas, resultando em baixas taxas de conversão e uso ineficaz de recursos.

---

### Desafio de Negócio
O desafio deste projeto é criar um modelo de propensão à compra de depósitos bancários a prazo que permita à instituição:

Desenvolver um modelo de aprendizado de máquina capaz de prever a propensão de um cliente à subscrição do produto com base em seus atributos e histórico.
Identificar os principais fatores que influenciam a decisão dos clientes de subscreverem ou não um depósito bancário a prazo com base nas informações disponíveis.
Classificar os clientes em grupos de alta, média e baixa propensão, para direcionar esforços de marketing de forma mais eficaz.
Aumentar a taxa de conversão das campanhas de marketing, economizando recursos e melhorando o retorno sobre o investimento.

### Ganhos Esperados
O projeto visa a obtenção dos seguintes ganhos:

Captação de Recursos: Depósitos a prazo permitem que o banco capte recursos de clientes, usados para financiar operações e empréstimos.
Fonte de Financiamento de Baixo Custo: Depósitos a prazo oferecem financiamento mais econômico ao banco, com taxas de juros menores para os clientes.
Aumento da Base de Clientes: Oferecer depósitos a prazo pode atrair novos clientes, expandindo a base de clientes e aumentando a participação de mercado.
Diversificação de Fontes de Financiamento: Reduz a dependência de outras formas de captação de recursos.
Construção de Relacionamentos: Permite a construção de relacionamentos duradouros com os clientes, levando a vendas cruzadas de outros produtos financeiros.
Gestão de Liquidez: Ajuda na gestão da liquidez do banco, fornecendo uma fonte de financiamento estável e de longo prazo.

### Público-Alvo
O banco tem interesse em realizar ofertas de serviços para o público entre 25 e 65 anos.

### Faixas de Score para Propensão
As faixas de score para classificar a propensão dos clientes são definidas da seguinte maneira:

* Alta Propensão: Score acima de 0.75
* Média Propensão: Score entre 0.5 e 0.75
* Baixa Propensão: Score abaixo de 0.5

### Implantação do Modelo
O modelo será implantado através de uma API que será consumida online. As equipes de marketing/vendas terão acesso a uma página web onde poderão fazer upload do conjunto de dados disponíveis no momento. Em retorno, obterão três planilhas separadas de acordo com o score dos clientes. O banco considera custos computacionais limitados em relação à infraestrutura em nuvem, portanto, o menor custo deve ser considerado.

### Métricas de Avaliação
O desempenho do modelo será avaliado com base nas seguintes métricas:

* AUC-ROC: Área sob a curva ROC, indicando a capacidade de discriminação do modelo.
* Índice Gini: Métrica derivada da AUC-ROC que quantifica a desigualdade ou impureza do modelo.
* Estatística KS (Kolmogorov-Smirnov): Mede a diferença máxima entre as funções de distribuição acumulada de eventos e não eventos.

### Dados Disponíveis
Será disponibilizado um conjunto de dados completo que inclui informações demográficas dos clientes, dados financeiros, histórico de contatos anteriores e resultados de campanhas de marketing anteriores.
