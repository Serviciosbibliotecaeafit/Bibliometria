import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

# path of the chromedriver we have just downloaded
# PATH = r"D:\chromedriver"
# driver = webdriver.Chrome(PATH)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# url of google news website
url = 'https://www.scopus.com/record/display.uri?eid=2-s2.0-85104656799&origin=resultslist&sort=plf-f&src=s&st1=Happy+birthday%2cMr.+Public+officer%21+About+the+justification&sid=45965b9f2bf88900774d04aa69295dfd&sot=b&sdt=b&sl=66&s=TITLE%28Happy+birthday%2c+Mr.+Public+officer%21+About+the+justification%29&relpos=0&citeCnt=0&searchTerm='

# to open the url in the browser
driver.get(url)

# XPath
news_path = '/html/body/div/div/div[1]/div[2]/div/div[3]/div[3]/div/div[1]/div[2]/micro-ui/scopus-document-details-page/div/article/div[2]/section/div[1]/div/h2[1]/span'

# I have used f-strings to format the string
"""c = 1
for x in range(2, 9):
    try:
        print(f"Heading {c}: ")
        c += 1
        curr_path = f'/html/body/c-wiz/div/div[2]/main/div[2]/c-wiz/section/div[2]/div/div[{x}]/c-wiz/c-wiz/div/article/h4'
        title = driver.find_element(By.XPATH, curr_path)
        print(title.text)
    except:
        break"""

# to get that element
link = driver.find_element(By.XPATH, news_path)

# to read the text from that element
print(link.text)

"""import requests
from bs4 import BeautifulSoup
import time

url  = 'https://finance.yahoo.com/cryptocurrencies/'
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0' } 
response = requests.get(url, headers=headers)
text = response.text
data = BeautifulSoup(text, 'html.parser')

# since, headings are the first row of the table
headings = data.find_all('tr')[0]
headings_list = []

for x in headings:
    headings_list.append(x.text)

# since, we require only the first ten columns
headings_list = headings_list[:10]

#print('Headings are: ')
#for column in headings_list:
#    print(column)

# since we need only first five coins
for x in range(1, 6):
    table = data.find_all('tr')[x]
    c = table.find_all('td')

    for x in c:
        print(x.text, end=' ')
    
    print(' ')"""
