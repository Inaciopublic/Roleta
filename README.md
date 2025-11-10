# Projeto Roleta

Painel inteligente para leitura e visualização de números de roleta.

## Pré-requisitos

- Python 3.11 ou superior
- Google Chrome instalado

Instale as dependências Python com:

```bash
pip install -r requirements.txt
```

## Captura contínua via linha de comando

Execute o coletor com:

```bash
python -m roleta.cli
```

Parâmetros opcionais:

- `--limit`: quantidade máxima de números exibidos (padrão: 8)
- `--delay`: intervalo em segundos entre capturas (padrão: 5)
- `--initial-wait`: tempo de espera inicial antes da primeira captura (padrão: 5)

Interrompa a execução com `Ctrl+C`.
