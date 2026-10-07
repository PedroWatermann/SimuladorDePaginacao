from simulador import Sequencia, Traco, Resultado

def simular_fifo(seq: Sequencia, n_quadros: int, traco: Traco) -> Resultado:
    if n_quadros <= 0:
        raise ValueError("O parâmetro n_quadros deve ser maior que 0")

    quadros: list[int] = []
    faltas: int = 0
    acertos: int = 0
    
    for pagina in seq.paginas:
        if pagina in quadros:
            acertos += 1
            if traco:
                traco.write(f'HIT\t{pagina} - {quadros}\n')
            continue 
        
        faltas += 1
        
        if len(quadros) == n_quadros:
            quadros.pop(0)
        quadros.append(pagina)
        if traco:
            traco.write(f'FAULT\t{pagina} - {quadros}\n')
            
    print(f'\nAcertos: {acertos} - Faltas: {faltas} - Quadros: {n_quadros}') # Teste, remover depois
    return Resultado(
        algoritmo="FIFO",
        n_quadros=n_quadros,
        faltas=faltas,
        acertos=acertos
    )

# Testes, remover depois
if __name__ == '__main__':
    import sys
    
    lista = Sequencia(paginas=[1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5])
    
    simular_fifo(lista, 3, sys.stdout) # 9 faltas, 3 acertos
    simular_fifo(lista, 4, sys.stdout) # 10 faltas, 2 acertos
