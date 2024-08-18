# Подготовка виртуальной машины

## Склонируйте репозиторий

Склонируйте репозиторий проекта:

```
git clone https://github.com/AV31459/mle-recsys-project.git
```

## Создайте и активируйте виртуальное окружение

Создать новое виртуальное окружение можно командой:

```
python3 -m venv .venv
```

После инициализируйте егоследующей командой

```
source .venv/bin/activate
```

установите в него необходимые Python-пакеты следующей командой

```
pip install -r requirements.txt
```

### Скачайте файлы с данными

Для начала работы понадобится три файла с данными:
- [tracks.parquet](https://storage.yandexcloud.net/mle-data/ym/tracks.parquet)
- [catalog_names.parquet](https://storage.yandexcloud.net/mle-data/ym/catalog_names.parquet)
- [interactions.parquet](https://storage.yandexcloud.net/mle-data/ym/interactions.parquet)
 
Скачайте их в директорию локального репозитория. Для удобства вы можете воспользоваться командой wget:

```
wget https://storage.yandexcloud.net/mle-data/ym/tracks.parquet

wget https://storage.yandexcloud.net/mle-data/ym/catalog_names.parquet

wget https://storage.yandexcloud.net/mle-data/ym/interactions.parquet
```

## Запустите Jupyter Lab

Запустите Jupyter Lab в командной строке

```
jupyter lab --ip=0.0.0.0 --no-browser
```

# Расчёт рекомендаций

Код для выполнения первой части проекта находится в файле `recommendations.ipynb`.

# Сервис рекомендаций

Настройки сервиса рекомендация (в т.ч. порт, уровень логгирования, пути к файлам с предрассчитанными рекомендациями) находятся в файле `.env_service`       

Перед запуском сервиса рекомендаций убедитесь, что в соответствующей директории (по умлочанию `/data`) находятся все необходимые файлы с предварительно рассчитанными рекомендациями и похожими объектами (имена файлов по умолчанию `top_popular.parquet`, `recommendations.parquet`, `similar.parquet`).      

Код сервиса рекомендаций находится в файле `service/recommendations_service.py`, для запуска сервиса в корне проекта выполните команду
```
python ./service/recommendations_service.py
```
По умлолчанию сервис запускается по адресу `http://127.0.0.1:8888/`

Основной ендпоинт сервиса находтся по пути `/recs`, формат запроса (передаваемые параметры) подробно описаны в автодокументации `http://localhost:8888/redoc`

# Инструкции для тестирования сервиса

Код для тестирования сервиса находится в файле `test_service.py`. Для запуска тестов выполните:   
```
python ./service/test_service.py
```

Исходные данные для тестов (uri, метод запроса, передаваемые параметны и т.д.) находятся в файле `service/test_data.json`.      
По умолчанию, в каждом единичном тесте проверяется http код ответа и количество получаемых рекомендаций (если применимо).

В том случае, если в файле с исходными данными для тестов содержатся заранее подготовленные(рассчитанные) точные значения id возвращаемых рекомендаций (ключ `response_data`), тесты могут быть запущены c параметром `--strict` (в _строгом_ режиме) - в этом случае будет проверятся точное совпадение получаемых рекомендаций с эталонными значениями.

Для запуска тестов в _строгом_ режиме c сохранением результатв в файле `test_service.log` выполните:
```
python ./service/test_service.py --strict > ./test_service.log
```
