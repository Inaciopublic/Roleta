# Projeto Roleta
Painel inteligente para leitura e visualização de números de roleta.

## Ferramenta de captura local

O repositório inclui um utilitário multiplataforma (`mnt/data/capture_and_send.py`) que captura a tela inteira ou uma região específica, extrai sequências numéricas via OCR e envia o resultado para um webhook do n8n.

### Requisitos

Instale as dependências em um ambiente virtual (opcional) executando:

```bash
pip install -r mnt/data/requirements.txt
```

Para o OCR, é necessário ter o [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) instalado e disponível no `PATH` do sistema.

### Uso

```bash
python mnt/data/capture_and_send.py --webhook "https://seu-webhook.n8n.cloud/webhook" \
    --region 100 200 600 300 --cooldown 1.5
```

- `--webhook`: URL do webhook do n8n (ou defina a variável de ambiente `WEBHOOK_URL`).
- `--region`: (opcional) região a capturar em pixels: `LEFT TOP WIDTH HEIGHT`.
- `--cooldown`: (opcional) atraso em segundos antes da captura, útil para preparar a tela.
- `--image`: nome do arquivo de saída para a captura (padrão `screenshot.png`).
- `--dry-run`: executa a captura e OCR, mas não envia dados ao webhook.

Ao finalizar, o script exibirá o texto bruto reconhecido, o número detectado e, se configurado, enviará os dados para o webhook informado.
