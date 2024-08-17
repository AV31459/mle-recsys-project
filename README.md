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

# Инструкции для тестирования сервиса

Код для тестирования сервиса находится в файле `test_service.py`.

<*укажите здесь необходимые шаги для тестирования сервиса рекомендаций*>
