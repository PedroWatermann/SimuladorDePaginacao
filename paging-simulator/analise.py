import csv
import os
import sys

# Para importar os módulos da pasta src
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from simulador import Resultado

USO: str = 'Uso: python3 analise.py --csv ARQUIVO [--saida GRAFICO.png]'

# Tamanhos decrescentes: quando duas curvas coincidem, o marcador maior continua aparecendo por baixo
MARCADORES: dict[str, tuple[str, int]] = {
    'FIFO': ('o', 13),
    'LRU': ('s', 10),
    'Ótimo': ('^', 8),
    'Segunda Chance': ('D', 6),
    'LFU': ('v', 4),
}

def ler_resultados(caminho: str) -> list[Resultado]:
    dados: list[Resultado] = []

    with open(caminho, newline='', encoding='utf-8') as arquivo:
        for linha in csv.DictReader(arquivo):
            resultado: Resultado = Resultado(
                algoritmo=linha['algoritmo'],
                n_quadros=int(linha['n_quadros']),
                faltas=int(linha['faltas']),
                acertos=int(linha['acertos'])
            )
            dados.append(resultado)

    return dados

def pegar_n_quadros(resultado: Resultado) -> int:
    return resultado.n_quadros

def agrupar_por_algoritmo(dados: list[Resultado]) -> dict[str, list[Resultado]]:
    grupos: dict[str, list[Resultado]] = {}
    for resultado in dados:
        if resultado.algoritmo not in grupos:
            grupos[resultado.algoritmo] = []
        grupos[resultado.algoritmo].append(resultado)

    for resultados in grupos.values():
        resultados.sort(key=pegar_n_quadros)

    return grupos

def detectar_anomalia_belady(dados: list[Resultado]) -> list[tuple[str, int]]:
    anomalias: list[tuple[str, int]] = []

    for algoritmo, resultados in agrupar_por_algoritmo(dados).items():
        for i in range(1, len(resultados)):
            anterior: Resultado = resultados[i - 1]
            atual: Resultado = resultados[i]
            if atual.n_quadros == anterior.n_quadros + 1 and atual.faltas > anterior.faltas:
                anomalias.append((algoritmo, atual.n_quadros))

    return anomalias

def plotar_faltas_por_quadros(dados: list[Resultado], saida: str) -> None:
    from matplotlib import pyplot

    pyplot.figure(figsize=(9, 5.5))

    grupos: dict[str, list[Resultado]] = agrupar_por_algoritmo(dados)
    for algoritmo, resultados in grupos.items():
        eixo_x: list[int] = []
        eixo_y: list[int] = []
        for r in resultados:
            eixo_x.append(r.n_quadros)
            eixo_y.append(r.faltas)

        marcador, tamanho = MARCADORES[algoritmo]
        pyplot.plot(eixo_x, eixo_y, marker=marcador, markersize=tamanho, label=algoritmo)

    anomalias: list[tuple[str, int]] = detectar_anomalia_belady(dados)
    if len(anomalias) > 0:
        anomalia_x: list[int] = []
        anomalia_y: list[int] = []
        for algoritmo, n_quadros in anomalias:
            for r in dados:
                if r.algoritmo == algoritmo and r.n_quadros == n_quadros:
                    anomalia_x.append(r.n_quadros)
                    anomalia_y.append(r.faltas)

        pyplot.scatter(anomalia_x, anomalia_y, s=300, facecolors='none', edgecolors='red', label='Anomalia de Belády')

    pyplot.title('Faltas de página por número de quadros')
    pyplot.xlabel('Número de quadros')
    pyplot.ylabel('Faltas de página')
    pyplot.grid(True)
    pyplot.legend()

    diretorio: str = os.path.dirname(saida)
    if diretorio:
        os.makedirs(diretorio, exist_ok=True)

    pyplot.savefig(saida, dpi=150)
    pyplot.close()

def imprimir_anomalias(dados: list[Resultado]) -> None:
    anomalias: list[tuple[str, int]] = detectar_anomalia_belady(dados)
    com_anomalia: list[str] = []
    for algoritmo, n_quadros in anomalias:
        print(f'Anomalia de Belady: {algoritmo} com {n_quadros} quadros (mais faltas que com {n_quadros - 1})')
        com_anomalia.append(algoritmo)

    sem_anomalia: list[str] = []
    for algoritmo in agrupar_por_algoritmo(dados):
        if algoritmo not in com_anomalia:
            sem_anomalia.append(algoritmo)

    if len(sem_anomalia) == 0:
        print('Sem anomalia: nenhum algoritmo')
    else:
        print(f'Sem anomalia: {", ".join(sem_anomalia)}')

def main(argv: list[str]) -> int:
    caminho_csv: str | None = None
    saida: str | None = None

    i: int = 0
    while i < len(argv):
        opcao: str = argv[i]

        if opcao != '--csv' and opcao != '--saida':
            print(f'Erro: opção desconhecida {opcao}')
            print(USO)
            return 1
        if i + 1 >= len(argv):
            print(f'Erro: falta o valor de {opcao}')
            return 1

        if opcao == '--csv':
            caminho_csv = argv[i + 1]
        else:
            saida = argv[i + 1]
        i += 2

    if caminho_csv is None:
        print('Erro: --csv é obrigatório')
        print(USO)
        return 1

    if not os.path.exists(caminho_csv):
        print(f'Erro: o arquivo {caminho_csv} não existe')
        return 1

    dados: list[Resultado] = ler_resultados(caminho_csv)

    imprimir_anomalias(dados)

    if saida is not None:
        plotar_faltas_por_quadros(dados, saida)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
