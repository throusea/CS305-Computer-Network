import dns.resolver

a = dns.resolver.resolve("www.baidu.com", 'a')
print(a)

for i in a.response.answer:
    for j in i.items:
        print(j)