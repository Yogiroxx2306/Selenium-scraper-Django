# example/views.py
from datetime import datetime
from main import run_Script
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect,render
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import csv
import sqlite3

# from Database import createDB
def createDB(results):
    # create a connection to the database
    conn = sqlite3.connect('verge_articles_django.db')

    # get the current date and time
    now = datetime.now()

    # format the date and time as a string
    timestamp = datetime.now().strftime("_%Y%m%d_Verge_%H%M%S")

    # create a table to store the articles
    conn.execute(f'CREATE TABLE {timestamp}_verge (id INTEGER PRIMARY KEY, name TEXT, url TEXT, author TEXT, date TEXT)')

    # insert the articles into the table
    for i, article in enumerate(results):
        conn.execute(f'INSERT INTO {timestamp}_verge (id, name, url, author, date) VALUES (?, ?, ?, ?, ?)', (i+1, article['name'], article['url'], article['author'], article['date']))

    # commit the changes and close the connection
    conn.commit()
    conn.close()

def python_file(request):
    print("main.py running")
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(options=chrome_options)
    now = datetime.now()
    results = []

    def handleDate(date):
        if "GMT" in date:
            new_date = datetime.now()
            timestamp = new_date.strftime("%b-%d")
            date = timestamp
        elif "AGO" in date:
            new_date = datetime.now()
            timestamp = new_date.strftime("%b-%d")
            date = timestamp
        else:
            date = date
        return date


    def make_csv(results):
        # get the current date and time
        now = datetime.now()
        # format the date and time as a string
        timestamp = datetime.now().strftime("_%Y-%m-%d_Verge_%H-%M-%S")
        with open(f'{timestamp}.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f,
                                    fieldnames=['name', 'url', 'author', 'date'])
            writer.writeheader()
            writer.writerows(results)


    def query():
        selector = '.dark\:group-hover\:shadow-underline-franklin'

        links = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
        )

        for i in range(len(links)):
            name = links[i].text
            link = links[i].get_attribute('href')
            parent_element = links[i].find_element(By.XPATH, "..")
            following_sibling = parent_element.find_element(By.XPATH, './following-sibling::*[1]')
            author_element = following_sibling.find_element(By.XPATH, './*[1]')
            author = author_element.text
            date_element = following_sibling.find_element(By.XPATH,'./*[2]')
            date = date_element.text
            date1 = ''
            try:
                date_element1 = following_sibling.find_element(By.XPATH, './*[3]')
                date1 = date_element1.text
            except:
                date1 = ''
            if(date1):
                date = date1
                author = author_element.text + date_element.text
            date = handleDate(date)
            details = {
                'name': name,
                'url' : link,
                'author': author,
                'date': date
            }
            results.append(details)


    # scraping through all the urls in page
    def run_Script():
        print("button clicked")
        for i in range(1,16):
            url = ('https://www.theverge.com/archives/{}').format(i)
            driver.get(url)
            query()
        # creating csv file for results
        make_csv(results)

    run_Script()

    createDB(results)
    driver.quit()
    context = {
        "result" : results,
        "date" : now
    }
    return render(request,'scrapedarticles.html',context)
    # return HttpResponse("Script Runned")
    

def index(request):
    now = datetime.now()
    context = {
        "button" : run_Script,
        "date" : now
    }
    print("requested")
    return render(request,'home.html',context)
    