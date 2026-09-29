from dataclasses import dataclass
from typing import TextIO

Traco = TextIO | None

@dataclass
class Sequencia:
    paginas: list[int]
    
@dataclass
class Resultado:
    algoritmo: str = ""
    n_quadros: int = 0
    faltas: int = 0
    acertos: int = 0
