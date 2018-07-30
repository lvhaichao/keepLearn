import queue
import time

from Project.DataOutput import DataOutput
from Project.URLManager import URLManager
from multiprocessing.managers import BaseManager
from multiprocessing import Process

class NodeManager(object):
    def start_manager(self,url_q,result_q):
        BaseManager.register('get_result_queue',callable=lambda:result_q)
        BaseManager.register('get_url_queue',callable=lambda:url_q)
        manager = BaseManager(address=('',8000),authkey='baike')
        return manager

    def url_manager_proc(self,con_q,url_q,root_url):
        urlManager = URLManager()
        urlManager.add_new_url(root_url)
        while True:
            if urlManager.has_new_url():
                new_url = urlManager.get_new_url()
                url_q.put(new_url)
                if(urlManager.old_url_size>1000):
                    url_q.put('end')
                    urlManager.save_progress('new_urls.txt',urlManager.new_urls)
                    urlManager.save_progress('old_urls.txt',urlManager.old_urls)
                    return
                try:
                    if not con_q.empty():
                        urls = con_q.get()
                        urlManager.add_new_urls(urls)
                    else:
                        time.sleep(0.1)
                except BaseException as e:
                    print(e)
            
    
    def result_solve_proc(self,result_q,conn_q,store_q):
        while True:
            if not result_q.empty():
                content = result_q.get()
                if(content == 'end'):
                    store_q.put('end')
                    return
                new_urls = content['new_urls']
                data = content['data']
                conn_q.put(new_urls)
                store_q.put(data)
            else:
                time.sleep(0.1)
        
    
    def store_proc(self,store_q):
        dataOutput = DataOutput()
        while True:
            if not store_q.empty():
                data = store_q.get()
                if(data == 'end'):
                    dataOutput.output_end()
                    return
                dataOutput.store_data(data)
                dataOutput.output_html()
            else:
                time.sleep(0.1)

if __name__ == '__main__':
    url_q = queue.Queue()
    result_q = queue.Queue()
    conn_q = queue.Queue()
    store_q = queue.Queue()
    node = NodeManager()      
    manager = node.start_manager(url_q,result_q)

    url_proc = Process(target='url_manager_proc',args=(conn_q,url_q,'https://baike.baidu.com/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB/5162711'))
    result_proc = Process(target='result_solve_proc',args=(result_q,conn_q,store_q))
    store_proc = Process(target='store_proc',args=(store_q,))

    url_proc.start()
    result_proc.start()
    store_proc.start()
    manager.get_server().serve_forever()
