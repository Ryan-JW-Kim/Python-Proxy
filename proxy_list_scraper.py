import requests
from bs4 import BeautifulSoup

class Scraper:

    def __init__(self):

        self.url = "https://free-proxy-list.net"
        self.html = requests.get(self.url).text
        self.soup = BeautifulSoup(self.html, "html.parser")
        
        table_body = self.soup.find("tbody")
        table_rows = table_body.find_all("tr")

        self.proxies_data = []

        for row in table_rows:

            row_data = row.find_all("td")

            proxy_data = []

            for data in row_data:
                proxy_data.append(data.text)
        
            self.proxies_data.append(proxy_data)
        
    def save_proxies(self, filename="scraped_proxies.txt"):

        with open(filename, "w") as f:
            for proxy in self.proxies_data:
                f.write("\t".join(proxy) + "\n")
