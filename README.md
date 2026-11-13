# 📐 ZelaSP — Differentiated Problem Solving (DPS)

> **Global Solution 2026.2 · FIAP**  
> **Disciplina:** Differentiated Problem Solving (Matemática / Cálculo)  
> **Tema:** CitizenTech  
> **Professor:** Prof. Jones Egydio  
> **Integrantes:**
> * Gustavo Rezende Louro — RM570708
> * João Pedro Lagonegro Bosco e Silva — RM569444
> * João Pedro Maschion da Cruz Sá — RM570509
> * Lucas Henrique Alves da Silva — RM572216

---

## 📋 A Ficha da CitizenTech (Modelagem Matemática)

* **Nome da CitizenTech:** ZelaSP
* **Cidade e Bairros de Aplicação:** São Paulo — SP (foco prioritário em **Jabaquara, Vila Mariana, Saúde, Bela Vista, Mooca e Vila Mascote**).
* **Cidadão Beneficiado:** Moradores, pedestres e comerciantes afetados por riscos de fios energizados caídos, tampas de bueiro deslocadas e acúmulo de galhos/entulho após tempestades.
* **Problema em uma Frase:** O SP 156 sofre sobrecarga massiva em dias de temporal por falta de triagem de chamados repetidos para o mesmo poste/rua, gerando uma fila de espera que ultrapassa 36 horas para atendimento de riscos elétricos graves.
* **Como a Matemática Resolve:** Aplica **Derivadas** ($q'(t)$) para identificar o horário exato de pico de ocorrências e a taxa instantânea de aceleração do estresse urbano, e **Integrais** ($\int q(t)\,dt$) para mensurar o volume físico acumulado de demandas, fundamentando o **Gatilho Preditivo de Contingência Territorial (GPCT)** e comprovando a redução de **38,5%** no backlog acumulado (alinhada à meta de **−45%** de chamados duplicados e registro cidadão em **< 15 segundos**).
* **Indicador de Impacto:** Redução do erro da integral contínua do modelo para apenas **$0{,}12\%$** ($516{,}36$ vs $517$ relatos reais), redução de **$38{,}5\%$** no backlog acumulado com reforço GPCT/meta **−45%** de duplicidade (e até **$78{,}0\%$** na área acima de $S=35$ com deduplicação integral) e registro em **< 15 segundos**.
* **ODS Conectados:** ODS 11 (Cidades e Comunidades Sustentáveis) e ODS 9 (Indústria, Inovação e Infraestrutura).

---

## 📁 Arquivos desta Entrega

```text
zelasp-math/
├── DPS_ZelaSP_Modelagem_Matematica.py   # Script Python oficial com cálculos, simulações e gráficos
├── relatorio_tecnico_dps_zelasp.pdf     # Relatório técnico oficial em PDF (fórmulas e gráficos)
├── relatorio_tecnico_dps_zelasp.md      # Relatório técnico em Markdown
├── imagens/                             # Gráficos de alta resolução (paleta viridis)
├── prompts.md                           # Relatório ético de transparência no uso de IA
└── README.md                            # Este documento explicativo
```

---

## 🚀 Como Executar o Código Python (`.py`)

### Pré-requisitos e Execução:
1. Clone este repositório:
   ```bash
   git clone https://github.com/ZelaSP/zelasp-math.git
   cd zelasp-math
   ```
2. Instale as bibliotecas científicas (caso não estejam instaladas):
   ```bash
   pip install numpy pandas matplotlib seaborn scipy
   ```
3. Execute o script oficial de modelagem:
   ```bash
   python DPS_ZelaSP_Modelagem_Matematica.py
   ```
   O script executa todas as validações estatísticas, ajustes polinomiais, derivadas, limites, integrais e simulação GPCT no terminal, e regenera os 3 gráficos em `imagens/`.

---

## 📊 Principais Resultados Obtidos

* **Total de Ocorrências Observadas no Temporal:** $517\text{ relatos}$ (pico observado de $62\text{ relatos/h}$ às $14{,}5\text{ h}$ na Bela Vista)
* **Modelo Cúbico Ajustado:** $q(t) = -0{,}02924\,t^3 + 0{,}73439\,t^2 - 1{,}59152\,t + 0{,}66653$ ($R^2 = 0{,}7721$, $\text{RMSE} = 9{,}08\text{ relatos/h}$)
* **Horário de Pico Calculado por Derivadas:** $t = 15{,}58\text{ h}$ ($15\text{h}35\text{min}$), com taxa contínua do modelo $q(15{,}58) = 43{,}55\text{ relatos/h}$ e $q''(15{,}58) = -1{,}2645 < 0$ (máximo local comprovado)
* **Integral Contínua Calculada:** $\int_0^{24} q(t)\,dt = 516{,}36\text{ relatos}$ (erro relativo de apenas **$0{,}12\%$** contra o total real de $517$)
* **Decisão Operacional ZelaSP:** O par $(q(t), q'(t))$ alimenta o **Gatilho Preditivo de Contingência Territorial (GPCT)**, disparando o alerta preventivo ao superar $30\text{ relatos/h}$ com $q'(t) > 0$ (antecipando o pico em pelo menos **2 horas** nos bairros críticos e reduzindo o backlog em **38,5%**).
