# ADA GitLab API

[![pipeline status](https://gitlab.com/adabot/ada-gitlab/badges/devel/pipeline.svg)](https://gitlab.com/adabot/ada-gitlab/commits/devel) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Sobre o Projeto

Microsserviço responsável por realizar requisições do GitLab e encaminhá-las para o [Bot](https://github.com/fga-eps-mds/2019.1-ADA).

## Contribuindo

Para colaborar com o projeto, siga o [Guia de Contribuição](https://github.com/fga-eps-mds/2019.1-ADA/blob/master/CONTRIBUTING.md)

## Executando a API localmente

### Pré-requisitos

É necessária a instalação dos seguintes programas:

* [docker](https://docs.docker.com/install/)
* [docker-compose](https://docs.docker.com/compose/install/#install-compose)

Exporte as variáveis de ambiente da API do GitLab:

```sh
- GITLAB_API_TOKEN='GITLAB_TOKEN'
- GITLAB_SERVICE_URL='http://<URL_API>:5000/'
``` 

Utilizando o Docker

* Execute o comando:

```sh
docker-compose -f docker-compose-dev.yml up --build
```

## Licença

[GPL](https://opensource.org/licenses/GPL-3.0)