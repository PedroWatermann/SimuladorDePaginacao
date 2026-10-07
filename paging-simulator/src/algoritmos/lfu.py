from simulador import Sequencia, Traco, Resultado

def simular_lfu(seq: Sequencia, n_quadros: int, traco: Traco) -> Resultado:
    if n_quadros <= 0:
        raise ValueError("O parâmetro n_quadros deve ser maior que 0")

    quadros: list[int] = []
    acessos: dict[int, int] = {}
    faltas: int = 0
    acertos: int = 0
    
    for pagina in seq.paginas:
        if pagina in quadros:
            acertos += 1
            
            acessos[pagina] += 1
            
            if traco:
                traco.write(f'HIT\t{pagina} - {[(p, acessos[p]) for p in quadros]}\n')
            continue 
        
        faltas += 1
        
        if len(quadros) == n_quadros:
            vitima = min(quadros, key=lambda p: acessos[p])
            quadros.remove(vitima)
            del acessos[vitima]
        
        quadros.append(pagina)
        acessos[pagina] = 1
    
        if traco:
            traco.write(f'FAULT\t{pagina} - {[(p, acessos[p]) for p in quadros]}\n')
    
    print(f'\nAcertos: {acertos} - Faltas: {faltas} - Quadros: {n_quadros}') # Teste, remover depois
    return Resultado(
        algoritmo="LFU",
        n_quadros=n_quadros,
        faltas=faltas,
        acertos=acertos
    )

# Testes, remover depois
if __name__ == '__main__':
    import sys
    
    lista = Sequencia(paginas=[1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5])
    
    simular_lfu(lista, 3, sys.stdout) # 10 faltas, 2 acertos
    simular_lfu(lista, 4, sys.stdout) # 8 faltas, 4 acertos
