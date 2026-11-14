"""Differentiated Problem Solving (DPS) — Global Solution 2026.2 · FIAP.

Simulação Acadêmica: Modelagem Matemática da Zeladoria Urbana Pós-Temporal.
CitizenTech: ZelaSP — Zeladoria Cidadã Inteligente (São Paulo — SP).

Nota de Escopo e Dados:
    Este trabalho utiliza uma série de dados simulados para fins acadêmicos.
    O cenário representa a variação horária de relatos de zeladoria ao longo
    de 24 horas, com crescimento de demanda no período de um temporal e
    redução posterior. Os valores são parâmetros do exercício de modelagem
    e não representam uma coleta real do SP156 ou de sensores.

Disciplina: Differentiated Problem Solving (Prof. Jones Egydio)
Curso: Engenharia de Software — 1º Ano (Campus Paulista/Lins)

Integrantes:
    - Gustavo Rezende Louro — RM570708
    - João Pedro Lagonegro Bosco e Silva — RM569444
    - João Pedro Maschion da Cruz Sá — RM570509
    - Lucas Henrique Alves da Silva — RM572216

ODS Conectados:
    - ODS 11 (Cidades e Comunidades Sustentáveis)
    - ODS 9 (Indústria, Inovação e Infraestrutura)
"""

from io import StringIO
import math
import os
import tempfile

# Evita falha de escrita em cache caso o diretório padrão de configuração esteja restrito.
os.environ.setdefault(
    "MPLCONFIGDIR",
    os.path.join(tempfile.gettempdir(), "matplotlib_zelasp"),
)

import matplotlib

matplotlib.use("Agg")

from matplotlib import font_manager
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.integrate import quad
import seaborn as sns


DADOS_ZELASP_CSV = """tempo_h,taxa_relatos_h,bairro_critico,apoios_comunitarios
0.5,4,Mooca,1
1.5,3,Bela Vista,0
2.5,2,Vila Mascote,0
3.5,2,Saude,0
4.5,3,Jabaquara,1
5.5,5,Vila Mariana,2
6.5,8,Bela Vista,3
7.5,12,Mooca,4
8.5,16,Jabaquara,6
9.5,21,Vila Mariana,9
10.5,28,Saude,14
11.5,38,Vila Mascote,18
12.5,49,Jabaquara,24
13.5,58,Vila Mariana,31
14.5,62,Bela Vista,35
15.5,55,Saude,28
16.5,42,Mooca,21
17.5,31,Vila Mascote,15
18.5,24,Jabaquara,11
19.5,18,Vila Mariana,8
20.5,14,Saude,6
21.5,10,Bela Vista,4
22.5,7,Mooca,2
23.5,5,Jabaquara,1
"""

# Hipóteses acadêmicas adotadas para o exercício de modelagem (não são medições reais)
CAPACIDADE_EQUIPES_HORA = 35.0
FATOR_DUPLICIDADE_CENARIO = 1.40
LIMIAR_GPCT_TAXA = 30.0
REFORCO_GPCT_CAPACIDADE = 4.85
META_REDUCAO_DUPLICIDADE = 0.45

TEXTO_ESCOPO_SIMULACAO = (
    "Este trabalho utiliza uma série de dados simulados para fins acadêmicos. "
    "O cenário representa a variação horária de relatos de zeladoria ao longo "
    "de 24 horas, com crescimento de demanda no período de um temporal e redução "
    "posterior. Os valores são parâmetros do exercício de modelagem e não "
    "representam uma coleta real do SP156 ou de sensores."
)


def configurar_estilo_visual() -> str:
    """Configura paleta viridis e tipografia serifada acadêmica nos gráficos."""
    fontes_disponiveis = {f.name for f in font_manager.fontManager.ttflist}
    fontes_preferidas = [
        "Latin Modern Roman",
        "CMU Serif",
        "Georgia",
        "DejaVu Serif",
    ]
    fonte_ativa = next(
        (f for f in fontes_preferidas if f in fontes_disponiveis),
        "DejaVu Serif",
    )

    sns.set_theme(style="whitegrid", palette="viridis", font=fonte_ativa)
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": [fonte_ativa] + fontes_preferidas,
            "mathtext.fontset": "cm",
            "text.usetex": False,
            "figure.figsize": (9.5, 5.2),
            "figure.dpi": 150,
            "axes.titlesize": 13.5,
            "axes.labelsize": 11.5,
            "xtick.labelsize": 10.5,
            "ytick.labelsize": 10.5,
            "legend.fontsize": 10,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "grid.alpha": 0.22,
            "grid.linewidth": 0.7,
        }
    )
    pd.set_option("display.float_format", lambda v: f"{v:.4f}")
    np.set_printoptions(suppress=True, precision=4)
    return fonte_ativa


