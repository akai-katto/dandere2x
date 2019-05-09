from dandere2x import Dandere2x
import time

start = time.time()

d = Dandere2x('config.ini')
d.run_concurrent()

end = time.time()
print("duration:" + str(end - start))

#d.difference_only()

#d.merge_only()