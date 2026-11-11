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

ALGORITMOS = {
    'fifo': simular_fifo,
    'lru': simular_lru,
    'otimo': simular_otimo,
    'segunda_chance': simular_segunda_chance,
    'lfu': simular_lfu,
}

USO: str = 'Uso: python3 src/main.py --entrada ARQUIVO --quadros N [--algoritmo NOME] [--csv ARQUIVO] [-q]'

def ler_argumentos(argv: list[str]) -> dict | None:
    args: dict = {
        'entrada': None,
        'quadros': None,
        'algoritmo': None,
        'csv': None,
        'quiet': False,
    }

    i: int = 0
    while i < len(argv):
        opcao: str = argv[i]

        if opcao == '-q' or opcao == '--quiet':
            args['quiet'] = True
            i += 1
        elif opcao == '--entrada' or opcao == '--quadros' or opcao == '--algoritmo' or opcao == '--csv':
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

    if args['entrada'] is None or args['quadros'] is None:
        print('Erro: --entrada e --quadros são obrigatórios')
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

def executar(seq: Sequencia, quadros: list[int], algoritmos: list[str], silencioso: bool) -> list[Resultado]:
    resultados: list[Resultado] = []
    varias_execucoes: bool = len(quadros) * len(algoritmos) > 1

    for n_quadros in quadros:
        for nome in algoritmos:
            if silencioso:
                resultado: Resultado = ALGORITMOS[nome](seq, n_quadros, None)
                traco_resumo(sys.stdout, resultado)
            else:
                if varias_execucoes:
                    print(f'== {nome}, {n_quadros} quadros ==')
                resultado = ALGORITMOS[nome](seq, n_quadros, sys.stdout)

            resultados.append(resultado)

    return resultados

def gravar_csv(resultados: list[Resultado], caminho: str) -> None:
    diretorio: str = os.path.dirname(caminho)
    if diretorio:
        os.makedirs(diretorio, exist_ok=True)

    with open(caminho, 'w', newline='', encoding='utf-8') as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(['algoritmo', 'n_quadros', 'referencias', 'faltas', 'acertos', 'taxa_faltas'])
        for r in resultados:
            escritor.writerow([r.algoritmo, r.n_quadros, r.referencias, r.faltas, r.acertos, f'{r.taxa_faltas:.2f}'])

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

    seq: Sequencia | None = ler_sequencia(args['entrada'])
    if seq is None:
        return 1

    quadros: list[int] | None = ler_quadros(args['quadros'])
    if quadros is None:
        return 1

    resultados: list[Resultado] = executar(seq, quadros, algoritmos, args['quiet'])

    if args['csv'] is not None:
        gravar_csv(resultados, args['csv'])

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
