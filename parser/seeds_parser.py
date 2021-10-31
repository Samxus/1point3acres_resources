import re
import requests
from lxml import etree
from prettytable import PrettyTable
from utils import json_loads, load_headers
from items.seed import seed


class seed_refer():
    def __init__(self):
        self.base_url = 'https://www.1point3acres.com/bbs/'
        self.url_list = []
        self.company_list = {}

        self.display_company()

        company_name = input('Input the Company name to Search\n')
        value = self.company_list[company_name]
        self.url = 'https://www.1point3acres.com/bbs/forum.php?mod=forumdisplay&fid=198&sortid=192&searchoption[3046][value]={}&searchoption[3046][type]=radio&filter=sortid&sortid=192&orderby=dateline'.format(
            value)

    def display_company(self):
        table = PrettyTable(['ID', 'Company_Name'])
        self.company_list = json_loads('./selective_key_value.json')
        for key, value in self.company_list.items():
            table.add_row([value, key])
        print(table)

    def download(self, url):
        self.url_list.append(url)
        headers = load_headers('desktop', 'mac', 'chrome')
        content = requests.get(url=url, headers=headers).text
        return content

    def parse_end_page(self):
        content = etree.HTML(self.download(self.url))
        page_col = content.xpath('//*[@id="fd_page_bottom"]/div/label/span')
        if page_col:
            last_page_re = re.compile('/ (.*?) 页')
            last_page = last_page_re.findall(page_col[0].text)[0]
            for i in range(2, int(last_page)):
                self.url_list.append(self.url + '&page=' + str(i))

    def parse(self):
        self.parse_end_page()
        display = PrettyTable(["Tag", "Title", "URL", "Views", "Reply", "Time", "Last_Post_Time"])
        for i in range(len(self.url_list)):
            url = self.url_list[i]
            content = etree.HTML(self.download(url))
            table = content.xpath('//*[@id="threadlisttableid"]')[0]
            posts = table.xpath('.//tbody')
            for post in posts:
                tr = post.xpath('./tr')[0]
                reply = tr.xpath('./td[@class="num"]/a')
                view = tr.xpath('./td[@class="num"]/em')
                title = tr.xpath('./th/a')
                tag = tr.xpath('./th/em/a')
                url = tr.xpath('./th/a/@href')
                time = tr.xpath('./td[@class="by"][1]/em/span')
                last_posts = tr.xpath('./td[@class="by"][2]/em/a')
                # print(reply, view, title, tag, url, time, last_posts)
                if reply and view and title and tag and url and time and last_posts:
                    item = seed()
                    item.title = title[0].text
                    item.reply = int(reply[0].text)
                    item.last_post = last_posts[0].text
                    item.url = self.base_url + url[0]
                    item.view = int(view[0].text)
                    item.tag = tag[0].text
                    item.time = time[0].text
                    display.add_row(
                        [item.tag, item.title[:12], item.url, item.view, item.reply, item.time, item.last_post])
        print(display)
