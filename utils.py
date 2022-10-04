
from os import mkdir, getcwd, stat, system
import requests as req
import random
from typing import Union, Tuple
from datetime import datetime
from functools import wraps
from auth_obj import Auth


CWD = getcwd()
url = "https://restcountries.com/v3.1"

test = Auth(f"{CWD}/users.json", f"{CWD}/cookies.json")

# coje todos los paises
def get_all() -> Tuple[list, str]: 
    res = req.get(url + "/all").json()
    return res, url

'''
DECORATORS
'''
def outter_logs(func):
    @wraps(func)
    def inner_logs(*args):
        date_info = datetime.now()
        date_info = date_info.strftime("%Y-%m-%d %H:%M:%S")
        with open(f"{CWD}/downloads.log", "a", encoding="utf8") as file:
            file.write(f"{date_info} | {args[3]} |  {func.__name__}\n")
        return(func(*args))
    return inner_logs



'''
FRONT
'''
# limpiamos terminal manteniendo menu
def clear(): 
    system("clear")
    menu()


# imprime menu
def menu():
    print("\n")
    print("Countires".center(50, "-"))
    print("1. Serch country".center(50))
    print("2. Play a game".center(50))
    print("Q. Exit".center(50))
    print("".center(50, "-"))

# impresion de busqueda de pais
def info(data: Union[dict, None], country: str) -> bool: 
    if data == None:  #si no encontramos pais buscamos posibles similitudes
        if len(guess(country)) > 0: 
            aprox = guess(country)
            if aprox != "Not found":
                print(f"Maybe you mean: {guess(country)}\n")
            else:
                print("Couldn't find it")
        return False
    else:
        print(f"\n{name(data)}\n") #si encontramos pais imprimimos informacion
        return True

# listamos los continentes
def continent_choises(regions: list):
    for k, cont in enumerate(regions,start=1):
        print(f'''{k}: {cont}''')

# imprimimos pregunta, posibles respuestas y evaluamos la respuesta que da el usuario. Devolvemos puntuación
def questions(question: str, answers: list, correct_answer: str) -> int:
    print(question) #imprimimos pregunta
    for k, ans in enumerate(answers, start=1): #imprimimos posibles respuestas
        print(f'''{k}. {ans}''')
    player_guess = input("Answer: ")
    if player_guess.isnumeric(): #evaluamos respuesta usuario
        if int(player_guess) in range(1,len(answers)+1):
            if answers[int(player_guess)-1] == correct_answer:
                print("\nCorrect answer\n")
                return 2
            else:
                print(f"\nIncorrect answer, the correct answer was {correct_answer}.\n")
                return 0
        else:
            print("\nThe answer is not valid, therefore you got 0 points in this question\n")
            return 0
    else:
        print("\nThe answer is not valid, therefore you got 0 points in this question\n")
        return 0

# damos puntuación
def result(points: int):
    if points >= 5:
        print(f"Congrats you got {points}/10.")
    else:
        print(f"Dummy, you got {points}/10.")


'''
BACK
'''
# Checks if the country exists, returns the country dic if yes or None if not
def exist_country(country: str) -> Union[dict, None]:
    try:
        data = req.get(f"{url}/name/{country}?fullText=true").json()[0]
        return data
    except KeyError:
        return None

# When the country is not found tries to make an educated guess of the country the user meant (not working so good yet)
def guess(country: str) -> str:
    maybe = []
    for data in get_all()[0]:
        letter = 0
        letter_position = 0
        for k, s in enumerate(data["name"]["common"]):
            if k == len(country):
                break
            if s in country:
                letter += 1
            if country[k] == s:
                letter_position += 1
            if letter_position > len(data["name"]["common"])-2:
                return data["name"]["common"]
        if letter > len(data["name"]["common"])/2 and letter_position > len(data["name"]["common"])/3:
            maybe.append(data["name"]["common"])
    if len(maybe) > 0:
        coun_maybe = ", ".join(maybe)
    else:
        coun_maybe = "Not found"
    return coun_maybe

# Gets all the required information about a country
def name(data: dict) -> str:
    if "capital" in data.keys():
        capital = data["capital"][0]
    else:
        capital = "There is no capital"
    # try:
    #     capital = data["capital"][0]
    # except KeyError:
    #     capital = "No hay capital"
    population = data["population"]
    area = data["area"]
    if "languages" in data.keys():
        language = ", ".join([leng for leng in data["languages"].values()])
    else:
        language = "No language"
    # try:
    #     language = ", ".join([leng for leng in data["languages"].values()])
    # except KeyError:
    #     language = "No hay lengua própia"
    info = f"Capital: {capital}\nPopulation: {population}\nArea: {area}\nLenguage: {language}"
    return info

