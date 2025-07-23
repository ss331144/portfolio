from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import time
import datetime
import os
from colorama import Fore, Style, init
from deep_translator import GoogleTranslator
import pandas as pd
import requests



init(autoreset=True)
translator = GoogleTranslator(source='auto', target='iw')
#for refresh the job file
DEL_FILE=False

N=150
BASE_URL = "https://nvidia.wd5.myworkdayjobs.com"
file_name = 'nvidia_jobs.csv'


def filter_li_by_experience(li_elements):
    """
    מקבלת רשימת אלמנטים מסוג <li> ומחזירה רק את אלה שמכילים מילים כמו:
    'experience', '1+', '2+', '3+'
    """
    keywords = ['experience', 'years of experience', 'years experience', 'minimum experience', 'required experience',
                'senior', 'junior', 'mid-level', 'mid level', 'entry level', '1+ years', '2+ years', '3+ years',
                '4+ years', '5+ years', '6+ years', '7+ years', '8+ years', '9+ years', '10+ years',
                'one year experience', 'two years experience', 'three years experience', 'four years experience',
                'five years experience', 'expert', 'proven experience', 'track record', 'seasoned professional',
                'hands-on experience', 'professional experience', 'skilled', 'extensive experience',
                'demonstrated experience', 'minimum required', 'strong knowledge', 'solid background', 'competent',
                'adequate experience', 'familiar with', 'able to', 'knowledge of', 'prior experience',
                'work experience', 'significant experience', 'relevant experience', 'in-depth experience',
                'demonstrated ability', 'proficient', 'well-versed', 'experienced', 'ability to', 'expertise',
                'technical experience', 'practical experience', 'field experience', 'work background',
                'industry experience']
    filtered = []

    for li in li_elements:
        text = li.get_text(strip=True)
        text_lower = text.lower()
        if any(keyword in text_lower for keyword in keywords):
            filtered.append(text)

    return filtered



def scrape_nvidia_jobs_selenium(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # בלי לפתוח דפדפן ויזואלי
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(url)
    time.sleep(5)  # לחכות שייטען (אפשר לשפר עם WebDriverWait)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    job_links = soup.find_all('a', class_='css-19uc56f')

    #li_tags = soup.find_all('li')


    job_dict = {}

    for i, tag in enumerate(job_links, start=1):
        title = tag.text.strip()
        href = tag['href']
        full_link = BASE_URL + href

        job_dict[f'Job {i}'] = {
            'title': title,
            'link': full_link,

        }



    print(job_dict)
    return job_dict



def save_jobs_to_csv_no_duplicates(job_dict, title_job, filename='nvidia_jobs.csv', Date=datetime.date.today()):
    existing_links = set()

    # שלב 1: קריאת קובץ קיים ואיסוף כל הקישורים
    if os.path.isfile(filename):
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                existing_links.add(row['Link'])

    # שלב 2: פתיחת קובץ להוספה
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Date','Time','Title Job', 'Job ID', 'Title', 'Hebrew Title'  , 'Link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # רק אם הקובץ ריק – נוסיף כותרות
        if os.path.getsize(filename) == 0:
            writer.writeheader()

        new_jobs_count = 0
        # שלב 3: כתיבת משרות שלא קיימות
        for job_id, job in job_dict.items():
            try:
                title_he = translator.translate(job['title'])
            except Exception:
                title_he = "שגיאת תרגום"

            if job['link'] not in existing_links:
                writer.writerow({
                    'Date': Date,
                    'Time':time.strftime("%H:%M:%S"),
                    'Title Job': title_job,
                    'Job ID': job_id,
                    'Title': job['title'],
                    'Hebrew Title':title_he,
                    'Link': job['link'],
                })
                new_jobs_count += 1
        if new_jobs_count != 0:
            writer.writerow({field: '' for field in fieldnames})
            print("✍️ Added a new empty row")
        else:
            print("✅ All jobs found already! 🎉")

    print(f"✅ Added {new_jobs_count} new jobs to file {filename} (title: {title_job}, date: {Date})")

def del_file(filename):
    os.remove(filename)
if DEL_FILE:
    del_file(filename=file_name)


def get_data_dicts(main_job_title):
    colors = [
        Fore.RED,         Fore.GREEN,       Fore.YELLOW,      Fore.BLUE,        Fore.MAGENTA,
        Fore.CYAN,        Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTYELLOW_EX, Fore.LIGHTBLUE_EX,
        Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX, Fore.WHITE,     Fore.BLACK,       Fore.RESET,
        Fore.LIGHTBLACK_EX, Fore.LIGHTWHITE_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTRED_EX,
        Fore.MAGENTA,     Fore.CYAN,        Fore.YELLOW,      Fore.BLUE,        Fore.GREEN
    ]


    key_color_map = {}

    for i, (title) in enumerate(main_job_title):
        key_color_map[title] = colors[i % len(colors)]
    return key_color_map





location_code = '970bf8c909a701c749f87bdcd4008607'
main_job_title=[
    'student',
    'intern',
    'data',
    'ai',
    'deep',
    'machine',
    'junior',
    'python',
    'analyst',
    'machine',
    'algorithm',

    ]


key_color_map = get_data_dicts(main_job_title=main_job_title)

t1 = datetime.datetime.now()
print('🚀 Starting NVIDIA job scraping...')

for i in range (len(main_job_title)):
    item = main_job_title[i]
    student_question = f'https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite?q={main_job_title[i]}&locations={location_code}'

    print('-' * N)
    color = key_color_map.get(item, Fore.WHITE)
    print(color + f'🔎 Searching for "{item}" jobs in Nvidia...')

    jobs  = scrape_nvidia_jobs_selenium(student_question)
    save_jobs_to_csv_no_duplicates(jobs, title_job=item)
    t_now = datetime.datetime.now()
    print(f'⏱️ Elapsed time for {item} job: {t_now - t1}')


    if i > 0:
        print(f'⏳ Elapsed diff time: {t_now - t_prev}')

    t_prev = t_now


print('✅ Program finished.')
t2 = datetime.datetime.now()
print(f'🕒 Total elapsed time: {t2 - t1}')

import subprocess
import platform

system_name = platform.system()
subprocess.call(('open', file_name))



