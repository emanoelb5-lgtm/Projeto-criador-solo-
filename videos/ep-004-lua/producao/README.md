# Produção do episódio 004

**Por que o Lua parece seguir você? | Quase Infinito**

69 cenas, 8min24s, 1920 × 1080, 24 fps. A narração usa a voz aprovada pt-BR-ThalitaMultilingualNeural, com variação pequena de cadência e pausas. Filmagens reais, uma fotografia em movimento, diagramas em pixel art, moldura persistente e o Pico acompanham a história.

## Reproduzir

Requer Python 3.12, FFmpeg com libx264 e fontes DejaVu em /usr/share/fonts/truetype/dejavu/. Os serviços externos de mídia e voz precisam estar disponíveis.

    python -m pip install -r videos/ep-004-lua/producao/requirements.txt
    python videos/ep-004-lua/producao/prepare_media.py
    python videos/ep-004-lua/producao/prepare_voice.py
    python videos/ep-004-lua/producao/render.py --workers 3
    python videos/ep-004-lua/producao/package.py

A miniatura JPG e PNG fica na pasta do episódio. Os resultados aparecem em producao/output; package.py prepara os materiais e valida a entrega com scripts/package_episode.py.

## Arquivos

- episode.json: roteiro original por bloco, cenas e ação do Pico.
- research_sources.json e FONTES.md: referências primárias e afirmações verificadas.
- prepare_voice.py: geração da narração Thalita e tempos das palavras.
- prepare_media.py e media_requests.json: download das mídias licenciadas.
- media_sources.json: autoria, licença, procedência, resolução e hashes.
- base_art.py: desenho estabelecido do Pico, paleta e fontes.
- pixel_art.py: diagramas e animações originais, moldura e legendas fixas.
- render.py: montagem com cache atômico, trilha original, normalização da voz e conferência integral.
- package.py: arquivos de publicação, metadados, relatórios e ZIP.

Os diagramas de paralaxe e órbitas ampliam deslocamentos, sem escala real. A sensação de ser seguido e a ilusão da Lua no horizonte são explicadas separadamente. A montagem inclui somente vídeo e áudio no MP4. As legendas são desenhadas nas imagens, e o verificador rejeita uma segunda faixa embutida. O SRT é uma transcrição separada.

O MP4 entregue é identificado pelo SHA-256 no relatório. Regenerar uma voz ou baixar novamente uma mídia pode mudar os bytes se um serviço externo for atualizado. Os intermediários e as mídias brutas não entram no histórico Git. O fluxo prepara a publicação manual e não envia arquivos ao YouTube.

[Publicar](../PUBLICAR.md) · [Fontes](../fontes.md) · [Verificação](../qa.json)
