# PUC Rio - Pós-Graduação em Desenvolvimento Full Stack
### Sprint: Desenvolvimento Back-End Avançado
### Aluno: Izidro Avelino de Queiroz Neto
### Abril/2024

## ToiGet Toilets API

O objetivo da API é fornecer as funções de inclusão, alteração, exclusão e consulta de banheiros, via REST, armazenando as informações via SQLite.

A documentação da API está disponível via Swagger (http://localhost:5000/#/](http://localhost:5000/#/)).

---
## Como executar

Certifique-se de ter o [Docker](https://docs.docker.com/engine/install/) instalado e em execução em sua máquina.

Navegue até o diretório que contém o Dockerfile e o requirements.txt no terminal.
Execute **como administrador** o seguinte comando para construir a imagem Docker:

```
$ docker build -t toilets-api .
```

Uma vez criada a imagem, para executar o container basta executar, **como administrador**, o seguinte comando:

```
$ docker run -p 5000:5000 toilets-api
```

Uma vez executando, para acessar a API, basta abrir o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador. Será apresentada a interface da documentação via Swagger.
