'''
网络安全工具中有一个常用软件称作端口扫描器，即通过一台主机发起向另一主机的常用端口发起连接，
探测目标主机是否开放了指定端口（1-1024），用于改善目标主机的安全状况。
1.使用扫描器可以基于 ping 命令快速检测一个 IP 段是否可以 ping 通，如果可以 ping 通返回主机 IP，如果无法 ping 通忽略连接。
2.使用扫描器可以快速检测一个指定 IP 地址开放了哪些 tcp 端口，并在终端显示该主机全部开放的端口。
3.IP 地址、使用 ping 或者使用 tcp 检测功能、以及并发数量，由命令行参数传入。
4.需考虑网络异常、超时等问题，增加必要的异常处理。
5.因网络情况复杂，避免造成网络拥堵，需支持用户指定并发数量。
pmap.py -n 4 -f ping -ip 192.168.0.1-192.168.0.100
pmap.py -n 10 -f tcp -ip 192.168.0.1 -w result.json

-n：指定并发数量。
-f ping：进行 ping 测试
-f tcp：进行 tcp 端口开放、关闭测试。
-ip：连续 IP 地址支持 192.168.0.1-192.168.0.100 写法。
-w：扫描结果进行保存。

(optional)
通过参数 [-m proc|thread] 指定扫描器使用多进程或多线程模型。
增加 -v 参数打印扫描器运行耗时 (用于优化代码)。
扫描结果显示在终端，并使用 json 格式保存至文件。
'''
import socket
import argparse
import os
import re
import ipaddress
import time

from enum import Enum
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from abc import ABCMeta


def check_ip(ipaddresses):
    ''' a helper method to validate the user passed in ips '''
    ip_regEX = re.compile(r"^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(\-\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})?$")
    match = ip_regEX.match(ipaddresses)
    if match and match.group(0) == ipaddresses:
        return ipaddresses
    raise argparse.ArgumentTypeError("%s is an invalid ipaddress/ipaddress range" % ipaddresses)


parser = argparse.ArgumentParser(description='scan the network connection of the target ipaddress')
parser.add_argument('-n', '--number', type=int, metavar='', required=True,
                    help='number of concurrent running threads/processes')
parser.add_argument('-f', '--function', type=str, metavar='', required=True, choices=['ping', 'tcp'],
                    help='put argument as ping or tcp')
parser.add_argument('-ip', '--ipaddress', type=check_ip, metavar='', required=True,
                    help='accept ipaddress or ipaddress range, TCP should be single ipaddress')
parser.add_argument('-w', '--writeto', type=str, metavar='', help='output to the specified file')
parser.add_argument('-m', '--mode', type=str, metavar='', choices=['proc', 'thread'], default='thread',
                    help='proc|thread multi process or multi threading')
parser.add_argument('-v', '--verbose', action='store_true', help='print the time consumed by the scanner')

args = parser.parse_args()


class FunctionEnum(Enum):
    PING = 'ping'
    TCP = 'tcp'


class ModeEnum(Enum):
    PROC = 'proc'
    THREAD = 'thread'


class IPScannerBase(metaclass=ABCMeta):
    def __init__(self, ip_args, mode, worker_number):
        self.ip_args = ip_args.strip()  # original ip value user passes in
        self.mode = mode
        # not that useful to create worker thread/proc more than CPU count especially when multiprocessing
        self.worker_number = worker_number if worker_number < os.cpu_count() else os.cpu_count()
        self.output_list = []

    def do_work(self):
        raise NotImplementedError

    def output_results(self):
        # output to file, otherwise display in console
        if self.output_list:
            if args.writeto:
                with open(args.writeto, 'w') as handler:
                    for item in self.output_list:
                        handler.write(item + '\n')
            else:
                for ele in self.output_list:
                    print(ele)
        else:
            print('Nothing to output')

    @staticmethod
    def get_ip_list(start_ip, end_ip):
        ''' ping the whole ip range, Note that need to convert IPV4Address to int in order to loop through '''
        start_IP = ipaddress.IPv4Address(start_ip)
        end_IP = ipaddress.IPv4Address(end_ip)

        # turn ipaddress into int for getting the range then map back to get the full ip address list
        return list(map(lambda ip: str(ipaddress.IPv4Address(ip)), range(int(start_IP), int(end_IP) + 1)))


