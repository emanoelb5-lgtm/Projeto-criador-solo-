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

**Como a geladeira mudou o que você come — 8min04s, 1080p, 16:9.**

O episódio atual combina 69 cenas, filmagens reais, arquivo histórico de 1919, pixel art, voz Thalita, Pico e a moldura do canal.

- [Vídeo e pacote atual para publicar](videos/ep-001-geladeira/PUBLICAR.md)
- [Título do vídeo](videos/ep-001-geladeira/publicacao-quase-infinito/titulo.txt)
- [Descrição com capítulos e créditos](videos/ep-001-geladeira/publicacao-quase-infinito/descricao.txt)

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

    python -m pip install -r requirements-production.txt
    python scripts/check_setup.py
    python scripts/generate_narration.py --text-file videos/ep-001-geladeira/narracao.txt --output-dir work/ep-001-geladeira
    python scripts/assemble_video.py --episode videos/ep-001-geladeira --work-dir work/ep-001-geladeira
    python scripts/prepare_delivery.py --episode videos/ep-001-geladeira --work-dir work/ep-001-geladeira
    python scripts/package_episode.py --episode videos/ep-001-geladeira

Os utilitários recebem o roteiro, as imagens e o storyboard preparados pelo assistente. Eles não escolhem pautas nem escrevem roteiros por conta própria.

## Referências técnicas

- [edge-tts: instalação e uso](https://github.com/rany2/edge-tts)
- [Vozes do Microsoft Speech](https://learn.microsoft.com/pt-br/azure/ai-services/speech-service/language-support)
- [Limites de arquivos no GitHub](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)
- [Condições de uso dos GitHub Actions](https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features)


