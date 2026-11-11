from simulador import Sequencia
import os

def ler_sequencia(caminho: str) -> Sequencia | None:
    if not os.path.exists(caminho):
        print(f'Erro: o arquivo {caminho} não existe')
        return None

    paginas: list[int] = []
    n_linha: int = 0

    with open(caminho, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            n_linha += 1
            linha = linha.strip()

            if linha == '' or linha.startswith('#'):
                continue

            for numero in linha.split():
                if not numero.isdigit():
                    print(f'Erro: {caminho}, linha {n_linha}: "{numero}" não é um número de página válido (use inteiros não negativos)')
                    return None
                paginas.append(int(numero))

    return Sequencia(paginas=paginas)
