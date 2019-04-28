from wrappers.frame import Frame
from dandere2x_core.dandere2x_utils import determine_sens
import random
from scipy import misc  # pip install Pillow

frame1 = misc.imread("C:\\Users\\windwoz\\Pictures\\ynn\\compression\\frame1.jpg").astype(float)

frame2 = misc.imread("C:\\Users\\windwoz\\Pictures\\ynn\\compression\\frame1comp.jpg").astype(float)

out = frame1 - frame2


misc.imsave("C:\\Users\\windwoz\\Pictures\\ynn\\compression\\hmm2.png", out)