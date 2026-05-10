import pytest
import requests


class TestUsersApi:
    def test_users_list(self,base_url,api_headers):
        params = {"page":2}

        response = requests.get(f"{base_url}/users",params=params,headers=api_headers)

        assert response.status_code == 200
 
        if response.status_code == 401:
            print(f"Текст ошибки: {response.text}")
        data = response.json()

        assert "data" in data
        assert len(data["data"]) > 0

        first_user = data["data"][0]
        assert "id" in first_user
        assert "email" in first_user
        assert "first_name" in first_user
        assert "last_name" in first_user


    def test_user_notfound(self,base_url):
        response = requests.get(f"{base_url}/users/23")
        assert response.status_code == 401


    @pytest.mark.parametrize("name,job, description",[
        ("Ivan","Web-Developer","Стандартная роль"),
        ("Ismail","QA Engineer","Другая роль"),
         ("", "Manager", "Граничный случай: пустое имя"),
        ("A" * 50, "Tester", "Граничный случай: длинное имя"),
    ],ids=["standard", "different_role", "empty_name", "long_name"])
    
    def test_post_users(self,base_url,name,job,description,api_headers):
        payload = {
            "name": name,
            "job": job
        }
        response = requests.post(f"{base_url}/users",json=payload,headers=api_headers)
        
        assert response.status_code == 201

        result = response.json()

        assert "id" in result
        assert "createdAt" in result
        assert result["name"] == name
        assert result["job"] == job



    def test_invalid_register(self,base_url,api_headers):

        payload = {
            "name": "ismailmendgaliev",
        }
        response = requests.post(f"{base_url}/register", json=payload,headers=api_headers)


        assert response.status_code == 400
        result = response.json()
        assert result["error"] == "Missing email or username"
   


    def test_put_users(self,base_url,api_headers):
        payload = {
            "name": "Ivan",
            "job": "Senior QA" 
        }
        response = requests.put(f"{base_url}/users/2",json=payload,headers=api_headers)

        assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}, Ответ: {response.text}"

        listed = response.json()

        assert listed["name"] == payload["name"] 
        assert listed["job"] == payload["job"]

        assert "updatedAt" in listed

    def test_delete_users(self,base_url,api_headers):

        response = requests.delete(f"{base_url}/users/2",headers=api_headers)

        assert response.status_code == 204
        assert response.text == ""





    