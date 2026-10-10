# Produção do episódio 005

**Por que a chuva tem cheiro? | Quase Infinito**

69 cenas, 8min24s, Full HD 1920 × 1080 e 24 fps. A voz permanece Thalita (pt-BR-ThalitaMultilingualNeural). O episódio combina filmagens reais, duas fotografias em movimento, ilustrações detalhadas em pixel art e esquemas científicos animados.

## Direção de arte

Pico v2 conserva capacete dourado, óculos verde-água, traje turquesa, cachecol coral e asas. O novo desenho traz olhos expressivos, volume, contornos definidos e seis poses coerentes. Há três cenários de pixel art com textura, profundidade e luz. Câmera, chuva, reflexos, folhas e partículas recebem movimento na composição. Moldura persistente e uma única camada de legendas acompanham as cenas.

Os cenários e o Pico são ilustrações geradas com a ferramenta integrada imagegen. art_direction.json, pico_prompt.txt e thumbnail_prompt.txt registram o modo e os prompts. assets contém as referências finais em 16:9.

## Reproduzir no repositório

Requer Python 3.12, FFmpeg com libx264 e fontes DejaVu em /usr/share/fonts/truetype/dejavu/. Voz e mídias usam serviços externos.

    python -m pip install -r videos/ep-005-chuva/producao/requirements.txt
    python videos/ep-005-chuva/producao/prepare_media.py
    python videos/ep-005-chuva/producao/prepare_voice.py
    python videos/ep-005-chuva/producao/render.py --workers 4
    python videos/ep-005-chuva/producao/package.py

As miniaturas JPG e PNG ficam na pasta do episódio. Os resultados vão para producao/output; package.py chama o validador geral scripts/package_episode.py.

## Referências e limites dos esquemas

FONTES.md registra fontes primárias, URL, data, afirmações e procedência das mídias. As gotas, bolhas, bactérias, partículas e colêmbolos são esquemas ampliados, sem escala. O cenário subterrâneo é uma ilustração artística. O papel de aerossóis no cheiro é apresentado como interpretação dos pesquisadores. Petricor e geosmina são distintos.

O MP4 contém apenas vídeo e áudio; as legendas são desenhadas uma vez. O SRT é uma transcrição separada. O verificador rejeita uma segunda faixa embutida e decodifica o vídeo inteiro. MP4s intermediários são fechados antes de copiar os bytes completos, preservando a integridade dos contêineres.

Mídias brutas e cache ficam fora do histórico Git. A voz completa sem trilha e os segmentos originais usados estão no pacote de publicação, para referência e edição. Regenerar a voz ou baixar uma mídia modificada no serviço pode alterar o resultado; hashes identificam os arquivos desta entrega. Emanuel faz a publicação manual.

[Publicação](../PUBLICAR.md) · [Fontes](../fontes.md) · [Verificação](../qa.json)
