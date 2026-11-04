import argparse
import csv
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from simulador import Resultado

# Cor e marcador seguem o algoritmo, para que ele tenha a mesma identidade em todos os gráficos.
# Os tamanhos decrescentes mantêm visíveis os marcadores de curvas que coincidem em um mesmo ponto
ESTILOS: dict[str, tuple[str, str, float]] = {
    'FIFO': ('#2a78d6', 'o', 13),
    'LRU': ('#eb6834', 's', 10.5),
    'Ótimo': ('#1baf7a', '^', 9),
    'Segunda Chance': ('#eda100', 'D', 6.5),
    'LFU': ('#e87ba4', 'v', 5),
}

SUPERFICIE: str = '#fcfcfb'
TINTA: str = '#0b0b0b'
TINTA_SECUNDARIA: str = '#52514e'
GRADE: str = '#e1e0d9'
EIXO: str = '#c3c2b7'

def ler_resultados(caminho: str) -> list[Resultado]:
    with open(caminho, newline='', encoding='utf-8') as arquivo:
        return [
            Resultado(
                algoritmo=linha['algoritmo'],
                n_quadros=int(linha['n_quadros']),
                faltas=int(linha['faltas']),
                acertos=int(linha['acertos'])
            )
            for linha in csv.DictReader(arquivo)
        ]

def agrupar_por_algoritmo(dados: list[Resultado]) -> dict[str, list[Resultado]]:
    grupos: dict[str, list[Resultado]] = {}
    for resultado in dados:
        grupos.setdefault(resultado.algoritmo, []).append(resultado)

    for resultados in grupos.values():
        resultados.sort(key=lambda r: r.n_quadros)

    return grupos

def detectar_anomalia_belady(dados: list[Resultado]) -> list[tuple[str, int]]:
    anomalias: list[tuple[str, int]] = []

    for algoritmo, resultados in agrupar_por_algoritmo(dados).items():
        for anterior, atual in zip(resultados, resultados[1:]):
            if atual.n_quadros == anterior.n_quadros + 1 and atual.faltas > anterior.faltas:
                anomalias.append((algoritmo, atual.n_quadros))

    return anomalias

def plotar_faltas_por_quadros(dados: list[Resultado], saida: str) -> None:
    # Importado aqui para que a detecção da anomalia e os testes não dependam do matplotlib
    import matplotlib
    matplotlib.use('Agg')
    from matplotlib import pyplot
    from matplotlib.ticker import MaxNLocator

    figura, eixos = pyplot.subplots(figsize=(9, 5.5), facecolor=SUPERFICIE)
    eixos.set_facecolor(SUPERFICIE)

    grupos: dict[str, list[Resultado]] = agrupar_por_algoritmo(dados)
    for algoritmo, resultados in grupos.items():
        cor, marcador, tamanho = ESTILOS[algoritmo]
        eixos.plot(
            [r.n_quadros for r in resultados],
            [r.faltas for r in resultados],
            label=algoritmo,
            color=cor,
            marker=marcador,
            markersize=tamanho,
            markeredgecolor=SUPERFICIE,
            markeredgewidth=0.8,
            linewidth=1.5,
            solid_capstyle='round',
            solid_joinstyle='round',
            zorder=20 - tamanho,
        )

    anomalias: list[tuple[str, int]] = detectar_anomalia_belady(dados)
    if anomalias:
        faltas: dict[tuple[str, int], int] = {(r.algoritmo, r.n_quadros): r.faltas for r in dados}
        eixos.scatter(
            [n_quadros for _, n_quadros in anomalias],
            [faltas[anomalia] for anomalia in anomalias],
            s=360,
            facecolors='none',
            edgecolors=TINTA,
            linewidths=1,
            zorder=20,
            label='Anomalia de Belády',
        )

    eixos.set_title('Faltas de página por número de quadros', color=TINTA, loc='left', pad=34, fontweight='bold')
    eixos.set_xlabel('Número de quadros', color=TINTA_SECUNDARIA)
    eixos.set_ylabel('Faltas de página', color=TINTA_SECUNDARIA)
    eixos.set_xlim(left=0.5)
    eixos.set_ylim(bottom=0)
    eixos.xaxis.set_major_locator(MaxNLocator(integer=True, steps=[1, 2, 5, 10]))
    eixos.yaxis.set_major_locator(MaxNLocator(integer=True, steps=[1, 2, 5, 10]))
    eixos.tick_params(colors=TINTA_SECUNDARIA, length=0)
    eixos.grid(axis='y', color=GRADE, linewidth=1)
    eixos.set_axisbelow(True)

    for lado in ('top', 'right', 'left'):
        eixos.spines[lado].set_visible(False)
    eixos.spines['bottom'].set_color(EIXO)

    eixos.legend(
        loc='lower left',
        bbox_to_anchor=(0, 1),
        ncols=len(grupos) + 1,
        frameon=False,
        labelcolor=TINTA_SECUNDARIA,
        fontsize=9,
        borderaxespad=0.2,
        columnspacing=1.2,
        handlelength=2,
    )

    diretorio: str = os.path.dirname(saida)
    if diretorio:
        os.makedirs(diretorio, exist_ok=True)

    figura.savefig(saida, dpi=200, bbox_inches='tight', facecolor=SUPERFICIE)
    pyplot.close(figura)

def imprimir_anomalias(dados: list[Resultado]) -> None:
    anomalias: list[tuple[str, int]] = detectar_anomalia_belady(dados)
    com_anomalia: set[str] = {algoritmo for algoritmo, _ in anomalias}
    sem_anomalia: list[str] = [a for a in agrupar_por_algoritmo(dados) if a not in com_anomalia]

    for algoritmo, n_quadros in anomalias:
        print(f'Anomalia de Belady: {algoritmo} com {n_quadros} quadros (mais faltas que com {n_quadros - 1})')

    print(f'Sem anomalia: {", ".join(sem_anomalia) if sem_anomalia else "nenhum algoritmo"}')

def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description='Análise dos resultados do modo em lote')
    parser.add_argument('--csv', required=True, help='arquivo gerado pelo modo em lote')
    parser.add_argument('--saida', help='arquivo em que o gráfico é gravado (se omitido, apenas detecta a anomalia)')
    args = parser.parse_args(argv)

    try:
        dados: list[Resultado] = ler_resultados(args.csv)
    except (OSError, ValueError, KeyError) as erro:
        print(f'Erro: não foi possível ler {args.csv}: {erro}', file=sys.stderr)
        return 1

    imprimir_anomalias(dados)

    if args.saida:
        plotar_faltas_por_quadros(dados, args.saida)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
