import json
from typing import Tuple
from uuid import uuid4
from os import getcwd
from hashlib import sha1
import secrets
from functools import wraps

CWD = getcwd()

class Auth():
    def __init__(self, file_path: str, cookies_path):
        self.file_path = file_path
        self.cookies_path = cookies_path

    @property
    def users(self) -> dict:
        file = open(self.file_path, encoding="utf8")
        data = json.load(file)
        file.close()
        return data

    @property
    def cookies(self) -> dict:
        file = open(self.cookies_path, encoding="utf8")
        cookies_data = json.load(file)
        file.close()
        return cookies_data
    
    def write(self, data: dict) -> bool:
        file = open(self.file_path, mode="w")
        json.dump(data, file, indent=4, ensure_ascii=True)
        return True

    def wirte_cookies(self, data):
        file = open(self.cookies_path, mode="w")
        json.dump(data, file, indent=4, ensure_ascii=True)
        return True
    
    def get_by_name(self, name: str) -> Tuple[dict, bool]:
        return next(filter(lambda user: user["name"] == name, self.users["data"]),False)

    def get_by_id(self, id: str):
        return next(filter(lambda user: user["id"] == id, self.users["data"]),False)
    
    def create_user(self, name: str, pwd: str) -> bool:  
        uniq_user = self.get_by_name(name)
        if uniq_user:
            return False
        pwd = sha1(pwd.encode()).hexdigest()
        user = {
            "id":uuid4().hex,
            "name": name,
            "pwd": pwd
        }
        users_list = self.users
        users_list["data"].append(user)
        self.write(users_list)
        return True
    

    def login(self, name, pwd):
        pwd = sha1(pwd.encode()).hexdigest()
        users = self.users.copy()
        for user in users["data"]:
            if user["name"] == name:
                if user["pwd"]==pwd:
                    # ADD TOKEN TO USER:
                    user["token"] = secrets.token_hex()
                    cooky = {"id": user["id"], "token": user["token"]}
                    self.write(users)
                    self.wirte_cookies(cooky)
                    return True
        return False


    def log(self, func):
        @wraps(func)
        def inner(*args):
            user_id = self.cookies.get("id")
            user_token = self.cookies.get("token")
            for user in self.users["data"]:
                if user["id"] == user_id and user["token"] == user_token:
                    return func(*args)
            print("NO ESTAS LOGEADO")
        return inner

    


if __name__ == "__main__":
    test_1 = Auth(f"{CWD}/users.json", f"{CWD}/cookies.json")
    test_1.login("test_2", "12345")
    @test_1.log
    def testing():
        print("logeado")
    testing()

def public():
    print("public")
def private():
    print("private")


