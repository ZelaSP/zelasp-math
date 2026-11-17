# 🤖 Documentação Transparente do Uso de Inteligência Artificial — `prompts.md` / `AI.md`

**Disciplina:** Differentiated Problem Solving (Matemática / Cálculo)  
**Professor:** Prof. Jones Egydio  
**Projeto:** ZelaSP — Zeladoria Cidadã Inteligente (Simulação Acadêmica)  
**Global Solution 2026.2:** CitizenTech · FIAP (Engenharia de Software — 1º Ano)  
**Integrantes:**  
* Gustavo Rezende Louro — RM570708  
* João Pedro Lagonegro Bosco e Silva — RM569444  
* João Pedro Maschion da Cruz Sá — RM570509  
* Lucas Henrique Alves da Silva — RM572216  

---

## 1. Ferramentas de IA Utilizadas e Finalidades

* **Google Antigravity (Gemini & Claude):** Utilizado como copiloto analítico e de engenharia de software para estruturar o script Python (`DPS_ZelaSP_Modelagem_Matematica.py`), implementar o ajuste polinomial por mínimos quadrados, codificar a taxa operacional não negativa $\text{taxa\_operacional}(t) = \max(0, q(t))$, configurar a geração dos gráficos científicos em alta resolução (`matplotlib` / `seaborn`) e diagramar o relatório técnico em Markdown/HTML para exportação em PDF (`relatorio_tecnico_dps_zelasp.pdf`).
* **ChatGPT / Codex (OpenAI):** Utilizado na auditoria técnica cruzada da entrega de Matemática e na elaboração do plano de ajustes de consistência entre disciplinas, apoiando a identificação das limitações algébricas do polinômio cúbico (trechos negativos na madrugada/noite e subestimação de $29{,}76\%$ no pico horário), a necessidade de adotar a integral sobre demanda física não negativa ($\max(0, q(t))$) como resultado operacional principal, a separação entre volume excedente acumulado contínuo e fila pendente discreta, e a explicitação da base de comparação do ganho simulado de $-38{,}5\%$.

---

## 2. Interações Realizadas (Exemplos de Prompts e Respostas)

### Interação 1 — Estruturação do Script Python (`.py`) e Modelagem de Cálculo (Limites, Derivadas e Integrais)
* **Prompt enviado:**  
  *"Como estruturar um script Python (`.py`) de modelagem matemática para a Global Solution da FIAP (Differentiated Problem Solving com o Prof. Jones Egydio), cobrindo regressão por mínimos quadrados, derivadas para otimização de pico, limites de fila e integrais definidas com regra dos trapézios, aplicado a uma série temporal simulada de 24h de chamados de zeladoria urbana em São Paulo?"*
* **Resposta obtida e aplicação no projeto:**  
  Foi estruturado o módulo `DPS_ZelaSP_Modelagem_Matematica.py` contendo a série temporal sintética embutida (`DADOS_ZELASP_CSV`, com 24 faixas horárias de $t = 0{,}5\text{ h}$ a $t = 23{,}5\text{ h}$ e soma de $517\text{ relatos}$), funções modulares (`carregar_e_validar_dados`, `calcular_metricas`, `calcular_trapezios`, `gerar_graficos`) e ajuste pelo método dos mínimos quadrados (`np.polyfit`) comparando o modelo quadrático $p_2(t)$ ($R^2 = 0{,}6149$, $\text{RMSE} = 11{,}8101$) com o modelo cúbico $q(t) = -0{,}02924\,t^3 + 0{,}73439\,t^2 - 1{,}59152\,t + 0{,}66653$ ($R^2 = 0{,}7721$, $\text{RMSE} = 9{,}0846$).

### Interação 2 — Desenvolvimento Analítico das Derivadas ($q'(t)$, $q''(t)$), Bhaskara e Limitações do Polinômio
* **Prompt enviado:**  
  *"Dada a função cúbica q(t) = a*t³ + b*t² + c*t + d ajustada sobre a série simulada de 24h, faça o desenvolvimento analítico das raízes da derivada q'(t) usando Bhaskara, aplique o teste da segunda derivada q''(t) e analise as limitações do polinômio (subestimação do pico e valores negativos)."*
