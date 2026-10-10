# Produção por comando neste chat

O usuário autorizou o assistente a decidir nome, nicho, pautas, voz e montagem e a disponibilizar as entregas no GitHub. O usuário faz a publicação no YouTube.

## Referência oficial do projeto

Usar exclusivamente `emanoelb5-lgtm/Projeto-criador-solo-` para este projeto. O usuário corrigiu expressamente o repositório em 9 de outubro de 2026. Este canal se chama **Quase Infinito**. Não tratar `Canal-YouTube-` como repositório deste projeto.

Leia config/channel.json e docs/canal.md antes de produzir. Temas: ciência, história, natureza, tecnologia e cotidiano. Idioma: pt-BR. Todas as imagens, miniaturas e cenas devem ter proporção 16:9.

A voz padrão é Thalita (`pt-BR-ThalitaMultilingualNeural`), expressiva e clara. Se o usuário enviar sua narração, usá-la. O mascote recorrente é Pico, um explorador voador em pixel art que participa da narrativa. Combinar imagens e filmagens reais da internet com pixel art animada; manter moldura persistente. Usar storytelling, perguntas e descobertas.

Para cada comando de produção:

1. Confira as entregas existentes e escolha uma pauta inédita, ou siga o tema solicitado.
2. Pesquise fontes primárias para afirmações factuais e registre URLs e data de consulta em fontes.md.
3. Escreva um roteiro original e gere narração com a voz definida. Confira termos, datas e pronúncia. Se a voz não funcionar, informe a limitação e não anuncie um vídeo pronto.
4. Crie cenas que ajudem a explicar o assunto. Use a habilidade imagegen para ilustrações; diagramas exatos devem ser construídos em código. Identifique reconstituições históricas.
5. Monte o vídeo em Full HD e 16:9, com duração próxima de oito minutos. Confira áudio, legendas, cenas e a transição final. Quando as legendas estiverem fixas nas imagens, use `subtitle_mode: burned_in`, mantenha o MP4 sem faixa de legenda embutida e apresente o SRT como transcrição separada para evitar texto duplicado.
   Se o usuário pedir um episódio sem legendas na tela, use `subtitle_mode: none`, remova a camada de transcrição dos quadros e exporte sem faixa de legenda embutida. O SRT separado é opcional para o usuário. Rótulos científicos e créditos não são legendas da narração.
6. Execute prepare_delivery.py quando o MP4 ultrapassar o limite de envio configurado. Confira novamente a qualidade visual e o áudio. Execute package_episode.py. Revise título, descrição, capítulos, fontes e créditos.
7. Disponibilize o MP4 e o pacote no GitHub e confira a versão remota antes de dizer que a entrega terminou. Preserve alterações de outros colaboradores e atualize a branch sem force push.

Não envie vídeos ao YouTube. Não peça OAuth do YouTube. Não dependa de um cron em GitHub Actions hospedado para produzir os episódios.

Não apresente arquivos de teste ou trechos como se fossem o episódio completo. Nenhum arquivo deve conter credenciais.


