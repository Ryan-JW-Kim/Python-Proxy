import requests
from bs4 import BeautifulSoup
from time import gmtime, strftime
import json

class FreeProxyList:
    free_proxy_list_key_mappings = ["IP Address", "Port", "Code", "Country", "Anonymity", "Google", "Https", "Last Checked"]
    def __init__(self, filename=None):
        """
        Tool for webscraping a list of free proxies.
        """

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
        """
        Test Proxy with data stored in dictionary.
        
        Input: 
            proxy_dict = {
                "IP Address",
                "Port",
                "Code",
                "Country",
                "Anonymity",
                "Google",
                "Https",
                "Last Checked"
            }
        
        Output:
            True if proxy is working, False if not.
        """

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
        """
        Format a proxy dictionary into a dictionary that can be used by the requests library.

        Input:
            proxy_dict = {
                "IP Address",
                "Port",
                "Code",
                "Country",
                "Anonymity",
                "Google",
                "Https",
                "Last Checked"
            }

            https = True if you want to use the proxy for https requests.
        """
        ip = proxy_dict["IP Address"]
        port = proxy_dict["Port"]
        proxy_dict = {"http": f"http://{ip}:{port}"}

        if https:
            if proxy_dict["Https"] == "yes":
                proxy_dict["https"] = f"https://{ip}:{port}"
            else:
                print(f"Error: Proxy {ip}:{port} does not support HTTPS.")

        return proxy_dict