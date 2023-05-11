import requests

class ProxyParser:
    
    free_proxy_list_key_mappings = ["IP Address", "Port", "Code", "Country", "Anonymity", "Google", "Https", "Last Checked"]
    valid_status_codes = [200, 301, 302, 307]
    default_test_url = "https://www.google.com/"

    @staticmethod
    def test_proxy(proxy_dict):
        try:
            ip = proxy_dict["IP Address"]
            response = requests.get(ProxyParser.default_test_url, proxies={"http": f"http://{ip}"}, timeout=30)

            if response.status_code in ProxyParser.valid_status_codes:
                return True

        except Exception as e:
            print(f"Error: {type(e)}")
            return False

    @staticmethod
    def parse_raw(filename="raw_proxies.txt"):
        filename = filename
        proxies = []

        with open(filename, "r") as f:
            for line in f.readlines():
                
                segments = line.split("\t")

                temp = {}

                for i in range(len(segments)):
                    temp[ProxyParser.free_proxy_list_key_mappings[i]] = segments[i]
                
                proxies.append(temp)
        return proxies
    
    @staticmethod
    def compile_valid_proxies():
        proxies = ProxyParser.parse_raw()

        valid_proxies = []

        for proxy in proxies:
            if ProxyParser.test_proxy(proxy):
                valid_proxies.append(proxy)
    
        with open("valid_proxies.txt", "w") as f:
            for proxy in valid_proxies:
                f.write(f"{proxy['IP Address']}\n")
    
        return valid_proxies
    
    @staticmethod
    def valid_proxy_generator(filename="raw_proxies.txt"):

        proxies = ProxyParser.parse_raw(filename)

        for proxy in proxies:
            if ProxyParser.test_proxy(proxy):
                yield proxy


class ProxyBatch:

    def __init__(self, proxies, urls, batch_size=10):
        self.proxies = proxies
        self.urls = urls
        self.batch_size = batch_size

    def execute_batch(self):

        proxy_index = 0
        batch_count = 0
        data = {}
        for url in self.urls:

            if proxy_index >= len(self.proxies):
                proxy_index = 0
            
            proxy = self.proxies[proxy_index]

            try:
                response = requests.get(url, proxies={"http": f"http://{proxy}"}, timeout=30)
                data[url] = response.text

            except Exception as e:
                print(f"Error: {type(e)}")
                data[url] = None

            batch_count += 1
            
            if batch_count >= self.batch_size:
                batch_count = 0
                proxy_index += 1
            
            return data
        