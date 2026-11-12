from algoritmos.fifo import simular_fifo
from algoritmos.lfu import simular_lfu
from algoritmos.lru import simular_lru
from algoritmos.otimo import simular_otimo
from algoritmos.segunda_chance import simular_segunda_chance
from sequencia import ler_sequencia
from simulador import Sequencia, Resultado
from traco import traco_resumo
import csv
import os
import sys
import time

# Para importar o analise.py (gráfico), que fica na pasta de cima
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ALGORITMOS = {
    'fifo': simular_fifo,
    'lru': simular_lru,
    'otimo': simular_otimo,
    'segunda_chance': simular_segunda_chance,
    'lfu': simular_lfu,
}

USO: str = 'Uso: python3 src/main.py (--entrada ARQUIVO | --todos) --quadros N [--algoritmo NOME] [--csv ARQUIVO] [--img ARQUIVO] [-q]'

def ler_argumentos(argv: list[str]) -> dict | None:
    args: dict = {
        'entrada': None,
        'quadros': None,
        'algoritmo': None,
        'csv': None,
        'img': None,
        'quiet': False,
        'todos': False,
    }

    i: int = 0
    while i < len(argv):
        opcao: str = argv[i]

        if opcao == '-q' or opcao == '--quiet':
            args['quiet'] = True
            i += 1
        elif opcao == '--todos':
            args['todos'] = True
            i += 1
        elif opcao == '--entrada' or opcao == '--quadros' or opcao == '--algoritmo' or opcao == '--csv' or opcao == '--img':
            if i + 1 >= len(argv):
                print(f'Erro: falta o valor de {opcao}')
                return None
            nome: str = opcao[2:]
            args[nome] = argv[i + 1]
            i += 2
        else:
            print(f'Erro: opção desconhecida {opcao}')
            print(USO)
            return None

    if (args['entrada'] is None and not args['todos']) or args['quadros'] is None:
        print('Erro: --entrada (ou --todos) e --quadros são obrigatórios')
        print(USO)
        return None

    if args['todos'] and (args['entrada'] is not None or args['algoritmo'] is not None or args['csv'] is not None or args['img'] is not None):
        print('Erro: --todos não pode ser usado com --entrada, --algoritmo, --csv ou --img (ele roda todos os algoritmos e já grava em resultados/)')
        print(USO)
        return None

    return args

def ler_quadros(texto: str) -> list[int] | None:
    quadros: list[int] = []

    for parte in texto.split(','):
        parte = parte.strip()

        if '-' in parte:
            limites: list[str] = parte.split('-')
            if len(limites) != 2 or not limites[0].isdigit() or not limites[1].isdigit():
                print(f'Erro: "{parte}" não é um número de quadros válido (use 3, 1-7 ou 1,2,4)')
                return None
            primeiro: int = int(limites[0])
            ultimo: int = int(limites[1])
        else:
            if not parte.isdigit():
                print(f'Erro: "{parte}" não é um número de quadros válido (use 3, 1-7 ou 1,2,4)')
                return None
            primeiro = int(parte)
            ultimo = primeiro

        if primeiro <= 0 or ultimo < primeiro:
            print(f'Erro: "{parte}" não é um número de quadros válido (os valores devem ser maiores que 0 e estar em ordem crescente)')
            return None

        for n_quadros in range(primeiro, ultimo + 1):
            if n_quadros not in quadros:
                quadros.append(n_quadros)

    quadros.sort()
    return quadros

def executar(seq: Sequencia, quadros: list[int], algoritmos: list[str], silencioso: bool, mostrar_resumo: bool = True) -> list[Resultado]:
    resultados: list[Resultado] = []
    varias_execucoes: bool = len(quadros) * len(algoritmos) > 1

    for n_quadros in quadros:
        for nome in algoritmos:
            # O tempo é medido sempre numa execução sem traço, para não contar o tempo de escrever na tela
            inicio: float = time.perf_counter()
            resultado: Resultado = ALGORITMOS[nome](seq, n_quadros, None)
            final: float = time.perf_counter()
            resultado.tempo_decorrido = (final - inicio) * 1000

            if not silencioso:
                if varias_execucoes:
                    print(f'== {nome}, {n_quadros} quadros ==')
                # Roda de novo só para mostrar o traço; o resultado é o mesmo
                ALGORITMOS[nome](seq, n_quadros, sys.stdout)

            if mostrar_resumo:
                traco_resumo(sys.stdout, resultado)
            resultados.append(resultado)

    return resultados

def gravar_csv(resultados: list[Resultado], caminho: str) -> None:
    diretorio: str = os.path.dirname(caminho)
    if diretorio:
        os.makedirs(diretorio, exist_ok=True)

    with open(caminho, 'w', newline='', encoding='utf-8') as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(['algoritmo', 'n_quadros', 'referencias', 'faltas', 'acertos', 'taxa_faltas', 'tempo_decorrido_(ms)'])
        for r in resultados:
            escritor.writerow([r.algoritmo, r.n_quadros, r.referencias, r.faltas, r.acertos, f'{r.taxa_faltas:.2f}', f'{r.tempo_decorrido:.2f}'])

def gravar_img(resultados: list[Resultado], caminho: str) -> bool:
    try:
        import matplotlib
    except ImportError:
        print('Erro: matplotlib não encontrado. Instale em .deps e defina o PYTHONPATH (veja o README)')
        return False

    from analise import plotar_faltas_por_quadros
    plotar_faltas_por_quadros(resultados, caminho)
    return True

def gerar_todos(quadros: list[int], silencioso: bool) -> int:
    # Roda cada sequência de entradas/ e grava o CSV e o gráfico em resultados/
    from analise import imprimir_anomalias

    for arquivo in sorted(os.listdir('entradas')):
        if not arquivo.endswith('.txt'):
            continue

        nome: str = arquivo[:-4]
        seq: Sequencia | None = ler_sequencia(os.path.join('entradas', arquivo))
        if seq is None:
            return 1

        print(f'== {nome} ==')
        # Nunca mostra o traço; sem -q mostra os totais de cada execução, com -q só as anomalias
        resultados: list[Resultado] = executar(seq, quadros, list(ALGORITMOS.keys()), True, not silencioso)
        gravar_csv(resultados, os.path.join('resultados', f'{nome}.csv'))
        if not gravar_img(resultados, os.path.join('resultados', f'{nome}.png')):
            return 1
        imprimir_anomalias(resultados)

    return 0

def main(argv: list[str]) -> int:
    args: dict | None = ler_argumentos(argv)
    if args is None:
        return 1

    if args['algoritmo'] is None:
        algoritmos: list[str] = list(ALGORITMOS.keys())
    elif args['algoritmo'] in ALGORITMOS:
        algoritmos = [args['algoritmo']]
    else:
        print(f'Erro: algoritmo "{args["algoritmo"]}" desconhecido (use fifo, lru, otimo, segunda_chance ou lfu)')
        return 1

    quadros: list[int] | None = ler_quadros(args['quadros'])
    if quadros is None:
        return 1

    if args['todos']:
        return gerar_todos(quadros, args['quiet'])

    seq: Sequencia | None = ler_sequencia(args['entrada'])
    if seq is None:
        return 1

    resultados: list[Resultado] = executar(seq, quadros, algoritmos, args['quiet'])

    if args['csv'] is not None:
        gravar_csv(resultados, args['csv'])

    if args['img'] is not None and not gravar_img(resultados, args['img']):
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
