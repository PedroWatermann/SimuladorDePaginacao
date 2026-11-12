from simulador import Resultado
from typing import TextIO

def traco_linha(saida: TextIO, algoritmo: str, pagina: int, quadros: list[int | None], houve_falta: bool, vitima: int | None) -> None:
    textos: list[str] = []
    for quadro in quadros:
        if quadro is None:
            textos.append("-")
        else:
            textos.append(str(quadro))
    estado: str = ",".join(textos)

    linha: str = f"Ref: {pagina}\tQuadros: [{estado}]\t"

    if not houve_falta:
        linha += "ACERTO"
    elif vitima is None:
        linha += "FALTA"
    else:
        linha += f"FALTA (substitui {vitima} - {algoritmo})"

    saida.write(linha + "\n")

def traco_resumo(saida: TextIO, resultado: Resultado) -> None:
    saida.write(
        f'Algoritmo: {resultado.algoritmo} | ' +
        f'Quadros: {resultado.n_quadros} | ' +
        f'Referencias: {resultado.referencias} | ' +
        f'Faltas: {resultado.faltas} | ' +
        f'Taxa: {resultado.taxa_faltas:.2f}% | ' +
        f'Tempo: {resultado.tempo_decorrido:.2f} ms\n'
    )