def carregar_e_validar_dados() -> pd.DataFrame:
    """Carrega a série temporal embutida de 24h e valida invariantes de domínio."""
    df = pd.read_csv(StringIO(DADOS_ZELASP_CSV.strip()))
    assert len(df) == 24, "A base deve conter exatamente 24 faixas horárias."
    assert (df["taxa_relatos_h"] >= 0).all(), "Taxa de relatos não pode ser negativa."
    assert df["tempo_h"].is_monotonic_increasing, "Ordenação temporal incorreta."
    return df


def calcular_metricas(y_real: np.ndarray, y_pred: np.ndarray) -> tuple[float, float]:
    """Calcula RMSE e coeficiente de determinação R² para um ajuste."""
    residuos = y_real - y_pred
    rmse = float(np.sqrt(np.mean(residuos**2)))
    ss_tot = float(np.sum((y_real - np.mean(y_real)) ** 2))
    ss_res = float(np.sum(residuos**2))
    r2 = 1.0 - (ss_res / ss_tot)
    return rmse, r2


def calcular_trapezios(t_dados: np.ndarray, y_dados: np.ndarray) -> float:
    """Integra numericamente pela regra dos trapézios com compatibilidade NumPy 1.x/2.x."""
    if hasattr(np, "trapezoid"):
        return float(np.trapezoid(y_dados, t_dados))
    if hasattr(np, "trapz"):
        return float(np.trapz(y_dados, t_dados))
    from scipy.integrate import trapezoid

    return float(trapezoid(y_dados, t_dados))


def criar_taxa_operacional(q: np.poly1d):
    """Retorna taxa_operacional(t) = max(0, q(t)) para demanda física não negativa."""
    def taxa_operacional(t):
        return np.maximum(0.0, q(t))

    return taxa_operacional


def calcular_volume_excedente_continuo(
    func_taxa,
    capacidade_fn,
    a: float = 0.0,
    b: float = 24.0,
) -> float:
    """Calcula o volume excedente acumulado acima da capacidade no intervalo [a, b]."""
    grid = np.linspace(a, b, 2401)
    excedente = np.maximum(0.0, func_taxa(grid) - capacidade_fn(grid))
    return float(np.trapezoid(excedente, grid))


