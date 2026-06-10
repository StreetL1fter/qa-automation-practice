
FROM mcr.microsoft.com/playwright/python:v1.49.0-noble

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "-m", "pytest"]
CMD ["--alluredir=allure-results"]