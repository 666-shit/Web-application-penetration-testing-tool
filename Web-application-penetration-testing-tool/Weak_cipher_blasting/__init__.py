# import DVWA_login_blasting as dvwa
# import MySQL_login_blasting as mysql


def menu():
    while True:
        print('[MENU] 输入数字选择功能:')
        print('1. DVWA登录爆破')
        print('2. Mysql登录爆破')
        print('0. 返回上一级')
        i = input('[INPUT] 输入数字选择功能:')
        if i == '1':
            DVWA_login_blasting.main()
        elif i == '2':
            MySQL_login_blasting.main()
        elif i == '0':
            break
        else:
            print('[-] 输入无效，请重新输入')


def main():
    menu()


# if __name__ == '__main__':
#     main()
