import csv
import socket
import threading
from tqdm import tqdm

# 定义要保存扫描结果的CSV文件名
output_file = 'Port_scanning/扫描结果/scanresult.csv'

# 定义锁，用于在写入CSV文件时控制对文件的并发访问
lock = threading.Lock()

# 进度条
global_bar = None


# 定义函数，用于扫描TCP端口是否开放
def tcp_scan(ip_address, port):
    # 创建套接字对象类型为SOCK_STREAM
    # AF_INET表示使用IPv4网络通讯协议，SOCK_STREAM代表所创建的 socket 的类型为面向连接的 TCP 套接字，SOCK_DGRAM面向UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置套接字超时时间，发送或接收数据时等待响应的最长时间
    sock.settimeout(0.5)
    try:
        # 尝试连接指定IP地址和端口
        result = sock.connect_ex((ip_address, port))
        if result == 0:
            # 获取锁，防止并发写入文件出错
            with lock:
                # 将扫描结果写入CSV文件
                with open(output_file, 'a', newline='') as f:
                    writer = csv.writer(f)
                    service_name = socket.getservbyport(port)
                    writer.writerow([ip_address, port, 'TCP', 'Open', service_name])
        else:
            pass
            # 获取锁，防止并发写入文件出错
            with lock:
                # 将扫描结果写入CSV文件
                with open(output_file, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([ip_address, port, 'TCP', 'Closed', ''])
    except socket.error:
        pass
    finally:
        # 关闭套接字连接
        sock.close()
        # 更新全局进度条
        global_bar.update(1)


# 定义函数，用于扫描UDP端口是否开放
def udp_scan(ip_address, port):
    # 创建套接字对象
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 设置套接字超时时间
    sock.settimeout(0.5)
    try:
        # 尝试连接指定IP地址和端口, data是要发送的数据, 类型为bytes, sendto()是UDP协议中用于发送数据的方法
        data = b"Hello"
        sock.sendto(data, (ip_address, port))
        result = sock.recvfrom(1024)
        if result == 0:
            with lock:
                with open(output_file, 'a', newline='') as g:
                    writer = csv.writer(g)
                    service_name = socket.getservbyport(port)
                    writer.writerow([ip_address, port, 'UDP', 'Open', service_name])
        else:
            pass
            with lock:
                with open(output_file, 'a', newline='') as g:
                    writer = csv.writer(g)
                    writer.writerow([ip_address, port, 'UDP', 'Closed', ''])
    except socket.error:
        pass
    finally:
        sock.close()
        global_bar.update(1)


# 定义函数，用于扫描SYN端口是否开放
# def syn_scan(ip_address, port):
#     sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
#     sock.settimeout(0.5)
#     try:
#         # 尝试向指定IP地址和端口发送SYN数据包
#         sock.connect_ex((ip_address, port)
#         with lock:
#             with open(output_file, 'a', newline='') as f:
#                 writer = csv.writer(f)
#                 writer.writerow([ip_address, port, 'SYN', 'Open'])
#     except socket.error:
#         pass
#     finally:
#         sock.close()
#         global_bar.update(1)


# 定义函数，用于创建多个线程进行端口扫描
def run_threads(ip_address, port_range, scan_mode):
    global global_bar
    threads = []
    # 创建多个线程，每个线程负责扫描指定的端口
    for port in port_range:
        if scan_mode == 'TCP':
            thread = threading.Thread(target=tcp_scan, args=(ip_address, port))
        elif scan_mode == 'UDP':
            thread = threading.Thread(target=udp_scan, args=(ip_address, port))
        # elif scan_mode == 'SYN':
        #     thread = threading.Thread(target=syn_scan, args=(ip_address, port))
        threads.append(thread)
    # 启动线程
    for thread in threads:
        thread.start()
    # 等待所有线程完成扫描
    for thread in threads:
        thread.join()


# if __name__ == '__main__':
def main():
    global global_bar
    # 获取用户输入的IP地址和端口号
    ip_address = input("[INPUT] 输入扫描ip地址: ")
    port_str = input("[INPUT] 输入想要扫描的端口号 (如 80 or 0-65535): ")
    # 解析用户输入的端口号范围
    if '-' in port_str:
        start_port, end_port = port_str.split('-')
        port_range = range(int(start_port), int(end_port) + 1)
    else:
        port_range = [int(port_str)]
    # 显示菜单，让用户选择扫描模式
    print("[MENU] 选择扫描模式:")
    print("1. TCP scan")
    print("2. UDP scan")
    # print("3. SYN scan")
    # 获取用户选择的扫描模式
    scan_mode = input("[INPUT] ")
    # 根据用户选择的扫描模式，调用不同的函数进行端口扫描
    if scan_mode == '1':
        global_bar = tqdm(total=len(port_range), desc='TCP scan')
        run_threads(ip_address, port_range, 'TCP')
    elif scan_mode == '2':
        global_bar = tqdm(total=len(port_range), desc='UDP scan')
        run_threads(ip_address, port_range, 'UDP')
    # elif scan_mode == '3':
    #     global_bar = tqdm(total=len(port_range), desc='SYN scan')
    #     run_threads(ip_address, port_range, 'SYN')
    else:
        print("[-] 选择无效")
        # 关闭全局进度条
    global_bar.close()
    print("[END] 扫描结束")

# if __name__ == '__main__':
#     main()
