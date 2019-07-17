import requests
from bs4 import BeautifulSoup
import pymongo


class IP_POOL():
    def __init__(self):
        self.data = {}
        #所有库
        self.client = pymongo.MongoClient('localhost', 27017)
        #指定具体库
        self.db_name = self.client['ip_pool']
        #指定具体表
        self.ip_port = self.db_name['ip_port']

    def get_ips_from_web(self):

        #cookie need paste every time, get from the website.
        #next try to get cookie auto matically
        cookies = '__jsluid_h=19232d6446d0181275a87c07056cefce; Hm_lvt_1761fabf3c988e7f04bec51acd4073f4=1563373299; ' \
                  'Hm_lpvt_1761fabf3c988e7f04bec51acd4073f4=1563373317; ' \
                  '__jsl_clearance=1563374443.876|0|O1LVKz9VC5nNQtkNXfYLvSt9Fj0%3D '
        header = {
            'Cookie': cookies,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/75.0.3770.100 Safari/537.36 '
        }
        url = 'http://www.66ip.cn/areaindex_2/1.html'
        web_content = requests.get(url, headers=header)
        soup = BeautifulSoup(web_content.text.encode('iso-8859-1'), 'lxml')
        ips = soup.select('#footer > div > table > tr > td:nth-child(1)')
        ports = soup.select('#footer > div > table > tr > td:nth-child(2)')
        for ip, port in zip(ips, ports):
            temp = {
                ip.get_text(): port.get_text()
            }
            self.data.update(temp)
        self.data.pop('ip')
        return self.data

    def check_ip_port(self,data):
        for ip in data:
            proxy = {ip: data[ip]}
            url = 'http://www.baidu.com/'
            web = requests.get(url, proxies=proxy)
            if web.status_code != 200:
                print('代理不能用')
                data.pop(ip)
            else:
                print('代理ok')
        return data

    def save_db(self,data):
        '''
        就按字典存入数据库
        '''
        data = self.replace_symble(data)
        self.ip_port.insert_one(data)

    def replace_symble(self,data):
        replace_data = {}
        for ip in data:
            port = data[ip]
            index = ip.find(".")
            if index != 1:
                ip = ip.replace(".",",")
            temp = {
                ip:port
            }
            replace_data.update(temp)
        return replace_data

    def check_valid(self):
        '''
        按时间检索ip和port是否能代理
        定时检查数据库中的数据。
        定时增删数据
        :return:
        '''
        pass

