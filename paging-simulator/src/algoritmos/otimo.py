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
            # Página que não volta tem distância len(seq.paginas); no empate fica o primeiro quadro (só troca se for maior)
            posicao = 0
            maior_distancia: int = proximo_uso(seq, i, quadros[0])
            for q in range(1, n_quadros):
                distancia: int = proximo_uso(seq, i, quadros[q])
                if distancia > maior_distancia:
                    maior_distancia = distancia
                    posicao = q
            vitima = quadros[posicao]

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
