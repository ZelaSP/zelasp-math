# 📘 Relatório Técnico de Modelagem Matemática — DPS
## Differentiated Problem Solving · Global Solution 2026.2 · FIAP

> **CitizenTech:** ZelaSP — Zeladoria Cidadã Inteligente (Simulação Acadêmica)  
> **Tema Geral:** CitizenTech  
> **Professor:** Prof. Jones Egydio  
> **Curso:** Engenharia de Software (1º Ano · Campus Paulista/Lins)  
> **Integrantes da Equipe:**
> * Gustavo Rezende Louro — RM570708
> * João Pedro Lagonegro Bosco e Silva — RM569444
> * João Pedro Maschion da Cruz Sá — RM570509
> * Lucas Henrique Alves da Silva — RM572216

---

## ⚠️ Apresentação e Origem dos Dados

> Este trabalho utiliza uma série de dados simulados para fins acadêmicos. O cenário representa a variação horária de relatos de zeladoria ao longo de 24 horas, com crescimento de demanda no período de um temporal e redução posterior. Os valores são parâmetros do exercício de modelagem e não representam uma coleta real do SP156 ou de sensores.

---

## 📋 A Ficha da CitizenTech (Contexto e Escopo)

* **Nome da CitizenTech:** ZelaSP
* **Cidade e Bairros de Referência:** São Paulo — SP (**Jabaquara, Vila Mariana, Saúde, Bela Vista, Mooca e Vila Mascote**).
* **Cidadão Beneficiado:** Moradores, pedestres e comerciantes expostos a ocorrências de zeladoria urbana (fios soltos/energizados, tampas de bueiro faltantes, buracos e entulho em calçadas).
* **Problema em uma Frase:** Canais tradicionais de zeladoria recebem solicitações repetidas para o mesmo ponto em cenários de alta demanda pós-temporal, dificultando a triagem de risco e a visualização coletiva de chamados já abertos no quarteirão.
* **Resumo das Formulações do Projeto:**
  * **Arquitetura:** Web com MockAPI e ViaCEP; CLI Python com JSON; estudo matemático independente; integração entre módulos e IoT prevista na evolução.
  * **Tempo de relato:** Meta de registro em até 15 segundos, a validar com testes de usabilidade (sem estimativa numérica não comprovada para canais oficiais externos).
  * **Duplicidade atual e meta:** Apoio manual a ocorrências existentes para incentivar a redução de relatos repetidos; meta futura de reduzir em 45% a parcela de chamados duplicados.
  * **Foto e localização:** Funcionalidade futura: foto como evidência e apoio à localização da ocorrência; seleção demonstrativa na versão atual (endereço informado por CEP ou digitação, com captura opcional de GPS do navegador no Web).
  * **Resultado matemático (simulado):** Redução simulada de 38,5% do excedente sobre a base já deduplicada, após reforço de capacidade, nas hipóteses do exercício.
* **ODS Conectados:** ODS 11 (Cidades e Comunidades Sustentáveis) e ODS 9 (Indústria, Inovação e Infraestrutura).

---

## 1. Contextualização e Construção do Cenário Simulado

Em bairros adensados de São Paulo com rede aérea mista (como **Jabaquara, Vila Mariana, Saúde, Bela Vista, Mooca e Vila Mascote**), episódios de chuva forte concentram demandas simultâneas de zeladoria ao longo de poucas horas.

Para o exercício de modelagem matemática em Cálculo Diferencial e Integral, construiu-se uma **série sintética de 24 faixas horárias** ($t_i = 0{,}5; 1{,}5; \dots; 23{,}5\text{ h}$):
* Menor taxa simulada na madrugada ($2\text{ relatos/h}$ em $t = 2{,}5\text{ h}$ e $3{,}5\text{ h}$);
* Crescimento contínuo a partir do fim da manhã até o pico de **$62\text{ relatos/h}$ às 14h30** ($t = 14{,}5\text{ h}$);
* Desaceleração gradual no fim da tarde e noite até $5\text{ relatos/h}$ em $t = 23{,}5\text{ h}$.

Os campos `bairro_critico` e `apoios_comunitarios` compõem o contexto didático da tabela; o ajuste polinomial utiliza exclusivamente o tempo ($t$) e a taxa horária de relatos ($y$).

