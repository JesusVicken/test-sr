# Aplicação de Upload de Arquivo com Processamento e Integração de Serviços

Este repositório contém uma aplicação que permite o upload de arquivos JSON e processa os dados de diferentes maneiras. A aplicação é construída com **FastAPI** e integra com **MongoDB**, **MySQL**, e **RabbitMQ** utilizando Docker Compose.

## Estrutura da Aplicação

A aplicação consiste em um backend desenvolvido com **FastAPI** que recebe arquivos JSON, os processa e os salva em bancos de dados. Além disso, a aplicação envia mensagens para o RabbitMQ para orquestrar a integração entre os serviços.

### Componentes

- **FastAPI**: Framework para o backend da aplicação.
- **MongoDB**: Armazenamento de dados JSON enviados via upload.
- **MySQL**: Armazenamento adicional de dados processados.
- **RabbitMQ**: Orquestração de mensagens entre os serviços.

## Requisitos para rodar o projeto

- Docker
- Docker Compose

## Como Rodar a Aplicação

1. **Clone este repositório** para sua máquina local:

   ```bash
   git clone https://github.com/JesusVicken/test-sr
   cd seu-repositorio

2. **Execute o comando abaixo para construir e iniciar os containers necessários:**

    ```bash
    docker-compose up --build



O Docker Compose irá construir os containers definidos no arquivo docker-compose.yml e iniciar os serviços de:

Web (FastAPI)
MongoDB
RabbitMQ
MySQL


3. **Acesse a aplicação: A API estará disponível na URL http://localhost:8000.**

    Documentação da API: A documentação automática da API gerada pelo FastAPI pode ser acessada em http://localhost:8000/docs.


4. **Endpoints**
    POST /upload/
        Descrição: Endpoint para upload de arquivos JSON.
        Formato do arquivo: O arquivo deve ser no formato JSON.
Respostas:
    200 OK: Arquivo processado com sucesso.
    400 Bad Request: Se o arquivo não for JSON ou estiver vazio.
    500 Internal Server Error: Se ocorrer um erro ao processar o arquivo.

    FASTAPI - http://localhost:8000/docs#/ 
    RABBITMQ - http://localhost:15672/  usuário: root pass: root


**Exemplo de Upload**
    Você pode testar o upload utilizando ferramentas como Postman ou Insomnia.

    Selecione o método POST e envie o arquivo JSON para http://localhost:8000/upload/.

    Exemplo de conteúdo JSON esperado:

    
### Exemplo de conteúdo JSON esperado:

    ```json
    [
    {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "age": 30
    },
    {
        "name": "Jane Smith",
        "email": "jane.smith@example.com",
        "age": 25
    }
    ]

   


5. **Variáveis de Ambiente**

As variáveis de ambiente são definidas no Docker Compose e incluem configurações para o MySQL, RabbitMQ e MongoDB:

MYSQL_HOST: Host do MySQL (definido como mysql no Docker Compose).
MYSQL_USER: Usuário do MySQL (definido como root).
MYSQL_PASSWORD: Senha do MySQL (definida como root).
MYSQL_DB: Nome do banco de dados (definido como users_db).
RABBITMQ_HOST: Host do RabbitMQ (definido como rabbitmq).
RABBITMQ_USER: Usuário do RabbitMQ (definido como root).
RABBITMQ_PASSWORD: Senha do RabbitMQ (definida como root).
MONGO_URI: URI de conexão com o MongoDB (definido como mongodb://mongodb:27017/).
Banco de Dados MySQL
O banco de dados MySQL é inicializado com o schema e dados padrão. Se necessário, edite o arquivo init.sql para personalizar o banco de dados.

6. **Logs**

Os logs da aplicação serão gerados no diretório app/logs/. Verifique o arquivo app.log para detalhes sobre o processamento de arquivos e eventuais erros.