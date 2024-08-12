# Check the brower you are using and install a stable version of driver for selenium
# from https://selenium-python.readthedocs.io/installation.html#drivers
# the requirement is mentioned in requirement.txt
# after basic setup the data is stored in data.xlsx in the same path as folder

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

path_to_drivers = 'msedgedriver.exe' # driver path
website_url = 'https://hprera.nic.in/PublicDashboard' #website url
num = 6 #number of records needed

find_arr=['Name','PAN No.','GSTIN No.','Permanent Address']  #the data we need from the table 
output={} #the data scraped 

service = Service(path_to_drivers)  #webdriver to run based on the brower used (here for eg: Microsoft-Edge) 
driver = webdriver.Edge(service = service)
driver.get(website_url) #the website from which we need to scrape

WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.ID,"reg-Projects")) #check if the "Registered Projects" are on screen
)
links = driver.find_elements(By.XPATH, f"//a[@title='View Application']") #finding the rera number
links = links[:num] 
for link in links:
    output[link.text]={} #creating a dictionary for each rera number
    link.click() #opening the link to get detail
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//tbody[contains(@class, 'lh-2')]")) #wait till the information table if avaliable 
    )
    temp={}
    table = driver.find_element(By.XPATH, "//tbody[contains(@class, 'lh-2')]") 
    rows = table.find_elements(By.TAG_NAME, 'tr')
    for row in rows:
        cells = row.find_elements(By.XPATH,'.//td') 
        ind = cells[0].text
        if(ind in find_arr): #check if the cells left column match the content arr
            temp[ind]  = cells[1].text
        output[link.text] = temp
        
    closeBtn = driver.find_element(By.XPATH,"//button[contains(text(),'Close')]") #close the information table after use
    closeBtn.click()

driver.quit() # close the brower 

for reraid in output.keys(): # clean the data 
    output[reraid]['Permanent Address'] = " ".join(output[reraid]['Permanent Address'].split(" ")[:-2]) 
    output[reraid]['PAN No.']=output[reraid]['PAN No.'].split(" ")[0]
    output[reraid]['GSTIN No.']=output[reraid]['GSTIN No.'].split(" ")[0]

df = pd.DataFrame.from_dict(output, orient='index') #using pandas to convert the data and save to excel
df.to_excel('data.xlsx', engine='openpyxl')
print('data saved in data.xlsx')
