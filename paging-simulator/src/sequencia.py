from simulador import Sequencia
import os

def ler_sequencia(caminho: str) -> Sequencia:
    if not os.path.exists(caminho):
        raise FileNotFoundError(f'O arquivo {caminho} não existe')

    paginas: list[int] = []

    with open(caminho, 'r', encoding='utf-8') as arquivo:
        for n_linha, linha in enumerate(arquivo, start=1):
            for numero in linha.split('#', 1)[0].split():
                paginas.append(converter_pagina(numero, caminho, n_linha))

    return Sequencia(paginas=paginas)

def converter_pagina(numero: str, caminho: str, n_linha: int) -> int:
    try:
        pagina: int = int(numero)
    except ValueError:
        pagina = -1

    if pagina < 0:
        raise ValueError(f'{caminho}, linha {n_linha}: "{numero}" não é um número de página válido (use inteiros não negativos)')

    return pagina
