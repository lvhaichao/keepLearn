class DataOutput(object):
    def __init__(self):
        self.datas = []
        self.filepath = 'Project2/baike.html'
        self.output_head()

    def store_data(self,data):
        if data is None:
            return None
        self.datas.append(data)
    
    def output_html(self):
        with open(self.filepath,'w',encoding='utf-8') as f:
            for data in self.datas:
                f.write('<tr>')
                f.write('<td>%s</td>'%data['url'])
                f.write('<td>%s</td>'%data['title'])
                f.write('<td>%s</td>'%data['summary'])
                f.write('</tr>') 
                self.datas.remove(data)

    def output_head(self):
        with open(self.filepath,'w',encoding='utf-8') as f:
            f.write('<html>')
            f.write('<body>')
            f.write('<table>')

    def output_end(self):
        with open(self.filepath,'w',encoding='utf-8') as f:
            f.write('</table>')
            f.write('</body>')
            f.write('</html>')