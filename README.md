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
| Mascote | **Pico**, pequeno explorador voador em pixel art que investiga, aponta e participa das cenas |
| Narração | **Thalita**, em português brasileiro, com expressão e clareza; gravações de Emanuel são usadas quando enviadas |
| Visual | Azul escuro, verde água e dourado; fotografias em movimento, filmagens reais e pixel art animada |
| Moldura | Persistente em imagens e filmagens |
| Formato | YouTube horizontal, Full HD e **16:9**, com duração próxima de oito minutos |
| Imagens | Todas as imagens geradas em **16:9** |

[Identidade completa e próximas pautas](docs/canal.md) · [Perfil e capa do canal](docs/identidade/README.md) · [Descrição pronta do canal](docs/descricao-do-canal.txt)

## Episódio em destaque

**Quem decidiu que o dia tem 24 horas? — 8min24s, 1080p, 16:9.**

![Miniatura do episódio](videos/ep-002-24-horas/miniatura.jpg)

Uma viagem dos relógios de sombra aos átomos, com 69 cenas, filmagens reais, fotos de acervos, pixel art, a voz Thalita e o Pico.

- [Vídeo e pacote para publicar](videos/ep-002-24-horas/PUBLICAR.md)
- [Título do vídeo](videos/ep-002-24-horas/titulo.txt)
- [Descrição com capítulos, fontes e créditos](videos/ep-002-24-horas/descricao.txt)
- [Todos os episódios](videos/README.md), incluindo o episódio sobre a geladeira

## Como pedir um vídeo

Envie neste chat:

> Crie o próximo vídeo do Quase Infinito e entregue no Projeto-criador-solo- com os materiais para eu publicar.

Também é possível informar um tema. Cada episódio recebe pesquisa, roteiro, narração, cenas, montagem e conferência. A produção é iniciada pelo pedido no chat. Emanuel faz a publicação no YouTube.

## Entrega de cada episódio

A pasta videos/ep-NNN-tema contém:

- video.mp4: arquivo final com narração e imagens.
- miniatura.jpg e miniatura.png: miniatura pronta em 16:9; o JPG também atende ao limite de tamanho para envio por celular.
- titulo.txt: título principal e alternativas.
- descricao.txt: texto para colar no YouTube, com capítulos, fontes e créditos.
- metadata.json: título, descrição, tags, hashtags, idioma e categoria.
- legendas.srt: legendas sincronizadas com a narração.
- roteiro.md e narracao.txt: roteiro de produção e texto falado.
- fontes.md: referências e procedência dos materiais.
- qa.json e checksums.sha256: verificação técnica e integridade dos arquivos.
- PUBLICAR.md: links dos arquivos e instruções de envio.

O vídeo só deve ser anunciado como entregue depois que o MP4 e os materiais estiverem acessíveis no GitHub. Arquivos acima do limite do Git comum precisam ser distribuídos por uma Release; o assistente deve conferir a ferramenta de upload disponível antes de prometer esse caminho. O histórico Git não deve acumular arquivos intermediários ou modelos de voz.

## Recursos

O roteiro e as decisões são feitos no chat. A narração usa edge-tts, que acessa um serviço externo de voz e precisa de internet; sua disponibilidade é verificada em cada produção. Não é usada uma chave de API da OpenAI para o roteiro feito neste chat. Não é necessário conectar o YouTube ou cadastrar credenciais de publicação.

FFmpeg monta o vídeo no ambiente de produção. GitHub guarda o projeto e as entregas. GitHub Actions executa apenas verificações do código e da configuração.

## Utilitários de produção

O episódio atual contém os scripts usados na produção, o roteiro por cena, as referências das mídias e as versões das dependências em [producao](videos/ep-002-24-horas/producao/README.md).

    python -m pip install -r videos/ep-002-24-horas/producao/requirements.txt
    python videos/ep-002-24-horas/producao/prepare_media.py
    python videos/ep-002-24-horas/producao/prepare_voice.py
    python videos/ep-002-24-horas/producao/render.py --workers 3
    python videos/ep-002-24-horas/producao/package.py

A renderização usa FFmpeg, fontes DejaVu e acesso à internet para baixar as mídias e sintetizar a voz. A conferência geral da entrega continua disponível em scripts/package_episode.py. O padrão de 24 fps acompanha o vídeo de referência aprovado; a tolerância de duração é de 30 segundos em torno de oito minutos. O limite de envio mantém margem abaixo do limite de arquivos do GitHub e preserva a qualidade do MP4.

## Referências técnicas

- [edge-tts: instalação e uso](https://github.com/rany2/edge-tts)
- [Vozes do Microsoft Speech](https://learn.microsoft.com/pt-br/azure/ai-services/speech-service/language-support)
- [Limites de arquivos no GitHub](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)
- [Condições de uso dos GitHub Actions](https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features)