def gerar_graficos(
    pasta_imagens: str,
    df: pd.DataFrame,
    p2: np.poly1d,
    q: np.poly1d,
    taxa_operacional,
    r2_p2: float,
    r2_q: float,
    integral_operacional_0_24: float,
    excedente_dedup: float,
) -> list[str]:
    """Gera e salva os três gráficos da simulação acadêmica em alta resolução."""
    os.makedirs(pasta_imagens, exist_ok=True)
    t_dados = df["tempo_h"].values
    y_dados = df["taxa_relatos_h"].values
    t_continuo = np.linspace(0.0, 24.0, 481)

    caminhos = []

    # Gráfico 1: Série simulada (24h) e janela crítica do cenário
    fig1, ax1 = plt.subplots(figsize=(9.5, 4.8))
    ax1.scatter(
        t_dados,
        y_dados,
        color="#21918c",
        s=70,
        edgecolor="#3b528b",
        linewidth=1.2,
        zorder=3,
        label="Série simulada (24 faixas horárias)",
    )
    ax1.plot(
        t_dados,
        y_dados,
        color="#3b528b",
        linestyle="--",
        linewidth=1.2,
        alpha=0.65,
        label="Perfil da série sintética",
    )
    ax1.axvspan(
        12,
        17,
        color="#fde725",
        alpha=0.18,
        label="Janela de pico do temporal simulado (12h–17h)",
    )
    ax1.set_title(
        "Simulação Acadêmica: Taxa Horária de Relatos de Zeladoria em 24h",
        pad=12,
    )
    ax1.set_xlabel("Tempo t (horas)")
    ax1.set_ylabel("Taxa de relatos simulada (relatos/h)")
    ax1.set_xticks(np.arange(0, 25, 2))
    ax1.set_ylim(-2, 70)
    ax1.legend(loc="upper left")
    plt.tight_layout()
    caminho1 = os.path.join(pasta_imagens, "grafico1_dispersao.png")
    fig1.savefig(caminho1, dpi=150)
    plt.close(fig1)
    caminhos.append(caminho1)

    # Gráfico 2: Ajustes polinomiais e taxa operacional não negativa
    fig2, ax2 = plt.subplots(figsize=(9.5, 5.0))
    ax2.scatter(
        t_dados,
        y_dados,
        color="#440154",
        s=65,
        zorder=4,
        label="Pontos da série simulada",
    )
    ax2.plot(
        t_continuo,
        p2(t_continuo),
        color="#d99a00",
        linestyle=":",
        linewidth=2.0,
        label=f"Ajuste Quadrático p\u2082(t) [R\u00b2={r2_p2:.3f}]",
    )
    ax2.plot(
        t_continuo,
        q(t_continuo),
        color="#3b528b",
        linestyle="--",
        linewidth=1.6,
        alpha=0.85,
        label=f"Ajuste Cúbico q(t) [R\u00b2={r2_q:.3f}]",
    )
    ax2.plot(
        t_continuo,
        taxa_operacional(t_continuo),
        color="#21918c",
        linestyle="-",
        linewidth=2.6,
        label="Taxa operacional = max(0, q(t))",
    )
    ax2.axhline(0, color="#64748b", linewidth=0.9, alpha=0.6)
    ax2.set_title(
        "Regressão Polinomial sobre Série Simulada e Taxa Operacional Não Negativa",
        pad=12,
    )
    ax2.set_xlabel("Tempo t (horas)")
    ax2.set_ylabel("Taxa de relatos (relatos/h)")
    ax2.set_xticks(np.arange(0, 25, 2))
    ax2.set_ylim(-22, 70)
    ax2.legend(loc="upper left")
    plt.tight_layout()
    caminho2 = os.path.join(pasta_imagens, "grafico2_ajustes.png")
    fig2.savefig(caminho2, dpi=150)
    plt.close(fig2)
    caminhos.append(caminho2)

    # Gráfico 3: Demanda não negativa, fator 1,40 e volume excedente acumulado acima de S
    fig3, ax3 = plt.subplots(figsize=(9.5, 5.0))
    op_vals = taxa_operacional(t_continuo)
    op_inflada = FATOR_DUPLICIDADE_CENARIO * op_vals

    ax3.plot(
        t_continuo,
        op_inflada,
        color="#440154",
        linestyle="--",
        linewidth=1.8,
        alpha=0.85,
        label="Cenário com duplicidade (1,40 · taxa_operacional(t))",
    )
    ax3.plot(
        t_continuo,
        op_vals,
        color="#21918c",
        linewidth=2.5,
        label="Base deduplicada: taxa_operacional(t) = max(0, q(t))",
    )
    ax3.fill_between(
        t_continuo,
        0,
        op_vals,
        color="#21918c",
        alpha=0.22,
        label=f"Integral operacional ∫ max(0, q(t)) dt = {integral_operacional_0_24:.2f} relatos",
    )
    ax3.axhline(
        CAPACIDADE_EQUIPES_HORA,
        color="#d95f02",
        linestyle="-.",
        linewidth=1.8,
        label=f"Capacidade hipotética (S = {int(CAPACIDADE_EQUIPES_HORA)} atendimentos/h)",
    )
    ax3.fill_between(
        t_continuo,
        CAPACIDADE_EQUIPES_HORA,
        op_vals,
        where=(op_vals >= CAPACIDADE_EQUIPES_HORA),
        color="#e7298a",
        alpha=0.35,
        label=f"Volume excedente acumulado acima de S ({excedente_dedup:.2f} relatos)",
    )
    ax3.set_title(
        "Simulação: Taxa Operacional, Fator 1,40 e Volume Excedente Acumulado",
        pad=12,
    )
    ax3.set_xlabel("Tempo t (horas)")
    ax3.set_ylabel("Taxa de fluxo simulada (chamados/h)")
    ax3.set_xticks(np.arange(0, 25, 2))
    ax3.set_ylim(0, 70)
    ax3.legend(loc="upper left")
    plt.tight_layout()
    caminho3 = os.path.join(pasta_imagens, "grafico3_integral.png")
    fig3.savefig(caminho3, dpi=150)
    plt.close(fig3)
    caminhos.append(caminho3)

    return caminhos


