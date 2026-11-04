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

    @property
    def referencias(self) -> int:
        return self.faltas + self.acertos

    @property
    def taxa_faltas(self) -> float:
        return 100 * self.faltas / self.referencias if self.referencias else 0.0

## Não será implementado, pois é código redundante, facilmente escrito de forma curta no método do próprio algoritmo

# def buscar_quadro(quadros: list[int | None], pagina: int) -> int:
#     pass