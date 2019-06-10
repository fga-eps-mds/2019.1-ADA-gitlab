## Setando variáveis de ambiente

##### Crie um bot no Telegram

<strong></strong>Observação:</strong></em> Caso você já tenha criado a application conforme o [readme do repositório da AdaBot](https://github.com/fga-eps-mds/2019.1-ADA), não é necessário criar outro. Apenas siga para o passo de exportações de variáveis do bot.

Converse com o [@BotFather do Telegram](https://t.me/BotFather) e crie um bot de teste unicamente seu seguindo as instruções dele.


##### Exporte as variáveis do seu bot
Após escolher um nome para seu bot, o @BotFather lhe dará um token para utilizar para acessar a API do Telegram. Exporte ambos no terminal como a seguir. Substitua o TELEGRAM_ACESS_TOKEN pelo token lhe enviado pelo @BotFather e TELEGRAM_BOT_NAME pelo nome do seu bot.

```sh
export ACCESS_TOKEN='TELEGRAM_ACCESS_TOKEN'
export BOT_NAME='TELEGRAM_BOT_NAME'
```
##### Exporte as variáveis do banco
Variáveis para utilização do banco de dados localmente.

```sh
export DB_NAME=api
export DB_URL=mongodb://mongo-gitlab:27010/api
```

##### Exporte a variável para o webhook do gitlab ser setado

Importe o seu domínio que irá receber posts do gitlab quando pipelines ocorrerem em repositórios cadastrados no bot. Para isso é recomendado um protocolo https por razões de segurança, porém caso você não possua um domínio você também pode colocar essa variável de acordo com a rota do serviço, no caso ``` http://localhost:5000/```. Por exemplo se o seu domínio é ```https://gitlab.meubot.com/```, a exportação ficará assim:
 
 ```sh
export GITLAB_WEBHOOK_URL=https://gitlab.meubot.com/
```

##### Crie uma Application no gitlab

<strong></strong>Observação:</strong></em> Caso você já tenha criado a application conforme o [readme do repositório da AdaBot](https://github.com/fga-eps-mds/2019.1-ADA), não é necessário criar outro. Apenas siga para o passo de exportações de variáveis do app.

Crie uma application no gitlab para a Ada realizar autenticação junto aos usuários, seguindo os passos a seguir:
- No seu perfil do gitlab clique em **Profile Settings** > **Applications** e selecione **New Application**.
- No formulário de registro da aplicação, escolha o nome da sua aplicação e preencha o campo **Redirect URI** com a url ```http://localhost:5000/user/gitlab/authorize```.
- Dentre os scopes disponíveis, selecione _api_ e _read_user_
- Ao clicar em **Save application** o gitlab irá retornar os tokens _Application id_ e _Secret_.

Agora sua application está pronta.

Para maiores informações clique nesse [link da documentação do gitlab](https://docs.gitlab.com/ee/integration/oauth_provider.html#adding-an-application-through-the-profile).


##### Exporte as variáveis do seu app
Após cadastrar um application o gitlab irá disponibilizar dois tokens. Para a execução da Ada é necessário a exportação do Application ID gerado na criação do App, além dessa variável também é preciso de exportar a variável utilizada no Authorization callback URL do app. Exporte ambos no terminal como a seguir. Substitua o APPLICATION_ID e APPLICATION_SECRET pelo _Application_id_ e _Secret_ respectivamente, gerados na criação do app.

```sh
export APP_ID='APPLICATION_ID'
export APP_SECRET='APPLICATION_SECRET'
```

#### Exporte a variável de redirecionamento para cadastro de usuários applications
URL definida para realizar o redirecionamento para o telegram assim que é cadastrado na application do gitlab.

```sh
export REDIRECT_URI=http://localhost:5000/user/gitlab/authorize
```

