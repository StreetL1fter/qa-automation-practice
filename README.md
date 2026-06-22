# QA Automation Practice

Репозиторий с примерами автоматизации UI и API тестов, интеграции с SQL-базой данных и практикой нагрузочного тестирования. Проект оптимизирован для запуска в Docker-контейнерах (Headless mode) и интеграции в CI/CD пайплайны.

## 🛠 Стек технологий
* **Язык:** Python 3.12+
* **Тест-раннер:** Pytest (фикстуры, параметризация)
* **UI-автоматизация:** Playwright (Python)
* **База данных:** SQLite3 (валидация данных в тестах)
* **Отчетность:** Allure Report
* **Нагрузочное тестирование:** Locust
* **Контейнеризация:** Docker

## 🏗 Структура проекта (POM)
```plaintext
├── pages/                # Классы страниц (Page Object Model)
│   ├── cataloge_page.py  # Локаторы и методы каталога Wildberries
│   └── demoblaze_page.py # Авторизация и компоненты Demoblaze
├── tests/                # Тесты по уровням
│   ├── api/
│   │   └── test_users.py # Тесты REST API (CRUD, статус-коды)
│   └── ui/
│       ├── conftest.py   # Глобальные фикстуры (браузер, сессии БД)
│       ├── test_demoblaze.py # E2E-сценарии с валидацией данных в SQL
│       └── test_elements.py  # UI-тесты (поиск, корзина с API-мокингом)
├── Dockerfile            # Контейнеризация для CI/CD запуска
├── pytest.ini            # Настройки pytest и логирования
└── requirements.txt      # Зависимости проекта