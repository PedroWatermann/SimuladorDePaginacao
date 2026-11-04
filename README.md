# SimuladorDePaginacao

Simulador de substituição de páginas de memória virtual, desenvolvido para a disciplina de Sistemas Operacionais da Universidade Estadual de Maringá (UEM).

A partir de uma sequência de referências a páginas e de um número de quadros, o programa conta as faltas de página, calcula a taxa de faltas e mostra o estado da memória a cada referência. Os algoritmos implementados são FIFO, LRU, Ótimo, Segunda Chance e LFU.

**Autores:** Pedro Luiz Pereira Zampar e Pedro Augusto dos Santos Watermann.

## Requisitos

- Linux (nativo ou WSL) com Python 3. O projeto foi testado com Python 3.14.
- O simulador, o gerador e os testes usam apenas a biblioteca padrão. Somente o gráfico depende do matplotlib.

## Como executar

Execute todos os comandos dentro da pasta `paging-simulator`:

```bash
cd paging-simulator
```

### Um algoritmo, com traço

```bash
python3 src/main.py --entrada entradas/sequencia1.txt --quadros 3 --algoritmo fifo
```

```text
Ref: 7	Quadros: [7,-,-]	FALTA
Ref: 0	Quadros: [7,0,-]	FALTA
Ref: 1	Quadros: [7,0,1]	FALTA
Ref: 2	Quadros: [2,0,1]	FALTA (substitui 7 - FIFO)
Ref: 0	Quadros: [2,0,1]	ACERTO
...
Algoritmo: FIFO | Quadros: 3 | Referencias: 20 | Faltas: 15 | Taxa: 75.00%
```

### Todos os algoritmos, só com os totais

Sem `--algoritmo`, todos os algoritmos são executados. A opção `-q` omite o traço:

```bash
python3 src/main.py --entrada entradas/sequencia1.txt --quadros 3 -q
```

### Faixa de quadros e exportação em CSV

```bash
python3 src/main.py --entrada entradas/sequencia1.txt --quadros 1-30 --csv resultados/sequencia1.csv -q
```

### Parâmetros

| Parâmetro | Descrição |
|---|---|
| `--entrada ARQUIVO` | Arquivo com a sequência de páginas (obrigatório) |
| `--quadros VALORES` | Um valor (`3`), uma faixa (`1-7`), uma lista (`1,2,4`) ou uma combinação (`1-4,8`) (obrigatório) |
| `--algoritmo NOME` | `fifo`, `lru`, `otimo`, `segunda_chance` ou `lfu`. Se omitido, executa todos |
| `--csv ARQUIVO` | Grava a tabela consolidada, com as colunas `algoritmo`, `n_quadros`, `referencias`, `faltas`, `acertos` e `taxa_faltas` |
| `-q`, `--quiet` | Mostra apenas os totais, sem o traço |

Arquivo inexistente ou malformado e número de quadros inválido geram uma mensagem de erro e código de saída 1.

### Detecção da Anomalia de Belady

```bash
python3 src/main.py --entrada entradas/belady.txt --quadros 1-30 --csv resultados/belady.csv -q
```

```bash
python3 analise.py --csv resultados/belady.csv
```

```text
Anomalia de Belady: FIFO com 4 quadros (mais faltas que com 3)
Anomalia de Belady: Segunda Chance com 4 quadros (mais faltas que com 3)
Sem anomalia: LRU, Ótimo, LFU
```

### Gráfico de faltas por número de quadros

Instale o matplotlib uma vez, em uma pasta local do projeto:

```bash
python3 -m pip install --target .deps -r requirements.txt
```

Depois gere o gráfico a partir de um CSV:

```bash
PYTHONPATH=.deps python3 analise.py --csv resultados/belady.csv --saida resultados/belady.png
```

### Geração de sequências

O gerador tem três modos: `sequencial`, `aleatorio` e `localidade`. Com a mesma semente, ele produz sempre a mesma sequência. O exemplo abaixo reproduz `entradas/localidade.txt`, com os valores padrão de 500 acessos, 30 páginas, working set de 4 páginas e semente 42:

