import datetime

# import json
import requests
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd

import re

provinces = {1:"Вінницька", 13 : "Миколаївська", 2:"Волинська", 14:"Одеська", 3:"Дніпропетровська", 15:"Полтавська",
    4:"Донецька", 16:"Рівенська", 5:"Житомирська", 17:'Сумська', 6:"Закарпатська", 18:"Тернопільська", 7:"Запорізька", 19:"Харківська",
    8:"Івано-Франківська", 20:"Херсонська", 9:"Київська", 21:"Хмельницька", 10:"Кіровоградська", 22:"Черкаська", 11:"Луганська", 23:"Чернівецька",
    12:"Львівська", 24:"Чернігівська", 25:"Республіка Крим" }



def get_url(url):
    
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content




def get_provinces_data(what, when, TYPE=["VHI_Parea", "Mean"]):

    # https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_provinceData.php?country=UKR&provinceID=11&year1=1981&year2=2018&type=Mean

    files = []

    for count in range(0, 2):

        url = "https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_provinceData.php?country=UKR&provinceID={}&year1={}&year2={}&type={}".format(what, when[0], when[1], TYPE[count])

        resp = get_url(url)

        timestamp = datetime.datetime.now().strftime("%Y_%m_%d-%Hh")#replace(' ', '_').replace('-', '_').replace(':', '_').replace('.', '_')

        filename = '{}_{}_{}-{}_{}.txt'.format(what, TYPE[count], when[0], when[1], timestamp)

        file = open(filename, 'wb')
        file.write(str.encode(resp))
        print(filename, " created.")
        files.append(filename)


    return files





def validation(what, when):
    if int(what) not in dict.keys(provinces) or int(when[0]) > int(when[1]):
        return False
    else:
        return True


def choose_province():
    print("Hey, choose province and years you need: (E.g. 11 2017 2018) ")
    for every in dict.keys(provinces):
        print(every, " <=> ", provinces[every])

    what, *when = input("Your choice: ").split()

    if validation(what, when):
        print("Proceeding...")
        return(get_provinces_data(what, when))

    else:
        print("Something wrong!")
        a = input("Try again?[y/n]")
        if a == 'y' or a == "Y":
            chose_province()
        elif a == 'n' or a == 'N':
            print("Bye.")
            exit()


def mean_file(file):
        raw = open(file,'r+')
        headers = raw.readline().rstrip()
        headers = headers.split(',')[:2] + headers.split(',')[4:]
        data = raw.readlines()

        result = []

        # deleting stuff to get it in df
        for every in data:
            result.append(str(re.sub(r',\s\s|\s\s|\s|,\s',',',every)[:-1]).split(','))


        df = pd.DataFrame(result,columns=headers)

        return df

def vhi_file(file):
    raw = open(file,'r+')
    headers = raw.readline().rstrip()
    headers = headers.split(',')[:2] + headers.split(',')[4:]
    data = raw.readlines()

    result = []

    # deleting stuff to get it in df
    for every in data:
        result.append(str(re.sub(r'\s\s\s|,\s\s|\s\s|,\s|\s',',',every)[:-1]).split(','))

    df = pd.DataFrame(result,columns=headers)

    # print(df)

    return df


def get_data_from_txt_to_df(filenames):
    for file in filenames:
        if "Mean" in file:
            df_mean = mean_file(file)
            return df_mean
        if "VHI" in file:
            df_vhi =vhi_file(file)
            return  df_vhi



def get_file_to_normal_stage(filenames):
    for file in filenames:
        data = open(file,'r').read()
        data = data[data.find('<pre>')+5:data.find("</pre></tt>")]

        write_to = open(file,'w').write(data)

def need_file( TYPE=["VHI_Parea", "Mean"]):
        file=[]
        what, *when = input("Your choice: ").split()
        for i in range(0, 2):
            timestamp = datetime.datetime.now().strftime("%Y_%m_%d-%Hh")
            filename = '{}_{}_{}-{}_{}.txt'.format(what, TYPE[i], when[0], when[1], timestamp)
            file.append(filename)
        return file   

def main():
    filenames = choose_province()
    get_file_to_normal_stage(filenames)
    df_vhi = get_data_from_txt_to_df(filenames)
    name = need_file()
    #TYPE=["VHI", "Mean"]
    print(name)
    for i in name:
        if "VHI" in i:  
            df = vhi_file(i)
            print(df.head(40))
            #print(df.idxmax())
            print(df.min())
            print(df.max())

        else:
            df = vhi_file(i)
            print(df.head(40))







if __name__ == "__main__":

    main()

     #df = vhi_file("13_VHI_Parea_2017-2018(2018-11-18 22:27:19.221941).txt")




     #print(df.VHI.max())

    # print(df1.head(20))


    # res = 0
    # for every in df.VHI:
    #     if  float(every) > 25:
    #         res += 1

    # print("res= ", res)
    # get_file_to_normal_stage(["11_Mean_2017-2018(2018-11-12 08:46:54.301805).txt"])
