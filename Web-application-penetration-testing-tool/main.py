import CMS_fingerprinting
import Cross_site_scripting
import Social_engineering_dictionary
import SQL_injection
import Vulnerability_scanning
import Weak_cipher_blasting
import Social_engineering_dictionary.Fake_info_generation
import Social_engineering_dictionary.Generate_dictionary
import Vulnerability_scanning.SQLi_scanner
import Vulnerability_scanning.XSS_scanner
import Weak_cipher_blasting.DVWA_login_blasting
import Weak_cipher_blasting.MySQL_login_blasting
import Port_scanning


def menu():
    while True:
        print('[START] ======欢迎进入简单的web应用渗透测试工具======')
        print('[MENU] 输入数字选择功能')
        print('1. CMS指纹扫描')
        print('2. 端口服务扫描')
        print('3. 社工字典生成')
        print('4. 弱密码爆破')
        print('5. 漏洞扫描')
        print('6. SQL注入攻击')
        print('7. 跨站脚本攻击')
        print('0. 退出程序')
        i = input('[INPUT] 输入数字选择功能:')
        if i == '1':
            CMS_fingerprinting.main()
        elif i == '2':
            Port_scanning.main()
        elif i == '3':
            Social_engineering_dictionary.main()
        elif i == '4':
            Weak_cipher_blasting.main()
        elif i == '5':
            Vulnerability_scanning.main()
        elif i == '6':
            SQL_injection.main()
        elif i == '7':
            Cross_site_scripting.main()
        elif i == '0':
            print("[END] ======欢迎下次使用======")
            break
        else:
            print('[-] 输入无效，请重新输入')


def main():
    menu()


if __name__ == '__main__':
    main()
