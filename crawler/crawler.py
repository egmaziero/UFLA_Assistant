import urllib3
import re
from bs4 import BeautifulSoup
import os
import justext

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}

http = urllib3.PoolManager(10, headers=user_agent)


class Crawler:
    
    def __init__(self, corpus_path, max_files, seed_url, url_pattern):
        self.corpus_path = corpus_path
        self.max_files = max_files
        self.seed_url = seed_url
        self.url_pattern = url_pattern
        self.visited_links = {}
        self.to_be_visited = []
        
        if not os.path.exists(self.corpus_path):
            os.makedirs(self.corpus_path)
        
    def crawl(self):
        first_urls = self.get_page(self.seed_url)
        self.add_links(first_urls)
        next_link = self.get_next_link()
        
        file_counter = 1
        while next_link and file_counter < self.max_files:
            links = self.get_page(next_link)
            self.add_links(links)
            next_link = self.get_next_link()
            file_counter += 1
    
    def get_links(self, page_data):
        links = re.findall(self.url_pattern, str(page_data))
        #print('wuw', links)
        links2 = []
        for link in links:
            link = ('https://ufla.br'+link)
            links2.append(link)
        #print(links)
        return links2            
    
    def get_page(self, url):
        print("getting page {}".format(url))
        response = http.request('GET', url)

        # store text content
        paragraphs = justext.justext(response.data, justext.get_stoplist("Portuguese"))
        with open("{}/{}.txt".format(self.corpus_path, url.replace(".", "_").replace("/","-")), "w") as output_file:
            for paragraph in paragraphs:
                if not paragraph.is_boilerplate:
                    output_file.write(paragraph.text)
        
        # get links
        links = self.get_links(response.data)
        
        return links

    def add_links(self, links):
        links = list(set(links))
        self.to_be_visited.extend([link for link in links if link not in self.visited_links])

    def get_next_link(self):
        next_link = self.to_be_visited.pop(0)
        self.visited_links[next_link] = None
        return next_link
    
crawler_ufla = Crawler("data/corpora/ufla/noticias/", 500, "https://ufla.br/noticias", '"(/noticias/\w+.*?)"') #'"(/noticias/ensino/\d+.*?)"'
crawler_ufla.crawl()
