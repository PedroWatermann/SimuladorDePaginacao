import argparse
import os
import random
import sys

def gerar_sequencial(n_acessos: int, n_paginas: int) -> list[int]:
    return [i % n_paginas for i in range(n_acessos)]

def gerar_aleatorio(n_acessos: int, n_paginas: int, semente: int) -> list[int]:
    rng = random.Random(semente)
    return [rng.randrange(n_paginas) for _ in range(n_acessos)]

def gerar_localidade(n_acessos: int, n_paginas: int, janela: int, semente: int) -> list[int]:
    rng = random.Random(semente)
    seq: list[int] = []

    while len(seq) < n_acessos:
        working_set: list[int] = rng.sample(range(n_paginas), janela)
        for _ in range(rng.randint(10, 30)):
            seq.append(rng.choice(working_set))

    return seq[:n_acessos]

def gravar_sequencia(seq: list[int], cabecalho: str, caminho: str) -> None:
    diretorio: str = os.path.dirname(caminho)
    if diretorio:
        os.makedirs(diretorio, exist_ok=True)

    with open(caminho, 'w', encoding='utf-8') as arquivo:
        arquivo.write(f'# {cabecalho}\n')
        for i in range(0, len(seq), 20):
            arquivo.write(' '.join(str(pagina) for pagina in seq[i:i + 20]) + '\n')

def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description='Gerador de sequências de referências a páginas')
    parser.add_argument('--modo', required=True, choices=['sequencial', 'aleatorio', 'localidade'], help='padrão de acesso')
    parser.add_argument('--saida', required=True, help='arquivo em que a sequência é gravada')
    parser.add_argument('--acessos', type=int, default=500, help='número de referências (padrão: 500)')
    parser.add_argument('--paginas', type=int, default=30, help='número de páginas distintas (padrão: 30)')
    parser.add_argument('--janela', type=int, default=4, help='tamanho do working set no modo localidade (padrão: 4)')
    parser.add_argument('--semente', type=int, default=42, help='semente do gerador (padrão: 42)')
    args = parser.parse_args(argv)

    if args.acessos <= 0 or args.paginas <= 0:
        print('Erro: --acessos e --paginas devem ser maiores que 0', file=sys.stderr)
        return 1
    if not 0 < args.janela <= args.paginas:
        print('Erro: --janela deve estar entre 1 e o número de páginas', file=sys.stderr)
        return 1

    if args.modo == 'sequencial':
        seq: list[int] = gerar_sequencial(args.acessos, args.paginas)
        cabecalho: str = f'modo=sequencial acessos={args.acessos} paginas={args.paginas}'
    elif args.modo == 'aleatorio':
        seq = gerar_aleatorio(args.acessos, args.paginas, args.semente)
        cabecalho = f'modo=aleatorio acessos={args.acessos} paginas={args.paginas} semente={args.semente}'
    else:
        seq = gerar_localidade(args.acessos, args.paginas, args.janela, args.semente)
        cabecalho = f'modo=localidade acessos={args.acessos} paginas={args.paginas} janela={args.janela} semente={args.semente}'

    try:
        gravar_sequencia(seq, cabecalho, args.saida)
    except OSError as erro:
        print(f'Erro: {erro}', file=sys.stderr)
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
