import urllib.request
from bs4 import BeautifulSoup
import cloudscraper
from time import sleep
import requests
import random












 
class ScraperDisboardInvites:
    def __init__(self):
        
        self.urls = ['https://disboard.org/pt-br/search?keyword=panela', 'https://disboard.org/pt-br/search?keyword=panelinha']
        self.html_contents = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
        }
        self.scraper_cloudscraper = cloudscraper.create_scraper(
            browser={"browser": "chrome", "platform": "windows", "mobile": False}
        )
        
        self.link_invites_brutos = []
        self.links_convites = []
        self.pegar_htmls()
        self.filtrar_links_brutos()
        self.pegar_link_discord()
        
    def pegar_htmls(self):
        for url in self.urls:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req) as response:
                html_content = response.read().decode('utf-8')
            self.html_contents.append(html_content)   
            
            
        
    def filtrar_links_brutos(self):
        contador = 0
        for html_content in self.html_contents:
            soup = BeautifulSoup(html_content, 'html.parser')
            for a in soup.find_all('a', class_="button button-join is-discord"):
                link = "https://disboard.org" + a['href']
                
                if link not in self.link_invites_brutos:
                    
                    self.link_invites_brutos.append(link)
                    print(self.link_invites_brutos)
                    print(contador)
                    contador += 1
                    if contador == 3:
                        return
                

                    
    def pegar_link_discord(self):

        for link in self.link_invites_brutos:
            try:
                
                page = self.scraper_cloudscraper.get(link)
                soup = BeautifulSoup(page.text, 'html.parser')
                csrf_token = soup.find("meta", attrs={"name": "csrf-token"})["content"]
                print(f"[!] Token CSRF encontrado")
                sleep(random.uniform(1, 10))
                self.scraper_cloudscraper.headers.update({
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/137.0.0.0 Safari/537.36"
                ),
                "X-Csrf-Token": csrf_token,
                "X-Requested-With": "XMLHttpRequest",
                "Referer": link,
                "Origin": "https://disboard.org"
})              
                
                
                link_pegar_invite = "https://disboard.org/site/get-invite/"
                server_id = link.split('/')[-1]
                link_final = link_pegar_invite + server_id
                response = self.scraper_cloudscraper.post(link_final, data={})
                self.links_convites.append(response.text.replace('"', ''))
                print(response.text)

            except Exception as e:
                print(f"[ERRO] Falha ao acessar {link}: {e}")
                

                
if __name__ == "__main__"
 scraper = ScraperDisboardInvites()
