from time import time, sleep
import internetUp

starttime = time()
x = 0
while x <= 30:
    internetUp.checkInternet()
    sleep(60.0 - ((time() - starttime) % 60.0))
    x+=1