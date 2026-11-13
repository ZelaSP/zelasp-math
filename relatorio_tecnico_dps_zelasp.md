# 📘 Relatório Técnico de Modelagem Matemática — DPS
## Differentiated Problem Solving · Global Solution 2026.2 · FIAP

> **CitizenTech:** ZelaSP — Zeladoria Cidadã Inteligente  
> **Tema Geral:** CitizenTech  
> **Professor:** Prof. Jones Egydio  
> **Curso:** Engenharia de Software (1º Ano · Campus Paulista/Lins)  
> **Integrantes da Equipe:**
> * Gustavo Rezende Louro — RM570708
> * João Pedro Lagonegro Bosco e Silva — RM569444
> * João Pedro Maschion da Cruz Sá — RM570509
> * Lucas Henrique Alves da Silva — RM572216

---

## 📋 A Ficha da CitizenTech (Aplicação em DPS)

* **Nome da CitizenTech:** ZelaSP
* **Cidade e Bairros de Aplicação:** São Paulo — SP (foco nos bairros **Jabaquara, Vila Mariana, Saúde, Bela Vista, Mooca e Vila Mascote**).
* **Cidadão Beneficiado:** Moradores, pedestres e comerciantes expostos a acidentes causados por fios caídos energizados, bueiros abertos e acúmulo de entulho em calçadas após temporais.
* **Problema em uma Frase:** O SP 156 sofre colapso operacional em dias de chuva torrencial devido ao envio em massa de chamados duplicados para o mesmo poste ou via, gerando uma fila de espera opaca que ultrapassa 36 horas para atendimento de riscos elétricos graves.
* **Como a Matemática Resolve:** A aplicação de **Derivadas e Taxas de Variação** ($q'(t)$) detecta o momento exato de aceleração e pico do estresse urbano, enquanto o **Cálculo Integral** ($\int q(t)\,dt$) quantifica o volume físico acumulado de demandas, comprovando que o agrupamento colaborativo e o disparo antecipado do **GPCT** reduzem o backlog acumulado de risco em **$38{,}5\%$** (com meta de **−45%** de chamados duplicados e até **$78{,}0\%$** de corte na sobrecarga acima de $S=35$ em deduplicação integral).
* **ODS Conectados:** ODS 11 (Cidades e Comunidades Sustentáveis) e ODS 9 (Indústria, Inovação e Infraestrutura).

---

## 1. Contextualização e Descrição do Fenômeno Urbano

A cidade de São Paulo possui mais de 45 mil quilômetros de vias públicas e uma malha de fiação aérea densa e desordenada. Em episódios severos de tempestades de verão (com ventos superiores a 60 km/h e precipitação acima de 40 mm/h), a queda de galhos sobre cabos de distribuição de energia elétrica provoca incidentes graves e simultâneos.

Bairros como **Jabaquara, Vila Mariana, Saúde, Bela Vista, Mooca e Vila Mascote** apresentam características urbanas críticas:
1. Alta densidade populacional e tráfego de pedestres próximo a corredores e estações de metrô.
2. Cabeamento aéreo misto (energia de média/baixa tensão compartilhada com dezenas de operadoras de telefonia e dados).
3. Histórico recorrente de quedas de energia que paralisam serviços essenciais e comércio local.

Para fundamentar as decisões da CitizenTech ZelaSP, analisou-se uma série temporal contínua de **24 horas de telemetria** de um temporal típico de verão, medindo a taxa horária de novas ocorrências registradas ($q(t)$ em relatos/hora).

---

## 2. Base de Dados Observacionais e Estatística Descritiva

A base de dados é composta por 24 faixas horárias ($t_i = 0{,}5; 1{,}5; \dots; 23{,}5\text{ h}$):

| Faixa Horária ($t_i$) | Demanda ($y_i$ relatos/h) | Bairro Crítico | Apoios Comunitários |
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

### Resumo Estatístico Observado:
* **Total Diário Observado ($\sum y_i$):** $517\text{ ocorrências}$
* **Taxa Média Horária:** $21{,}54\text{ relatos/h}$
* **Horário de Pico Observado:** $t = 14{,}5\text{ h}$ (62 relatos/h na Bela Vista)
* **Horário de Menor Demanda:** $t = 2{,}5\text{ h}$ e $3{,}5\text{ h}$ (2 relatos/h na Vila Mascote e Saúde)
* **Taxa Média de Variação Pré-Temporal ($9{,}5\text{ h} \to 14{,}5\text{ h}$):**
  $$\frac{\Delta y}{\Delta t} = \frac{62 - 21}{14{,}5 - 9{,}5} = \frac{41}{5{,}0} = \mathbf{+8{,}20\text{ relatos/h}^2}$$

---

## 3. Ajuste de Modelos Matemáticos por Mínimos Quadrados

Ajustaram-se duas famílias polinomiais pelo método dos mínimos quadrados:

### Modelo Quadrático ($p_2(t)$):
$$p_2(t) = -0{,}31828\,t^2 + 8{,}52439\,t - 19{,}66762$$
* $R^2 = 0{,}6149$
* $\text{RMSE} = 11{,}81\text{ relatos/h}$
* *Limitação:* A parábola é simétrica e subestima fortemente a subida explosiva do meio da tarde, além de prever valores negativos expressivos na madrugada.

### Modelo Cúbico ($q(t)$) — **Modelo Oficial Adotado**:
$$q(t) = -0{,}02924\,t^3 + 0{,}73439\,t^2 - 1{,}59152\,t + 0{,}66653$$
* $R^2 = 0{,}7721$
* $\text{RMSE} = 9{,}08\text{ relatos/h}$
* *Vantagem e Análise Crítica:* Supera o modelo quadrático tanto em explicação da variância ($0{,}7721$ vs $0{,}6149$) quanto em erro médio ($9{,}08$ vs $11{,}81$), acompanha o repouso matutino e a assimetria da dispersão noturna, e mantém uma integral diária praticamente exata ($516{,}36$ contra $517$ relatos reais). Como todo ajuste cúbico global sobre um pico agudo discreto ($62\text{ relatos/h}$ às $14{,}5\text{ h}$), a curva suave atenua ligeiramente a crista do pico para $43{,}55\text{ relatos/h}$.

---

## 4. Cálculo Diferencial: Taxas de Variação e Otimização

### 4.1 Derivação Analítica do Modelo Cúbico
Aplicando a regra da potência ($\frac{d}{dt}[t^n] = n t^{n-1}$):

$$\mathbf{q'(t) = -0{,}08772\,t^2 + 1{,}46879\,t - 1{,}59152 \quad [\text{relatos/h}^2]}$$

Segunda derivada:
$$\mathbf{q''(t) = -0{,}17545\,t + 1{,}46879 \quad [\text{relatos/h}^3]}$$

### 4.2 Determinação Analítica dos Pontos Críticos ($q'(t) = 0$)
Equação quadrática $A t^2 + B t + C = 0$:
* $A = -0{,}08772$, $B = 1{,}46879$, $C = -1{,}59152$
* $\Delta = (1{,}46879)^2 - 4(-0{,}08772)(-1{,}59152) = 2{,}15734 - 0{,}55846 = 1{,}59888$
* $\sqrt{\Delta} \approx 1{,}26447$

Raízes da derivada:
$$t_1 = \frac{-1{,}46879 - 1{,}26447}{2(-0{,}08772)} = \frac{-2{,}73326}{-0{,}17545} \approx \mathbf{15{,}5789\text{ h} \quad (15\text{h}35\text{min})}$$
$$t_2 = \frac{-1{,}46879 + 1{,}26447}{2(-0{,}08772)} = \frac{-0{,}20432}{-0{,}17545} \approx \mathbf{1{,}1646\text{ h} \quad (01\text{h}10\text{min})}$$

### 4.3 Classificação pelo Teste da Segunda Derivada
* **Em $t_1 = 15{,}5789\text{ h}$:**
  $$q''(15{,}5789) = -0{,}17545(15{,}5789) + 1{,}46879 = -1{,}2645 < 0 \implies \mathbf{M\acute{A}XIMO\ LOCAL\ (PICO)}$$
  Taxa contínua do modelo no ápice: $q(15{,}5789) = \mathbf{43{,}55\text{ relatos/h}}$.
* **Em $t_2 = 1{,}1646\text{ h}$:**
  $$q''(1{,}1646) = -0{,}17545(1{,}1646) + 1{,}46879 = +1{,}2645 > 0 \implies \mathbf{M\acute{I}NIMO\ LOCAL}$$
  Taxa estimada: $q(1{,}1646) \approx -0{,}24\text{ relatos/h}$ (compatível com repouso da madrugada).

### 4.4 Taxas Instantâneas em Três Pontos Operacionais
1. **$t = 4{,}0\text{ h}$ (Madrugada/Manhã):** $q'(4{,}0) = +2{,}88\text{ relatos/h}^2$ (aceleração positiva moderada).
2. **$t = 15{,}58\text{ h}$ (Pico de estresse):** $q'(15{,}58) = 0{,}00\text{ relatos/h}^2$ (ponto estacionário de máxima severidade).
3. **$t = 18{,}0\text{ h}$ (Pós-chuva / Anoitecer):** $q'(18{,}0) = -3{,}58\text{ relatos/h}^2$ (desaceleração rápida).

---

## 5. Comportamento Assintótico e Limites

1. **Continuidade:** Como $q(t)$ é polinomial, $\lim_{t \to t_0} q(t) = q(t_0)$. Para o pico contínuo, $\lim_{t \to 15{,}5789} q(t) = 43{,}55\text{ relatos/h}$.
2. **Dinâmica de Fila e Saturação Operacional:**
   Seja $S = 35\text{ atendimentos/hora}$ a capacidade média das viaturas da Prefeitura e Enel nos 6 bairros.
   * **Cenário Tradicional (SP 156 sem triagem):** Cada cabo caído gera em média $1{,}4\times$ chamados repetidos de vizinhos diferentes. A taxa de entrada inflacionada atinge $1{,}4 \cdot 43{,}55 \approx \mathbf{60{,}97\text{ chamados/h}}$ no modelo contínuo ($86{,}8\text{ chamados/h}$ no pico discreto), acumulando uma área excedente de $192{,}70\text{ chamados}$ acima da capacidade $S=35$ e encerrando o ciclo de 24h com **$127{,}4\text{ ocorrências represadas}$** no balanço horário discreto ($\lim_{t \to 24} T_{\text{espera}} > 36\text{ horas}$ em eventos subsequentes).
   * **Cenário CitizenTech ZelaSP:** O aplicativo identifica a proximidade geográfica e converte relatos adicionais em *apoio comunitário* (< 15 segundos por relato). Com deduplicação integral, a entrada retorna a $q(t)$, reduzindo o backlog contínuo acima de $S=35$ em **$78{,}0\%$** ($192{,}70 \to 42{,}41\text{ relatos}$) e zerando o saldo da fila ao final das 24h ($\lim_{t \to 24} Fila_{\text{ZelaSP}}(t) \to 0$).

---

## 6. Cálculo Integral: Acumulação e Erro do Modelo

### 6.1 Primitiva Analítica $Q(t)$
Pelo Teorema Fundamental do Cálculo:

$$Q(t) = \int q(t)\,dt = \frac{-0{,}02924}{4} t^4 + \frac{0{,}73439}{3} t^3 - \frac{1{,}59152}{2} t^2 + 0{,}66653\,t + C$$
$$\mathbf{Q(t) = -0{,}007310\,t^4 + 0{,}244798\,t^3 - 0{,}795758\,t^2 + 0{,}666527\,t + C}$$

### 6.2 Cálculo das Integrais Definidas
1. **No intervalo dos dados observados $[0{,}5; 23{,}5]$:**
   $$\int_{0{,}5}^{23{,}5} q(t)\,dt = Q(23{,}5) - Q(0{,}5) = 523{,}68 - 0{,}16 = \mathbf{523{,}52\text{ ocorrências}}$$
2. **No dia civil completo $[0; 24]$:**
   $$\int_{0}^{24} q(t)\,dt = Q(24) - Q(0) = 516{,}36 - 0{,}00 = \mathbf{516{,}36\text{ ocorrências}}$$

### 6.3 Comparação com o Total Real Observado
* **Total Real Observado:** $517{,}00\text{ relatos}$
* **Integral do Modelo Contínuo $[0; 24]$:** $516{,}36\text{ relatos}$
* **Erro Absoluto:** $|516{,}36 - 517{,}00| = \mathbf{0{,}64\text{ relatos}}$
* **Erro Relativo:** $\frac{0{,}64}{517{,}00} \times 100\% = \mathbf{0{,}12\%}$
* **Aproximação pela Regra dos Trapézios:** $512{,}50\text{ relatos}$ (erro de $0{,}87\%$).

---

## 7. Decisão de Projeto para a CitizenTech ZelaSP

Com base na modelagem matemática, o sistema ZelaSP implementa a funcionalidade **Gatilho Preditivo de Contingência Territorial (GPCT)**:

* **Variáveis de Entrada:** Telemetria horária de taxa instantânea $q(t)$ e derivada primeira $q'(t)$.
* **Destinatários:** Centro de Operações da Defesa Civil de São Paulo e Subprefeituras de Jabaquara, Vila Mariana, Saúde, Bela Vista, Mooca e Vila Mascote.
* **Regra de Decisão:**
  $$\mathbf{SE} \quad q(t) \geq 30\text{ relatos/h} \quad \mathbf{E} \quad q'(t) > 0 \implies \mathbf{Disparar\ Alerta\ de\ Contingência}$$
* **Ação no Mundo Real e Impacto Simulado:**
  1. No modelo contínuo, o disparo ocorre em **$t = 10{,}25\text{ h}$**, garantindo **antecedência mínima superior a 2 horas** antes tanto do pico discreto ($14{,}5\text{ h}$) quanto do pico contínuo ($15{,}58\text{ h}$) para deslocar equipes de poda e viaturas de cesto aéreo da Enel.
  2. Com o reforço GPCT durante a janela crítica ($+4{,}85\text{ equipes/h}$ sobre $S=35$) aplicado à demanda $q(t)$, o backlog residual cai exatamente **$38{,}5\%$** ($42{,}41 \to 26{,}08\text{ relatos}$), resultado compatível com a fase de transição do roadmap (**meta de −45% de chamados duplicados**, que reduz o backlog do SP 156 em **$37{,}9\%$**, de $192{,}70$ para $119{,}69$ chamados).

---

## 8. Limitações Técnicas e Responsabilidade Ética

1. **Janela de Validade do Polinômio:** O modelo cúbico tem validade física estrita em $[0; 24]\text{ h}$. Extrapolações para além de 24 horas divergem matematicamente para $-\infty$.
2. **Especificidade Climática:** O modelo representa temporais convectivos de verão com rajadas de vento e fiação aérea mista; não deve ser utilizado em estiagens sem recalibração de coeficientes.
3. **Inclusão Digital:** A prefeitura não deve basear a alocação de equipes exclusivamente no volume de chamados do aplicativo em regiões com baixo sinal de internet celular, sob risco de negligenciar comunidades vulneráveis.

---

## 9. Conclusão

A aplicação do Cálculo Diferencial e Integral demonstrou que a crise de zeladoria pós-temporal em São Paulo não decorre apenas da falta de equipes, mas sim da **opacidade da informação e da duplicidade de chamados** no canal oficial 156. A modelagem matemática comprovou a viabilidade técnica e a alta eficiência da **ZelaSP** como ferramenta de cidadania ativa e tomada de decisão preditiva baseada em dados reais.
