# Produção do episódio 007

**Por que um navio de aço flutua, mas um prego afunda? | Quase Infinito**

52 planos com durações variáveis, 8min06s, Full HD 1920 × 1080 e 24 fps. Voz Thalita e Pico v2. Este episódio não tem legendas na tela; o SRT separado é uma transcrição opcional. Moldura, créditos e rótulos científicos permanecem.

Três novos cenários de pixel art — porto, oficina e fundo do mar — acompanham modelos originais de pressão, deslocamento de água, forma do casco, carga, inundação e lastro. Há cinco filmagens reais e uma fotografia com movimento. As experiências e o exemplo numérico são ilustrados. Há movimentos de câmera, reflexos, carga, água nos tanques e do Pico. quality_editorial.md registra as escolhas de qualidade. art_direction.json registra os prompts e o modo da geração de imagem.

## Reproduzir

Requer Python 3.12, FFmpeg com libx264, fontes DejaVu, internet e as dependências de requirements.txt. As miniaturas ficam na pasta do episódio. Mídias brutas e cache ficam fora do histórico Git. Os segmentos de voz congelados e a voz completa sem trilha estão no ZIP.

    python -m pip install -r videos/ep-007-navio/producao/requirements.txt
    python videos/ep-007-navio/producao/prepare_media.py
    python videos/ep-007-navio/producao/prepare_voice.py
    python videos/ep-007-navio/producao/render.py --workers 4
    python videos/ep-007-navio/producao/package.py --repo-root . --visual-reviewed

Antes do último comando, inspecione os quadros finais. Os MP4 são fechados e validados em arquivos temporários antes de copiar os bytes completos. O validador geral confere voz, formato, duração, transcrição, miniatura, capítulos e decodificação integral. A opção de revisão visual só deve ser usada depois da inspeção real.

FONTES.md documenta os limites dos modelos e a procedência dos materiais. Regenerar a voz ou baixar mídias alteradas pelo provedor pode mudar o resultado. Emanuel faz a publicação manual no YouTube.

[Publicação](../PUBLICAR.md) · [Fontes](../fontes.md) · [Verificação](../qa.json)
