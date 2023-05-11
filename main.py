from proxy import ProxyParser
from proxy_list_scraper import Scraper

def main():

    # for valid in ProxyParser.valid_proxy_generator():
    #     print(valid)

    scraper = Scraper()
    scraper.save_proxies()

    proxies_filename = "scraped_proxies.txt"

    ProxyParser.parse_raw(proxies_filename)

    for valid in ProxyParser.valid_proxy_generator(proxies_filename):
        print(valid)


if __name__ == '__main__':
    main()