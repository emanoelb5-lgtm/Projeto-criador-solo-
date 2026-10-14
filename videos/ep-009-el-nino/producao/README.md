# Produção do episódio 009

**O que é El Niño? | Quase Infinito**

54 planos com durações variáveis, 8min18s, Full HD 1920 × 1080 e 24 fps. Voz Thalita e Pico v2. Este episódio não tem legendas na tela; o SRT separado é uma transcrição opcional. Moldura, créditos e rótulos científicos permanecem.

Três novos cenários — Pacífico, laboratório e propriedade rural — acompanham modelos originais de ventos, águas superficiais, ressurgência, nuvens, teleconexões e monitoramento. Há cinco filmagens reais e uma fotografia com movimento. Os mapas usam contornos Natural Earth. O Pico v2 usa uma nova folha de doze quadros: voar, acenar e apontar, com asas, membros, expressão e cachecol animados. As trajetórias incluem voos entre regiões do esquema, mergulho, curvas, gestos e despedida. Os exemplos numéricos e as curvas são conceituais e identificados. quality_editorial.md registra as escolhas de qualidade. art_direction.json registra os prompts e o modo da geração de imagem.

## Reproduzir

Requer Python 3.12, FFmpeg com libx264, fontes DejaVu, internet e as dependências de requirements.txt. As miniaturas ficam na pasta do episódio. Mídias brutas e cache ficam fora do histórico Git. Os segmentos de voz congelados e a voz completa sem trilha estão no ZIP.

    python -m pip install -r videos/ep-009-el-nino/producao/requirements.txt
    python videos/ep-009-el-nino/producao/prepare_media.py
    python videos/ep-009-el-nino/producao/prepare_voice.py
    python videos/ep-009-el-nino/producao/render.py --workers 4
    python videos/ep-009-el-nino/producao/package.py --repo-root . --visual-reviewed

Antes do último comando, inspecione os quadros finais. Os MP4 são fechados e validados em arquivos temporários antes de copiar os bytes completos. O validador geral confere voz, formato, duração, transcrição, miniatura, capítulos e decodificação integral. A opção de revisão visual só deve ser usada depois da inspeção real.

FONTES.md documenta os limites das ilustrações e a procedência dos materiais. Regenerar a voz ou baixar mídias alteradas pelo provedor pode mudar o resultado. Emanuel faz a publicação manual no YouTube.

[Publicação](../PUBLICAR.md) · [Fontes](../fontes.md) · [Verificação](../qa.json)
