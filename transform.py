import argparse

import numpy
import numpy as np
from PIL import Image


def parse_args():
    parser = argparse.ArgumentParser(
        description='Simulate Color Blindness')
    parser.add_argument(
        '-input', type=str, help='Path to input image')
    parser.add_argument(
        '-output', type=str, help='Path for output image')
    transform_group = parser.add_mutually_exclusive_group(required=True)
    transform_group.add_argument('-sp', action='store_true', help='Simulate Protanopia (Common Red-Green  Blindness)')
    transform_group.add_argument('-sd', action='store_true', help='Simulate Deutranopia (Rare Red-Green Blindness)')
    transform_group.add_argument('-st', action='store_true', help='Simulate Tritanopia (Blue-Yellow Color Blindness)')
    args = parser.parse_args()
    return args


# Matrix Multiplication Block (Common for all operations, just varying matrix)
def get_image_array(transform_matrix, image_array):
    width, height, _ = image_array.shape
    for i in range(width):
        for j in range(height):
            curr_matrix = np.array((0, 0, 0), dtype=float)
            for k in range(3):
                curr_matrix[k] = image_array[i, j, k]
            lms_image = np.dot(transform_matrix, curr_matrix)
            for k in range(3):
                image_array[i, j, k] = lms_image[k]
    return image_array


# Converting RGB to LMS
# https://en.wikipedia.org/wiki/LMS_color_space
def convert_to_lms(input_image):
    image_array = np.array(np.asarray(input_image))  # np.asarray is readonly
    image_array = np.divide(image_array, 255.0)
    lms_convert = numpy.array(
        [[17.8824, 43.5161, 4.11935], [3.45565, 27.1554, 3.86714], [0.0299566, 0.184309, 1.46709]])
    return get_image_array(lms_convert, image_array)


# Simulating Protanopia
def convert_to_protanopes(image):
    protanope_convert = numpy.array([[0, 2.02344, -2.52581], [0, 1, 0], [0, 0, 1]])
    return get_image_array(protanope_convert, image)


# Simulating Deutranopia
def convert_to_deuteranopes(image):
    deuteranopes_convert = numpy.array([[1, 0, 0], [0.494207, 0, 1.24827], [0, 0, 1]])
    return get_image_array(deuteranopes_convert, image)


# Simulating Tritanopia
def convert_to_tritanope(image):
    tritanope_convert = numpy.array([[1, 0, 0], [0, 1, 0], [-0.395913, 0.801109, 0]])
    return get_image_array(tritanope_convert, image)


# Converting LMS to RGB
def convert_to_rgb(image_array):
    rgb2lms = numpy.array([[17.8824, 43.5161, 4.11935], [3.45565, 27.1554, 3.86714], [0.0299566, 0.184309, 1.46709]])
    rgb_convert = numpy.linalg.inv(rgb2lms)
    image_array_rgb = get_image_array(rgb_convert, image_array)
    image_array_rgb = np.multiply(image_array_rgb, 255)
    return image_array_rgb


# Converting Processed Array to Image
def array_to_image(image_array, out_file_name):
    rgb_array = np.array(image_array, dtype='uint8')
    img = Image.fromarray(rgb_array)
    img.save(out_file_name)


def main():
    args = parse_args()
    input_image = Image.open(args.input)
    lms_array = convert_to_lms(input_image)
    if args.sp:
        lms_array_transformed = convert_to_protanopes(lms_array)
    elif args.sd:
        lms_array_transformed = convert_to_deuteranopes(lms_array)
    else:  # args.st
        lms_array_transformed = convert_to_tritanope(lms_array)
    rgb_array_transformed = convert_to_rgb(lms_array_transformed)
    array_to_image(rgb_array_transformed, args.output)


if __name__ == '__main__':
    main()
