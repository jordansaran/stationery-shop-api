<p align="center">
    <h2 align="center">
        Papelaria API
    </h2>
    <a href="https://github.com/jordansaran/stationery-shop-api/actions">
      <img alt="Tests Passing" src="https://github.com/jordansaran/stationery-shop-api/workflows/stationery-shop-api-test-coverage/badge.svg" />
    </a>
    <a href="https://codecov.io/gh/jordansaran/sales-api">
      <img src="https://codecov.io/gh/jordansaran/stationery-shop-api/branch/main/graph/badge.svg" />
    </a>
    <a href="https://github.com/jordansaran/stationery-shop-api/issues">
      <img alt="Issues" src="https://img.shields.io/github/issues/jordansaran/stationery-shop-api?color=0088ff" />
    </a>
    <a href="https://github.com/jordansaran/stationery-shop-api/pulls">
      <img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/jordansaran/stationery-shop-api?color=0088ff" />
    </a>
</p>

Foi desenvolvido uma API onde seu objetivo é a venda de produtos de uma papelaria

# 1.Instalação
Certifique-se de utilizar a última versão do código fonte, que normalmente fica na branch "main"(principal) do repositório do github.
Logo abaixo é apresentado opções de instalação de ambiente, sendo:
1. Ambiente Virtual(env)
2. Docker

````shell
# clone o repositório
$ git clone https://github.com/jordansaran/stationery-shop-api.git
$ cd stationery-shop-api
````

## 1.1. Criar ambiente virtual
Crie um virtualenv em ambiente Unix e ative-o:
````shell
$ python3 -m venv venv
$ . venv/bin/activate
````
Ou no Windows cmd:
````shell
$ python3 -m venv venv
$ venv\Scripts\activate.bat
````
Instalando bibliotecas e suas dependências realcionados a API.  
````shell
$ pip install -r requirements.txt
````

## 1.2. Docker

Para replicar o ambiente de desenvolvimento e colocar em execução a API, execute o comando logo abaixo. 
Destacando que é necessário que seu ambiente de desenvolvimento possua [**Docker**](https://www.docker.com/products/docker-desktop/) instalado.
```
docker-compose up stationery-shop-api
```
### Observações
A url de acesso a API é **http://127.0.0.1:8000/**, caso deseje alterar a porta de acesso modifique
o arquivo **docker-compose.yml** no parametro **ports** (8000:8000) e o arquivo **Dockerfile** na linha 22 referente ao EXPOSE.

# 2. Inicializar API
Antes de executar a API crie um arquivo **.env** na raiz do projeto caso ele não tenha sido criado, para servir de referência
o arquivo **.env.example** demonstra a estrutura necessário para o arquivo **.env**.
O arquivo deve conter os seguintes variáveis de ambiente.
````dotenv
DEBUG=1
ALLOWED_HOSTS=['*']
SECRET_KEY=development
````
A variável **SECRET_KEY** deve conter um hash que será utilizado quando a API for utilizada em **production**.
A variável **DEBUG** deve possuir os valores 1 ou 0 para referenciar a condição de **True** ou **False** para
executar aplicação em modo **DEBUG**.
A variável **ALLOWED_HOSTS** é utilizada para destacar os domíniosda aplicação.
## 2.1. Terminal
Antes de executar o comando de execução da API, é necessário criar o banco de dados. Execute o comando logo abaixo.
````shell
$ python manage.py migrate
````
Para inserir seeders(fixtures) no seu banco de dados, execute o seguinte comando:
````shell
$ python manage.py loaddata users.json
$ python manage.py loaddata people.json
$ python manage.py loaddata sellers.json
$ python manage.py loaddata customers.json
$ python manage.py loaddata commissions.json
$ python manage.py loaddata sales.json
$ python manage.py loaddata items.json
````

````shell
$ python manage.py runserver 0.0.0.0:8000
````

**Caso ocorra erro ao utilizar o termo python, subistitua por python3.**

## 2.2. Docker
Apenas execute o seguinte comando para inicializar o container da aplicação via terminal ou IDE para inseir os seeders dentro do banco de dados.
````shell
$ docker-compose start stationery-shop-api
````

# Documentação

Abra http://127.0.0.1:8000/ em seu navegador para acessar a documentação da API.
Caso deseje visualizar outra forma de documentação
1. http://127.0.0.1:8000/redoc
2. http://127.0.0.1:8000/swagger

# Teste/Coverage
Executar com coverage report:
````shell
$ coverage run -m pytest
$ coverage report
$ coverage html  # abrir htmlcov/index.html em um navegador
````