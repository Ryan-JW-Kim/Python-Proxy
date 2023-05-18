import requests
from bs4 import BeautifulSoup
from time import gmtime, strftime
import json

class FreeProxyList:
    free_proxy_list_key_mappings = ["IP Address", "Port", "Code", "Country", "Anonymity", "Google", "Https", "Last Checked"]
    def __init__(self, filename=None):

        self.url = "https://free-proxy-list.net"
        self.html = requests.get(self.url).text
        self.soup = BeautifulSoup(self.html, "html.parser")
        timestamp = strftime("%Y_%m_%d-%H_%M_%S", gmtime())
        
        table_body = self.soup.find("tbody")
        table_rows = table_body.find_all("tr")

        self.proxies_data = []

        for row in table_rows:

            row_data = row.find_all("td")

            proxy_data = {}

            for i in range(len(row)):
                proxy_data[FreeProxyList.free_proxy_list_key_mappings[i]] = row_data[i].text
        
            self.proxies_data.append(proxy_data)

        if filename is not None:
            with open(f"{filename}_{timestamp}.json", "w") as json_file:
                json.dump(self.proxies_data, json_file, indent=4)

class ProxyTools:
    
    valid_status_codes = [200, 301, 302, 307]
    default_test_url = "https://www.google.com/"

    @staticmethod
    def test_proxy(proxy_dict):
        try:
            ip = proxy_dict["IP Address"]
            port = proxy_dict["Port"]
            response = requests.get(ProxyTools.default_test_url, proxies={"http": f"http://{ip}:{port}"}, timeout=3)

            if response.status_code in ProxyTools.valid_status_codes:
                print(f"Working Proxy: {ip}:{port}")
                return True

        except Exception as e:
            print(f"Error: {e}")
            return False
        
    @staticmethod
    def format_proxy(proxy_dict, https=False):
        ip = proxy_dict["IP Address"]
        port = proxy_dict["Port"]

        proxy_dict = {"http": f"http://{ip}:{port}"}

        if https:
            proxy_dict["https"] = f"https://{ip}:{port}"

        return proxy_dict