Adotam-se como **hipóteses acadêmicas** deste exercício (e não como medições reais do serviço público):
* Capacidade de atendimento de **$S = 35\text{ atendimentos/h}$**;
* Fator de entrada inflacionada por chamados duplicados de **$1{,}40$**;
* Reforço hipotético de capacidade de **$+4{,}85\text{ atendimentos/h}$** acionado acima do limiar;
* Limiar de gatilho de **$30\text{ relatos/h}$** com inclinação positiva ($q'(t) > 0$).

---

## 2. Série Simulada e Estatística Descritiva

| Faixa Horária ($t_i$) | Taxa Simulada ($y_i$ relatos/h) | Bairro (Contexto) | Apoios (Contexto) |
| :---: | :---: | :---: | :---: |
| 0,5 h | 4 | Mooca | 1 |
| 1,5 h | 3 | Bela Vista | 0 |
| 2,5 h | 2 | Vila Mascote | 0 |
| 3,5 h | 2 | Saúde | 0 |
| 4,5 h | 3 | Jabaquara | 1 |
| 5,5 h | 5 | Vila Mariana | 2 |
| 6,5 h | 8 | Bela Vista | 3 |
| 7,5 h | 12 | Mooca | 4 |
| 8,5 h | 16 | Jabaquara | 6 |
| 9,5 h | 21 | Vila Mariana | 9 |
| 10,5 h | 28 | Saúde | 14 |
| 11,5 h | 38 | Vila Mascote | 18 |
| 12,5 h | 49 | Jabaquara | 24 |
| 13,5 h | 58 | Vila Mariana | 31 |
| 14,5 h | 62 | Bela Vista | 35 |
| 15,5 h | 55 | Saúde | 28 |
| 16,5 h | 42 | Mooca | 21 |
| 17,5 h | 31 | Vila Mascote | 15 |
| 18,5 h | 24 | Jabaquara | 11 |
| 19,5 h | 18 | Vila Mariana | 8 |
| 20,5 h | 14 | Saúde | 6 |
| 21,5 h | 10 | Bela Vista | 4 |
| 22,5 h | 7 | Mooca | 2 |
| 23,5 h | 5 | Jabaquara | 1 |

### Resumo Estatístico da Série Simulada:
* **Soma da Série Simulada ($\sum y_i$):** $517\text{ relatos}$
* **Taxa Média Horária:** $21{,}54\text{ relatos/h}$
* **Pico da Série Simulada:** $62\text{ relatos/h}$ às 14h30 ($t = 14{,}5\text{ h}$)
* **Menor Taxa Simulada:** $2\text{ relatos/h}$ em $t = 2{,}5\text{ h}$ e $3{,}5\text{ h}$
* **Taxa Média de Variação Pré-Pico ($9{,}5\text{ h} \to 14{,}5\text{ h}$):**
  $$\frac{\Delta y}{\Delta t} = \frac{62 - 21}{14{,}5 - 9{,}5} = \frac{41}{5{,}0} = \mathbf{+8{,}20\text{ relatos/h}^2}$$

---

## 3. Ajuste Polinomial e Definição da Taxa Operacional

Ajustaram-se dois polinômios pelo método dos mínimos quadrados:

### Modelo Quadrático ($p_2(t)$):
$$p_2(t) = -0{,}31828\,t^2 + 8{,}52439\,t - 19{,}66762$$
* $R^2 = 0{,}6149$ | $\text{RMSE} = 11{,}81\text{ relatos/h}$
* *Limitação:* Como parábola simétrica, não representa bem a concentração do pico e assume valores negativos extensos na madrugada.

### Modelo Cúbico Algébrico ($q(t)$) e Taxa Operacional Não Negativa:
$$q(t) = -0{,}02924\,t^3 + 0{,}73439\,t^2 - 1{,}59152\,t + 0{,}66653$$
* $R^2 = 0{,}7721$ | $\text{RMSE} = 9{,}08\text{ relatos/h}$

Embora $q(t)$ melhore o ajuste global em relação a $p_2(t)$, o polinômio cúbico ainda assume valores negativos nos subintervalos $t \in (0{,}5606;\,1{,}7859)\text{ h}$ e $t \in (22{,}7688;\,24{,}0]\text{ h}$ — uma **limitação algébrica do ajuste polinomial**. Como taxas físicas de chegada de relatos não podem ser negativas, este trabalho adota uniformemente para a demanda física, as integrais operacionais, os gráficos de fluxo e as simulações de capacidade a função contínua por partes:

$$\text{taxa\_operacional}(t) = \max\bigl(0,\, q(t)\bigr), \quad 0 \leq t \leq 24\text{ horas}$$

* **Pontos de transição onde $q(t) = 0$:** $t \approx 0{,}5606\text{ h}$, $t \approx 1{,}7859\text{ h}$ e $t \approx 22{,}7688\text{ h}$.
* Nos trechos recortados onde $q(t) < 0$, $\text{taxa\_operacional}(t)$ é **constante igual a zero**; portanto, não se atribui a esses trechos a derivada do polinômio $q'(t)$.

---

## 4. Cálculo Diferencial: Estudo Algébrico de $q(t)$

### 4.1 Primeira e Segunda Derivadas Analíticas do Ajuste Cúbico
Aplicando a regra da potência ($\frac{d}{dt}[t^n] = n t^{n-1}$) sobre $q(t)$ nos intervalos onde $q(t)$ descreve o perfil analítico:

$$\mathbf{q'(t) = -0{,}08772\,t^2 + 1{,}46879\,t - 1{,}59152 \quad [\text{relatos/h}^2]}$$
$$\mathbf{q''(t) = -0{,}17545\,t + 1{,}46879 \quad [\text{relatos/h}^3]}$$

### 4.2 Pontos Críticos de $q(t)$ ($q'(t) = 0$) via Bhaskara
* $A = -0{,}08772$, $B = 1{,}46879$, $C = -1{,}59152$
* $\Delta = (1{,}46879)^2 - 4(-0{,}08772)(-1{,}59152) = 1{,}59888 \implies \sqrt{\Delta} \approx 1{,}26447$
* **Raízes:**
  $$t_1 = \frac{-1{,}46879 - 1{,}26447}{2(-0{,}08772)} \approx \mathbf{15{,}5789\text{ h} \quad (15\text{h}35\text{min})}$$
  $$t_2 = \frac{-1{,}46879 + 1{,}26447}{2(-0{,}08772)} \approx \mathbf{1{,}1646\text{ h} \quad (01\text{h}10\text{min})}$$

### 4.3 Classificação e Análise Crítica da Subestimação do Pico
* **Em $t_1 = 15{,}5789\text{ h}$:** $q''(15{,}5789) = -1{,}2645 < 0 \implies \mathbf{M\acute{a}ximo\ Local}$, com $q(15{,}5789) \approx \mathbf{43{,}55\text{ relatos/h}}$ (trecho positivo onde $\text{taxa\_operacional}(t) = q(t)$).
* **Subestimação do Pico:** Enquanto o pico da série simulada ocorre às 14h30 com $62\text{ relatos/h}$, o pico do ajuste cúbico atinge aproximadamente $43{,}55\text{ relatos/h}$, subestimando esse máximo horário em cerca de **$29{,}76\%$**. Como limitação clássica de polinômios de grau 3 sobre cristas agudas, o pequeno erro de um total diário não demonstra precisão da previsão horária.
* **Em $t_2 = 1{,}1646\text{ h}$:** $q''(1{,}1646) = +1{,}2645 > 0 \implies \mathbf{M\acute{i}nimo\ Local\ alg\acute{e}brico}$ com $q(1{,}1646) \approx -0{,}24\text{ relatos/h}$ (recortado para zero na $\text{taxa\_operacional}(t)$).

### 4.4 Taxas Instantâneas de $q(t)$ em Pontos Selecionados
1. **$t = 4{,}0\text{ h}$:** $q'(4{,}0) = +2{,}88\text{ relatos/h}^2$ (crescimento positivo no trecho $\text{taxa\_operacional}(t) = q(t)$).
2. **$t = 15{,}58\text{ h}$:** $q'(15{,}58) = 0{,}00\text{ relatos/h}^2$ (ponto estacionário de máximo contínuo).
3. **$t = 18{,}0\text{ h}$:** $q'(18{,}0) = -3{,}58\text{ relatos/h}^2$ (queda da taxa no período pós-pico).

---

## 5. Limites, Fila Pendente Discreta e Capacidade

1. **Continuidade:** Como $q(t)$ é contínua em $\mathbb{R}$ e a função $\max(0, \cdot)$ preserva continuidade, $\text{taxa\_operacional}(t)$ é contínua em todo o intervalo $[0; 24]\text{ h}$, incluindo os pontos de transição ($0{,}5606\text{ h}$, $1{,}7859\text{ h}$ e $22{,}7688\text{ h}$), embora não seja diferenciável exatamente nesses três pontos. No máximo contínuo, $\lim_{t \to 15{,}5789} \text{taxa\_operacional}(t) \approx 43{,}55\text{ relatos/h}$.
2. **Distinção de Métricas:**
   * **Fila pendente:** saldo calculado passo a passo pela evolução horária discreta ($\text{fila}_i = \max(0,\, \text{fila}_{i-1} + \text{entrada}_i - S)$). Na hipótese $S = 35\text{ atendimentos/h}$ e entrada $1{,}40\,y_i$, o saldo discreto às 24h fecha em $127{,}4\text{ chamados pendentes}$; na base deduplicada ($1{,}00\,y_i$), o saldo discreto zera ao final de 24h ($\text{fila}_{24\text{h}} = 0{,}0$). *(O modelo não estabelece prazos de espera em horas como $> 36\text{ horas}$.)*
   * **Volume excedente acumulado acima da capacidade:** integral contínua da parte positiva entre demanda e capacidade ($\int_0^{24} \max(0,\, \text{entrada}(t) - S(t))\,dt$), detalhada na Seção 7.

---

## 6. Cálculo Integral: Taxa Operacional vs. Primitiva Algébrica

### 6.1 Resultado Operacional Principal ($\text{taxa\_operacional}(t) = \max(0, q(t))$)
Integrando numericamente a taxa não negativa sobre o dia completo $[0; 24]$:

$$\int_{0}^{24} \text{taxa\_operacional}(t)\,dt = \int_{0}^{0{,}5606} q(t)\,dt + \int_{1{,}7859}^{22{,}7688} q(t)\,dt \approx \mathbf{527{,}69\text{ relatos}}$$

* **Comparação com a Soma Simulada ($517\text{ relatos}$):**
  * Diferença absoluta: $|527{,}69 - 517{,}00| = \mathbf{10{,}69\text{ relatos}}$
  * Diferença relativa: $\frac{10{,}69}{517{,}00} \times 100\% \approx \mathbf{2{,}07\%}$
* **Aproximação Numérica pela Regra dos Trapézios (série discreta):** $512{,}50\text{ relatos}$ (diferença de $0{,}87\%$).

### 6.2 Análise Algébrica da Primitiva Original $Q(t)$
Pelo Teorema Fundamental do Cálculo, a primitiva algébrica do polinômio cúbico puro é:
$$\mathbf{Q(t) = -0{,}007310\,t^4 + 0{,}244798\,t^3 - 0{,}795758\,t^2 + 0{,}666527\,t + C}$$

Avaliando a integral do polinômio **sem recorte de não negatividade** em $[0; 24]$:
$$\int_{0}^{24} q(t)\,dt = Q(24) - Q(0) = \mathbf{516{,}36\text{ relatos}}$$

*Nota explicativa:* O valor $516{,}36$ (aparentemente próximo de $517$, diferença nominal de $0{,}12\%$) ocorre por **compensação algébrica** com áreas negativas geradas por $q(t) < 0$ em $(0{,}5606;\,1{,}7859)$ e $(22{,}7688;\,24{,}0]$. Por isso, **$516{,}36$ não é adotado como total operacional principal nem fundamenta precisão de $0{,}12\%$ para a taxa corrigida**.

---

## 7. Estudo Didático do GPCT e Cenários Simulados de Excedente

Como exercício de apoio à decisão, estuda-se o mecanismo temporal **Gatilho Preditivo de Contingência Territorial (GPCT)**:
* **Regra simulada:** $\text{taxa\_operacional}(t) \geq 30\text{ relatos/h}$ e $q'(t) > 0$ (no modelo contínuo, dispara a partir de **$t = 10{,}25\text{ h}$**, antecipando o pico em mais de 2 horas).
* **Nota de arquitetura:** Este estudo matemático é uma simulação temporal independente; no WebApp atual, o indicador GPCT utiliza apenas a contagem simples de chamados não resolvidos de nível $\geq 4$, permanecendo eventual integração preditiva para evolução futura.

### Cenários de Volume Excedente Acumulado Acima de $S = 35\text{ atendimentos/h}$:

| Cenário Simulado | Volume Excedente Acumulado | Comparação Verificada |
| :--- | :---: | :--- |
| Entrada com fator $1{,}40$ e capacidade $35$ | **$192{,}70$** | Referência da simulação |
| Redução de $45\%$ da parcela duplicada: fator $1{,}22$ | **$119{,}69$** | Redução de **$37{,}9\%$** frente a $192{,}70$ |
| Entrada integralmente deduplicada: fator $1{,}00$ | **$42{,}41$** | Redução de **$78{,}0\%$** frente a $192{,}70$ |
| Base já deduplicada com reforço no gatilho ($+4{,}85\text{ atend./h}$) | **$26{,}08$** | Redução de **$38{,}5\%$ frente a $42{,}41$** |

> No cenário acadêmico simulado, o reforço de capacidade acionado pelo gatilho reduz em aproximadamente 38,5% o volume excedente acumulado em relação ao cenário já deduplicado, sem reforço. Esse resultado depende das hipóteses do exercício e não representa um ganho medido em operação real.

---

## 8. Limitações do Modelo e Cuidados Éticos

1. **Caráter Sintético dos Dados:** Todos os números decorrem de uma série didática e de hipóteses acadêmicas de simulação, sem coleta de campo ou validação em operação real.
2. **Limitação Polinomial:** $q(t)$ diverge fora de $[0; 24]\text{ h}$, subestima o pico em $29{,}76\%$ e gera valores negativos sem significado físico antes do recorte $\text{taxa\_operacional}(t) = \max(0, q(t))$.
3. **Inclusão Digital e Equidade:** Nenhuma política pública baseada em relatos digitais deve substituir vistorias presenciais em áreas com menor acesso à internet ou telefonia.
