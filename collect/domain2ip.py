import subprocess
from multiprocessing import Pool
from datetime import datetime
import re
import json


def setcallback(relist):
    if len(relist) > 1:
        domain = relist[0]
        date = datetime.now().strftime("%Y%m%d-%H%M%S")  # 获取当前查询时间
        dns_server = relist[1]
        country = "China"
        # country = "America"
        with open(fileW, 'a') as ipfile:
            data = {"domain": domain, "date": [{"querytime": date, "dns_server": dns_server, "country": country, "IPv4_addresses": relist[2], "IPv6_addresses": relist[3]}]}
            json.dump(data, ipfile)
            ipfile.write('\n')

def nslookup(argu_ns):
    # 调用系统命令nslookup，向指定DNS服务器查询指定域名
    result = subprocess.run(['dig', argu_ns[1],argu_ns[0]], capture_output=True, text=True)
    # 解析命令输出结果
    if result.returncode == 0:
        # 如果命令执行成功，提取DNS解析结果
        # ipv4和ipv6地址表达式
        ipv4_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
        ipv6_pattern = r'(?:[0-9a-fA-F]{1,4}:){6}(?:(?:[0-9a-fA-F]{1,4}:)?[0-9a-fA-F]{1,4}|:(?::[0-9a-fA-F]{1,4}){1,2}|:)|' \
               r'(?:[0-9a-fA-F]{1,4}:){5}(?:(?:[0-9a-fA-F]{1,4}:){0,2}[0-9a-fA-F]{1,4}|(?::[0-9a-fA-F]{1,4}){1,3}|:)|' \
               r'(?:[0-9a-fA-F]{1,4}:){4}(?:(?:[0-9a-fA-F]{1,4}:){0,3}[0-9a-fA-F]{1,4}|(?::[0-9a-fA-F]{1,4}){1,4}|:)|' \
               r'(?:[0-9a-fA-F]{1,4}:){3}(?:(?:[0-9a-fA-F]{1,4}:){0,4}[0-9a-fA-F]{1,4}|(?::[0-9a-fA-F]{1,4}){1,5}|:)|' \
               r'(?:[0-9a-fA-F]{1,4}:){2}(?:(?:[0-9a-fA-F]{1,4}:){0,5}[0-9a-fA-F]{1,4}|(?::[0-9a-fA-F]{1,4}){1,6}|:)|' \
               r'(?:[0-9a-fA-F]{1,4}:){1}(?:(?:[0-9a-fA-F]{1,4}:){0,6}[0-9a-fA-F]{1,4}|(?::[0-9a-fA-F]{1,4}){1,7}|:)|' \
               r':(?:(?:[0-9a-fA-F]{1,4}:){0,7}[0-9a-fA-F]{1,4}|(?::[0-9a-fA-F]{1,4}){1,8})'
        # 编译正则表达式，不使用 VERBOSE 标志，由于ipv6地址更加复杂，所以需要这一步以更明确地规范正则表达式
        ipv6_regex = re.compile(ipv6_pattern)

        # 使用 findall() 函数查找文本中的全部 IPv6 地址
        ipv4_addresses = re.findall(ipv4_pattern, result.stdout)
        ipv6_addresses = ipv6_regex.findall(result.stdout)
        ipv4_addresses.pop(0)# 第一个ipv4地址是DNS服务器的地址
        relist = [argu_ns[1],argu_ns[0],ipv4_addresses,ipv6_addresses]
        return relist
    else:
        # 如果命令执行失败，打印错误信息
        relist = ['error']
        return relist

if __name__ == '__main__':
    # 打开域名列表、按行读取内容，将域名、DNS服务器地址传入多进程的参数进行查询、将查询结果传入异步函数、最终写入结果文件。
    file_path=r"/home/wzy/PycharmProjects/pythonProject/NIM/collect"# 获取文件路径
    fileR = file_path + r'/subdomain.txt'
    fileDNS=file_path+r'/DNSlistCH.txt'
    # fileDNS = file_path + r'/DNSlistUS.txt'
    fileW=file_path+rf'/domain2ip.json'
    p = Pool(8)
    with open(fileDNS,'r') as DNSfile:
        for DNSline in DNSfile:
            DNS_server=DNSline.strip('\n')
            with open (fileR,'r',) as domainfile:
                for line in domainfile:
                    domain=line.strip('\n')
                    argu_ns=[DNS_server,domain]
                    p.apply_async(func=nslookup, args=(argu_ns,), callback=setcallback)
    p.close()
    p.join()



