# 🤖 Documentação do Uso de Inteligência Artificial — `prompts.md`

**Disciplina:** Differentiated Problem Solving (Matemática / Cálculo)  
**Projeto:** ZelaSP — Zeladoria Cidadã Inteligente  
**Global Solution 2026.2:** CitizenTech · FIAP  
**Professor:** Prof. Jones Egydio  
**Integrantes:**  
* Gustavo Rezende Louro — RM570708  
* João Pedro Lagonegro Bosco e Silva — RM569444  
* João Pedro Maschion da Cruz Sá — RM570509  
* Lucas Henrique Alves da Silva — RM572216  

---

## 1. Ferramentas de IA Utilizadas e Finalidades

* **Google Antigravity (Gemini & Claude):** Utilizado como copiloto analítico para estruturar a notação matemática das equações, conferir o passo a passo algébrico, apoiar na organização do script em Python (`DPS_ZelaSP_Modelagem_Matematica.py`), aprimorar a clareza dos textos explicativos e auxiliar na geração do relatório em HTML para exportação fiel do PDF sem falhas de glifos tipográficos.

---

## 2. Prompts Utilizados Durante o Desenvolvimento

### Prompt 1: Estruturação dos Requisitos Obrigatórios de DPS
> *"Como estruturar um script Python (`.py`) de modelagem matemática para a Global Solution da FIAP (Differentiated Problem Solving com o Prof. Jones Egydio), cobrindo regressão por mínimos quadrados, derivadas passo a passo para otimização de pico, limites assintóticos de fila e integrais definidas com regra dos trapézios, aplicado ao fluxo de chamados de zeladoria pós-temporal em São Paulo?"*

### Prompt 2: Verificação Algébrica da Derivada e Raízes
> *"Dada a função cúbica q(t) = a*t³ + b*t² + c*t + d ajustada para dados horários de um dia de 24h, faça o desenvolvimento manual das raízes da derivada q'(t) usando a fórmula de Bhaskara e aplique o teste da segunda derivada q''(t) para classificar o ponto de máximo e de mínimo."*

### Prompt 3: Cálculo da Primitiva e Erro Relativo da Integral
> *"Determine a primitiva analítica Q(t) de q(t) e calcule a integral definida no intervalo [0.5, 23.5] e [0, 24]. Compare o resultado com a soma discreta observada dos relatos para determinar o erro absoluto e o erro relativo percentual."*

### Prompt 4: Revisão Factual, Consolidação em `.py` e Correção do PDF
> *"Converta a modelagem matemática do notebook para um script Python autônomo (`DPS_ZelaSP_Modelagem_Matematica.py`) que gere os gráficos na pasta `imagens/` com os valores exatos de R², RMSE e máximo local calculados pelo NumPy/SciPy, alinhe o relatório técnico a esses mesmos valores reais e corrija a renderização do PDF para eliminar caracteres Unicode quebrados nas fórmulas."*

---

## 3. Funcionalidades Desenvolvidas e Modificadas pelo Grupo

1. **Contextualização com Bairros Reais de São Paulo:**
   * *Ajuste do Grupo:* A IA sugeriu exemplos genéricos de cidades americanas ou bicicletas compartilhadas. O grupo substituiu e modelou o problema real de São Paulo nos bairros foco (**Jabaquara, Vila Mariana, Saúde, Bela Vista, Mooca e Vila Mascote**), focando nos relatos de cabos caídos energizados e bueiros abertos pós-chuva de verão.
2. **Conferência Manual da Álgebra e Correção do Modelo:**
   * A equipe recalculou no papel cada etapa do discriminante de Bhaskara ($\Delta = 1{,}59888$) e das raízes ($t = 15{,}58\text{ h}$ e $t = 1{,}16\text{ h}$), identificou divergências de arredondamento e de $R^2$ entre o texto inicial e a saída numérica real do `np.polyfit` ($q(15{,}58) = 43{,}55\text{ relatos/h}$, $R^2 = 0{,}7721$), corrigindo tanto o script quanto o relatório PDF.
3. **Regra de Decisão de Projeto para a ZelaSP:**
   * O grupo definiu a lógica do **Gatilho Preditivo de Contingência Territorial (GPCT)** baseado no par $(q(t), q'(t))$, transformando a teoria matemática em uma especificação de engenharia de software diretamente utilizável no aplicativo da CitizenTech.

---

## 4. Verificação, Testes e Validação dos Resultados

* **Teste de Aderência da Integral:** A integral calculada $\int_0^{24} q(t)\,dt = 516{,}36$ foi confrontada com a soma discreta dos dados reais ($517{,}00$). O erro relativo obtido de apenas $0{,}12\%$ validou a precisão do ajuste contínuo.
* **Teste do Ponto de Máximo:** A derivada primeira avaliada em $t = 15{,}5789$ resultou exatamente em $0{,}0000$, e a segunda derivada resultou em $-1{,}2645 < 0$, confirmando rigorosamente o ápice do estresse operacional no meio da tarde ($q(15{,}5789) = 43{,}55\text{ relatos/h}$).
* **Teste de Execução Autônoma (`.py`):** Os dados foram incorporados via `StringIO` no próprio `DPS_ZelaSP_Modelagem_Matematica.py`, permitindo execução direta em terminal sem arquivos externos nem conexão à internet, gerando os 3 gráficos em `imagens/`.
* **Inspeção Visual do PDF:** Todas as páginas de `relatorio_tecnico_dps_zelasp.pdf` foram verificadas visualmente após a geração via HTML/Chrome Headless, confirmando a ausência de erros de fonte ou caixas pretas (`■`) nas equações.

---

## 5. Análise Crítica e Reflexão Ética

A inteligência artificial atuou como aceleradora na conferência simbólica, organização do script Python e estruturação tipográfica do PDF. Contudo, a auditoria dos resultados reais do `np.polyfit`, a definição de como modelar o fenômeno, a escolha dos bairros afetados, a interpretação da saturação das centrais de atendimento e as conclusões de engenharia foram elaboradas e validadas integralmente pelos integrantes da equipe.
