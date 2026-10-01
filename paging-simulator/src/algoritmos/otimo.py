from simulador import Sequencia, Traco, Resultado

def simular_otimo(seq: Sequencia, n_quadros: int, traco: Traco) -> Resultado:
    if n_quadros <= 0:
        raise ValueError("O parâmetro n_quadros deve ser maior que 0")

    quadros: list[int] = []
    faltas: int = 0
    acertos: int = 0

    for i, pagina in enumerate(seq.paginas):
        if pagina in quadros:
            acertos += 1
            if traco:
                traco.write(f'HIT\t{pagina} - {quadros}\n')
            continue

        faltas += 1

        if len(quadros) == n_quadros:
            futuro = seq.paginas[i + 1:]
            vitima = max(quadros, key=lambda p: proximo_uso(p, futuro)) # max() itera entre os elementos e key define sobre qual propriedade do elemento será feita a avaliação do maior para se obter ele. proximo_uso apenas calcula qual a "distância" a página está a partir da página que será inserida
            quadros.remove(vitima)

        quadros.append(pagina)

        if traco:
            traco.write(f'FAULT\t{pagina} - {quadros}\n')

    print(f'\nAcertos: {acertos} - Faltas: {faltas} - Quadros: {n_quadros}') # Teste, remover depois
    return Resultado(
        algoritmo="Ótimo",
        n_quadros=n_quadros,
        faltas=faltas,
        acertos=acertos
    )

def proximo_uso(pagina: int, futuro: list[int]) -> int:
    return futuro.index(pagina) if pagina in futuro else len(futuro)

# Testes, remover depois
if __name__ == '__main__':
    import sys
    
    lista = Sequencia(paginas=[1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5])
    
    simular_otimo(lista, 3, sys.stdout) # 7 faltas, 5 acertos
    simular_otimo(lista, 4, sys.stdout) # 6 faltas, 6 acertos
