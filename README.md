# Projeto Criador Solo

Produção de vídeos iniciada por comando no ChatGPT Work. Emanuel pede uma produção; o ChatGPT pesquisa, escreve o roteiro e conduz a montagem com as ferramentas disponíveis. A meta é entregar vídeos de oito minutos, em português e Full HD 16:9, até a publicação quando houver uma integração de upload conectada.

**Estado atual:** base de configuração. Existem um guia, um assistente de autorização do YouTube e uma verificação sem chamadas externas. O fluxo completo de produção e a integração de publicação ainda serão implementados e testados. Nenhum canal está conectado por esta configuração.

## Modo escolhido: comando nesta conversa

| Parte | Onde funciona |
|---|---|
| Iniciar uma produção | Emanuel envia o comando no ChatGPT Work |
| Pesquisa, roteiro e decisões de edição | ChatGPT nesta conversa, com o uso do plano |
| Montagem e verificação | Ferramentas de execução disponíveis ao trabalho; processamento externo pode ser necessário conforme o vídeo |
| Código e arquivos editáveis | Este repositório |
| Publicação | Integração de upload do YouTube, autorizada para o canal correto |

Não é necessário criar uma chave da OpenAI API para usar o modelo desta conversa na pesquisa e no roteiro. Ferramentas ou serviços externos que venham a ser escolhidos, inclusive para voz ou processamento, podem ter custos próprios.

Cada pedido inicia um trabalho. É possível repetir os pedidos conforme os limites do plano, a complexidade das produções e a disponibilidade das ferramentas. A meta de dois vídeos por dia precisa ser medida em testes e não representa uma capacidade já confirmada. Este modo não define uma agenda que execute a produção sem um novo comando.

## Comando de exemplo

> Produza um vídeo de oito minutos sobre [tema], em português e 16:9, com roteiro original e fontes, narração, pixel art animada, cenas relacionadas à fala, legendas e miniatura. Publique no canal conectado e entregue o MP4 e o link final. Se a conexão de publicação estiver indisponível, entregue o MP4 e informe a etapa pendente.

A narração pode usar um áudio enviado por Emanuel ou um mecanismo de voz que esteja configurado. Este projeto ainda não tem um gerador de voz integrado.

## O que Emanuel precisa informar agora

1. O link do canal que receberá os vídeos.
2. O nicho ou o tema da primeira produção.
3. A preferência de narração: áudio gravado por Emanuel ou voz sintetizada.

O próximo teste precisa validar a produção, a reprodução do MP4 e uma integração efetiva de publicação. Uma credencial guardada no GitHub não fica automaticamente acessível ao ChatGPT; GitHub Secrets não expõe seu conteúdo pela conexão de repositórios. A forma de conectar o upload ao ambiente que executará essa etapa ainda precisa ser definida.

## Assistente de autorização do YouTube

O assistente local está disponível para a opção de integração por OAuth:

1. Abra o [Google Cloud Console](https://console.cloud.google.com/) e crie um projeto para o Criador Solo.
2. Ative a **YouTube Data API v3**.
3. Configure o aplicativo na **Google Auth Platform**, incluindo o nome e o e-mail de suporte. Durante os testes, inclua o e-mail proprietário do canal nos usuários de teste.
4. Crie um cliente OAuth do tipo **Desktop app / Aplicativo para computador** e baixe o JSON.

Com Python 3.10 ou superior instalado, baixe ou clone este repositório e execute na pasta do projeto:

```powershell
py -m pip install -r requirements-setup.txt
py scripts/authorize_youtube.py --client-file "C:\caminho\credenciais-baixadas.json"
```

No Linux ou macOS, substitua `py` por `python3` e use o caminho local correspondente.

O assistente abrirá o consentimento oficial do Google e salvará `.secrets/youtube_oauth.json` no computador. Ele solicita upload e leitura do canal. A conta selecionada precisa ter acesso ao canal de destino.

Mantenha a credencial privada; não a envie à conversa nem ao repositório público. A implantação da integração determinará onde ela ficará disponível de forma segura. Na opção de verificar somente seu formato no GitHub, o conteúdo pode ser cadastrado no Secret `YOUTUBE_OAUTH_JSON`, pelos [Secrets do repositório](https://github.com/emanoelb5-lgtm/Projeto-criador-solo-/settings/secrets/actions). Isso não conecta o upload a esta conversa.

No OAuth externo em **Testing / Em teste**, a credencial de renovação para esse acesso normalmente expira após sete dias. Depois dos testes, a configuração de produção e eventuais requisitos de verificação do Google precisam ser concluídos para a operação contínua. Credenciais revogadas ou invalidadas exigem uma nova conexão.

## Verificação inicial

Abra **Actions → Verificar configuração → Run workflow**.

O relatório confere os campos e o formato das credenciais sem mostrar segredos, chamar IA ou publicar vídeos. No modo `chat_command`, uma chave `OPENAI_API_KEY` e um servidor externo não são exigidos para essa conferência.

Um relatório aprovado não comprova conexão válida, narração disponível, capacidade de renderização ou publicação funcionando. Esses pontos dependem de uma produção completa de teste.

## Papel do GitHub

O GitHub mantém o código, as versões e os testes do projeto. Os termos dos executores hospedados do Actions restringem atividades alheias ao ciclo de desenvolvimento de software. A produção recorrente de vídeos não será colocada nesses executores como uma infraestrutura gratuita de operação.

A configuração mantém `schedule.enabled` como `false`: as produções são iniciadas por mensagem. Imagens geradas e vídeos do canal terão proporção 16:9, conforme solicitado.

## Documentação oficial

- [ChatGPT Work](https://learn.chatgpt.com/docs/get-started-with-work)
- [ChatGPT Work: limites e uso](https://learn.chatgpt.com/docs/pricing)
- [Trabalhos de longa duração](https://learn.chatgpt.com/docs/long-running-work)
- [GitHub Actions: termos](https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features)
- [YouTube: autorização](https://developers.google.com/youtube/v3/guides/authentication)
- [Google: OAuth e validade das credenciais](https://developers.google.com/identity/protocols/oauth2)

Modo por comando adotado em 9 de outubro de 2026.
