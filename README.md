# Simulador de Paginação

Simulador de substituição de páginas (FIFO, LRU, Ótimo, Segunda Chance e LFU) para a disciplina de Sistemas Operacionais da UEM.

**Autores:** Pedro Luiz Pereira Zampar e Pedro Augusto dos Santos Watermann.

Precisa de Python 3. Rode todos os comandos dentro da pasta `paging-simulator`:

```bash
cd paging-simulator
```

## Simulador

```bash
python3 src/main.py --entrada ARQUIVO --quadros N [--algoritmo NOME] [--csv ARQUIVO] [-q]
```

| Opção | O que faz |
|---|---|
| `--entrada` | Arquivo com a sequência de páginas (obrigatório) |
| `--quadros` | Número de quadros: `3`, uma faixa `1-7` ou uma lista `1,2,4` (obrigatório) |
| `--algoritmo` | `fifo`, `lru`, `otimo`, `segunda_chance` ou `lfu`. Sem ela, roda todos |
| `--csv` | Grava os resultados em um arquivo CSV |
| `-q` | Mostra só os totais, sem o traço |

Exemplos:

```bash
# Um algoritmo, com o traço passo a passo
python3 src/main.py --entrada entradas/sequencia1.txt --quadros 3 --algoritmo fifo

# Todos os algoritmos, só os totais
python3 src/main.py --entrada entradas/sequencia1.txt --quadros 3 -q

# Faixa de quadros, gravando o CSV
python3 src/main.py --entrada entradas/belady.txt --quadros 1-30 --csv resultados/belady.csv -q
```

## Análise (Anomalia de Belady e gráfico)

```bash
python3 analise.py --csv ARQUIVO [--saida GRAFICO.png]
```

Sem `--saida`, só mostra em quais algoritmos houve a Anomalia de Belady:

```bash
python3 analise.py --csv resultados/belady.csv
```

Para gerar o gráfico, instale o matplotlib uma vez e rode com `--saida`:

```bash
python3 -m pip install --target .deps -r requirements.txt
PYTHONPATH=.deps python3 analise.py --csv resultados/belady.csv --saida resultados/belady.png
```

## Gerador de sequências

```bash
python3 gerador.py --modo MODO --saida ARQUIVO [--acessos N] [--paginas N] [--janela N] [--semente N]
```

| Opção | O que faz | Padrão |
|---|---|---|
| `--modo` | `sequencial`, `aleatorio` ou `localidade` (obrigatório) | |
| `--saida` | Arquivo onde a sequência é gravada (obrigatório) | |
| `--acessos` | Quantidade de referências | 500 |
| `--paginas` | Quantidade de páginas diferentes | 30 |
| `--janela` | Tamanho do working set (só no modo `localidade`) | 4 |
| `--semente` | Semente do sorteio (mesma semente, mesma sequência) | 42 |

Exemplo:

```bash
python3 gerador.py --modo localidade --saida entradas/localidade.txt
```

## Arquivo de entrada

Números de página inteiros e não negativos, separados por espaço ou quebra de linha. Linhas vazias e linhas que começam com `#` são ignoradas.

```text
# sequência clássica
7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1
```

Sequências em `entradas/` (os CSVs e gráficos de cada uma ficam em `resultados/`):

| Arquivo | Para que serve |
|---|---|
| `sequencia1.txt` | Sequência clássica do roteiro, para conferir os resultados |
| `belady.txt` | Reproduz a Anomalia de Belady no FIFO |
| `sequencial.txt` | Padrão sequencial, sem reuso próximo (gerador) |
| `aleatoria.txt` | Padrão aleatório, sem localidade (gerador) |
| `localidade.txt` | Padrão com localidade, working set de 4 páginas (gerador) |
| `periodica.txt` | Páginas que se repetem em ciclos, para comparar Segunda Chance e FIFO |
| `longa.txt` | Sequência muito longa, com 10000 acessos (gerador) |

As sequências do gerador foram criadas com:

```bash
python3 gerador.py --modo sequencial --saida entradas/sequencial.txt
python3 gerador.py --modo aleatorio --saida entradas/aleatoria.txt
python3 gerador.py --modo localidade --saida entradas/localidade.txt
python3 gerador.py --modo localidade --acessos 10000 --saida entradas/longa.txt
```
