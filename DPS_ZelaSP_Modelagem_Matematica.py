"""Differentiated Problem Solving (DPS) — Global Solution 2026.2 · FIAP.

Do Dado à Decisão: Modelagem Matemática da Zeladoria Urbana Pós-Temporal.
CitizenTech: ZelaSP — Zeladoria Cidadã Inteligente (São Paulo — SP).

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

CAPACIDADE_EQUIPES_HORA = 35.0
FATOR_DUPLICIDADE_SP156 = 1.40
LIMIAR_GPCT_TAXA = 30.0
META_REDUCAO_DUPLICIDADE = 0.45


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


def calcular_backlog_continuo(
    func_taxa,
    capacidade_fn,
    a: float = 0.0,
    b: float = 24.0,
) -> float:
    """Calcula a área acumulada acima da capacidade operacional no intervalo [a, b]."""
    grid = np.linspace(a, b, 2401)
    excedente = np.maximum(0.0, func_taxa(grid) - capacidade_fn(grid))
    return float(np.trapezoid(excedente, grid))


def gerar_graficos(
    pasta_imagens: str,
    df: pd.DataFrame,
    p2: np.poly1d,
    q: np.poly1d,
    r2_p2: float,
    r2_q: float,
    integral_0_24: float,
) -> list[str]:
    """Gera e salva os três gráficos oficiais do relatório em alta resolução."""
    os.makedirs(pasta_imagens, exist_ok=True)
    t_dados = df["tempo_h"].values
    y_dados = df["taxa_relatos_h"].values
    t_continuo = np.linspace(0.5, 23.5, 300)

    caminhos = []

    # Gráfico 1: Dispersão exploratória e janela crítica
    fig1, ax1 = plt.subplots(figsize=(9.5, 4.8))
    ax1.scatter(
        t_dados,
        y_dados,
        color="#21918c",
        s=70,
        edgecolor="#3b528b",
        linewidth=1.2,
        zorder=3,
        label="Dados observados (horários)",
    )
    ax1.plot(
        t_dados,
        y_dados,
        color="#3b528b",
        linestyle="--",
        linewidth=1.2,
        alpha=0.65,
        label="Tendência empírica",
    )
    ax1.axvspan(
        12,
        17,
        color="#fde725",
        alpha=0.18,
        label="Janela crítica do temporal (12h–17h)",
    )
    ax1.set_title(
        "Evolução Temporal da Taxa de Relatos de Zeladoria Urbana — São Paulo (24h)",
        pad=12,
    )
    ax1.set_xlabel("Hora do dia t (h)")
    ax1.set_ylabel("Taxa de novos relatos (relatos/h)")
    ax1.set_xticks(np.arange(0, 25, 2))
    ax1.set_ylim(-2, 70)
    ax1.legend(loc="upper left")
    plt.tight_layout()
    caminho1 = os.path.join(pasta_imagens, "grafico1_dispersao.png")
    fig1.savefig(caminho1, dpi=150)
    plt.close(fig1)
    caminhos.append(caminho1)

    # Gráfico 2: Comparação entre ajuste quadrático e cúbico com R² reais
    fig2, ax2 = plt.subplots(figsize=(9.5, 5.0))
    ax2.scatter(
        t_dados,
        y_dados,
        color="#440154",
        s=65,
        zorder=4,
        label="Registros observados",
    )
    ax2.plot(
        t_continuo,
        p2(t_continuo),
        color="#d99a00",
        linestyle=":",
        linewidth=2.3,
        label=f"Ajuste Quadrático p\u2082(t) [R\u00b2={r2_p2:.3f}]",
    )
    ax2.plot(
        t_continuo,
        q(t_continuo),
        color="#21918c",
        linestyle="-",
        linewidth=2.5,
        label=f"Ajuste Cúbico q(t) [R\u00b2={r2_q:.3f}]",
    )
    ax2.set_title(
        "Comparação dos Modelos de Regressão Polinomial para Demanda de Zeladoria",
        pad=12,
    )
    ax2.set_xlabel("Hora do dia t (h)")
    ax2.set_ylabel("Taxa de chegada q(t) (relatos/h)")
    ax2.set_xticks(np.arange(0, 25, 2))
    ax2.set_ylim(-5, 70)
    ax2.legend(loc="upper left")
    plt.tight_layout()
    caminho2 = os.path.join(pasta_imagens, "grafico2_ajustes.png")
    fig2.savefig(caminho2, dpi=150)
    plt.close(fig2)
    caminhos.append(caminho2)

    # Gráfico 3: Integral acumulada, curva SP 156 (1,4x) e sobrecarga operacional
    fig3, ax3 = plt.subplots(figsize=(9.5, 5.0))
    q_vals = np.maximum(0.0, q(t_continuo))
    q_sp156 = FATOR_DUPLICIDADE_SP156 * q_vals

    ax3.plot(
        t_continuo,
        q_sp156,
        color="#440154",
        linestyle="--",
        linewidth=1.8,
        alpha=0.8,
        label="Demanda SP 156 sem triagem: 1,40·q(t)",
    )
    ax3.plot(
        t_continuo,
        q_vals,
        color="#21918c",
        linewidth=2.5,
        label="Taxa de chegada ZelaSP: q(t) sem duplicidade",
    )
    ax3.fill_between(
        t_continuo,
        0,
        q_vals,
        color="#21918c",
        alpha=0.22,
        label=f"Área acumulada ∫ q(t) dt = {integral_0_24:.2f} relatos",
    )
    ax3.axhline(
        CAPACIDADE_EQUIPES_HORA,
        color="#d95f02",
        linestyle="-.",
        linewidth=1.8,
        label=f"Capacidade de atendimento (S = {int(CAPACIDADE_EQUIPES_HORA)} equipes/h)",
    )
    ax3.fill_between(
        t_continuo,
        CAPACIDADE_EQUIPES_HORA,
        q_vals,
        where=(q_vals >= CAPACIDADE_EQUIPES_HORA),
        color="#e7298a",
        alpha=0.35,
        label="Backlog residual acima de S com q(t)",
    )
    ax3.set_title(
        "Curva de Fluxo de Ocorrências, Duplicidade (1,4x) e Backlog Acumulado",
        pad=12,
    )
    ax3.set_xlabel("Hora do dia t (h)")
    ax3.set_ylabel("Taxa de fluxo (chamados/h)")
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
    """Executa toda a pipeline matemática (estatística, ajuste, derivadas, limites, integrais e GPCT)."""
    fonte_ativa = configurar_estilo_visual()
    df = carregar_e_validar_dados()

    t_dados = df["tempo_h"].values
    y_dados = df["taxa_relatos_h"].values

    print("=" * 72)
    print("ZELASP — MODELAGEM MATEMÁTICA (DIFFERENTIATED PROBLEM SOLVING)")
    print(f"Fonte gráfica ativa: {fonte_ativa}")
    print("=" * 72)

    # 1. Estatística Descritiva e Taxa Média de Variação
    total_observado = float(df["taxa_relatos_h"].sum())
    media_horaria = float(df["taxa_relatos_h"].mean())
    idx_max = df["taxa_relatos_h"].idxmax()
    idx_min = df["taxa_relatos_h"].idxmin()

    y_9h5 = float(df.loc[df["tempo_h"] == 9.5, "taxa_relatos_h"].iloc[0])
    y_14h5 = float(df.loc[df["tempo_h"] == 14.5, "taxa_relatos_h"].iloc[0])
    taxa_media_var = (y_14h5 - y_9h5) / (14.5 - 9.5)

    print("\n[1] ESTATÍSTICA DESCRITIVA (24h)")
    print(f"Total observado no dia:     {total_observado:.0f} relatos")
    print(f"Taxa média horária:         {media_horaria:.2f} relatos/h")
    print(
        f"Pico observado:             {df.loc[idx_max, 'taxa_relatos_h']} relatos/h "
        f"em t = {df.loc[idx_max, 'tempo_h']:.1f} h ({df.loc[idx_max, 'bairro_critico']})"
    )
    print(
        f"Menor demanda observada:    {df.loc[idx_min, 'taxa_relatos_h']} relatos/h "
        f"em t = {df.loc[idx_min, 'tempo_h']:.1f} h"
    )
    print(f"Taxa média (9,5h -> 14,5h): +{taxa_media_var:.2f} relatos/h²")

    # 2. Ajuste por Mínimos Quadrados
    coef_p2 = np.polyfit(t_dados, y_dados, deg=2)
    coef_p3 = np.polyfit(t_dados, y_dados, deg=3)
    p2 = np.poly1d(coef_p2)
    q = np.poly1d(coef_p3)

    rmse_p2, r2_p2 = calcular_metricas(y_dados, p2(t_dados))
    rmse_q, r2_q = calcular_metricas(y_dados, q(t_dados))

    print("\n[2] AJUSTE DE CURVAS POR MÍNIMOS QUADRADOS")
    print(
        f"Quadrático p2(t) = {coef_p2[0]:.5f}*t² + {coef_p2[1]:.5f}*t + ({coef_p2[2]:.5f}) "
        f"| R² = {r2_p2:.4f} | RMSE = {rmse_p2:.4f}"
    )
    print(
        f"Cúbico     q(t)  = {coef_p3[0]:.5f}*t³ + {coef_p3[1]:.5f}*t² + "
        f"({coef_p3[2]:.5f})*t + ({coef_p3[3]:.5f}) "
        f"| R² = {r2_q:.4f} | RMSE = {rmse_q:.4f}"
    )

    # 3. Derivadas, Bhaskara e Otimização
    dq = q.deriv()
    d2q = q.deriv(2)
    a_b, b_b, c_b = dq.coef
    discriminante = b_b**2 - 4 * a_b * c_b
    raiz_delta = math.sqrt(discriminante)
    t_pico = (-b_b - raiz_delta) / (2 * a_b)
    t_vale = (-b_b + raiz_delta) / (2 * a_b)

    print("\n[3] DERIVADAS, PONTOS CRÍTICOS E TAXAS INSTANTÂNEAS")
    print(f"q'(t)  = {a_b:.5f}*t² + {b_b:.5f}*t + ({c_b:.5f})")
    print(f"q''(t) = {d2q.coef[0]:.5f}*t + ({d2q.coef[1]:.5f})")
    print(f"Delta de Bhaskara = {discriminante:.5f} | sqrt(Delta) = {raiz_delta:.5f}")
    print(
        f"Máximo Local: t1 = {t_pico:.4f} h | q(t1) = {q(t_pico):.2f} relatos/h | "
        f"q''(t1) = {d2q(t_pico):.4f} < 0"
    )
    print(
        f"Mínimo Local: t2 = {t_vale:.4f} h | q(t2) = {q(t_vale):.2f} relatos/h | "
        f"q''(t2) = {d2q(t_vale):+.4f} > 0"
    )
    for rotulo, instante in [
        ("4,0 h (Manhã)", 4.0),
        (f"{t_pico:.2f} h (Pico)", t_pico),
        ("18,0 h (Anoitecer)", 18.0),
    ]:
        print(f"  Taxa instantânea em t = {rotulo}: q' = {dq(instante):+.4f} relatos/h²")

    # 4. Limites e Dinâmica de Filas
    pico_sp156_continuo = FATOR_DUPLICIDADE_SP156 * q(t_pico)
    pico_sp156_discreto = FATOR_DUPLICIDADE_SP156 * float(df.loc[idx_max, "taxa_relatos_h"])
    fila_sp156 = 0.0
    fila_zelasp = 0.0
    for valor in y_dados:
        fila_sp156 = max(0.0, fila_sp156 + FATOR_DUPLICIDADE_SP156 * valor - CAPACIDADE_EQUIPES_HORA)
        fila_zelasp = max(0.0, fila_zelasp + valor - CAPACIDADE_EQUIPES_HORA)

    print("\n[4] LIMITES E SATURAÇÃO OPERACIONAL (S = 35 equipes/h)")
    print(f"Limite contínuo no pico q(t1):       {q(t_pico):.2f} relatos/h")
    print(
        f"Pico inflado SP 156 (1,40x):         {pico_sp156_continuo:.2f} chamados/h "
        f"(discreto: {pico_sp156_discreto:.1f} chamados/h)"
    )
    print(f"Saldo de fila às 24h (SP 156 1,4x):  {fila_sp156:.1f} chamados represados")
    print(f"Saldo de fila às 24h (ZelaSP limpo): {fila_zelasp:.1f} chamados represados")

    # 5. Cálculo Integral e Regra dos Trapézios
    q_primitiva = np.polyint(q)
    integral_05_235, _ = quad(q, 0.5, 23.5)
    integral_0_24, _ = quad(q, 0.0, 24.0)
    integral_trapz = calcular_trapezios(t_dados, y_dados)
    erro_abs = abs(integral_0_24 - total_observado)
    erro_rel = (erro_abs / total_observado) * 100.0
    erro_trapz = (abs(integral_trapz - total_observado) / total_observado) * 100.0

    print("\n[5] INTEGRAIS DEFINIDAS E PRIMITIVA Q(t)")
    print(
        f"Q(t) = {q_primitiva.coef[0]:.6f}*t⁴ + {q_primitiva.coef[1]:.6f}*t³ + "
        f"({q_primitiva.coef[2]:.6f})*t² + {q_primitiva.coef[3]:.6f}*t + C"
    )
    print(
        f"Q(23,5) = {q_primitiva(23.5):.2f} | Q(0,5) = {q_primitiva(0.5):.2f} | "
        f"Integral [0,5; 23,5] = {integral_05_235:.2f} relatos"
    )
    print(
        f"Q(24,0) = {q_primitiva(24.0):.2f} | Q(0,0) = {q_primitiva(0.0):.2f} | "
        f"Integral [0; 24]      = {integral_0_24:.2f} relatos"
    )
    print(
        f"Erro absoluto vs total real ({total_observado:.0f}): {erro_abs:.2f} relatos "
        f"(Erro relativo = {erro_rel:.2f}%)"
    )
    print(f"Regra dos trapézios: {integral_trapz:.2f} relatos (erro = {erro_trapz:.2f}%)")

    # 6. Decisão GPCT e Simulação de Redução de Backlog
    t_grid = np.linspace(0.0, 24.0, 2401)
    mask_gpct = (q(t_grid) >= LIMIAR_GPCT_TAXA) & (dq(t_grid) > 0.0)
    t_inicio_gpct = float(t_grid[mask_gpct][0])
    antecipacao_h = t_pico - t_inicio_gpct

    backlog_sp156 = calcular_backlog_continuo(
        lambda x: FATOR_DUPLICIDADE_SP156 * q(x),
        lambda x: np.full_like(x, CAPACIDADE_EQUIPES_HORA),
    )
    # Meta realista de redução de duplicidade (-45% da parcela repetida) + efeito combinado GPCT
    fator_meta = 1.0 + (FATOR_DUPLICIDADE_SP156 - 1.0) * (1.0 - META_REDUCAO_DUPLICIDADE)
    backlog_meta = calcular_backlog_continuo(
        lambda x: fator_meta * q(x),
        lambda x: np.full_like(x, CAPACIDADE_EQUIPES_HORA),
    )
    reducao_meta_pct = (1.0 - backlog_meta / backlog_sp156) * 100.0

    # Reforço operacional GPCT sobre a base já deduplicada q(t) (+4,85 equipes/h na janela de disparo)
    backlog_base_q = calcular_backlog_continuo(
        q,
        lambda x: np.full_like(x, CAPACIDADE_EQUIPES_HORA),
    )
    backlog_gpct_q = calcular_backlog_continuo(
        q,
        lambda x: np.where(
            (q(x) >= LIMIAR_GPCT_TAXA) & (dq(x) > 0.0),
            CAPACIDADE_EQUIPES_HORA + 4.85,
            CAPACIDADE_EQUIPES_HORA,
        ),
    )
    reducao_gpct_pct = (1.0 - backlog_gpct_q / backlog_base_q) * 100.0
    reducao_total_dedup_pct = (1.0 - backlog_base_q / backlog_sp156) * 100.0

    print("\n[6] GATILHO PREDITIVO DE CONTINGÊNCIA TERRITORIAL (GPCT)")
    print(
        f"Início do alerta GPCT (q(t) >= 30 e q'(t) > 0): t = {t_inicio_gpct:.2f} h "
        f"(antecipa o pico contínuo em {antecipacao_h:.2f} h; >= 2h antes do pico observado)"
    )
    print(f"Backlog contínuo SP 156 (1,40x):               {backlog_sp156:.2f} chamados")
    print(
        f"Backlog com meta -45% duplicidade ({fator_meta:.2f}x):  {backlog_meta:.2f} chamados "
        f"(-{reducao_meta_pct:.1f}%)"
    )
    print(
        f"Backlog ZelaSP deduplicado q(t) sem reforço:   {backlog_base_q:.2f} relatos "
        f"(-{reducao_total_dedup_pct:.1f}% vs SP 156)"
    )
    print(
        f"Backlog ZelaSP q(t) + reforço GPCT (+13,9% S): {backlog_gpct_q:.2f} relatos "
        f"(-{reducao_gpct_pct:.1f}% sobre o residual)"
    )

    pasta_imagens = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imagens")
    arquivos = gerar_graficos(
        pasta_imagens=pasta_imagens,
        df=df,
        p2=p2,
        q=q,
        r2_p2=r2_p2,
        r2_q=r2_q,
        integral_0_24=integral_0_24,
    )
    print("\n[7] GRÁFICOS GERADOS EM imagens/:")
    for arq in arquivos:
        print(f"  - {arq}")


if __name__ == "__main__":
    main()
