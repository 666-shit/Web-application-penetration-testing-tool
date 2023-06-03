# import Fake_info_generation as fake
# import Generate_dictionary as generate


def menu():
    while True:
        print('[MENU] 输入数字选择功能:')
        print('1. 生成虚假个人信息')
        print('2. 生成社工字典')
        print('0. 返回上一级')
        i = input('[INPUT] 输入数字选择功能:')
        if i == '1':
            Fake_info_generation.main()
        elif i == '2':
            Generate_dictionary.main()
        elif i == '0':
            break
        else:
            print('[-] 输入无效，请重新输入')


def main():
    menu()


# if __name__ == '__main__':
#     main()