* **Resposta obtida e aplicação no projeto:**  
  Foram derivadas analiticamente $q'(t) = -0{,}08772\,t^2 + 1{,}46879\,t - 1{,}59152$ e $q''(t) = -0{,}17545\,t + 1{,}46879$, obtendo $\Delta = 1{,}59888$ ($\sqrt{\Delta} \approx 1{,}26447$) e os pontos críticos $t_1 \approx 15{,}5789\text{ h}$ (máximo local contínuo, $q''(t_1) = -1{,}2645 < 0$, com $q(t_1) \approx 43{,}55\text{ relatos/h}$) e $t_2 \approx 1{,}1646\text{ h}$ (mínimo local algébrico, $q''(t_2) = +1{,}2645 > 0$, com $q(t_2) \approx -0{,}24\text{ relatos/h}$). Documentou-se explicitamente que o polinômio de grau 3 suaviza a crista aguda da série ($43{,}55$ contra $62\text{ relatos/h}$ às 14h30, subestimação de $29{,}76\%$) e assume valores negativos nos subintervalos $(0{,}5606;\,1{,}7859)\text{ h}$ e $(22{,}7688;\,24{,}0]\text{ h}$.

### Interação 3 — Auditoria e Uniformização com Taxa Operacional Não Negativa ($\max(0, q(t))$) e Cenários GPCT
* **Ferramentas:** **ChatGPT / Codex** (auditoria matemática e plano de ajustes) e **Google Antigravity** (implementação no Python e atualização dos gráficos/relatório).
* **Prompt enviado:**  
  *"Defina taxa_operacional(t) = max(0, q(t)) em [0, 24], recalcule os gráficos, a integral operacional e os cenários de volume excedente acumulado acima de S = 35, mantendo q(t) apenas no estudo algébrico e distinguindo volume excedente acumulado de fila pendente discreta."*
* **Resposta obtida e aplicação no projeto:**  
  1. **Função não negativa (`criar_taxa_operacional`):** Implementada `taxa_operacional(t) = np.maximum(0.0, q(t))`, contínua em $[0, 24]\text{ h}$, com transições nas raízes reais de $q(t)$ ($0{,}5606\text{ h}$, $1{,}7859\text{ h}$ e $22{,}7688\text{ h}$).
  2. **Integral operacional principal vs. primitiva algébrica:** A integral operacional não negativa resultou em $\int_0^{24} \max(0, q(t))\,dt = 527{,}69\text{ relatos}$ (diferença de $10{,}69\text{ relatos}$ ou $2{,}07\%$ frente aos $517$ da série discreta, e $512{,}50$ pela regra dos trapézios). A integral algébrica pura $\int_0^{24} q(t)\,dt = Q(24) - Q(0) = 516{,}36\text{ relatos}$ foi mantida apenas na seção algébrica com a explicação de que sua proximidade nominal ($0{,}12\%$) decorre de compensação com áreas negativas sem significado físico.
  3. **Separação entre fila discreta e volume excedente contínuo (`calcular_volume_excedente_continuo`):** Distinguiu-se o saldo discreto de fila às 24h ($127{,}4\text{ chamados}$ no fator $1{,}40$ e $0{,}0$ na base deduplicada) da integral contínua do excedente acima de $S = 35\text{ atend./h}$: $192{,}70$ (fator $1{,}40$, referência), $119{,}69$ (meta de $-45\%$ na parcela duplicada, fator $1{,}22$, $-37{,}9\%$), $42{,}41$ (base deduplicada, fator $1{,}00$, $-78{,}0\%$) e $26{,}08$ (base deduplicada com reforço GPCT de $+4{,}85\text{ atend./h}$ a partir de $t = 10{,}25\text{ h}$, representando **$-38{,}5\%$ frente a $42{,}41$**).

### Interação 4 — Enquadramento Estrito como Simulação Acadêmica e Geração do Relatório Técnico em PDF
* **Prompt enviado:**  
  *"Reformule todo o texto do script, Markdown, README e HTML/PDF para deixar explícito que o estudo usa dados simulados e hipóteses acadêmicas, sem atribuir a série a sensores ou coleta real do SP156."*
* **Resposta obtida e aplicação no projeto:**  
  Todos os títulos, cabeçalhos, legendas dos 3 gráficos (`grafico1_dispersao.png`, `grafico2_ajustes.png` e `grafico3_integral.png`), textos de `relatorio_tecnico_dps_zelasp.md` e `relatorio_tecnico_dps_zelasp.pdf` foram revisados para declarar na abertura que a série de 24h e os parâmetros ($S = 35$, fator $1{,}40$, limiar $30$ e reforço $+4{,}85$) são hipóteses didáticas do exercício acadêmico, além de esclarecer que o estudo temporal do GPCT em Matemática é independente da regra operacional simples adotada no protótipo Web.

---

## 3. Aplicação no Projeto (Arquivos e Módulos)

