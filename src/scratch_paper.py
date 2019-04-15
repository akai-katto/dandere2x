from wrappers.frame import Frame
from wrappers.ffmpeg import gradfun_save


f1 = Frame()


f1.load_from_string("C:\\Users\\windwoz\\Desktop\\workspace\\debanding_testing\\merged\\merged_83.jpg")



gradfun_save('ffmpeg', f1, "C:\\Users\\windwoz\\Desktop\\workspace\\debanding_testing\\testout2.jpg" )