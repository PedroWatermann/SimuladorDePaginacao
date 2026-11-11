from simulador import Sequencia, Traco, Resultado
from traco import traco_linha, traco_resumo

def simular_lfu(seq: Sequencia, n_quadros: int, traco: Traco) -> Resultado:
    if n_quadros <= 0:
        raise ValueError("O parâmetro n_quadros deve ser maior que 0")

    quadros: list[int | None] = [None] * n_quadros
    acessos: dict[int, int] = {}
    chegada: dict[int, int] = {}
    faltas: int = 0
    acertos: int = 0

    for instante, pagina in enumerate(seq.paginas):
        if pagina in quadros:
            acertos += 1

            acessos[pagina] += 1

            if traco:
                traco_linha(traco, 'LFU', pagina, quadros, False, None)
            continue

        faltas += 1

        vitima: int | None = None
        if None in quadros:
            posicao: int = quadros.index(None)
        else:
            # Sai a de menos acessos; no empate, sai a que chegou primeiro
            posicao = 0
            for i in range(1, n_quadros):
                candidata: int = quadros[i]
                atual: int = quadros[posicao]
                if acessos[candidata] < acessos[atual]:
                    posicao = i
                elif acessos[candidata] == acessos[atual] and chegada[candidata] < chegada[atual]:
                    posicao = i
            vitima = quadros[posicao]
            del acessos[vitima]
            del chegada[vitima]

        quadros[posicao] = pagina
        acessos[pagina] = 1
        chegada[pagina] = instante

        if traco:
            traco_linha(traco, 'LFU', pagina, quadros, True, vitima)

    resultado: Resultado = Resultado(
        algoritmo="LFU",
        n_quadros=n_quadros,
        faltas=faltas,
        acertos=acertos
    )

    if traco:
        traco_resumo(traco, resultado)

    return resultado
