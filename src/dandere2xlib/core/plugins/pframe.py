from wrappers.frame.frame import DisplacementVector
from wrappers.frame.frame import Frame


def pframe_image(context,
                 out_image: Frame, frame_base: Frame, frame_inversion: Frame,
                 list_differences: list, list_predictive: list):
    # load context
    predictive_vectors = []
    difference_vectors = []
    scale_factor = int(context.scale_factor)
    block_size = context.block_size
    bleed = context.bleed

    # load list into vector displacements
    for x in range(int(len(list_differences) / 4)):
        difference_vectors.append(DisplacementVector(int(list_differences[x * 4 + 0]),
                                                     int(list_differences[x * 4 + 1]),
                                                     int(list_differences[x * 4 + 2]),
                                                     int(list_differences[x * 4 + 3])))

    for x in range(int(len(list_predictive) / 4)):
        if int(list_predictive[x * 4 + 0]) != int(list_predictive[x * 4 + 1]) and\
           int(list_predictive[x * 4 + 2]) != int(list_predictive[x * 4 + 3]):

                predictive_vectors.append(DisplacementVector(int(list_predictive[x * 4 + 0]),
                                                     int(list_predictive[x * 4 + 1]),
                                                     int(list_predictive[x * 4 + 2]),
                                                     int(list_predictive[x * 4 + 3])))

    # copy over predictive vectors into new image
    for vector in predictive_vectors:
        out_image.copy_block(frame_base, block_size * scale_factor,
                             vector.x_2 * scale_factor,
                             vector.y_2 * scale_factor,
                             vector.x_1 * scale_factor,
                             vector.y_1 * scale_factor)

    # copy over inversion vectors (the difference images) into new image
    for vector in difference_vectors:
        out_image.copy_block(frame_inversion, block_size * scale_factor,
                             (vector.x_2 * (block_size + bleed * 2)) * scale_factor + (bleed * scale_factor),
                             (vector.y_2 * (block_size + bleed * 2)) * scale_factor + (bleed * scale_factor),
                             vector.x_1 * scale_factor,
                             vector.y_1 * scale_factor)

    return out_image
