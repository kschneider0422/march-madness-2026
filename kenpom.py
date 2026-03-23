from pathlib import Path
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

class Kenpom:
    
    def __init__(self):
        self.ratings_path = Path('data/ratings.json')
        if not self.ratings_path.exists():
            self.update()
        else:
            with self.ratings_path.open(mode='r', encoding='utf-8') as f:
                self.ratings = json.load(f)
                
    def update(self):
        
        # web scrape
        url = 'https://kenpom.com/index.php'
        browser = webdriver.Chrome()
        browser.get(url)
        sleep(10)
        html_source = browser.page_source
        soup = BeautifulSoup(html_source, 'lxml')
        browser.close()
        
        # parse html
        self.ratings = {}
        for tr in soup.find_all('tr'):
            tds = list(tr.find_all('td'))
            if len(tds) < 10:
                continue
            team_cell = tds[1]
            if team_cell.find('span') is None:
                continue
            team = team_cell.find('a').text
            AdjEM_cell = tds[4]
            AdjEM = AdjEM_cell.text.replace('+', '')
            AdjT_cell = tds[9]
            AdjT = AdjT_cell.text
            self.ratings[team] = {}
            self.ratings[team]['AdjEM'] = float(AdjEM)
            self.ratings[team]['AdjT'] = float(AdjT)
            
        #store
        with self.ratings_path.open(mode='w', encoding='utf-8') as f:
            f.write(json.dumps(self.ratings, indent=4))
            
            

            
            
