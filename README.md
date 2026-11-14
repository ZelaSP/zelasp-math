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

## ⚠️ Nota sobre os Dados (Simulação Acadêmica)

> Este trabalho utiliza uma série de dados simulados para fins acadêmicos. O cenário representa a variação horária de relatos de zeladoria ao longo de 24 horas, com crescimento de demanda no período de um temporal e redução posterior. Os valores são parâmetros do exercício de modelagem e não representam uma coleta real do SP156 ou de sensores.

---

## 📋 A Ficha da CitizenTech (Modelagem Matemática)

* **Nome da CitizenTech:** ZelaSP
* **Cidade e Bairros de Referência:** São Paulo — SP (**Jabaquara, Vila Mariana, Saúde, Bela Vista, Mooca e Vila Mascote**).
* **Cidadão Beneficiado:** Moradores, pedestres e comerciantes expostos a fios soltos/energizados, bueiros abertos, buracos e descarte de entulho após temporais.
* **Problema em uma Frase:** O volume de ocorrências e chamados duplicados sobrecarrega a triagem urbana pós-temporal, dificultando a identificação de cenários críticos sem apoio quantitativo.
* **Como a Matemática Resolve:** Ajusta um modelo cúbico $q(t)$ à série simulada de 24h, adota a demanda física não negativa $\text{taxa\_operacional}(t) = \max(0, q(t))$ para integrais e simulações de capacidade, analisa pontos críticos via derivadas ($q'(t)$, $q''(t)$) e explora um estudo didático de antecipação de demanda (GPCT).
* **Formulações Comuns do Projeto:**
  * **Arquitetura:** Web com MockAPI e ViaCEP; CLI Python com JSON; estudo matemático independente; integração entre módulos e IoT prevista na evolução.
  * **Tempo de relato:** Meta de registro em até 15 segundos, a validar com testes de usabilidade.
  * **Duplicidade atual:** Apoio manual a ocorrências existentes para incentivar a redução de relatos repetidos.
  * **Meta de duplicidade:** Meta futura de reduzir em 45% a parcela de chamados duplicados.
  * **Resultado matemático:** Redução simulada de 38,5% do excedente sobre a base já deduplicada, após reforço de capacidade, nas hipóteses do exercício.
  * **Foto e localização:** Funcionalidade futura: foto como evidência e apoio à localização da ocorrência; seleção demonstrativa na versão atual.
* **ODS Conectados:** ODS 11 (Cidades e Comunidades Sustentáveis) e ODS 9 (Indústria, Inovação e Infraestrutura).

---

## 📁 Arquivos desta Entrega

```text
zelasp-math/
├── DPS_ZelaSP_Modelagem_Matematica.py   # Script Python com simulação, cálculo e geração de gráficos
├── relatorio_tecnico_dps_zelasp.pdf     # Relatório técnico em PDF (com fórmulas e gráficos)
├── relatorio_tecnico_dps_zelasp.md      # Relatório técnico em Markdown
├── imagens/                             # Gráficos da simulação em alta resolução
├── prompts.md                           # Documentação ética do uso de IA
└── README.md                            # Documentação geral da entrega de DPS
```

---

## 🚀 Como Executar o Código Python (`.py`)

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
   O script carrega a série sintética de 24h, executa o ajuste polinomial, calcula $\text{taxa\_operacional}(t) = \max(0, q(t))$, derivadas, fila pendente discreta, integrais definidas e os cenários de volume excedente acumulado, regenerando os 3 gráficos em `imagens/`.

---

## 📊 Principais Resultados da Simulação

* **Série Simulada (24 faixas horárias):** Soma de $517\text{ relatos}$, com menor demanda na madrugada ($2\text{ relatos/h}$) e pico de **$62\text{ relatos/h}$ às 14h30** ($t = 14{,}5\text{ h}$).
* **Ajuste Cúbico Algébrico ($q(t)$):** $q(t) = -0{,}02924\,t^3 + 0{,}73439\,t^2 - 1{,}59152\,t + 0{,}66653$ ($R^2 = 0{,}7721$, $\text{RMSE} = 9{,}08\text{ relatos/h}$).
* **Máximo Contínuo do Ajuste ($q'(t) = 0$):** $t_1 = 15{,}58\text{ h}$ ($q(15{,}58) \approx 43{,}55\text{ relatos/h}$, $q''(15{,}58) = -1{,}2645 < 0$), subestimando o pico da série ($62\text{ relatos/h}$) em cerca de **$29{,}76\%$**.
* **Integral Operacional Principal:** $\int_0^{24} \max(0, q(t))\,dt \approx \mathbf{527{,}69\text{ relatos}}$ (diferença de aproximadamente **$2{,}07\%$** em relação à soma simulada de $517$; a integral algébrica pura $\int_0^{24} q(t)\,dt = 516{,}36$ compensa trechos negativos do polinômio e não é adotada como total operacional).
* **Cenários de Volume Excedente Acumulado ($S = 35\text{ atend./h}$ como hipótese):**
  * Fator $1{,}40$: $192{,}70$ (referência da simulação)
  * Meta $-45\%$ da parcela duplicada (fator $1{,}22$): $119{,}69$ ($-37{,}9\%$ frente a $192{,}70$)
  * Base deduplicada (fator $1{,}00$): $42{,}41$ ($-78{,}0\%$ frente a $192{,}70$)
  * Base deduplicada + reforço no gatilho GPCT ($+4{,}85\text{ atend./h}$): **$26{,}08$** (**$-38{,}5\%$ frente a $42{,}41$**)
