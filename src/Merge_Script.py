from Frame import copy_from
from Frame import Frame
from Frame import DisplacementVector
from datetime import timedelta
from timeit import default_timer as timer
from Dandere2xUtils import wait_on_text


def merge(block_size, bleed, frame_inversion, frame_base, list_predictive, list_differences, output_location):
    predictive_vectors = []
    diference_vectors = []
    out_image = Frame()
    out_image.create_new(3840,2160)

    if not list_predictive and not list_differences:
        frame_inversion.save_image(output_location)
        return

    if not list_predictive and list_differences:
        frame_base.save_image(output_location)
        return

    start = timer()
    # load list into vector displacements
    for x in range(int(len(list_differences)/4)):
        diference_vectors.append(DisplacementVector(int(list_differences[x * 4]), int(list_differences[x * 4 + 1]),
                                                    int(list_differences[x * 4 + 2]), int(list_differences[x * 4 + 3])))

    for x in range(int(len(list_predictive)/7)):
        predictive_vectors.append(DisplacementVector(int(list_predictive[x * 7]), int(list_predictive[x *7 + 1]),
                                                     int(list_predictive[x * 7 + 2]), int(list_predictive[x * 7 + 3])))


    # copy over predictive vectors into new image
    for vector in predictive_vectors:
        out_image.copy_block(frame_base, block_size * 2, vector.x_2 * 2, vector.y_2 * 2, vector.x_1 * 2, vector.y_1 * 2)

    # copy over inversion vectors (the difference images) into new image
    for vector in diference_vectors:
        out_image.copy_block(frame_inversion, block_size * 2, vector.x_2 * (block_size + bleed * 2) * 2 + 2, vector.y_2 * (block_size + bleed * 2) * 2 + 2,
                             vector.x_1 * 2, vector.y_1 * 2)

    out_image.save_image(output_location)
    end = timer()

    print(timedelta(seconds=end - start))



def loop():
    block_size = 30
    bleed = 1
    for x in range(1,90):

        f1 = Frame()
        f1.load_from_string("/home/linux/Videos/Your_Name/dn/newrun_old/upscaled/output_" + str(x) + ".png")

        base = Frame()
        base.load_from_string("/home/linux/Videos/Your_Name/dn/newrun_old/merged/merged_" + str(x) + ".jpg")


        difference_data = wait_on_text("/home/linux/Videos/Your_Name/dn/newrun_old/inversion_data/inversion_" +  str(x) +  ".txt")
        prediction_data = wait_on_text("/home/linux/Videos/Your_Name/dn/newrun_old/pframe_data/pframe_" + str(x) + ".txt")

        print(difference_data)
        print(x)
        merge(block_size, bleed, f1, base, prediction_data, difference_data,
              "/home/linux/Videos/Your_Name/dn/newrun_old/merged/merged_" + str(x+1) + ".jpg")

def main():
    loop()
    print("hi")



if __name__== "__main__":
  main()
