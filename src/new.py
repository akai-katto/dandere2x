import time

from dandere2x import Dandere2x
import configparser

start = time.time()

# Load Config File
config = configparser.ConfigParser()
config.read('config.ini')

# Start Dandere2x with config file
d = Dandere2x(config)
d.run_concurrent()

end = time.time()

print("\n duration: " + str(time.time() - start))


