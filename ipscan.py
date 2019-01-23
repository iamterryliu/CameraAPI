import subprocess

ping = int(35)
address = "172.19.100." + str(ping)
res = subprocess.call(['ping', '-c', '1', address])
print("res:" + str(res))
if res == 0:
    print ("PASS")
else:
    print ("FAIL")
