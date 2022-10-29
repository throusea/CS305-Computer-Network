import dns.resolver

data = dns.resolver.resolve('www.baidu.com', 'A')

for i in data.response.answer:
    for j in i.items:
        print(j)