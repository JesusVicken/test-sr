🚀 Projeto com Docker Compose

Este projeto utiliza Docker Compose para orquestrar os serviços necessários.

📌 Pré-requisitos

Certifique-se de ter instalado na sua máquina:

Docker

Docker Compose

🔥 Como subir o projeto

Clone este repositório:

git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>

Suba os contêineres com o Docker Compose:

docker-compose up -d

Esse comando executa os serviços em segundo plano.

Verifique se os contêineres estão rodando:

docker ps

Para visualizar os logs em tempo real:

docker-compose logs -f

📦 Como parar e remover os contêineres

Para interromper os serviços e remover os contêineres, execute:

docker-compose down

Se quiser remover volumes persistentes (dados armazenados), use:

docker-compose down -v

🛠️ Como reconstruir os contêineres

Se houver alterações no código ou na configuração, reconstrua os serviços com:

docker-compose up --build -d

🚀 Acesso aos serviços

Caso o projeto tenha uma API ou interface web, ela poderá ser acessada via:

http://localhost:<PORTA>

Substitua <PORTA> pela porta mapeada no docker-compose.yml.

