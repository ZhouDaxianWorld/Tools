# -*- coding:UTF-8 -*-

import gevent.monkey
gevent.monkey.patch_all()
import warnings
warnings.simplefilter("ignore", category=UserWarning)
from prettyprinter import cpprint

import optparse
import xlwt
import xlrd
import nmap

"""
端口扫描选项：
-sS SYN扫描不易被发现，不完成TCP连接，速度快，没有入侵防火墙的情境。 
-sT 当-sS不能用是使用，易发现，系统会产生syslog日志，-sS和-sT都会被IDS发现。
-sU 不可忽视的端口扫描选项，可以与-sS搭配使用，速度慢。
-sA 
其它端口扫描选项：当目标系统有防火墙的情况下使用，如何出现防火墙，可针对性地使用命令行进行扫描，不需要使用该脚本。 
"""

class Scan(object):

    nmap = nmap.PortScanner()

    def run(self, ip, arguments):
        try:
            scan_result = self.nmap.scan(hosts=ip, ports="0-65535", arguments=arguments, sudo=True)
            scan_result = scan_result["scan"][ip]
            os_info = "系统：" + str(scan_result["osmatch"][0]["name"]) + " 准确性：" + str(scan_result["osmatch"][0]["accuracy"]) + "\r\n"
            status_info = "状态：" + str(scan_result["status"]["state"]) + "\r\n"
            tcp_info = ""
            for key, value in scan_result["tcp"].items():
                tcp_info += "端口：" + str(key) + " 状态：" + str(value["state"]) + " " + \
                            "服务：" + str(value["name"]) + " " + str(value["version"]) + "\r\n"
            result = os_info + status_info + tcp_info
            print(result)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    ip = "192.168.156.3"
    arguments = "-sS -O -P0 -sV --version-all"


    scan = Scan()
    scan.run(ip, arguments)

