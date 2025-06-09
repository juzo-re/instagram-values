import subprocess
import time

password = "password"
timestamp = str(int(time.time()))

result = subprocess.check_output([
    "node", "c.js", "237", "91b03050a79fb0148debef99bcd76494707018c3005a90d1a4eab63e1f38bc20", password, timestamp
])

print(result.decode().strip())