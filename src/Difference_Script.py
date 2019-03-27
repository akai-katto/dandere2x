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
        out_image.create_new(raw_frame.width, raw_frame.height)
        out_image.copy_image(raw_frame)
        out_image.save_image(out_location)
        return

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


    out_image.save_image(out_location)


def difference_loop(workspace, count, block_size):
    start = timer()
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

if __name__ == "__main__":
    main()
