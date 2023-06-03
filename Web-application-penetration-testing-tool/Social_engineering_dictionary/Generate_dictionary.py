import itertools
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Cxq09071999",
    database="sedictionary"
)

cursor = db.cursor()


def generate():
    # 创建密码表
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS pwd (id INT AUTO_INCREMENT PRIMARY KEY, first_name VARCHAR(255), last_name VARCHAR(255), pwd VARCHAR(255))")

    # 从info表检索个人信息
    cursor.execute("SELECT * FROM info")
    result = cursor.fetchall()

    # 从个人信息生成密码并插入到pwd表中
    for row in result:
        first_name = row[1]
        last_name = row[2]
        birth_year = row[3]
        phone_number = row[4]
        hobby = row[5]
        name_passwords = [first_name, last_name, first_name + last_name, last_name + first_name,
                          first_name + str(birth_year), last_name + str(birth_year)]
        phone_passwords = [phone_number, phone_number.replace("-", ""), phone_number.replace(" ", ""),
                           phone_number.replace("-", "").replace(" ", "")]
        hobby_passwords = [hobby, hobby.capitalize(), hobby.upper(), hobby.lower()]
        passwords = []
        for password_list in [name_passwords, phone_passwords, hobby_passwords]:
            for i in range(1, len(password_list) + 1):
                for combination in itertools.combinations(password_list, i):
                    passwords.append("".join(combination))
        for password in passwords:
            sql = "INSERT INTO pwd (first_name, last_name, pwd) VALUES (%s, %s, %s)"
            val = (first_name, last_name, password)
            cursor.execute(sql, val)

    db.commit()
    db.close()


def main():
    print("[+] 正在生成社工字典...")
    generate()
    print("[*] 社工字典生成结束\n[END]\n")

# if __name__ == '__main__':
#     main()
