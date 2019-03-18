import re
from urllib import request, parse
from lxml import etree
import time
import pymysql
import sys


class SaveLiterature:
    def __init__(self, url, word):
        self.version = 3
        self.url = url
        self.word = word

    def analyse_url(self):
        # 判断相关关键字文献爬取的是具体还是模糊的
        url = self.url
        req = request.Request(url)
        response = request.urlopen(req, timeout=30)
        page = response.read()
        html = page.decode('utf-8')
        # page的数据格式为bytes类型，需要decode（）解码，转换成str类型
        selector = etree.HTML(html)
        div = selector.xpath('//div[@class="sc_content"]')
        if len(div) != 0:
            # 爬取模糊查询页面上的url
            self.get_lit_url(selector)
        else:
            # 直接爬取文献数据
            self.get_lit_data(selector)

    def get_lit_url(self, selector):
        print(1)
        urls = selector.xpath('//h3[@class="t c_font"]/a/@href')
        i = 0
        # 一页一般10个url
        while i < len(urls):
            url_req = request.Request('http://xueshu.baidu.com' + urls[i])
            url_response = request.urlopen(url_req, timeout=30)
            url_page = url_response.read()
            url_html = url_page.decode('utf-8')
            url_selector = etree.HTML(url_html)
            literature_name = url_selector.xpath('//h3[1]')[0]
            literature_name = literature_name.xpath('string(.)').strip()
            print(literature_name)
            author = url_selector.xpath('//p[@class="author_text"]')[0]
            author = author.xpath('string(.)').strip()
            pattern = re.compile(u"[\u4e00-\u9fa5]+")
            author_text = ""
            author_list = pattern.findall(author)
            for index in range(len(author_list)):
                author_text = author_text + author_list[index]
                if index < len(author_list) - 1:
                    author_text = author_text + ","
            print(author_text)
            abstract = url_selector.xpath('//p[@class="abstract"]/text()')[0]
            print(abstract)
            publish_text = url_selector.xpath('//div[@class="publish_wr"]/p[@class="publish_text"]')
            publish_time = url_selector.xpath('//p[@class="publish_text"]/span[1]/text()')
            if len(publish_text) == 0:
                publish_text = ""
            else:
                pattern = re.compile(u"[《]*[\u4e00-\u9fa5]+[》]*")
                text = pattern.search(publish_text[0].xpath('string(.)'), 0)
                # publish_text = publish_text[0]
                publish_text = text.group()
            print(publish_text)
            if len(publish_time) == 0:
                publish_time = ""
            else:
                publish_time = publish_time[0]
            print(publish_time)
            use_number = url_selector.xpath('//div[@class="ref_wr"]/p[2]')[0]
            use_number = use_number.xpath('string(.)').strip()
            print(use_number)
            self.data_db(literature_name, author_text, str(abstract),
                         publish_text, publish_time, use_number)
            i += 1

    def get_lit_data(self, selector):
        print(2)
        literature_name = selector.xpath('//h3[1]')[0]
        literature_name = literature_name.xpath('string(.)').strip()
        print(literature_name)
        author = selector.xpath('//p[@class="author_text"]')[0]
        author = author.xpath('string(.)').strip()
        pattern = re.compile(u"[\u4e00-\u9fa5]+")
        author_text = ""
        author_list = pattern.findall(author)
        for index in range(len(author_list)):
            author_text = author_text + author_list[index]
            if index < len(author_list) - 1:
                author_text = author_text + ","
        print(author_text)
        abstract = selector.xpath('//p[@class="abstract"]/text()')[0]
        print(abstract)
        publish_text = selector.xpath('//div[@class="publish_wr"]/p[@class="publish_text"]')
        publish_time = selector.xpath('//p[@class="publish_text"]/span[1]/text()')
        if len(publish_text) == 0:
            publish_text = ""
        else:
            pattern = re.compile(u"[《]*[\u4e00-\u9fa5]+[》]*")
            text = pattern.search(publish_text[0].xpath('string(.)'), 0)
            # publish_text = publish_text[0]
            publish_text = text.group()
        print(publish_text)
        if len(publish_time) == 0:
            publish_time = ""
        else:
            publish_time = publish_time[0]
        print(publish_time)
        use_number = selector.xpath('//div[@class="ref_wr"]/p[2]')[0]
        use_number = use_number.xpath('string(.)').strip()
        print(use_number)
        download = selector.xpath('//div[@class="allversion_content"]//a[@class="dl_item"]/@href')
        download_name = selector.xpath('//div[@class="allversion_content"]//span[@class="dl_source"]/text()')
        print(len(download))
        for n in range(0, len(download)):
            self.save_download_url(literature_name, str(download_name[n]), str(download[n].strip()))
        self.data_db(literature_name, author_text, str(abstract),
                     publish_text, str(publish_time), use_number)

    def data_db(self, literature_name, author_, abstract_, publish_, publish_time, use_number):
        print(type(literature_name), type(author_), type(abstract_), type(publish_), type(publish_time), type(use_number))
        db = pymysql.connect(host="localhost", user="root", password="123456",
                             database="literature_assistant", charset="utf8")
        cursor = db.cursor()
        sql = "insert into lit_literature(literatureName,author,abstractText,publish,publishTime,useNumber,downloadUrl)\
                   values('%s','%s','%s','%s','%s','%s')" % \
              (literature_name, author_, abstract_, publish_, publish_time, use_number)
        print(1)
        try:
            cursor.execute(sql)
            db.commit()
            print(2)
        except:
            db.rollback()
        db.close()

    def save_download_url(self, literature_name, url_name, url):
        db = pymysql.connect(host="localhost", user="root", password="123456",
                             database="literature_assistant", charset="utf8")
        cursor = db.cursor()
        sql = "insert into lit_download_url(literatureName,urlName,url)\
                           values('%s','%s','%s')" % \
              (literature_name, url_name, url)
        try:
            cursor.execute(sql)
            db.commit()
            print(1)
        except:
            db.rollback()
        db.close()



if __name__ == "__main__":
    for i in range(1, len(sys.argv)):
        keyword = sys.argv[i]
    server = 'http://xueshu.baidu.com'
    target = 'http://xueshu.baidu.com/s'
    wd = "关于教育公平的几个基本理论问题"
    #wd = keyword
    word_url = target + '?wd=' + parse.quote(wd)
    print(word_url)
    save_lit = SaveLiterature(word_url, wd)
    save_lit.analyse_url()
