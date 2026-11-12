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
    tempo_decorrido: float = 0.0

    @property
    def referencias(self) -> int:
        return self.faltas + self.acertos

    @property
    def taxa_faltas(self) -> float:
        if self.referencias == 0:
            return 0.0
        return 100 * self.faltas / self.referencias
