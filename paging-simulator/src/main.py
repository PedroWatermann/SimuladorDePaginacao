from algoritmos.fifo import simular_fifo
from algoritmos.lfu import simular_lfu
from algoritmos.lru import simular_lru
from algoritmos.otimo import simular_otimo
from algoritmos.segunda_chance import simular_segunda_chance
from sequencia import ler_sequencia
from simulador import Sequencia, Resultado
from traco import traco_resumo
import argparse
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

def ler_argumentos(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Simulador de substituição de páginas')
    parser.add_argument('--entrada', required=True, help='arquivo com a sequência de páginas')
    parser.add_argument('--quadros', required=True, help='número de quadros: um valor (3), uma faixa (1-7) ou uma lista (1,2,4)')
    parser.add_argument('--algoritmo', choices=ALGORITMOS, help='política de substituição (todas, se omitido)')
    parser.add_argument('--csv', help='arquivo em que a tabela consolidada é gravada')
    parser.add_argument('-q', '--quiet', action='store_true', help='mostra apenas os totais, sem o traço')
    return parser.parse_args(argv)

def ler_quadros(texto: str) -> list[int]:
    quadros: set[int] = set()

    for parte in texto.split(','):
        inicio, separador, fim = parte.partition('-')
        try:
            primeiro: int = int(inicio)
            ultimo: int = int(fim) if separador else primeiro
        except ValueError:
            raise ValueError(f'"{parte}" não é um número de quadros válido (use 3, 1-7 ou 1,2,4)') from None

        if primeiro <= 0 or ultimo < primeiro:
            raise ValueError(f'"{parte}" não é um número de quadros válido (os valores devem ser maiores que 0 e estar em ordem crescente)')

        quadros.update(range(primeiro, ultimo + 1))

    return sorted(quadros)

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
    args = ler_argumentos(argv)

    try:
        seq: Sequencia = ler_sequencia(args.entrada)
        quadros: list[int] = ler_quadros(args.quadros)
        algoritmos: list[str] = [args.algoritmo] if args.algoritmo else list(ALGORITMOS)

        resultados: list[Resultado] = executar(seq, quadros, algoritmos, args.quiet)

        if args.csv:
            gravar_csv(resultados, args.csv)
    except (OSError, ValueError) as erro:
        print(f'Erro: {erro}', file=sys.stderr)
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