* **`DPS_ZelaSP_Modelagem_Matematica.py`:** Script principal executável em Python contendo a série simulada de 24h, validação de invariantes (`assert`), ajuste quadrático e cúbico, cálculo de raízes e derivadas, função `criar_taxa_operacional(q)`, integração numérica (`scipy.integrate.quad` e regra dos trapézios compatível com NumPy 1.x/2.x), simulação de fila discreta e volume excedente acumulado, e geração automatizada dos 3 gráficos.
* **`imagens/grafico1_dispersao.png`, `grafico2_ajustes.png` e `grafico3_integral.png`:** Visualizações em 150 DPI com tipografia serifada acadêmica e paleta `viridis`, destacando a janela de pico (12h–17h), o comparativo entre $p_2(t)$, $q(t)$ tracejado e $\text{taxa\_operacional}(t)$ contínua com máximo em $(15{,}58\text{ h};\,43{,}55\text{ rel./h})$, e a área de excedente acima de $S = 35$.
* **`relatorio_tecnico_dps_zelasp.md` e `relatorio_tecnico_dps_zelasp.pdf`:** Relatório técnico completo com 8 seções (Contextualização e Hipóteses, Série Simulada e Estatística Descritiva, Ajuste Polinomial e Taxa Operacional, Cálculo Diferencial, Limites e Fila Discreta, Cálculo Integral, Estudo Didático do GPCT e Limitações/Ética).
* **`README.md`:** Documentação do repositório `zelasp-math` com a Ficha da CitizenTech unificada, instruções de instalação/execução e síntese dos resultados verificados.

---

## 4. Validação das Respostas pelo Grupo

1. **Conferência Algébrica e de Raízes:** O grupo conferiu manualmente a derivação termo a termo de $q(t)$, o discriminante $\Delta = B^2 - 4AC$ na fórmula de Bhaskara, os sinais de $q''(t_1) < 0$ e $q''(t_2) > 0$ e as raízes reais de $q(t) = 0$ no intervalo $[0, 24]\text{ h}$.
2. **Reprodutibilidade e Consistência Numérica no Terminal:** Executamos `python DPS_ZelaSP_Modelagem_Matematica.py` do zero e verificamos que todas as saídas impressas no console batem exatamente com os números e tabelas de `relatorio_tecnico_dps_zelasp.md`, `relatorio_tecnico_dps_zelasp.pdf` e `README.md` ($517$, $21{,}54$, $+8{,}20$, $R^2 = 0{,}6149$ e $0{,}7721$, $43{,}55$, $-29{,}76\%$, $527{,}69$, $2{,}07\%$, $516{,}36$, $512{,}50$, $192{,}70$, $119{,}69$, $42{,}41$ e $26{,}08$ / $-38{,}5\%$).
3. **Alinhamento entre Disciplinas (Web e TX Design):** Validamos que a descrição do resultado matemático ($-38{,}5\%$ sobre a base já deduplicada após reforço de capacidade, nas hipóteses do exercício) e a distinção entre o estudo temporal do GPCT e o contador operacional do painel Web estão idênticas nos repositórios `zelasp-math`, `zelasp-web`, `zelasp-tx-design` e `zelasp-python`.
4. **Inspeção Visual dos Gráficos e do PDF:** Inspecionamos visualmente os 3 arquivos PNG em `imagens/` e todas as páginas de `relatorio_tecnico_dps_zelasp.pdf` para confirmar ausência de cortes de fórmulas LaTeX, sobreposição de rótulos ou divergência de legendas.

---

## 5. Análise Crítica e Reflexão Ética

* **Benefícios:** As ferramentas de IA aceleraram a codificação científica em Python (`numpy`, `scipy`, `matplotlib`), a formatação rigorosa das demonstrações de Cálculo Diferencial e Integral em LaTeX e a revisão crítica cruzada do modelo — em especial, o apoio do **ChatGPT/Codex** ao apontar a compensação algébrica da integral bruta nos trechos em que $q(t) < 0$ e a subestimação do pico pelo polinômio de 3º grau, e do **Google Antigravity** ao reestruturar o código com `taxa_operacional(t) = max(0, q(t))` e regenerar os artefatos visuais e o PDF.
* **Limitações e Dificuldades:** Em versões preliminares, um ajuste polinomial pode parecer "preciso" apenas porque erros positivos e negativos se cancelam na integral definida ($\int_0^{24} q(t)\,dt = 516{,}36$ vs. $517$), ocultando taxas negativas fisicamente impossíveis na madrugada e uma subestimação de quase $30\%$ no horário de pico. Além disso, sem direcionamento claro sobre o domínio do problema, textos gerados com auxílio de IA tendem a misturar parâmetros de simulação com dados operacionais reais.
* **Reflexão Ética e Responsabilidade do Grupo:** O uso ético de IA em modelagem matemática exige transparência sobre o papel de cada ferramenta e rigor na interpretação física das equações. Ao grupo coube definir o problema urbano do ZelaSP, avaliar e aprovar as correções metodológicas da revisão, validar cada cálculo reproduzido pelo script Python e garantir honestidade científica ao apresentar o estudo de forma clara como uma simulação acadêmica fundamentada em hipóteses explícitas.
