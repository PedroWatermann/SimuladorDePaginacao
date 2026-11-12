# Simulador de Paginação

Simulador de substituição de páginas (FIFO, LRU, Ótimo, Segunda Chance e LFU) para a disciplina de Sistemas Operacionais da UEM.

**Autores:** Pedro Luiz Pereira Zampar e Pedro Augusto dos Santos Watermann.

## Preparação

Rode tudo dentro de `paging-simulator`:

```bash
cd paging-simulator
```

Instale o matplotlib (só uma vez, só é preciso para os gráficos):

```bash
python3 -m pip install --target .deps -r requirements.txt
```

Para os gráficos, aponte o `PYTHONPATH` para `.deps`. No PowerShell, rode uma vez por terminal:

```powershell
$env:PYTHONPATH = ".deps"
```

No Bash, coloque `PYTHONPATH=.deps` antes do comando (ex.: `PYTHONPATH=.deps python3 src/main.py --todos --quadros 1-30`).

Precisam do `PYTHONPATH`: `--img` e `--todos` do simulador e `--saida` da análise.

## Simulador

```bash
python3 src/main.py (--entrada ARQUIVO | --todos) --quadros N [--algoritmo NOME] [--csv ARQUIVO] [--img ARQUIVO] [-q]
```

| Opção | Obrigatório | O que faz |
|---|---|---|
| `--entrada` | Sim, ou `--todos` | Arquivo com as páginas, separadas por espaço ou linha (`#` comenta) |
| `--todos` | Sim, ou `--entrada` | Roda todos os algoritmos em todas as sequências de `entradas/` e grava `resultados/NOME.csv` e `resultados/NOME.png` (precisa do `PYTHONPATH`). Não aceita `--entrada`, `--algoritmo`, `--csv` nem `--img` |
| `--quadros` | Sim | `3`, faixa `1-30` ou lista `1,2,4` |
| `--algoritmo` | Não | `fifo`, `lru`, `otimo`, `segunda_chance` ou `lfu`. Sem ela, roda todos. Não pode com `--todos` |
| `--csv` | Não | Grava os resultados num CSV. Não pode com `--todos` |
| `--img` | Não | Grava o gráfico de faltas por quadros num PNG (precisa do `PYTHONPATH`). Não pode com `--todos` |
| `-q` | Não | Só os totais, sem o traço. Com `--todos`, esconde os totais e mostra só as anomalias |

```bash
# Traço passo a passo de um algoritmo
python3 src/main.py --entrada entradas/sequencia1.txt --quadros 3 --algoritmo fifo

# Totais de todos os algoritmos
python3 src/main.py --entrada entradas/sequencia1.txt --quadros 3 -q

# Faixa de quadros gravando o CSV e o gráfico
python3 src/main.py --entrada entradas/belady.txt --quadros 1-30 --csv resultados/belady.csv --img resultados/belady.png -q

# Regerar todos os CSVs e gráficos de resultados/, mostrando só as anomalias
python3 src/main.py --todos --quadros 1-30 -q
```

## Análise de um CSV

```bash
python3 analise.py --csv ARQUIVO [--saida GRAFICO.png]
```

| Opção | Obrigatório | O que faz |
|---|---|---|
| `--csv` | Sim | CSV gerado pelo simulador. Mostra em quais algoritmos houve a Anomalia de Belady |
| `--saida` | Não | Grava o gráfico nesse arquivo (precisa do `PYTHONPATH`) |

```bash
python3 analise.py --csv resultados/belady.csv --saida resultados/belady.png
```

## Gerador de sequências

```bash
python3 gerador.py --modo MODO --saida ARQUIVO [--acessos N] [--paginas N] [--janela N] [--semente N]
```

| Opção | Obrigatório | O que faz | Padrão |
|---|---|---|---|
| `--modo` | Sim | `sequencial`, `aleatorio` ou `localidade` | |
| `--saida` | Sim | Arquivo gravado | |
| `--acessos` | Não | Quantidade de referências | 500 |
| `--paginas` | Não | Quantidade de páginas diferentes | 30 |
| `--janela` | Não | Working set, só no modo `localidade` | 4 |
| `--semente` | Não | Semente do sorteio | 42 |

```bash
python3 gerador.py --modo sequencial --saida entradas/sequencial.txt
python3 gerador.py --modo aleatorio --saida entradas/aleatoria.txt
python3 gerador.py --modo localidade --saida entradas/localidade.txt
python3 gerador.py --modo localidade --acessos 10000 --saida entradas/longa.txt
```
