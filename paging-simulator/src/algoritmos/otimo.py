from simulador import Sequencia, Traco, Resultado
from traco import traco_linha, traco_resumo

def simular_otimo(seq: Sequencia, n_quadros: int, traco: Traco) -> Resultado:
    if n_quadros <= 0:
        raise ValueError("O parâmetro n_quadros deve ser maior que 0")

    quadros: list[int | None] = [None] * n_quadros
    faltas: int = 0
    acertos: int = 0

    for i, pagina in enumerate(seq.paginas):
        if pagina in quadros:
            acertos += 1
            if traco:
                traco_linha(traco, 'Ótimo', pagina, quadros, False, None)
            continue

        faltas += 1

        vitima: int | None = None
        if None in quadros:
            posicao: int = quadros.index(None)
        else:
            vitima = max(quadros, key=lambda p: proximo_uso(seq, i, p)) # max() itera entre os elementos e key define sobre qual propriedade do elemento será feita a avaliação do maior para se obter ele. proximo_uso apenas calcula a posição em que a página será referenciada novamente
            posicao = quadros.index(vitima)

        quadros[posicao] = pagina

        if traco:
            traco_linha(traco, 'Ótimo', pagina, quadros, True, vitima)

    resultado: Resultado = Resultado(
        algoritmo="Ótimo",
        n_quadros=n_quadros,
        faltas=faltas,
        acertos=acertos
    )

    if traco:
        traco_resumo(traco, resultado)

    return resultado

def proximo_uso(seq: Sequencia, posicao: int, pagina: int) -> int:
    for i in range(posicao + 1, len(seq.paginas)):
        if seq.paginas[i] == pagina:
            return i
    return len(seq.paginas)
