# 1. Берем официальный образ Playwright с Python
FROM mcr.microsoft.com/playwright/python:v1.49.0-noble

# 2. Создаем рабочую папку
WORKDIR /usr/src/app

# 3. Копируем requirements.txt
COPY requirements.txt ./

# 4. ВАЖНО: Устанавливаем зависимости через python -m pip глобально
RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

# 5. Копируем остальные файлы проекта
COPY . .

# 6. Запуск тестов
CMD ["python3", "-m", "pytest", "--alluredir=allure-results"]