from bs4 import BeautifulSoup
import requests
import threading
import tkinter as tk
from tkinter import ttk
import sv_ttk
import csv
import datetime
import json
import threading
from multiprocessing import freeze_support
from urllib.parse import urlparse
import pandas as pd 
import numpy as np
import re

def scrape_link():
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'en-US,en;q=0.9',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':'session-id=140-4630537-5492465; session-id-time=2082787201l; ubid-main=131-0148058-7172139; session-token=Eisk3nOzWnkHgskZw3hNSHa65W7VSWNUfheit1OCCZRkteGXiyYd3Q8BWfK8dCOIQQI/Hf1atzyh2tIDr29NfEzJw3ya5IArqCWYK+QOrAjuJhGPRa2bbjpL9Wm5w1mwOQcmT15h7GBMPD6oRyguu3mDH/S6yGRNopfRV1h5xwVoQlmBQrnq8FqBlkplsuTSMweiZyKjPE7ry4Or6agOthWLR60NywMlwTd48yc/vtJBOUidAdY+UzpDPkpTJ00+A8Ve8bnCsHdVX7l8ZvGrtZjRpNvz7UbNVmUNUrjQ/AAt6DqpslKU8FcoAcIoJanDFollezfqO3frU4fBZhZB2A; csm-hit=adb:adblk_yes&t:1696169066448&tb:ZXBCF05XVT3FYYT69K5R+b-ESXFGXDEWV1YW2JVRTV1|1696169066448',
        'Host':'www.boxofficemojo.com',
        'Referer':'https://www.boxofficemojo.com/year/?ref_=bo_nb_yl_secondarytab',
        'Sec-Ch-Ua':'"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'Sec-Ch-Ua-Mobile':'?0',
        'Sec-Ch-Ua-Platform':"Windows",
        'Sec-Fetch-Dest':'document',
        'Sec-Fetch-Mode':'navigate',
        'Sec-Fetch-Site':'same-origin',
        'Sec-Fetch-User':'?1',
        'Upgrade-Insecure-Requests': 1,
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    }
    response=requests.get('https://www.boxofficemojo.com/year/?ref_=bo_nb_yl_secondarytab')
    soup = BeautifulSoup(response.text, "lxml")
    # soup = soup.encode("utf-8")
    csv_content = []
    table = soup.find('div', {"id":"table"}).find('table', class_='mojo-table-annotated')
    for i, row in enumerate(table.find_all('tr')):
        if i == 0:
            
            continue
        else:
            content = {}
            film_years = row.find_all('td')
            if len(film_years) > 0:
                url_film = film_years[0].find_all('a')[0]
                url_film_year = url_film.get('href')
                if (int(url_film.text.strip()) > 1979):
                    content['year'] = url_film.text.strip()
                    response1 = requests.get('https://www.boxofficemojo.com' + url_film_year)
                    soup1 = BeautifulSoup(response1.text, "lxml")
                    year_film_lists_table = soup1.find('div', {'id':'table'}).find('table', class_="mojo-body-table-compact")

                    for j, row1 in enumerate(year_film_lists_table.find_all('tr')):
                        if j == 0:
                            # response3 = requests.get('https://pro.imdb.com/company/co0002663/boxoffice/?area=XDOM&ref_=mojo_rl_su&rf=mojo_rl_su')
                            # soup3 = BeautifulSoup(response3.text, 'lxml')
                            # print(soup3.encode('utf-8'))
                            continue
                        else:
                            each_film = row1.find_all('td')
                            if (len(each_film) > 0):
                                film_selector = each_film[1].find('a', class_='a-link-normal')
                                
                                each_film_url = 'https://www.boxofficemojo.com' + film_selector.get('href')
                                content['film_name'] = film_selector.text
                                response2 = requests.get(each_film_url)
                                soup2 = BeautifulSoup(response2.text, "lxml")
                                earning = soup2.find('div', class_='mojo-performance-summary-table').find_all('span', class_='money')
                                try:
                                    if (earning[0]):
                                        content['domestic'] = earning[0].text
                                    else:
                                        content['domestic'] = ''
                                    if (earning[1]):
                                        content['international'] = earning[1].text
                                    else:
                                        content['international'] = ''
                                    if (earning[2]):
                                        content['worldwide'] = earning[2].text
                                    else:
                                        content['worldwide'] = ''
                                    
                                except Exception as e:
                                    print(f"{e}")

                                #getting properties
                                property_part_list = soup2.find('div', class_='mojo-hidden-from-mobile').find_all('div', class_='a-spacing-none')
                                try:
                                    
                                    if (property_part_list[0].find_all('span')[1]):
                                        distributer_temp = property_part_list[0].find_all('span')[1].text
                                        distributer_search_char = property_part_list[0].find_all('span')[1].find('a', class_='a-link-normal').text
                                    
                                        distributer_start_pos = distributer_temp.index(distributer_search_char.strip())
                                        
                                        content['distributer'] = distributer_temp[0:distributer_start_pos]
                                        
                                    else:
                                        content['distributer'] = ''
                                    if (property_part_list[2].find_all('span')[1]):
                                        content['release_date'] = property_part_list[2].find_all('span')[1].text
                                    else:
                                        content['release_date'] = ''
                                    if (property_part_list[3].find_all('span')[1]):
                                        content['MPAA'] = property_part_list[3].find_all('span')[1].text
                                    else:
                                        content['MPAA'] = ''
                                    if (property_part_list[5].find_all('span')[1]):
                                        genres_temp = property_part_list[5].find_all('span')[1].text
                                        genres_temp = genres_temp.replace(' ', '')
                                        genres_temp = re.sub(r'\n', '', genres_temp)
                                        genres_arry = re.split(r'(?=[A-Z])', genres_temp)
                                        genres_temp = ", ".join(genres_arry)
                                        content['genres'] = genres_temp[2:]
                                    else:
                                        content['genres'] = ''
                                    # if (property_part_list[8].find('a', class_='a-link-normal')):
                                    #     deep_url = property_part_list[8].find('a', class_='a-link-normal').get('href')
                                    #     response3 = requests.get(deep_url)
                                    #     soup3 = BeautifulSoup(response3, 'lxml')
                                    #     print(soup3.find('div', id='const_page_summary_section'))
                                except Exception as e:
                                    print(f'{e}')
                                print(content)
                                csv_content.append(content)
                                # break
                
            # break
                

                
    current_datetime = datetime.datetime.now()
    csv_file = f"BoxOffice Scrape - {current_datetime.strftime('%d-%m-%Y %H_%M_%S')}.csv"

    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["film_name", "domestic", "international", "worldwide", "distributer", "release_date", "MPAA","genres", "year"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for csv_row in csv_content:
            writer.writerow(csv_row)
    
    # print(csv_content)
    # print(csv_header)
    # arr = np.asarray(csv_content)
    # pd.DataFrame(arr).to_csv('sample.csv', index_label = "", header  = csv_header) 
    startbot.config(state='disabled', text='Completed!')

def main():
    startbot.config(state='enabled', text='Processing...')
    scrape_link()

if __name__ == "__main__":
    global startbot
    
    freeze_support()
    app = tk.Tk()
    app.title(f'BoxOffice Scraper')
    app.minsize(400, 300)
    app.maxsize(400, 300)
    ttk.Frame(app, height=30).pack()
    title = tk.Label(app, text='BoxOffice Scraper', font=("Calibri", 24, "bold"))
    title.pack(padx=10, pady=30, fill=tk.X)
    startbot = ttk.Button(app, text='Start Bot', style='Accent.TButton', width=15,
                          command=lambda:threading.Thread(target=main).start())
    startbot.pack(pady=40)
    sv_ttk.set_theme('dark')
    app.mainloop()


