from time import sleep
import sys





for i in range(1000):
    sys.stdout.write('\r')
    # the exact output you're looking for:
    sys.stdout.write("Frame: [%s] %d%%    Average of Last 10 Frames: %s" % (i, 5*i, i*1.1))
    sys.stdout.flush()
    sleep(0.25)