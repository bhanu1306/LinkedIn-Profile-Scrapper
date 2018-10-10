from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import os
import time
import datetime
import math
from threading import Timer
import csv
import pandas as pd
import hashlib

class Linkedin:
    
    def __init__(self):
        print("Running...")
        options = Options()
        options.add_argument('-headless')
        self.driver = webdriver.Firefox(firefox_options=options)
        #self.driver = webdriver.Firefox()
        WebDriverWait(self.driver, timeout=10)
        self.driver.get("https://www.linkedin.com/uas/login?")
        username = ''
        password = ''
        with open('credentials.csv', 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                username = row['Username']
                password = row['Password']
        self.driver.find_element_by_name('session_key').send_keys(username)
        self.driver.find_element_by_name('session_password').send_keys(password)
        self.driver.find_element_by_name('signin').click()
        self.scrap()
    
        
    def scrap(self):
        profiles_list=[]
        data_list = []
        new_data = []
        
        #Reading the Profiles
        with open('profiles.csv', 'r', newline='') as file:
            profiles_dict = csv.DictReader(file)
            for profile in profiles_dict:
                p_dict = {}
                p_dict['Name'] = profile['Name']
                p_dict['Surname'] = profile['Surname']
                p_dict['Linkedin_profile'] = profile['Linkedin_profile']
                profiles_list.append(p_dict)
            
        
        #Scraping the individual profile 
        for i in range(0 , len(profiles_list)):
            profile = profiles_list[i]
            name = profile['Name']
            surname = profile['Surname']
            profile_link = profile['Linkedin_profile']
            if profile_link is not None :
                if os.path.exists('old_data.csv'):
                    df = pd.read_csv('old_data.csv', sep=',')
                    df.set_index("Link", inplace=True)
                    try:
                        data_indi = df.loc[profile_link[28:]]
                    except KeyError:
                        data_indi = None
                    if data_indi is not None:
                        data_as_dict, data_comp = self.scrap_profile(name, surname, profile_link, data_indi["Skills"], data_indi["Title"], data_indi["Desc"])
                        data_list.append(data_as_dict)
                        new_data.append(data_comp)
                    else:
                        data_as_dict, data_comp = self.scrap_profile(name, surname, profile_link)
                        data_list.append(data_as_dict)
                        new_data.append(data_comp)
                else:            
                    data_as_dict, data_comp = self.scrap_profile(name, surname, profile_link)
                    data_list.append(data_as_dict)
                    new_data.append(data_comp)
        
        
        #Writing data for next comparison of skills, title/headline and desciption/summary
        with open('old_data.csv', 'w', newline='') as file1:
            writer = csv.DictWriter(file1, fieldnames=['Link', 'Skills', 'Title', 'Desc'])
            writer.writeheader()
            for i in range(0, len(new_data)):
                new_d = new_data[i]
                writer.writerow({'Link': new_d['Link'], 'Skills': new_d['Skills'], 'Title': new_d['Title'], 'Desc': new_d['Desc']})
        
        #Writing the scraped data to a file with date as the file name
        file_name = str(datetime.datetime.now())[:10]+'.csv'
        with open(file_name, 'w', newline='') as file2:
            fieldnames = ['Name', 'Surname', 'Linkedin_profile', 'Count_contacts', 'Count_contacts_recruiter', 'Count_recommendations', 'Skills_updated', 'Title_updated', 'Description_updated']
            writer = csv.DictWriter(file2, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(0, len(data_list)):
                data = data_list[i]
                writer.writerow({'Name': data['Name'], 'Surname': data['Surname'], 'Linkedin_profile': data['Linkedin_profile'], 'Count_contacts': data['Count_contacts'], 'Count_contacts_recruiter': data['Count_cont_recruit'], 'Count_recommendations': data['Count_recommendations'], 'Skills_updated': data['Skills_updated'], 'Title_updated': data['Title_updated'], 'Description_updated': data['Description_updated']})
            
        self.driver.quit()
        print("Exiting...")

# 0  == No
# 1  == Yes
        
    def scrap_profile(self, name, surname, link, skills=None, title=None, desc=None):
        self.driver.get(link)
        
        #Getting data -->  Title, Desciption, Skills, No. of Recommendations
        WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'pv-top-card-section__headline')))
        Title = self.driver.find_element_by_class_name('pv-top-card-section__headline').text
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2.7);")
        try:
            self.driver.find_element_by_class_name('pv-top-card-section__summary-toggle-button')
            WebDriverWait(self.driver, 100).until(EC.element_to_be_clickable((By.CLASS_NAME, 'pv-top-card-section__summary-toggle-button')))
            self.driver.find_element_by_class_name('pv-top-card-section__summary-toggle-button').click()
        except NoSuchElementException:
            pass
        try:
            Desc = self.driver.find_element_by_class_name('pv-top-card-section__summary-text').text
        except:
            Desc = 'No Description'
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/1.7);")
        Skills = ''
        flag = False
        try:
            WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'pv-skills-section__additional-skills')))
            self.driver.find_element_by_class_name('pv-skills-section__additional-skills')
            WebDriverWait(self.driver, 100).until(EC.element_to_be_clickable((By.CLASS_NAME, 'pv-skills-section__additional-skills')))
            time.sleep(0.25)
            self.driver.find_element_by_class_name('pv-skills-section__additional-skills').click()
        except ElementClickInterceptedException:
            try:
                WebDriverWait(self.driver, 100).until(EC.element_to_be_clickable((By.CLASS_NAME, 'pv-skills-section__additional-skills')))
                self.driver.find_element_by_class_name('pv-skills-section__additional-skills').click()
            except:
                pass
        except NoSuchElementException:
            pass
        try:
            WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'pv-skill-category-entity__name')))
            s = self.driver.find_elements_by_class_name('pv-skill-category-entity__name')
            for item in s:
                Skills = Skills+item.text
                Skills = Skills+' '
        except:
            flag = True
        if flag == True:
            Skills = 'No Skills'
        
        WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.TAG_NAME, "artdeco-tab")))
        received_recomm = self.driver.find_element_by_tag_name("artdeco-tab").text
        Count_received_recomm = int(received_recomm[10:-1])
        
        #Getting data --> Count of contacts, Count of contacts with recruiter designation
        self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
        Count_contacts = int(self.driver.find_element_by_class_name('pv-top-card-v2-section__connections ').text[17:-1])
        self.driver.find_element_by_class_name('pv-top-card-v2-section__link--connections').click()
        WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'search-results-container')))
        url = self.driver.current_url+"&page="
        total_pages = int(math.ceil(Count_contacts/10.0))
        list_conn_head = []
        for i in range(1, total_pages+1):
            self.driver.set_page_load_timeout(time_to_wait=10000)
            self.driver.get(url+str(i))
            WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'search-results-container')))
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(0.25)
            WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'search-results-container')))
            conn_html = self.driver.execute_script("return document.body.innerHTML")
            parsed = BeautifulSoup(conn_html, "lxml")
            paras = parsed.select('p.subline-level-1.search-result__truncate')
            for i in range(0, len(paras)):
                list_conn_head.append(paras[i].text)
        
        Count_cont_recruit = 0
        
        #List of words to look in Headlines of Connections for identifying Recruiter's Profiles. Add any new designation, if there is any.  
        list_comp = ['recruiter', 'hr', 'human resource']
        for i in range(0, len(list_conn_head)):
            desig = list_conn_head[i].lower()
            for j in range(0, len(list_comp)):
                if list_comp[j] in desig:
                    Count_cont_recruit+=1		
        #Hashing Title, Description and Skills using md5
        Skills = hashlib.md5(Skills.encode('utf-8')).hexdigest()
        Title = hashlib.md5(Title.encode('utf-8')).hexdigest()
        Desc = hashlib.md5(Desc.encode('utf-8')).hexdigest()
        
        #Checking Title Updation
        is_title_updated = 0
        if title is not None:
            if Title != title :
                is_title_updated = 1
        
        #Checking Description Updation
        is_desc_updated = 0
        if desc is not None:
            if Desc != desc :
                is_desc_updated = 1
        
        #Checking Skills Updation
        is_skills_updated = 0
        if skills is not None:
            if Skills != skills :
                is_skills_updated = 1
        
        data = {'Name': name, 'Surname': surname, 'Linkedin_profile': link, 'Count_contacts': Count_contacts, 'Count_cont_recruit': Count_cont_recruit, 'Count_recommendations': Count_received_recomm, 'Skills_updated': is_skills_updated, 'Title_updated': is_title_updated, 'Description_updated': is_desc_updated}
        data_comp = {'Link': link[28:], 'Skills': Skills, 'Title': Title, 'Desc': Desc }
        return data, data_comp


#Time interval = 3 days = 259200 seconds
def starter():
    t = Timer(500, starter)
    t.start()
    Linkedin()
    
#Main execution starts here
if __name__ == '__main__':
    starter()
                