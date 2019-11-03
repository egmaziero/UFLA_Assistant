# Como executar:

# Entre no virtual environment (caso você use)
# Vá para a pasta do projeto (você deverá ver crawler e scrapy.cfg. A pasta data irá aparecer quando você executar o crawler)
# Execute no terminal
# scrapy crawl pages5


#ATENÇÃO!!!
# 1 - Só pega até o dia 04/07/18 (Equipe de robótica Troia disputa Winter Challenge...)
# 2 - Não para sozinho após chegar no último post

import scrapy
import re
import os


class UflaSpider(scrapy.Spider):
    
    name = "pages5"
    
    #Local de armazenamento das páginas
    corpus_path = 'data/corpora/ufla/noticias/ensino'
    
    def start_requests(self):
        urls = [
            'https://ufla.br/noticias/ensino',
            #'https://ufla.br/noticias/ensino?start=9',
            #'https://ufla.br/noticias/ensino?start=18',
            #'https://ufla.br/noticias/ensino/13386-congressos-da-ufla-iniciam-segunda-feira-4-11-confira-a-programacao-e-participe',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
    def parse(self, response):
        
        #Cria a pasta onde serão salvas as páginas
        if not os.path.exists(self.corpus_path):
            os.makedirs(self.corpus_path)
        
        page_name = response.url.split("/")
        
        #Este passo só é necessário para a correta nomenclatura do arquivo no passo abaixo
        try:
            page_name[5]
        except IndexError:
            page_name.append('')

        #Salva o arquivo no local indicado usando o nome extraído do próprio link.
        #Seguindo o padrão: uflanoticias - categoria - nomedopost. 
        filename = 'uflanoticias-{}-{}.html'.format(page_name[4], page_name[5])
        with open(os.path.join(self.corpus_path, filename), 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        
        
        
        #Links úteis por página

        posts = [
        
            #1 Post
            'https://ufla.br'+str(response.css('.blog > div:nth-child(2) > div:nth-child(1) > h3:nth-child(3) > a:nth-child(1)::attr(href)').get()),
        
            #2 Post
            'https://ufla.br'+str(response.css('.blog > div:nth-child(2) > div:nth-child(2) > h3:nth-child(3) > a:nth-child(1)::attr(href)').get()),
        
            #3 Post
            'https://ufla.br'+str(response.css('.blog > div:nth-child(2) > div:nth-child(3) > h3:nth-child(3) > a:nth-child(1)::attr(href)').get()),
        
            #4 Post
            'https://ufla.br'+str(response.css('div.row:nth-child(3) > div:nth-child(1) > h3:nth-child(3) > a:nth-child(1)::attr(href)').get()),
        
            #5 Post
            'https://ufla.br'+str(response.css('div.row:nth-child(3) > div:nth-child(2) > h3:nth-child(3) > a:nth-child(1)::attr(href)').get()),
        
            #6 Post
            'https://ufla.br'+str(response.css('div.row:nth-child(3) > div:nth-child(3) > h3:nth-child(3) > a:nth-child(1)::attr(href)').get()),
        
            #7 Post
            'https://ufla.br'+str(response.css('div.row:nth-child(4) > div:nth-child(1) > h3:nth-child(3) > a:nth-child(1)::attr(href)').get()),
        
            #8 Post
            'https://ufla.br'+str(response.css('div.row:nth-child(4) > div:nth-child(2) > h3:nth-child(3) > a:nth-child(1)::attr(href)').get()),
        
            #9 Post
            'https://ufla.br'+str(response.css('div.row:nth-child(4) > div:nth-child(3) > h3:nth-child(3) > a:nth-child(1)::attr(href)').get()),
        
        ]
        
        
        #Pega todos os 9 posts de uma página
        
        for post in posts:
            yield scrapy.Request(url=post, callback=self.parse)
        
        
        #Passa para a próxima página
        
        
        #Primeira página:
        #'https://ufla.br/noticias/ensino'
        
        #Segunda página adianta:
        #'https://ufla.br/noticias/ensino?start={}'
        #Onde {} é um múltiplo de 9. (Ex.: 9, 18, 27...)
        
        #Esta linha é necessária para pegar os números da URL para passar as páginas
        regex = re.findall('[0-9][0-9][0-9]|[0-9][0-9]|[0-9]', response.url.split('/')[4])
        
        #Condição de parada no post da equipe do troia ~gambiarra~ não implementado ainda
        
        try:
            response.url.split('/')[5]
        except IndexError:
            
            #Primeira página
            #Pelo comportamento do site da UFLA se esta for a primeira
            #página não haverá números na URL. Então se a lista contendo
            #os números da URL for vazia isso irá provar que está na 
            #primeira página.
            
            if regex == []:
                next_page = 'https://ufla.br/noticias/ensino?start=9'
                
            #Não é primeira página
            #Se não é a primeira página pega o número que há na URL
            #soma 9 a esse número e monta a URL da próxima página.
            else: 
                
                oldnumber = ''.join(regex)
                oldnumber = int(oldnumber)
                newnumber = oldnumber + 9
                newnumber = str(newnumber)
                next_page = 'https://ufla.br/noticias/ensino?start={}'.format(newnumber)
            
            #Se tudo deu certo no passo anterior chama a função novamente
            #passando o novo endereço garantindo que o crawler
            #percorra todo o site.
            if next_page is not None:
                yield scrapy.Request(next_page, callback=self.parse)
                
        
        #Checo se é o post do troia
        #print(response.url.split('/'))
        #regexfinal = re.findall('[0-9][0-9][0-9][0-9][0-9]|[0-9][0-9][0-9][0-9]|[0-9][0-9][0-9]|[0-9][0-9]|[0-9]', response.url.split('/')[5])
        #regexfinal = ''.join(regexfinal)
        
        #if regexfinal == 12012:
            #next_page = None
        
