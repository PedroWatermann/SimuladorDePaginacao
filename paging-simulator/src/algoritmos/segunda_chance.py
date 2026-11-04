from simulador import Sequencia, Traco, Resultado
from traco import traco_linha, traco_resumo

def simular_segunda_chance(seq: Sequencia, n_quadros: int, traco: Traco) -> Resultado:
    if n_quadros <= 0:
        raise ValueError("O parâmetro n_quadros deve ser maior que 0")

    quadros: list[int | None] = [None] * n_quadros
    referencia: dict[int, int] = {}
    proximo: int = 0
    faltas: int = 0
    acertos: int = 0

    for pagina in seq.paginas:
        if pagina in quadros:
            acertos += 1

            referencia[pagina] = 1

            if traco:
                traco_linha(traco, 'Segunda Chance', pagina, quadros, False, None)
            continue

        faltas += 1

        while quadros[proximo] is not None and referencia[quadros[proximo]] == 1:
            referencia[quadros[proximo]] = 0
            proximo = (proximo + 1) % n_quadros

        vitima: int | None = quadros[proximo]
        if vitima is not None:
            del referencia[vitima]

        quadros[proximo] = pagina
        referencia[pagina] = 1
        proximo = (proximo + 1) % n_quadros

        if traco:
            traco_linha(traco, 'Segunda Chance', pagina, quadros, True, vitima)

    resultado: Resultado = Resultado(
        algoritmo="Segunda Chance",
        n_quadros=n_quadros,
        faltas=faltas,
        acertos=acertos
    )

    if traco:
        traco_resumo(traco, resultado)

    return resultado
