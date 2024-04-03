import sublist3r
import os

def find_all_domain(domain,domain_txt):
    subdomains = sublist3r.main(domain, 40, domain_txt, ports=None, silent=False, verbose=False,enable_bruteforce=False, engines=None)

if __name__ == "__main__":
    file_path=r"/home/wzy/PycharmProjects/pythonProject/NIM/collect"# 获取文件路径
    domain_path=r"/home/wzy/PycharmProjects/pythonProject/NIM/domain"# 获取域名文件存放位置
    fileR=file_path+r'/top-1000000-domains.txt'# 获取初始域名列表
    fileW = file_path + r'/subdomain.txt'# 生成扩展域名列表
    # 从初始域名列表读取域名，调用sublist3r搜集子域名，写入域名文件夹
    with open(fileR,'r') as domainfile:
        for line in domainfile:
            domain=line.strip()
            domain_txt=domain_path+rf"/{domain}.txt"
            find_all_domain(domain, domain_txt)
    # 读域名文件夹中文件，生成扩展域名列表
    domainfiles=os.listdir(domain_path)
    with open(fileW,'a')as subdomainfile:
        for filename in domainfiles:
            with open(domain_path+rf"/{filename}",'r')as domain_i:
                for line in domain_i:
                    domain=line.strip()
                    subdomainfile.write(domain+'\n')