class IPScannerPing(IPScannerBase):
    ''' Simply check ipaddresses connectivity '''

    def __init__(self, ip_args, mode, worker_number):
        super().__init__(ip_args, mode, worker_number)

    def ping_IP(self, ipaddress):
        try:
            # Note that gethostbyaddr returns hostname, aliaslist, ipaddrlist
            return socket.gethostbyaddr(ipaddress)[2]
        except socket.gaierror:
            print('network error')
            pass
        except Exception:
            pass

    def do_work(self):
        if '-' not in self.ip_args:
            ''' ping one single ipaddress or ipaddress range '''
            self.output_list = self.ping_IP(self.ip_args)
        else:
            # turn ipaddress into int for getting the range then map back to get the full ip address list
            full_ip_list = IPScannerBase.get_ip_list(self.ip_args.split('-')[0], self.ip_args.split('-')[1])

            try:
                if self.mode == ModeEnum.THREAD:
                    # Multi thread mode
                    with ThreadPoolExecutor(self.worker_number) as thread_executor:
                        ipaddresses = thread_executor.map(self.ping_IP, full_ip_list)
                    self.output_list = list(ipaddresses)
                else:
                    # Multi proc mode
                    with ProcessPoolExecutor(self.worker_number) as proc_executor:
                        ipaddresses = proc_executor.map(self.ping_IP, full_ip_list)
                    self.output_list = list(ipaddresses)
            except TimeoutError:
                print('Timeout')
        self.output_results()


class IPScannerTCP(IPScannerBase):
    ''' Check opening port number in target ipaddresses '''

    def __init__(self, ip_args, mode, worker_number):
        super().__init__(ip_args, mode, worker_number)

    def scan_port(self, ip_port):
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip = ip_port[0]
        port = ip_port[1]
        location = (ip, port)
        result_of_check = a_socket.connect_ex(location)

        if result_of_check == 0:
            return ip_port
        else:
            return

    def do_work(self):
        if '-' not in self.ip_args:
            ips_ports = [(self.ip_args, port) for port in range(70, 81)]
        else:
            # turn ipaddress into int for getting the range then map back to get the full ip address list
            full_ip_list = IPScannerBase.get_ip_list(self.ip_args.split('-')[0], self.ip_args.split('-')[1])
            ips_ports = [(ip, port) for ip in full_ip_list for port in range(70, 81)]

        try:
            if self.mode == ModeEnum.THREAD:
                # Multi thread mode
                with ThreadPoolExecutor(self.worker_number) as thread_executor:
                    self.output_list = [f'{item[0]} has port number {item[1]} open' for item in
                                        thread_executor.map(self.scan_port, ips_ports) if item]
            else:
                # Multi proc mode
                with ProcessPoolExecutor(self.worker_number) as proc_executor:
                    self.output_list = [f'{item[0]} has port number {item[1]} open' for item in
                                        proc_executor.map(self.scan_port, ips_ports) if item]
        except TimeoutError:
            print('Timeout')
        self.output_results()


if __name__ == '__main__':
    try:
        ip_args = args.ipaddress
        mode = ModeEnum(args.mode) if args.mode else ModeEnum.THREAD
        worker_number = args.number

        start = time.perf_counter()
        if args.function == FunctionEnum.PING.value:
            pinger = IPScannerPing(ip_args, mode, worker_number)
            pinger.do_work()
        elif args.function == FunctionEnum.TCP.value:
            scanner = IPScannerTCP(ip_args, mode, worker_number)
            scanner.do_work()
        end = time.perf_counter()

        if args.verbose:
            print(f'time used: {str(end - start)} seconds')
    except argparse.ArgumentTypeError as e:
        print(e)
    except Exception as e:
        print(e)
