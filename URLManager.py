#coding:utf-8
import pickle
import hashlib
class URLManager(object):
    def __init__(self):
        self.new_urls = self.load_progress('new_urls.txt')
        self.old_urls = self.load_progress('old_urls.txt')

    # 是否还有新的url
    def has_new_url(self):
        return self.new_url_size() > 0
    def get_new_url(self):
        new_url = self.new_urls.pop()
        url_md5 = self.getUrl_md5(new_url)
        self.old_urls.add(url_md5)
        return new_url
    def new_url_size(self):
        return len(self.new_urls)
    def old_url_size(self):
        return len(self.old_urls)

    def add_new_urls(self,urls):
        if urls is not None and len(urls)>0:
            for url in urls:
                self.add_new_url(url)
                
    def add_new_url(self,url):
        if url is not None:
            url_md5 = self.getUrl_md5(url)
            if url not in self.new_urls and url_md5 not in self.old_urls:
                self.new_urls.add(url)
            
    def save_progress(self,path,data):
        with open(path,'wb') as f:
            pickle.dump(data,f)

    def load_progress(self,path):
        try:
            with open(path,'r') as f:
                return pickle.load(f)
        except:
            return set()
        

    def getUrl_md5(self,url):
        md = hashlib.md5()
        md.update(url)
        return md.hexdigest()[8:-8]