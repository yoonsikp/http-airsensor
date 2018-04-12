import time
import os
import g3
air = g3.g3sensor()
while True:
    try:
        pmdata = air.read("/dev/ttyS1")
    except:
        pmdata = [0,0,0,0,0,0]
        continue
    print(pmdata)
    time.sleep(1.0)
