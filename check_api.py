import requests

url = "https://reqres.in/api/users?page=2"
print(f"Запрос к: {url}")

response = requests.get(url)

print(f"Статус: {response.status_code}")
print(f"Заголовки запроса: {response.request.headers}") 
print(f"Тело ответа: {response.text[:200]}")