# downloads the flag of the country in the dir flags
# @test.log
# @outter_logs
# def bandera(country: str, flag_im: req.Response, img_format: str, user_name): #HOW TO SHOW REQUESTS TYPE
def bandera(country: str, flag_im: req.Response, img_format: str):
    try: # creates the directory in case it dosen't exist
        mkdir(f"{CWD}/flags")
    except FileExistsError:
        pass
    open(f'''{CWD}/flags/{country}.{img_format}''', "wb").write(flag_im.content)
    return True

# Given a continent return the lsit of countries in that continent
def count_in_continent(continent: str) -> list:
    list_countries = req.get(f"{url}/region/{continent}").json()
    return list_countries

# Creates the question and the possible answers for the numerical questions (the corretc answer is always the first value of the list answers)
def numerical(list_countries: list, request: str) -> Tuple[str, list]:
    if request == "area":
        quest = "Whats the biggest country of the continent?"
    else:
        quest = "Whats the most populated country of the continent?"
    list_countries.sort(key=lambda list_countries: list_countries[request], reverse=True)
    random_list = random.sample(range(1,int(len(list_countries)/2)),3) #ordenamos lista por area o pobl, elegimos 3 paises random de la mitad superior de la lista ordenada para dificultar respuesta
    answers = [list_countries[0]["name"]["common"]]
    [answers.append(list_countries[q]["name"]["common"]) for q in random_list]
    return quest, answers

# Creates the question and the possible answers for capital guessing the capital of a random country (the corretc answer is always the first value of the list answers)
def capital(list_countries: list) -> Tuple[str, list]:
    random.shuffle(list_countries)
    quest =  f'''What's the capital of {list_countries[0]["name"]["common"]}'''
    answers = list(map(lambda a: a["capital"][0], list_countries[0:4]))
    return quest, answers

# Creates the question and the possible answers for capital guessing an oficial language of a random country (the corretc answer is always the first value of the list answers)
def language(list_countries: list) -> Tuple[str, list]:
    lang = []
    for data in list_countries:
        if "languages" in data.keys():
            for i in data["languages"].values():
                if i not in lang:
                    lang.append(i)
    country = "Not defined"
    while country == "Not defined": #selects a random country that has the key "languages"
        random.shuffle(list_countries)
        if "languages" in list_countries[0].keys():
            list_countries[0]["languages"]
            country = list_countries[0]["name"]["common"]
    quest = f"Which of the following is an official language of {country}?"
    correct_answer = [random.choice(list(list_countries[0]["languages"].values()))]
    tuple(map(lambda s: lang.remove(s), list_countries[0]["languages"].values())) #  QUESTION: SI NO PONGO EL LIST AL PRINCIPIO NO SE EJECUTA, ES DECIR, LOS VALORES NO SE BORRAN
    other_answers = [others for others in lang[1:4]]
    answers = correct_answer + other_answers
    return quest, answers

# Creates the question and the possible answers for capital guessing driving side of a random country (the corretc answer is always the first value of the list answers)
def car_side(list_countries: list) -> Tuple[str, list]:
    country = "Not defined"
    while country == "Not defined":
        random.shuffle(list_countries)
        try:
            list_countries[0]["car"]["side"]
            country = list_countries[0]["name"]["common"]
        except:
            pass
    quest = f'''What side of the road do they drive in {country}'''
    if list_countries[0]["car"]["side"] == "left":
        answer = ["left", "right"]
        return quest, answer
    answer = ["right", "left"]
    return quest, answer

def telefon(list_countries: list) -> Tuple[str, list]:
    country = "Not defined"
    while country == "Not defined":
        random.shuffle(list_countries)
        if "idd" in list_countries[0].keys():
            if "root" in list_countries[0]["idd"].keys() and "suffixes" in list_countries[0]["idd"].keys():
                country = list_countries[0]["name"]["common"]
    quest = f'''What number idd does this {country} has?'''
    answer = [list_countries[0]["idd"]["root"] + list_countries[0]["idd"]["suffixes"][0]]
    while len(answer) < 4:
        for dic in list_countries[1:4]:
            if "idd" in list_countries[0].keys():
                if "root" in list_countries[0]["idd"].keys() and "suffixes" in list_countries[0]["idd"].keys():
                    possible_answer = dic["idd"]["root"] + dic["idd"]["suffixes"][0] 
                    if possible_answer not in answer:
                        answer.append(possible_answer)
    return quest, answer





if __name__ == "__main__": #testing this file
    pass