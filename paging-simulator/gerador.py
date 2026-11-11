import os
import random
import sys

def gerar_sequencial(n_acessos: int, n_paginas: int) -> list[int]:
    seq: list[int] = []
    for i in range(n_acessos):
        seq.append(i % n_paginas)
    return seq

def gerar_aleatorio(n_acessos: int, n_paginas: int, semente: int) -> list[int]:
    rng = random.Random(semente)
    seq: list[int] = []
    for _ in range(n_acessos):
        seq.append(rng.randrange(n_paginas))
    return seq

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
            linha: list[str] = []
            for pagina in seq[i:i + 20]:
                linha.append(str(pagina))
            arquivo.write(' '.join(linha) + '\n')

USO: str = 'Uso: python3 gerador.py --modo MODO --saida ARQUIVO [--acessos N] [--paginas N] [--janela N] [--semente N]'

def ler_argumentos(argv: list[str]) -> dict | None:
    args: dict = {
        'modo': None,
        'saida': None,
        'acessos': 500,
        'paginas': 30,
        'janela': 4,
        'semente': 42,
    }

    i: int = 0
    while i < len(argv):
        opcao: str = argv[i]
        nome: str = opcao[2:]

        if not opcao.startswith('--') or nome not in args:
            print(f'Erro: opção desconhecida {opcao}')
            print(USO)
            return None
        if i + 1 >= len(argv):
            print(f'Erro: falta o valor de {opcao}')
            return None

        valor: str = argv[i + 1]
        if nome == 'modo' or nome == 'saida':
            args[nome] = valor
        else:
            if not valor.isdigit():
                print(f'Erro: o valor de {opcao} deve ser um número inteiro')
                return None
            args[nome] = int(valor)
        i += 2

    if args['modo'] is None or args['saida'] is None:
        print('Erro: --modo e --saida são obrigatórios')
        print(USO)
        return None

    return args

def main(argv: list[str]) -> int:
    args: dict | None = ler_argumentos(argv)
    if args is None:
        return 1

    modo: str = args['modo']
    acessos: int = args['acessos']
    paginas: int = args['paginas']
    janela: int = args['janela']
    semente: int = args['semente']

    if acessos <= 0 or paginas <= 0:
        print('Erro: --acessos e --paginas devem ser maiores que 0')
        return 1
    if janela <= 0 or janela > paginas:
        print('Erro: --janela deve estar entre 1 e o número de páginas')
        return 1

    if modo == 'sequencial':
        seq: list[int] = gerar_sequencial(acessos, paginas)
        cabecalho: str = f'modo=sequencial acessos={acessos} paginas={paginas}'
    elif modo == 'aleatorio':
        seq = gerar_aleatorio(acessos, paginas, semente)
        cabecalho = f'modo=aleatorio acessos={acessos} paginas={paginas} semente={semente}'
    elif modo == 'localidade':
        seq = gerar_localidade(acessos, paginas, janela, semente)
        cabecalho = f'modo=localidade acessos={acessos} paginas={paginas} janela={janela} semente={semente}'
    else:
        print('Erro: --modo deve ser sequencial, aleatorio ou localidade')
        return 1

    gravar_sequencia(seq, cabecalho, args['saida'])

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
