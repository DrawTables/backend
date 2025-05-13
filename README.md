# DrawTables

## 1. Создание приватного и публичного ключей
### 1.1 Создание папки для сертификатов
```shell
mkdir certs
```
### 1.2 Получение приватного ключа
```shell
cd certs
openssl genrsa -out jwt-private.pem 2048
```

### 1.3 Получение публичного ключа на основе приватного
```shell
cd certs
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```

## 2. Создание переменных окружения
### 2.1 Создание файла ".env" с переменными окружения из шаблона
```shell
cp .env.template .env
```
После создания файла ".env" его необходимо отредактировать,
изменив значения переменных окружения.

### 2.2 Создание файла "docker-compose.env" с переменными окружения из шаблона
```shell
cp ./docker/docker-compose.env.template ./docker/docker-compose.env
```
После создания файла "docker-compose.env" его необходимо отредактировать,
изменив значения переменных окружения.

## 3. Поднятие базы данных через "Docker Compose"
```shell
sudo docker-compose --env-file ./docker/docker-compose.env up --build -d backend-postgres
```

## 4. Установка зависимостей
### 4.1 Создание виртуального окружения
```shell
python3 -m venv .venv
source .venv/bin/activate
```

### 4.2 Установка зависимостей
```shell
poetry install --no-root
```

## 5.1 Миграции
```shell
alembic upgrade heads
```
