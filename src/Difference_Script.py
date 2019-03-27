import math
from datetime import timedelta
from timeit import default_timer as timer

from Dandere2xUtils import wait_on_text
from Frame import DisplacementVector
from Frame import Frame


def generate_difference_image(raw_frame, block_size, bleed, list_difference, list_predictive, out_location):
    difference_vectors = []
    buffer = 5

    # first make a 'bleeded' version of input_frame
    # so we can preform numpy calculations w.o having to catch
    bleed_frame = raw_frame.create_bleeded_image(buffer)

    # if there are no items in 'differences' but have list_predictives
    # then the two frames are identical, so no differences image needed.
    if not list_difference and list_predictive:
        out_image = Frame()
        out_image.create_new(1, 1)
        out_image.save_image(out_location)
        return

    # if there are neither any predictive or inversions
    # then the frame is a brand new frame with no resemblence to previous frame.
    # in this case copy the entire frame over
    if not list_difference and not list_predictive:
        out_image = Frame()
        out_image.create_new(1920, 1080)
        out_image.copy_image(raw_frame)
        out_image.save_image(out_location)
        return

    debug = Frame()
    debug.create_new(1920, 1080)

    # turn the list of differences into a list of vectors
    for x in range(int(len(list_difference) / 4)):
        difference_vectors.append(DisplacementVector(int(list_difference[x * 4]), int(list_difference[x * 4 + 1]),
                                                     int(list_difference[x * 4 + 2]), int(list_difference[x * 4 + 3])))

    # size of image is determined based off how many differences there are
    image_size = int(math.sqrt(len(list_difference) / 4) + 2) * (block_size + bleed * 2)
    out_image = Frame()
    out_image.create_new(image_size, image_size)

    # move every block from the complete frame to the differences frame using vectors.
    for vector in difference_vectors:
        out_image.copy_block(bleed_frame, block_size + bleed * 2, vector.x_1 + buffer - bleed,
                             vector.y_1 + buffer + - bleed,
                             vector.x_2 * (block_size + bleed * 2), vector.y_2 * (block_size + bleed * 2))

    debug.save_image("/home/linux/Videos/testrun/testrun2/huh.jpg")

    out_image.save_image(out_location)


def difference_loop(workspace, count):
    start = timer()
    block_size = 30
    bleed = 1
    for x in range(1, count):
        f1 = Frame()
        f1.load_from_string_wait(workspace + "inputs/frame" + str(x + 1) + ".jpg")

        difference_data = wait_on_text(workspace + "inversion_data/inversion_" + str(x) + ".txt")
        prediction_data = wait_on_text(workspace + "pframe_data/pframe_" + str(x) + ".txt")

        generate_difference_image(f1, block_size, bleed, difference_data, prediction_data,
                                  workspace + "/outputs/output_" + str(x) + ".png")

    end = timer()
    print(timedelta(seconds=end - start))


def main():
    difference_loop("/home/linux/Videos/testrun/testrun2/", 95)
    #
    # f1 = Frame()
    # f1.load_from_string("/home/linux/Videos/newdebug/yn2/inputs/frame1.jpg")
    #
    # a = open("/home/linux/Videos/newdebug/yn2/inversion_data/inversion_1.txt", "r")
    #
    # inversion_data = a.read().split('\n')
    # a.close()
    #
    # b = open("/home/linux/Videos/newdebug/yn2/pframe_data/pframe_1.txt", "r")
    #
    # difference_data = b.read().split('\n')
    # b.close()
    #
    # block_size = 30
    # bleed = 1
    # generate_difference_image(f1, block_size, bleed, inversion_data, difference_data , "/home/linux/Videos/newdebug/yn2/huh8.png")
    #
    # print("hi")


if __name__ == "__main__":
    main()
