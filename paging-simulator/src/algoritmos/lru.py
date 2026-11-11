from simulador import Sequencia, Traco, Resultado
from traco import traco_linha, traco_resumo

def simular_lru(seq: Sequencia, n_quadros: int, traco: Traco) -> Resultado:
    if n_quadros <= 0:
        raise ValueError("O parâmetro n_quadros deve ser maior que 0")

    quadros: list[int | None] = [None] * n_quadros
    ultimo_acesso: dict[int, int] = {}
    faltas: int = 0
    acertos: int = 0

    for instante, pagina in enumerate(seq.paginas):
        if pagina in quadros:
            acertos += 1
            ultimo_acesso[pagina] = instante
            if traco:
                traco_linha(traco, 'LRU', pagina, quadros, False, None)
            continue

        faltas += 1

        vitima: int | None = None
        if None in quadros:
            posicao: int = quadros.index(None)
        else:
            posicao = 0
            for i in range(1, n_quadros):
                if ultimo_acesso[quadros[i]] < ultimo_acesso[quadros[posicao]]:
                    posicao = i
            vitima = quadros[posicao]
            del ultimo_acesso[vitima]

        quadros[posicao] = pagina
        ultimo_acesso[pagina] = instante

        if traco:
            traco_linha(traco, 'LRU', pagina, quadros, True, vitima)

    resultado: Resultado = Resultado(
        algoritmo="LRU",
        n_quadros=n_quadros,
        faltas=faltas,
        acertos=acertos
    )

    if traco:
        traco_resumo(traco, resultado)

    return resultado