```bash
python3 gerador.py --modo localidade --saida entradas/localidade.txt
```

Os parâmetros `--acessos`, `--paginas`, `--janela` e `--semente` alteram esses valores. No modo `localidade`, cada working set recebe uma rajada de 10 a 30 acessos.

### Testes

```bash
python3 -m unittest discover -s testes
```

## Arquivos de entrada

Cada arquivo contém números de página inteiros e não negativos, separados por espaços ou quebras de linha. Linhas vazias são ignoradas, assim como tudo o que vem depois de `#`.

| Arquivo | Conteúdo |
|---|---|
| `entradas/sequencia1.txt` | Sequência clássica do roteiro: 20 referências e 6 páginas distintas |
| `entradas/belady.txt` | Sequência que provoca a Anomalia de Belady no FIFO |
| `entradas/periodica.txt` | 1000 referências: as páginas 1 a 4 se repetem a cada ciclo, intercaladas com uma varredura das páginas 5 a 44 |
| `entradas/sequencial.txt` | 500 referências em varredura de 30 páginas, sem reuso próximo |
| `entradas/aleatoria.txt` | 500 referências sorteadas entre 30 páginas, sem localidade (semente 42) |
| `entradas/localidade.txt` | 500 referências entre 30 páginas, com working set de 4 páginas (semente 42) |

## Convenções adotadas

| Tema | Convenção |
|---|---|
| Posição das páginas | Fixa: a nova página ocupa o quadro da vítima, e os quadros livres são preenchidos em ordem |
| FIFO | Um índice circular aponta o próximo quadro a ser substituído; acertos não alteram esse índice |
| LRU | Relógio lógico: um dicionário guarda o instante do último acesso de cada página. Atualizar o acesso custa O(1), e buscar a página ou escolher a vítima custa O(q), sendo q o número de quadros |
| Ótimo | Se várias páginas nunca mais forem usadas, sai a de menor índice de quadro |
| Segunda Chance | Relógio com ponteiro circular. O bit R é **ligado na carga** e em cada acerto |
| LFU | Conta os acessos desde a carga, e a contagem é descartada quando a página sai da memória. No empate, sai a página que está há mais tempo na memória |

A convenção do bit R é a mesma do roteiro: com a sequência clássica e 3 quadros, a Segunda Chance produz 14 faltas. Com o bit desligado na carga, seriam 11.

## Resultados de referência

Faltas de página na sequência `entradas/sequencia1.txt`:

| Quadros | FIFO | LRU | Ótimo | Segunda Chance | LFU |
|---:|---:|---:|---:|---:|---:|
| 1 | 20 | 20 | 20 | 20 | 20 |
| 2 | 15 | 17 | 13 | 15 | 15 |
| 3 | 15 | 12 | 9 | 14 | 13 |
| 4 | 10 | 8 | 8 | 9 | 9 |
| 5 | 9 | 7 | 7 | 9 | 7 |
| 6 | 6 | 6 | 6 | 6 | 6 |
| 7 | 6 | 6 | 6 | 6 | 6 |

## Estrutura do projeto

```text
paging-simulator/
|-- src/
|   |-- main.py              # linha de comando e execução dos algoritmos
|   |-- simulador.py         # tipos compartilhados
|   |-- sequencia.py         # leitura do arquivo de entrada
|   |-- traco.py             # impressão do traço e do resumo
|   `-- algoritmos/          # um módulo por algoritmo
|       |-- fifo.py
|       |-- lru.py
|       |-- otimo.py
|       |-- segunda_chance.py
|       `-- lfu.py
|-- entradas/                # sequências de teste
|-- resultados/              # CSVs e gráficos gerados
|-- testes/                  # testes automatizados
|-- analise.py               # gráfico e detecção da anomalia
|-- gerador.py               # gerador de sequências
`-- requirements.txt         # dependência do gráfico
```

## Licença

Distribuído sob os termos do arquivo [LICENSE](LICENSE).
