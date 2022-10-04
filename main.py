import requests as req
from os import system
from utils import car_side, exist_country, info, bandera, continent_choises, count_in_continent, numerical, questions, capital, clear, result, get_all, language, telefon
from random import shuffle
clear()

regions = ["Africa", "Americas", "Asia", "Europe", "Oceania"]


'''
API
'''
user = ""
while user != "q":
    user = input("Select an option: ")
    clear()
    if user == "1":
        country = input("Choose country: ").capitalize()
        clear()
        data = exist_country(country)
        printing = info(data, country)
        if printing == False:
            clear()
            pass
        else:
            flag = ""
            while flag != "y" and flag != "n":
                flag = input("Do you want to download the flag (y/n): ").lower()
                if flag == "y":
                    if "flags" in data.keys():
                        flag_im =req.get(list(data["flags"].values())[0])
                        img_format = list(data["flags"].keys())[0]
                        country = data["name"]["common"]
                        bandera(country, flag_im, img_format)  
                        print(f'''{country} flag downloaded corretly''') 
                    else:
                        print(f'''{country} has no flag available to download\n''')
        input("\nPress any to restart")
        clear()
    elif user == "2":
        continent_choises(regions)  
        user_1 = input("Wich continent do you want to play with?: ")
        if user_1.isnumeric() == False: #Validamos opcion elegida
            print("\nOption not valid")
            input("\nPress any to restart")
            clear()
            continue
        if int(user_1) not in range(1,6):
            print("\nOption not valid")
            input("\nPress any to restart")
            clear()
            continue
        continent = regions[int(user_1)-1]
        system("clear")
        print(continent.center(50, "-"))
        list_countries = count_in_continent(continent)
        quest_list=[numerical(list_countries, "area"), numerical(list_countries, "population"), capital(list_countries), language(list_countries), car_side(list_countries), telefon(list_countries)]
        shuffle(quest_list)
        points = 0
        for i in quest_list[:-1]: #Ejecutamos lista de funciones de preguntas
            quest, answer = i
            correct_answer = answer[0]
            shuffle(answer)
            points += questions(quest, answer, correct_answer)
        result(points)
        input("\nPress any to restart")
        clear()
    elif user == "q":
        pass
    else:
        print("\nNot a valid option\n")
        input("\nPress any to restart")
        clear()
