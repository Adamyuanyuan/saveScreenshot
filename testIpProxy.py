import ipProxy

ip = ipProxy.getIpFromRegion("beijing")

print(ip)
print("ip: " + ip)

ipProxy.setProxy(ip)
ipProxy.disableProxy()
ipProxy.refresh()