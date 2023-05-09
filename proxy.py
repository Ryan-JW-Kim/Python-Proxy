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
