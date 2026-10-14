# Quase Infinito

![Capa do canal](docs/identidade/Capa_Quase_Infinito_16x9.jpg)

**Cada pergunta abre outra viagem.**

Canal de Emanuel Bonfim sobre ciência, história, natureza, tecnologia e as surpresas do cotidiano. Perguntas conduzem documentários em português brasileiro, com imagens e vídeos reais, arquivos históricos e pixel art animada.

**Repositório oficial do projeto: `emanoelb5-lgtm/Projeto-criador-solo-`.**

## Identidade do canal

| Elemento | Padrão |
| --- | --- |
| Nome | **Quase Infinito** |
| Proposta | Histórias e descobertas que fazem olhar o mundo com outros olhos |
| Mascote | **Pico v2**, explorador voador com olhos expressivos e acabamento detalhado; a animação 3 usa doze quadros corporais e trajetórias narrativas |
| Narração | **Thalita**, em português brasileiro, com expressão e clareza; gravações de Emanuel são usadas quando enviadas |
| Visual | Azul escuro, verde água e dourado; fotografias em movimento, filmagens reais e pixel art animada |
| Moldura | Persistente em imagens e filmagens |
| Formato | YouTube horizontal, Full HD e **16:9**, com duração próxima de oito minutos |
| Imagens | Todas as imagens geradas em **16:9** |

[Identidade completa e próximas pautas](docs/canal.md) · [Perfil e capa do canal](docs/identidade/README.md) · [Descrição pronta do canal](docs/descricao-do-canal.txt)

## Episódio em destaque

**O que é El Niño? — 8min18s, 1080p, 16:9.**

![Miniatura do episódio](videos/ep-009-el-nino/miniatura.jpg)

O Pico investiga a ligação entre o Pacífico, os ventos e as chuvas. São 54 planos, voz Thalita, cenários novos de oceano, laboratório e propriedade rural, cinco filmagens reais e uma fotografia com movimento. Os modelos explicam alísios, ressurgência, redistribuição de calor, teleconexões, possíveis efeitos no Brasil e a diferença entre El Niño e aquecimento global.

**O Pico agora tem animação corporal por quadros:** asas, braços, pernas, expressão e cachecol mudam, com voos entre regiões do esquema, mergulho, curvas, gestos, reações e despedida. O design v2 foi preservado. **Sem legendas na tela.**

- [Vídeo completo e pacote para publicar](videos/ep-009-el-nino/PUBLICAR.md)
- [Título](videos/ep-009-el-nino/titulo.txt) · [Descrição com capítulos, fontes e créditos](videos/ep-009-el-nino/descricao.txt)
- [Decisões editoriais](videos/ep-009-el-nino/decisoes-editoriais.md)
- [Nova animação do Pico](docs/identidade/Pico_Animacao_v3.md)
- [Todos os episódios](videos/README.md)

## Como pedir um vídeo

Envie neste chat:

> Crie o próximo vídeo do Quase Infinito e entregue no Projeto-criador-solo- com os materiais para eu publicar.

Também é possível informar um tema. Cada episódio recebe pesquisa, roteiro, narração, cenas, montagem e conferência. A produção é iniciada pelo pedido no chat. Emanuel faz a publicação no YouTube.

## Entrega de cada episódio

A pasta videos/ep-NNN-tema contém:

- video.mp4: arquivo final com narração e imagens.
- publicacao.zip: materiais para publicação, áudio da narração, assets do Pico e cenários, prompts e código de produção.
- miniatura.jpg e miniatura.png: miniatura pronta em 16:9; o JPG também atende ao limite de tamanho para envio por celular.
- titulo.txt: título pronto para publicar; alternativas nos metadados e no pacote.
- descricao.txt: texto para colar no YouTube, com capítulos, fontes e créditos.
- metadata.json: título, descrição, tags, hashtags, idioma e categoria.
- legendas.srt: transcrição sincronizada separada; o modo de legendas de cada episódio consta nos metadados. Nos episódios 006, 007, 008 e 009, o arquivo é opcional e o MP4 não tem legendas na tela.
- roteiro.md e narracao.txt: roteiro de produção e texto falado.
- fontes.md: referências e procedência dos materiais.
- qa.json e checksums.sha256: verificação técnica e integridade dos arquivos.
- PUBLICAR.md: links dos arquivos e instruções de envio.

O vídeo só deve ser anunciado como entregue depois que o MP4 e os materiais estiverem acessíveis no GitHub. Arquivos acima do limite do Git comum precisam ser distribuídos por uma Release; o assistente deve conferir a ferramenta de upload disponível antes de prometer esse caminho. O histórico Git não deve acumular arquivos intermediários ou modelos de voz. A preparação preserva a faixa de áudio e exige nova revisão visual quando há compressão. Se a API recusar um arquivo grande, enviar os mesmos bytes em partes menores. O workflow finalizar-entrega.yml recompõe o MP4 e confere o SHA-256 dos metadados antes de disponibilizar o arquivo único. Essa etapa apenas conclui o envio, sem gerar voz, produzir cenas ou recomprimir o vídeo.

## Recursos

O roteiro e as decisões são feitos no chat. A narração usa edge-tts, que acessa um serviço externo de voz e precisa de internet; sua disponibilidade é verificada em cada produção. Não é usada uma chave de API da OpenAI para o roteiro feito neste chat. Não é necessário conectar o YouTube ou cadastrar credenciais de publicação.

FFmpeg monta o vídeo no ambiente de produção. GitHub guarda o projeto e as entregas. GitHub Actions executa apenas verificações do código e da configuração.

## Utilitários de produção

O episódio atual contém os scripts usados na produção, o roteiro por cena, as referências das mídias e as versões das dependências em [producao](videos/ep-009-el-nino/producao/README.md).

    python -m pip install -r videos/ep-009-el-nino/producao/requirements.txt
    python videos/ep-009-el-nino/producao/prepare_media.py
    python videos/ep-009-el-nino/producao/prepare_voice.py
    python videos/ep-009-el-nino/producao/render.py --workers 4
    python videos/ep-009-el-nino/producao/package.py --repo-root . --visual-reviewed

Use a opção de revisão visual somente depois de inspecionar o MP4 final. Rótulos informativos e créditos não são transcrições da narração.

A renderização usa FFmpeg, fontes DejaVu e acesso à internet para baixar as mídias e sintetizar a voz. A conferência geral da entrega continua disponível em scripts/package_episode.py. O padrão de 24 fps acompanha o vídeo de referência aprovado; a tolerância de duração é de 30 segundos em torno de oito minutos. O limite de envio mantém margem abaixo do limite de arquivos do GitHub e preserva a qualidade do MP4.

## Referências técnicas

- [edge-tts: instalação e uso](https://github.com/rany2/edge-tts)
- [Vozes do Microsoft Speech](https://learn.microsoft.com/pt-br/azure/ai-services/speech-service/language-support)
- [Limites de arquivos no GitHub](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)
- [Condições de uso dos GitHub Actions](https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features)
