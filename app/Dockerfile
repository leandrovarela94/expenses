# Imagem base

FROM python:3.11-slim

# Define o diretório de trabalho

WORKDIR /app

# Expor a porta 8000

EXPOSE 8000

# Copia os arquivos Pipfile e Pipfile.lock para o diretório de trabalho

COPY . /app

COPY . /app/.env

# Instalação do Python e de suas dependências

RUN apt-get update

# Adicionado o '&&' para executar o comando de instalação do python3-dev e default-libmysqlclient-dev no mesmo RUN

RUN apt-get install -y python3-dev default-libmysqlclient-dev build-essential

# Instala o pipenv

RUN pip install pip --upgrade

RUN pip install pipenv

# Mudei a localização do comando 'pipenv install --system --deploy' para que ele seja executado depois de todas as dependências instaladas corretamente

# Instala as dependências do projeto

RUN pipenv install --system --deploy

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]