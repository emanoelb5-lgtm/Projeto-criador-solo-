# Produção do episódio 002

**Quem decidiu que o dia tem 24 horas? | Quase Infinito**

Estes são os arquivos usados para produzir o episódio final: 69 cenas, 8min24s, 1920 × 1080, 24 fps. A voz é `pt-BR-ThalitaMultilingualNeural`, a mesma referência aprovada no episódio anterior. O Pico e a moldura são desenhados em código e animados durante a renderização.

## Reproduzir

Requer Python 3.12, FFmpeg com libx264 e fontes DejaVu em `/usr/share/fonts/truetype/dejavu/`. Os serviços de mídia e síntese de voz precisam estar disponíveis na internet.

    python -m pip install -r videos/ep-002-24-horas/producao/requirements.txt
    python videos/ep-002-24-horas/producao/prepare_media.py
    python videos/ep-002-24-horas/producao/prepare_voice.py
    python videos/ep-002-24-horas/producao/render.py --workers 3
    python videos/ep-002-24-horas/producao/package.py

Os novos arquivos aparecem na pasta `producao/output`. A miniatura pronta fica na pasta do episódio e é reutilizada pelo empacotador. Regenerar a voz ou baixar novamente uma mídia pode produzir bytes diferentes caso um serviço externo mude; o MP4 entregue é identificado pelo SHA-256 no relatório de verificação.

## Organização

- `episode.json`: texto original e três cenas por bloco narrativo.
- `prepare_voice.py`: síntese por bloco, referência da voz e tempos de palavras.
- `prepare_media.py`: download das oito filmagens e quatro fotos, com origem e licença.
- `media_sources.json`: manifesto das mídias efetivamente utilizadas, incluindo os hashes.
- `pixel_art.py`: 38 cenas explicativas, Pico animado e moldura persistente.
- `render.py`: montagem, narração ajustada à duração, trilha original, legendas, cache atômico e decodificação integral.
- `package.py`: título, descrição, capítulos, créditos, metadados, miniatura, roteiro e ZIP de publicação.

O fluxo usa apenas os materiais deste episódio. Não envia arquivos ao YouTube. Não guarda chaves nem credenciais no repositório. Os downloads e arquivos intermediários não fazem parte do histórico Git.

## Entrega conferida

Além da decodificação integral, a produção conferiu o alinhamento das legendas com os tempos da voz, as proporções das mídias, os capítulos e os créditos. A cadência de 24 fps acompanha a referência aprovada; a meta permanece próxima de oito minutos. O limite de envio do canal mantém margem abaixo do limite de arquivo do GitHub, para conservar o MP4 em Full HD sem compressão adicional desnecessária.

[Fontes](../fontes.md) · [Publicar](../PUBLICAR.md) · [Verificação técnica](../qa.json)
