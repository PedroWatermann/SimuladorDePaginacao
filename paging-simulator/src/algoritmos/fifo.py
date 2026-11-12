from simulador import Sequencia, Traco, Resultado
from traco import traco_linha

def simular_fifo(seq: Sequencia, n_quadros: int, traco: Traco) -> Resultado:
    if n_quadros <= 0:
        raise ValueError("O parâmetro n_quadros deve ser maior que 0")

    quadros: list[int | None] = [None] * n_quadros
    proximo: int = 0
    faltas: int = 0
    acertos: int = 0

    for pagina in seq.paginas:
        if pagina in quadros:
            acertos += 1
            if traco:
                traco_linha(traco, 'FIFO', pagina, quadros, False, None)
            continue

        faltas += 1

        # Enquanto a memória não enche, quadros[proximo] é None: entra no quadro livre, sem vítima
        vitima: int | None = quadros[proximo]
        quadros[proximo] = pagina
        proximo = (proximo + 1) % n_quadros

        if traco:
            traco_linha(traco, 'FIFO', pagina, quadros, True, vitima)

    resultado: Resultado = Resultado(
        algoritmo="FIFO",
        n_quadros=n_quadros,
        faltas=faltas,
        acertos=acertos
    )

    return resultado
