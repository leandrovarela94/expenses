# Imagem base
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Expor a porta 8000
EXPOSE 8000

# Copia os arquivos Pipfile e Pipfile.lock para o diretório de trabalho
COPY . /app

# Instalação do Python e de suas dependências
RUN apt-get update
# RUN apt-get install -y python3-dev default-libmysqlclient-dev build-essential

# Instala o pipenv
RUN pip install pip --upgrade
RUN pip install pipenv

# Instala as dependências do projeto

COPY . .

RUN pipenv install --system --deploy

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]