def main() -> None:
    """Executa a simulação acadêmica (estatística, ajuste, derivadas, limites, integrais e GPCT)."""
    fonte_ativa = configurar_estilo_visual()
    df = carregar_e_validar_dados()

    t_dados = df["tempo_h"].values
    y_dados = df["taxa_relatos_h"].values

    print("=" * 72)
    print("ZELASP — SIMULAÇÃO ACADÊMICA (DIFFERENTIATED PROBLEM SOLVING)")
    print(f"Escopo: {TEXTO_ESCOPO_SIMULACAO}")
    print(f"Fonte gráfica ativa: {fonte_ativa}")
    print("=" * 72)

    # 1. Estatística Descritiva da Série Simulada
    total_simulado = float(df["taxa_relatos_h"].sum())
    media_horaria = float(df["taxa_relatos_h"].mean())
    idx_max = df["taxa_relatos_h"].idxmax()
    idx_min = df["taxa_relatos_h"].idxmin()

    y_9h5 = float(df.loc[df["tempo_h"] == 9.5, "taxa_relatos_h"].iloc[0])
    y_14h5 = float(df.loc[df["tempo_h"] == 14.5, "taxa_relatos_h"].iloc[0])
    taxa_media_var = (y_14h5 - y_9h5) / (14.5 - 9.5)

    print("\n[1] ESTATÍSTICA DESCRITIVA DA SÉRIE SIMULADA (24h)")
    print(f"Soma da série simulada (24h): {total_simulado:.0f} relatos")
    print(f"Taxa média horária:           {media_horaria:.2f} relatos/h")
    print(
        f"Pico da série simulada:       {df.loc[idx_max, 'taxa_relatos_h']} relatos/h "
        f"em t = {df.loc[idx_max, 'tempo_h']:.1f} h (contexto: {df.loc[idx_max, 'bairro_critico']})"
    )
    print(
        f"Menor taxa da série:          {df.loc[idx_min, 'taxa_relatos_h']} relatos/h "
        f"em t = {df.loc[idx_min, 'tempo_h']:.1f} h"
    )
    print(f"Taxa média (9,5h -> 14,5h):   +{taxa_media_var:.2f} relatos/h²")

    # 2. Ajuste por Mínimos Quadrados + Taxa Operacional Não Negativa
    coef_p2 = np.polyfit(t_dados, y_dados, deg=2)
    coef_p3 = np.polyfit(t_dados, y_dados, deg=3)
    p2 = np.poly1d(coef_p2)
    q = np.poly1d(coef_p3)
    taxa_operacional = criar_taxa_operacional(q)
    raizes_q = sorted(float(r.real) for r in np.roots(q.coef) if abs(r.imag) < 1e-9)

    rmse_p2, r2_p2 = calcular_metricas(y_dados, p2(t_dados))
    rmse_q, r2_q = calcular_metricas(y_dados, q(t_dados))

    print("\n[2] AJUSTE POLINOMIAL E TAXA OPERACIONAL NÃO NEGATIVA")
    print(
        f"Quadrático p2(t) = {coef_p2[0]:.5f}*t² + {coef_p2[1]:.5f}*t + ({coef_p2[2]:.5f}) "
        f"| R² = {r2_p2:.4f} | RMSE = {rmse_p2:.4f}"
    )
    print(
        f"Cúbico     q(t)  = {coef_p3[0]:.5f}*t³ + {coef_p3[1]:.5f}*t² + "
        f"({coef_p3[2]:.5f})*t + ({coef_p3[3]:.5f}) "
        f"| R² = {r2_q:.4f} | RMSE = {rmse_q:.4f}"
    )
    print(
        "Raízes de q(t) em [0, 24] (transições da taxa_operacional(t) = max(0, q(t))): "
        + ", ".join(f"{r:.4f} h" for r in raizes_q)
    )

    # 3. Derivadas e Pontos Críticos do Polinômio Cúbico q(t)
    dq = q.deriv()
    d2q = q.deriv(2)
    a_b, b_b, c_b = dq.coef
    discriminante = b_b**2 - 4 * a_b * c_b
    raiz_delta = math.sqrt(discriminante)
    t_pico = (-b_b - raiz_delta) / (2 * a_b)
    t_vale = (-b_b + raiz_delta) / (2 * a_b)
    subestimacao_pico_pct = (1.0 - float(q(t_pico)) / float(df.loc[idx_max, "taxa_relatos_h"])) * 100.0

    print("\n[3] ESTUDO ALGÉBRICO DE q(t) — DERIVADAS E PONTOS CRÍTICOS")
    print(f"q'(t)  = {a_b:.5f}*t² + {b_b:.5f}*t + ({c_b:.5f})")
    print(f"q''(t) = {d2q.coef[0]:.5f}*t + ({d2q.coef[1]:.5f})")
    print(f"Delta de Bhaskara = {discriminante:.5f} | sqrt(Delta) = {raiz_delta:.5f}")
    print(
        f"Máximo Local de q(t): t1 = {t_pico:.4f} h | q(t1) = {q(t_pico):.2f} relatos/h | "
        f"q''(t1) = {d2q(t_pico):.4f} < 0"
    )
    print(
        f"Subestimação do pico ({q(t_pico):.2f} vs {df.loc[idx_max, 'taxa_relatos_h']} simulado): "
        f"{subestimacao_pico_pct:.2f}%"
    )
    print(
        f"Mínimo Local de q(t): t2 = {t_vale:.4f} h | q(t2) = {q(t_vale):.2f} relatos/h "
        "(valor negativo é limitação algébrica do ajuste; taxa_operacional = 0 nos trechos recortados)"
    )
    for rotulo, instante in [
        ("4,0 h (Manhã)", 4.0),
        (f"{t_pico:.2f} h (Pico)", t_pico),
        ("18,0 h (Anoitecer)", 18.0),
    ]:
        print(f"  Taxa instantânea de q(t) em t = {rotulo}: q' = {dq(instante):+.4f} relatos/h²")

    # 4. Limites e Dinâmica de Fila Pendente (Hipótese S = 35 atendimentos/h)
    pico_inflado_continuo = FATOR_DUPLICIDADE_CENARIO * float(taxa_operacional(t_pico))
    pico_inflado_discreto = FATOR_DUPLICIDADE_CENARIO * float(df.loc[idx_max, "taxa_relatos_h"])
    fila_pendente_140 = 0.0
    fila_pendente_dedup = 0.0
    for valor in y_dados:
        fila_pendente_140 = max(
            0.0,
            fila_pendente_140 + FATOR_DUPLICIDADE_CENARIO * valor - CAPACIDADE_EQUIPES_HORA,
        )
        fila_pendente_dedup = max(0.0, fila_pendente_dedup + valor - CAPACIDADE_EQUIPES_HORA)

    print("\n[4] LIMITES E FILA PENDENTE NA SIMULAÇÃO (HIPÓTESE S = 35 atendimentos/h)")
    print(f"Limite no pico contínuo taxa_op(t1): {taxa_operacional(t_pico):.2f} relatos/h")
    print(
        f"Pico com fator 1,40:                 {pico_inflado_continuo:.2f} chamados/h "
        f"(discreto: {pico_inflado_discreto:.1f} chamados/h)"
    )
    print(f"Fila pendente às 24h (fator 1,40):   {fila_pendente_140:.1f} chamados")
    print(f"Fila pendente às 24h (deduplicado):  {fila_pendente_dedup:.1f} chamados")

    # 5. Cálculo Integral: Taxa Operacional Principal vs. Primitiva Algébrica Q(t)
    q_primitiva = np.polyint(q)
    integral_q_0_24, _ = quad(q, 0.0, 24.0)
    integral_op_0_24, _ = quad(
        taxa_operacional,
        0.0,
        24.0,
        points=raizes_q,
    )
    integral_trapz = calcular_trapezios(t_dados, y_dados)

    diff_op_abs = abs(integral_op_0_24 - total_simulado)
    diff_op_rel = (diff_op_abs / total_simulado) * 100.0
    diff_q_rel = (abs(integral_q_0_24 - total_simulado) / total_simulado) * 100.0
    erro_trapz = (abs(integral_trapz - total_simulado) / total_simulado) * 100.0

    print("\n[5] INTEGRAIS DEFINIDAS (TAXA OPERACIONAL VS. PRIMITIVA ALGÉBRICA)")
    print(
        f"Integral operacional ∫_0^24 max(0, q(t)) dt = {integral_op_0_24:.2f} relatos "
        f"(diferença vs soma simulada {total_simulado:.0f}: {diff_op_abs:.2f} | {diff_op_rel:.2f}%)"
    )
    print(
        f"Primitiva algébrica Q(t) = {q_primitiva.coef[0]:.6f}*t⁴ + {q_primitiva.coef[1]:.6f}*t³ + "
        f"({q_primitiva.coef[2]:.6f})*t² + {q_primitiva.coef[3]:.6f}*t + C"
    )
    print(
        f"Integral algébrica pura ∫_0^24 q(t) dt     = {integral_q_0_24:.2f} relatos "
        f"(diferença nominal {diff_q_rel:.2f}% por compensar trechos negativos de q)"
    )
    print(f"Regra dos trapézios na série discreta:      {integral_trapz:.2f} relatos (dif. = {erro_trapz:.2f}%)")

    # 6. Cenários Simulados de Volume Excedente Acumulado e GPCT Didático
    t_grid = np.linspace(0.0, 24.0, 2401)
    mask_gpct = (taxa_operacional(t_grid) >= LIMIAR_GPCT_TAXA) & (dq(t_grid) > 0.0)
    t_inicio_gpct = float(t_grid[mask_gpct][0])
    antecipacao_h = t_pico - t_inicio_gpct

    excedente_140 = calcular_volume_excedente_continuo(
        lambda x: FATOR_DUPLICIDADE_CENARIO * taxa_operacional(x),
        lambda x: np.full_like(x, CAPACIDADE_EQUIPES_HORA),
    )
    fator_meta = 1.0 + (FATOR_DUPLICIDADE_CENARIO - 1.0) * (1.0 - META_REDUCAO_DUPLICIDADE)
    excedente_meta_45 = calcular_volume_excedente_continuo(
        lambda x: fator_meta * taxa_operacional(x),
        lambda x: np.full_like(x, CAPACIDADE_EQUIPES_HORA),
    )
    reducao_meta_pct = (1.0 - excedente_meta_45 / excedente_140) * 100.0

    excedente_dedup = calcular_volume_excedente_continuo(
        taxa_operacional,
        lambda x: np.full_like(x, CAPACIDADE_EQUIPES_HORA),
    )
    reducao_dedup_pct = (1.0 - excedente_dedup / excedente_140) * 100.0

    excedente_gpct = calcular_volume_excedente_continuo(
        taxa_operacional,
        lambda x: np.where(
            (taxa_operacional(x) >= LIMIAR_GPCT_TAXA) & (dq(x) > 0.0),
            CAPACIDADE_EQUIPES_HORA + REFORCO_GPCT_CAPACIDADE,
            CAPACIDADE_EQUIPES_HORA,
        ),
    )
    reducao_gpct_pct = (1.0 - excedente_gpct / excedente_dedup) * 100.0

    print("\n[6] ESTUDO DIDÁTICO DO GPCT E VOLUME EXCEDENTE ACUMULADO ACIMA DE S=35")
    print(
        f"Início do gatilho simulado (taxa_op >= 30 e q' > 0): t = {t_inicio_gpct:.2f} h "
        f"(antecipa o pico contínuo em {antecipacao_h:.2f} h)"
    )
    print(f"Volume excedente (fator 1,40, S=35):            {excedente_140:.2f} chamados [Referência]")
    print(
        f"Volume excedente (meta -45% dup., fator {fator_meta:.2f}): {excedente_meta_45:.2f} chamados "
        f"(-{reducao_meta_pct:.1f}% vs {excedente_140:.2f})"
    )
    print(
        f"Volume excedente (deduplicado, fator 1,00):     {excedente_dedup:.2f} relatos "
        f"(-{reducao_dedup_pct:.1f}% vs {excedente_140:.2f})"
    )
    print(
        f"Volume excedente (dedup. + reforço GPCT +4,85): {excedente_gpct:.2f} relatos "
        f"(-{reducao_gpct_pct:.1f}% frente a {excedente_dedup:.2f})"
    )

    pasta_imagens = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imagens")
    arquivos = gerar_graficos(
        pasta_imagens=pasta_imagens,
        df=df,
        p2=p2,
        q=q,
        taxa_operacional=taxa_operacional,
        r2_p2=r2_p2,
        r2_q=r2_q,
        integral_operacional_0_24=integral_op_0_24,
        excedente_dedup=excedente_dedup,
    )
    print("\n[7] GRÁFICOS GERADOS EM imagens/:")
    for arq in arquivos:
        print(f"  - {arq}")


if __name__ == "__main__":
    main()
