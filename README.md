## Архитектура микросервиса NeuroSupport
Код: https://github.com/Ytgerr/yandex_micro_service 
### Общее описание

 Данный микросервис предоставляет интерфейс для взаимодействия с Yandex NeuroSupport через чат и управлением индексами. Сервис разделён на два компонента:

- Frontend – Streamlit приложение для пользователей и администраторов.

- Backend – FastAPI сервис, который инкапсулирует всю логику работы с Yandex NeuroSupport.

Все взаимодействия между фронтом и бэком происходят через REST API.

### Компоненты
- Frontend (Streamlit)

    - Чат: пользователь вводит вопросы, фронт отправляет их на бэкенд, получает ответ и отображает в интерфейсе.

    - Управление индексами: позволяет просматривать индексы, загружать документы, удалять их, получать информацию о документах.

- Backend (FastAPI)

- Обрабатывает все запросы фронта.

- Инкапсулирует работу с Yandex NeuroSupport через клиентскую библиотеку.

### Реализует следующие REST API:

- POST /answer – генерация ответа по диалогу.

- GET /indexes – список индексов.

- GET /indexes/{index_name} – информация по индексу.

- POST /indexes/{index_name}/documents – загрузка документов.

- GET /indexes/{index_name}/documents – получение документов.

- DELETE /indexes/{index_name}/documents – удаление документов.

- POST /indexes/{index_name}/switch_version – переключение версии индекса.

- POST /indexes/{index_name}/rename – переименование индекса.

- DELETE /indexes/{index_name}/delete – удаление индекса.

### Docker и контейнеризация

Каждый компонент фронт и бэк упакован в отдельный Docker-контейнер.

Для запуска используется Docker Compose.

```bash
docker compose up --build
```

Бэкенд запускается через uvicorn.

Для управлениями зависимостями используется uv от astra

### Используемые ссылки
- https://yandex.cloud/ru/docs/neurosupport/quick-start
- https://github.com/yandex/neurosupport-api/blob/main/cookbook_neurosupport.ipynb
- https://docs.astral.sh/uv/
