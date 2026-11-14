# 🤖 Documentação do Uso de Inteligência Artificial — `prompts.md`

**Disciplina:** Differentiated Problem Solving (Matemática / Cálculo)  
**Projeto:** ZelaSP — Zeladoria Cidadã Inteligente (Simulação Acadêmica)  
**Global Solution 2026.2:** CitizenTech · FIAP  
**Professor:** Prof. Jones Egydio  
**Integrantes:**  
* Gustavo Rezende Louro — RM570708  
* João Pedro Lagonegro Bosco e Silva — RM569444  
* João Pedro Maschion da Cruz Sá — RM570509  
* Lucas Henrique Alves da Silva — RM572216  

---

## 1. Ferramentas de IA Utilizadas e Finalidades

* **Google Antigravity (Gemini & Claude):** Utilizado como copiloto analítico para estruturar a notação matemática das equações, organizar o script Python (`DPS_ZelaSP_Modelagem_Matematica.py`), implementar o tratamento não negativo $\text{taxa\_operacional}(t) = \max(0, q(t))$ e gerar o relatório técnico em HTML/PDF sem falhas tipográficas.
* **ChatGPT / Codex (OpenAI):** Utilizado na auditoria técnica cruzada da entrega de Matemática e na elaboração do plano de ajustes, apontando as limitações algébricas do ajuste cúbico (trechos negativos e subestimação de pico), a necessidade de corrigir a integral para demanda física não negativa ($\max(0, q(t))$) e a separação correta entre volume excedente acumulado e fila pendente discreta.

---

## 2. Prompts Utilizados Durante o Desenvolvimento

### Prompt 1: Estruturação dos Requisitos Obrigatórios de DPS
> *"Como estruturar um script Python (`.py`) de modelagem matemática para a Global Solution da FIAP (Differentiated Problem Solving com o Prof. Jones Egydio), cobrindo regressão por mínimos quadrados, derivadas para otimização de pico, limites de fila e integrais definidas com regra dos trapézios, aplicado a uma série temporal simulada de 24h?"*

### Prompt 2: Verificação Algébrica da Derivada e Raízes
> *"Dada a função cúbica q(t) = a*t³ + b*t² + c*t + d ajustada sobre a série simulada de 24h, faça o desenvolvimento analítico das raízes da derivada q'(t) usando Bhaskara, aplique o teste da segunda derivada q''(t) e analise as limitações do polinômio (subestimação do pico e valores negativos)."*

### Prompt 3: Uniformização com Taxa Operacional Não Negativa e Separação de Métricas
> *"Defina taxa_operacional(t) = max(0, q(t)) em [0, 24], recalcule os gráficos, a integral operacional e os cenários de volume excedente acumulado acima de S = 35, mantendo q(t) apenas no estudo algébrico e distinguindo volume excedente acumulado de fila pendente discreta."*

### Prompt 4: Revisão de Escopo Acadêmico e Exportação do PDF
> *"Reformule todo o texto do script, Markdown, README e HTML/PDF para deixar explícito que o estudo usa dados simulados e hipóteses acadêmicas, sem atribuir a série a sensores ou coleta real do SP156."*

---

## 3. Funcionalidades Desenvolvidas e Modificadas pelo Grupo

1. **Enquadramento Claro como Simulação Acadêmica:**
   * *Ajuste do Grupo:* A equipe definiu os parâmetros sintéticos de 24 faixas horárias (com menor demanda na madrugada e pico de 62 relatos/h às 14h30) e explicitou que $S=35$, fator $1{,}40$, limiar $30$ e reforço $+4{,}85$ são hipóteses didáticas do exercício.
2. **Padronização da Curva Não Negativa (`taxa_operacional(t) = max(0, q(t))`):**
   * Na revisão crítica conduzida com apoio do **ChatGPT/Codex** e validada pelo grupo, constatou-se que a integral bruta $\int_0^{24} q(t)\,dt = 516{,}36$ compensava trechos negativos do polinômio cúbico. Com apoio do Google Antigravity e revisão da equipe, implementou-se `criar_taxa_operacional(q)` no script Python, obtendo $\int_0^{24} \max(0, q(t))\,dt = 527{,}69\text{ relatos}$ (diferença de $2{,}07\%$ para $517$), e registraram-se os três pontos de transição onde $q(t) = 0$ ($0{,}5606\text{ h}$, $1{,}7859\text{ h}$ e $22{,}7688\text{ h}$).
3. **Análise Crítica de Limitações:**
   * A partir dos apontamentos levantados com o Codex e revisados pelo grupo, registraram-se explicitamente a subestimação do pico ($43{,}55$ vs $62$ simulado, $\approx 29{,}76\%$), a distinção entre "volume excedente acumulado acima da capacidade" (integral contínua) e "fila pendente" (saldo discreto) e a separação entre o estudo didático do GPCT e o indicador simples presente no protótipo Web.

---

## 4. Verificação, Testes e Validação dos Resultados

* **Teste de Consistência Numérica:** Execução de `DPS_ZelaSP_Modelagem_Matematica.py` reproduzindo exatamente os valores de referência: integral operacional $527{,}69$ ($2{,}07\%$), volume excedente $192{,}70$ (fator $1{,}40$), $119{,}69$ (fator $1{,}22$, $-37{,}9\%$), $42{,}41$ (fator $1{,}00$, $-78{,}0\%$) e $26{,}08$ (base deduplicada + reforço, $-38{,}5\%$ frente a $42{,}41$).
* **Conferência dos Gráficos (`imagens/`):** Validação visual de `grafico1_dispersao.png`, `grafico2_ajustes.png` e `grafico3_integral.png` com legendas alinhadas à série simulada, aos trechos recortados em zero e ao volume excedente acumulado.
* **Inspeção Visual do PDF:** Verificação de todas as páginas de `relatorio_tecnico_dps_zelasp.pdf` após geração via HTML e Chrome Headless.

---

## 5. Análise Crítica e Reflexão Ética

As ferramentas de IA tiveram participação relevante tanto na produção inicial quanto na revisão técnica do trabalho: o **Google Antigravity** auxiliou na escrita dos scripts de plotagem, na implementação em Python e na geração do relatório em HTML/PDF, enquanto o **ChatGPT/Codex** apoiou a auditoria matemática crítica que identificou limitações algébricas da regressão polinomial (trechos negativos e subestimação do pico) e orientou a correção da integral para demanda física não negativa ($\text{taxa\_operacional}(t) = \max(0, q(t))$). Ao grupo coube avaliar e aprovar as decisões do plano de revisão, conferir os cálculos e saídas numéricas do script `DPS_ZelaSP_Modelagem_Matematica.py`, validar visualmente os gráficos e o PDF e assegurar honestidade acadêmica ao apresentar o estudo como simulação didática com dados sintéticos.
