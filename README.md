# Projeto Criador Solo

Sistema em preparação para pesquisar assuntos, escrever roteiros, montar vídeos de oito minutos e publicá-los no YouTube. A meta de capacidade é dois vídeos por dia, em Full HD e proporção 16:9; o ritmo será confirmado com produções de teste.

**Estado atual:** configuração inicial. Este repositório contém o guia, a configuração proposta, um assistente de autorização do YouTube e uma verificação sem chamadas externas. A produção, a publicação e o agendamento automático ainda serão implementados.

## Onde cada parte funciona

| Parte | Responsável |
|---|---|
| Desenvolvimento e ajustes | Emanuel e ChatGPT |
| Execução programada, montagem e verificações | GitHub Actions com Python e FFmpeg |
| Roteiros, narração e imagens geradas | Serviços de IA; a primeira integração proposta usa chave da OpenAI API |
| Upload e horário de publicação | YouTube Data API, com autorização do proprietário do canal |

O repositório está público. Os executores padrão do GitHub Actions em repositórios públicos não têm cobrança de minutos, mas continuam sujeitos aos limites e termos do serviço. Armazenamento, executores maiores e serviços externos têm regras de cobrança próprias.

Na modalidade com chave da OpenAI API, as chamadas são cobradas por uso. A assinatura usada nesta conversa não é automaticamente aplicada às chamadas dessa chave. Existe uma integração oficial para usar planos ChatGPT em aplicações elegíveis, mas ela tem requisitos próprios e não oferece a geração de imagens e as APIs de áudio necessárias a toda esta produção. O uso em serviços hospedados remotamente também tem condições específicas; ele não foi configurado neste projeto.

## 1. Definir o canal e o orçamento

Informe o link do canal, o nicho, os dois horários desejados e o teto mensal que pretende gastar com IA. Os valores não secretos ficarão em `config/channel.json`.

Já estão propostas estas metas: português do Brasil, 480 segundos, 1920 × 1080 e dois vídeos por dia. Tema, canal, orçamento e horários ficam pendentes até serem definidos. A automação permanece desativada nesta fase.

## 2. Configurar a IA

1. Acesse a [OpenAI Platform](https://platform.openai.com/).
2. Crie um projeto exclusivo para esta produção, confira as condições de cobrança e configure saldo/faturamento conforme o orçamento escolhido. Na fase inicial, mantenha a recarga automática desligada.
3. Crie uma chave de API no projeto, pela [página de chaves](https://platform.openai.com/api-keys).
4. Abra os [Secrets deste repositório](https://github.com/emanoelb5-lgtm/Projeto-criador-solo-/settings/secrets/actions).
5. Clique em **New repository secret**. Em **Name**, escreva `OPENAI_API_KEY`; em **Secret**, cole a chave e salve.

Guarde a chave somente em Secrets. Não a publique em arquivos, issues ou mensagens. O programa terá seu próprio controle de consumo; alertas de faturamento não devem ser tratados como uma garantia de interrupção imediata dos gastos.

## 3. Autorizar o YouTube

1. Abra o [Google Cloud Console](https://console.cloud.google.com/) e crie um projeto para o Criador Solo.
2. Ative a **YouTube Data API v3**.
3. Configure o aplicativo na **Google Auth Platform**, incluindo o nome e o e-mail de suporte. Para os testes, adicione o e-mail proprietário do canal aos usuários de teste.
4. Crie um cliente OAuth do tipo **Desktop app / Aplicativo para computador** e baixe o JSON de credenciais. Uma chave simples de API não autoriza uploads no seu canal.
5. Faça a autorização inicial no seu computador com o assistente deste projeto. Ele abrirá a tela oficial do Google e salvará a credencial localmente. Selecione a conta que possui o canal de destino.

Com Python 3.10 ou superior instalado, baixe ou clone este repositório, abra o terminal na pasta do projeto e execute:

```powershell
py -m pip install -r requirements-setup.txt
py scripts/authorize_youtube.py --client-file "C:\caminho\credenciais-baixadas.json"
```

No Linux ou macOS, substitua `py` por `python3` e use o caminho local correspondente.

O resultado será `.secrets/youtube_oauth.json`. Abra esse arquivo **no seu computador** e cole o conteúdo inteiro em um novo GitHub Secret chamado `YOUTUBE_OAUTH_JSON`, na mesma tela usada para a chave de IA. Não envie esse arquivo ao repositório público ou à conversa. O assistente solicita autorização de upload e leitura do canal; o programa futuro verificará a identidade do canal antes de publicar.

Em OAuth externo com status **Testing / Em teste**, a credencial de renovação para esse acesso normalmente expira após sete dias. Depois dos testes, a configuração de produção e eventuais requisitos de verificação do Google precisam ser concluídos para a operação contínua. Mesmo em produção, a conexão poderá precisar ser refeita se for revogada ou invalidada.

## 4. Conferir a configuração

Abra **Actions → Verificar configuração → Run workflow**.

O relatório confere os campos de configuração e o formato das credenciais sem mostrar os segredos, chamar a IA ou publicar vídeos. Credenciais com formato correto ainda precisam ser testadas contra os serviços; um relatório aprovado não comprova saldo, permissões ou conexão válida.

## Próxima implementação

Depois de definir o canal e o orçamento: geração de roteiro com fontes, narração, seleção de mídias com direitos de uso compatíveis, cenas em 16:9, legendas, montagem com movimento, miniatura, validação, upload e publicação agendada. O controle de custo, a identificação de episódios e a recuperação de falhas precisam estar funcionando antes do ritmo de dois vídeos por dia.

## Documentação oficial consultada

- [GitHub Actions: cobrança](https://docs.github.com/en/billing/concepts/product-billing/github-actions)
- [GitHub Actions: Secrets](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets)
- [OpenAI API: início](https://developers.openai.com/api/docs/quickstart)
- [OpenAI API: preços](https://developers.openai.com/api/docs/pricing)
- [Uso de planos ChatGPT em apps elegíveis](https://developers.openai.com/siwc/token-sharing-open-source)
- [Limitações dessa integração](https://developers.openai.com/siwc/token-sharing-open-source/preview-limitations)
- [YouTube: autorização](https://developers.google.com/youtube/v3/guides/authentication)
- [Google: OAuth e validade das credenciais](https://developers.google.com/identity/protocols/oauth2)

Orientações verificadas em 9 de outubro de 2026.
