# Antes de Ser Normal

**A história e a ciência das coisas que parecem comuns.**

Canal em português brasileiro com documentários de cerca de oito minutos sobre objetos, hábitos e tecnologias do cotidiano. Nome, nicho, pauta e produção são decididos pelo assistente neste chat. O usuário publica os vídeos no YouTube.

## Como pedir um vídeo

Envie neste chat:

> Crie o próximo vídeo do Antes de Ser Normal e entregue no Projeto-criador-solo- com todos os materiais para eu publicar.

Também é possível informar um tema ou pedir um lote. Cada episódio recebe roteiro original, pesquisa, narração, cenas, montagem e conferência. O chat precisa executar a produção: este repositório não é um robô que fica produzindo enquanto o chat está parado. Quantidade e tempo dependem dos recursos disponíveis e da complexidade do episódio.

## Padrão do canal

| Item | Decisão |
|---|---|
| Nome | Antes de Ser Normal |
| Nicho | História e ciência de objetos, hábitos e tecnologias do cotidiano |
| Narração | Antônio Neural, masculino, pt-BR, com ritmo tranquilo e pausas naturais |
| Formato | 1920 × 1080, 16:9, 30 fps, aproximadamente oito minutos |
| Imagens e miniaturas | Sempre 16:9 |
| Publicação | Manual, feita pelo usuário |
| Primeiro tema | Como a geladeira mudou o que você come |

[Conheça a identidade e as próximas pautas](docs/canal.md).

## Primeiro episódio

[Como a geladeira mudou o que você come — vídeo de 8 minutos e pacote para publicar](videos/ep-001-geladeira/PUBLICAR.md).

O pacote inclui MP4 em Full HD, miniatura, descrição, capítulos, tags, roteiro, referências e legendas. Abra PUBLICAR.md para baixar os arquivos.

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
