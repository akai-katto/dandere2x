from wrappers.frame import Frame

# f1 = Frame()
# f1.load_from_string("C:\\Users\\windwoz\\Desktop\\workspace\\violetfade\\100\\frame20.png")
#
# f2 = Frame()
# f2.load_from_string("C:\\Users\\windwoz\\Desktop\\workspace\\violetfade\\100\\frame21.png")
#


f1 = Frame()

f1.load_from_string("C:\\Users\\windwoz\\Desktop\\workspace\\violetfade\\inputs\\frame30.jpg")

f1.fade_block(0, 0, 100, -100)

f1.save_image("C:\\Users\\windwoz\\Desktop\\workspace\\violetfade\\lmfao.jpg")
