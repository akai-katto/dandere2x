from wrappers.frame import Frame
from dandere2x_core.dandere2x_utils import determine_sens
import random

list = []
for x in range(1, 10):
    num = random.randint(1, 240)
    print(num)

    f1 = Frame()
    f1.load_from_string("C:\\Users\\windwoz\\Desktop\\workspace\\correctiontest_4\\inputs\\frame" + str(num) + ".jpg")
    workspace = "C:\\Users\\windwoz\\Desktop\\workspace\\correctiontest_4\\"
    list.append(determine_sens(workspace,f1,50,60))

output = [sum(y) / len(y) for y in zip(*list)]

print(output)
print(list)