import requests
from bs4 import BeautifulSoup
import json

class DBLP:
    def __init__(self):
        self.base_url = 'https://dblp.org/'
        self.headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
        }

    def get_name(self, name:str):
        name_list = name.split(' ')
        name_request = '+'.join(name_list)
        search_url = self.base_url + 'search/author/api'
        search_name_data = requests.get(search_url, params={'q':name_request, 'format': 'json'}, headers=self.headers).json()
        json.dump(search_name_data, open('data.json', 'w'), indent=4)

        if_find = False
        for hit in search_name_data['result']['hits']['hit']:
            info = hit['info']
            author = info['author']
            if author == name:
                if_find = True
                author_url = info['url'] + '.xml'
                author_response = requests.get(author_url, headers=self.headers)
                soup = BeautifulSoup(author_response.text, 'xml')
                entries = soup.find_all('r')  # 每一篇论文
                return entries, if_find

        if len(search_name_data['result']['hits']['hit']) >= 1:
            # 如果没有找到完全匹配的作者，返回第一个作者的信息
            info = search_name_data['result']['hits']['hit'][0]['info']

            author_url = info['url']+'.xml'
            author_response = requests.get(author_url, headers=self.headers)
            soup = BeautifulSoup(author_response.text, 'xml')
            entries = soup.find_all('r')  # 每一篇论文
            return entries, if_find
        else:
            # 如果没有找到任何作者，返回空列表
            return [], if_find

    def get_candidate_authors(self, name: str):
        name_list = name.split(' ')
        name_request = '+'.join(name_list)
        search_url = self.base_url + 'search/author/api'
        search_name_data = requests.get(search_url, params={'q': name_request, 'format': 'json'}, headers=self.headers).json()
        
        candidates = []
        for hit in search_name_data['result']['hits']['hit']:
            info = hit['info']
            candidates.append({
                'author': info['author'],
                'url': info['url']
            })
        return candidates

    def test_print(self):
        url = 'https://dblp.org/pid/09/2187.xml'  # 换成目标作者的pid地址
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'xml')  # 用 xml 解析器！

        entries = soup.find_all('r')  # 每一篇论文

        for entry in entries:
            title = entry.find('title')
            authors = entry.find_all('author')
            year = entry.find('year')

            print(f"标题: {title.text if title else 'N/A'}")
            print(f"作者: {[a.text for a in authors]}")
            print(f"年份: {year.text if year else 'N/A'}")
            print('-' * 40)

if __name__ == '__main__':
    dblp = DBLP()
    # dblp.test_print()
    entries, flag = dblp.get_name('Ya-qin Yang')
    for entry in entries:
        title = entry.find('title')
        authors = entry.find_all('author')
        year = entry.find('year')
        ee_tags = entry.find_all('ee')

        print(f"标题: {title.text if title else 'N/A'}")
        print(f"作者: {[a.text for a in authors]}")
        print(f"年份: {year.text if year else 'N/A'}")
        print(f"链接: {[ee.text for ee in ee_tags]}")
        print('-' * 40)