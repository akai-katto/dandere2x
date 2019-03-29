import logging
import os

from Dandere2xUtils import get_lexicon_value
from Dandere2xUtils import wait_on_text
from Frame import DisplacementVector
from Frame import Frame


def merge(workspace, block_size, bleed, frame_inversion, frame_base, list_predictive, list_differences,
          output_location):
    logger = logging.getLogger(__name__)

    predictive_vectors = []
    difference_vectors = []
    out_image = Frame()
    out_image.create_new(frame_base.width, frame_base.height)

    if not list_predictive and not list_differences:
        logger.info("list_predictive and not list_differences: true")
        logger.info("Saving inversion image..")

        out_image.copy_image(frame_inversion)
        out_image.save_image(output_location)
        return

    if list_predictive and not list_differences:
        logger.info("list_predictive and not list_differences")
        logger.info("saving last image..")

        out_image.copy_image(frame_base)
        out_image.save_image(output_location)
        return

    # load list into vector displacements
    for x in range(int(len(list_differences) / 4)):
        difference_vectors.append(DisplacementVector(int(list_differences[x * 4]), int(list_differences[x * 4 + 1]),
                                                     int(list_differences[x * 4 + 2]),
                                                     int(list_differences[x * 4 + 3])))

    for x in range(int(len(list_predictive) / 4)):
        predictive_vectors.append(DisplacementVector(int(list_predictive[x * 4]), int(list_predictive[x * 4 + 1]),
                                                     int(list_predictive[x * 4 + 2]), int(list_predictive[x * 4 + 3])))

    # copy over predictive vectors into new image
    for vector in predictive_vectors:
        out_image.copy_block(frame_base, block_size * 2, vector.x_2 * 2, vector.y_2 * 2, vector.x_1 * 2, vector.y_1 * 2)

    # copy over inversion vectors (the difference images) into new image
    for vector in difference_vectors:
        out_image.copy_block(frame_inversion, block_size * 2, vector.x_2 * (block_size + bleed * 2) * 2 + 2,
                             vector.y_2 * (block_size + bleed * 2) * 2 + 2,
                             vector.x_1 * 2, vector.y_1 * 2)

    out_image.save_image(output_location)


def merge_loop(workspace, start_frame, count, block_size, file_type):
    logger = logging.getLogger(__name__)

    bleed = 1
    for x in range(start_frame, count):
        logger.info("Upscaling frame " + str(x))
        f1 = Frame()
        f1.load_from_string_wait(workspace + "upscaled/output_" + get_lexicon_value(6, x) + ".png")

        base = Frame()
        base.load_from_string_wait(workspace + "merged/merged_" + str(x) + file_type)

        difference_data = wait_on_text(workspace + "inversion_data/inversion_" + str(x) + ".txt")
        prediction_data = wait_on_text(workspace + "pframe_data/pframe_" + str(x) + ".txt")

        merge(workspace, block_size, bleed, f1, base, prediction_data, difference_data,
              workspace + "merged/merged_" + str(x + 1) + file_type)


# find the last photo to be merged, then start the loop from there
def merge_loop_resume(workspace, count, block_size, file_type):
    logger = logging.getLogger(__name__)
    last_found = count

    while last_found > 1:
        exists = os.path.isfile(workspace + os.path.sep + "merged" + os.path.sep + "merged_" + str(last_found) + ".jpg")
        logging.info(workspace + os.path.sep + "merged" + os.path.sep + "merged_" + str(last_found) + ".jpg")
        if not exists:
            last_found -= 1

        elif exists:
            break

    logger.info("resume info: last found: " + str(last_found))

    merge_loop(workspace, last_found, count, block_size, file_type)


def main():
    # merge_loop("/home/linux/Videos/testrun/testrun2/", 120)
    merge_loop_resume("C:\\Users\\windwoz\\Desktop\\workspace\\stealpython\\", 95, 16)
    print("hi")


if __name__ == "__main__":
    main()
