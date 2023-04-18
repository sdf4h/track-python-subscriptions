from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from pyfzf.pyfzf import FzfPrompt
import os
import sqlite3
from os.path import exists

print("Загрузка...5 секунд....")

options = Options()
options.headless = True

driver = webdriver.Firefox(options=options)


driver.get("https://www.youtube.com/channel/UCZ26MoNJKaGXFQWKuGVzmAg")
time.sleep(2)


### ЕСЛИ ВЫ СМОТРИТЕ YOUTUBE С ТЕРРИТОРИИ СНГ ЗАКОММЕНТИРУЙТЕ 3 СТРОЧКИ

element = driver.find_element(By.XPATH, """/html/body/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div[1]/div/button""")
element.click()
time.sleep(3)




print("Браузер загружен!")

fzf = FzfPrompt()



def search():
    sear = input("Введите то что вы хотите найти: ")
    print("Начинаю поиск " + sear)
    search_bar = driver.find_element(By.XPATH, """//input[@id="search"]""")
    search_bar.send_keys(sear)
    searchbutton = driver.find_element(By.XPATH, '//*[@id="search-icon-legacy"]')
    searchbutton.click()
    time.sleep(2)

    sear_list = []
    videos =  driver.find_elements(By.ID, "video-title")
    for i in range(len(videos)):
        print(videos[i].text)
        sear_l = videos[i].text
        sear_list.append(sear_l)
        if i == 10:
            break
    target_half=fzf.prompt(sear_list)
    print(target_half[0])
    vibor2 = target_half[0]
    for i in range(len(videos)):
        name = videos[i].text
        if name == vibor2:
            print(videos[i].get_attribute('href'))
            zzzz = videos[i].get_attribute('href')
    
    comand = "mpv " + zzzz
            
    os.system(comand)

def func():
    db = sqlite3.connect('Chanelll.db')
    db.row_factory = lambda cursor, row: row[0]
    c = db.cursor()
    ids = c.execute('SELECT NAME FROM Chanelll').fetchall()
    ids.append("ПОИСК+++")

    target_chanel=fzf.prompt(ids)
    print(target_chanel[0])
    vibor = target_chanel[0]

    if vibor == "ПОИСК+++":
        search()


    else:
        
        nomber_chanel = (ids.index(target_chanel[0]))
        
        
        url = f[nomber_chanel]
        
        end_url = url[0]


        driver.get(end_url)
        
        time.sleep(2) 
        spisokNAME=[]
        video_name = driver.find_elements(By.ID, "video-title")

        for i in range(len(video_name)):
            print(video_name[i].text)
            ggg = video_name[i].text
            
            spisokNAME.append(ggg)
            if i == 20:
                break
        target1=fzf.prompt(spisokNAME)

        
        print(target1[0])

        cccc = target1[0]


        for i in range(len(video_name)):
            ggg = video_name[i].text
            if ggg == cccc:
                 print(video_name[i].get_attribute('href'))
                 link = video_name[i].get_attribute('href')
        
        comand2 = "mpv " + link
        
        os.system(comand2)           

while(True):
    chanel_list = []

    kom = exists("Chanelll.db")


    f = [i.strip('\n').split(',') for i in open('subscribe.txt')]


    if kom == True:
        print("База каналов найдена!")
        db = sqlite3.connect('Chanel.db')
        func()

        

    else:
        print("Генерируем базу каналов, это может занять некоторое время...")

        db = sqlite3.connect('Chanelll.db')
        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS Chanelll (
            ID INTEGER PRIMARY KEY,
            NAME TEXT,
            URL TEXT
        )""")
        
        db.commit()
        
        


        for k in f:
            h = (k[0])
            driver.get(h)
            time.sleep(3)
            element2 = driver.find_element(By.XPATH, """//*[@id="channel-name"]""")
            pre_canell = element2.text

            cur.execute("""INSERT INTO Chanelll(NAME, URL) VALUES (?,?);""", (pre_canell, h))
            db.commit()
            print(pre_canell + "  Добавлен в базу!  ")
            chanel_list.append(pre_canell)
        func()