# ADA GitLab API

![Ada_logo_horizontal](https://user-images.githubusercontent.com/22121504/56839465-006c8200-6859-11e9-8feb-ad76c573b844.png)

[![pipeline status](https://gitlab.com/adabot/ada-gitlab/badges/devel/pipeline.svg)](https://gitlab.com/adabot/ada-gitlab/commits/devel)
[![coverage report](https://gitlab.com/adabot/ada-gitlab/badges/devel/coverage.svg?job=unit-test)](https://gitlab.com/adabot/ada-gitlab/commits/devel)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Sobre o Projeto

Microsserviço responsável por realizar requisições do GitLab e encaminhá-las para o [Bot](https://github.com/fga-eps-mds/2019.1-ADA).

## Contribuindo

Para colaborar com o projeto, siga o [Guia de Contribuição](https://github.com/fga-eps-mds/2019.1-ADA/blob/master/CONTRIBUTING.md)

## Executando a API localmente
#### Pré-requisitos
##### Instale o Docker
Seguindo as instruções dos links a seguir, instale o docker conforme seu sistema operacional.

* [docker](https://docs.docker.com/install/)
* [docker-compose](https://docs.docker.com/compose/install/#install-compose) (já incluído na instalação do Docker Desktop para MacOS)

##### Obtenha seu token de acesso a API do GitLab
Para obter seu token de acesso, você deve fazer um POST à /oauth/token com os seguintes parâmetros, substituindo user@example.com e secret pelos seus respectivos.

```sh
{
  "grant_type"    : "password",
  "username"      : "user@example.com",
  "password"      : "secret"
}
```

Um exemplo:

```sh
echo 'grant_type=password&username=<your_username>&password=<your_password>' > auth.txt
curl --data "@auth.txt" --request POST https://gitlab.example.com/oauth/token

```

E então você receberá seu token de acesso na resposta:

```sh
{
  "access_token": "1f0af717251950dbd4d73154fdf0a474a5c5119adad999683f5b450c460726aa",
  "token_type": "bearer",
  "expires_in": 7200
}
```

Você pode encontrar mais informações em [GitLab as an OAuth2 provider | GitLab](https://docs.gitlab.com/ee/api/oauth2.html#resource-owner-password-credentials-flow).

##### Exporte seu token de acesso
Exporte seu token de acesso conforme o comando a seguir, substituindo-o em GITLAB_TOKEN.

```sh
export GITLAB_API_TOKEN='GITLAB_TOKEN'
```

##### Exporte as variáveis do banco

```sh
export DB_NAME=api
export DB_URL=mongodb://mongo-gitlab:27010/api
```

##### Execute o Docker
Execute o Docker a partir do seguinte comando:

```sh
docker-compose -f docker-compose-dev.yml up --build
```

## Licença

[GPL](https://opensource.org/licenses/GPL-3.0)
