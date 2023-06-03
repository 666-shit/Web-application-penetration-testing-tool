from faker import Faker
import faker
import mysql.connector


def main():
    # 连接MySQL数据库
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Cxq09071999",
        database="sedictionary"
    )

    # 生成虚假个人信息并插入到数据库
    fake = Faker()
    cursor = db.cursor()

    # 创建info表
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS info (id INT AUTO_INCREMENT PRIMARY KEY, first_name VARCHAR(255), last_name VARCHAR(255), birth_year INT, phone_number VARCHAR(255), hobby VARCHAR(255))")

    while True:
        print("[MENU] 请选择操作：")
        print("1. 生成虚假信息")
        print("2. 删除全部虚假信息")
        print("3. 删除全部密码表")
        print("4. 查看所有虚假信息")
        print("0. 返回上一级")
        choice = input("[INPUT] 请输入选项: ")

        if choice == "1":
            n = input("[INPUT] 输入虚假信息生成数量: ")
            for i in range(int(n)):
                first_name = fake.first_name()
                last_name = fake.last_name()
                birth_year = fake.date_of_birth().year
                phone_number = fake.phone_number()
                hobby = fake.word()
                sql = "INSERT INTO info (first_name, last_name, birth_year, phone_number, hobby) VALUES (%s, %s, %s, %s, %s)"
                val = (first_name, last_name, birth_year, phone_number, hobby)
                cursor.execute(sql, val)

            db.commit()
            print("[+] 虚假信息已生成并插入到数据库中。")

        elif choice == "2":
            cursor.execute("DELETE FROM info WHERE 1 = 1")
            db.commit()
            print("[+] 已删除全部虚假信息。")

        elif choice == "3":
            cursor.execute("DELETE FROM pwd WHERE 1 = 1")
            db.commit()
            print("[+] 已删除全部虚假信息。")

        elif choice == "4":
            cursor.execute("SELECT * FROM info")
            result = cursor.fetchall()
            for row in result:
                print(row)

        elif choice == "0":
            print("[END] 程序已退出。")
            break

        else:
            print("[-] 输入有误，请重新输入。")

    # 关闭数据库连接
    db.close()

# if __name__ == '__main__':
#     main()
