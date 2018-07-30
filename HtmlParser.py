from bs4 import BeautifulSoup
import re
import urllib

class HtmlParser(object):
    def parser(self,page_url,html_content):
        if page_url is None or html_content is None:
            return
        soup = BeautifulSoup(html_content,'html.parser',from_encoding='utf-8')
        new_urls = self._get_new_urls(page_url,soup)
        new_data = self._get_new_data(page_url,soup)
        return new_urls,new_data
    
    def _get_new_urls(self,page_url,soup):
        new_urls = set()
        links = soup.find_all('a',href=re.compile(r'/item/.*'))
        for link in links:
            url = link['href'];
            new_url = urllib.parse.urljoin(page_url,url)
            new_urls.add(new_url)
        return new_urls
    
    def _get_new_data(self,page_url,soup):
        data = {}
        data['url'] = page_url
        title = soup.find('dd',class_='lemmaWgt-lemmaTitle-title').find('h1')
        data['title'] = title.get_text()

        summary = soup.find('div',class_='lemma-summary')
        data['summary'] = summary.get_text()
        return data
