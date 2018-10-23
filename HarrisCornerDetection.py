# Author: Laurent Lao
# For: UAV Concordia Sprint Demo on Oct 19 2018
# Date created: Oct 18, 2018
# Purpose: Test Harris Corner Detection as per tutorial on
# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_features_harris/py_features_harris.html#harris-corners
# The program:
# Needs a file argument and will locate some corners on the provided images

import cv2
import numpy as np
import argparse
import sys


def main(input_file):

    is_continue = 0
    while is_continue != 9:

        # displays menu
        is_continue = display_menu()

        if is_continue != 9:

            # input file
            file_to_process = input_file

            # converts file into greyscale then into a float32
            img = cv2.imread(file_to_process)
            greyscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            greyscale = np.float32(greyscale)

            # dst creates an array containing the transformed greyscale'd and corners
            dst = cv2.cornerHarris(greyscale, corner_harris_block_size, corner_harris_k_size, corner_harris_k)

            # result of dst is dilated for marking the corners, not important
            # as per OpenCV2 tutorial
            dst = cv2.dilate(dst, None)

            # Threshold the greyscale'd img according to the array given by dst and an optimal value
            # Mark higher than threshold stuff blue?
            img[dst > dst_percentage*dst.max()] = dst_colour

            # Show the result img
            print("Press Escape to close windows")
            cv2.imshow('dst', img)
            if cv2.waitKey(0) & 0xff == 27:
                cv2.destroyAllWindows()

        else:
            print("End of Program")
            exit(0)


def display_menu(): # displays a menu for changing variables

    # initializing variables
    global corner_harris_block_size, corner_harris_k_size, corner_harris_k, dst_percentage, dst_colour, colour_label
    str_block_size = "Block Size value"
    str_k_size = "Aperture Parameter value"
    str_k = "Free Parameter value"
    str_dst = "Sensitivity of Corner"
    str_colour = "Colour of corner detection"

    while True:
        # displaying menu options
        print("\nMenu options for Harris Corner Detection")
        print("0:\tConfirm values and Render")
        print("1:\tReset to default values")
        print("2:\t" + str_block_size + ": \t\t\t" + str(corner_harris_block_size) + "\t\tdefault is: 2")
        print("3:\t" + str_k_size + ": \t" + str(corner_harris_k_size) + "\t\tdefault is: 3")
        print("4:\t" + str_k + ": \t\t" + str(corner_harris_k) + "\tdefault is: 0.04")
        print("5:\t" + str_dst + ": \t\t" + str(dst_percentage) + "\tdefault is: 0.01")
        print("6:\t" + str_colour + ": " + colour_label + "\t\tdefault is: red")
        print("9:\tEnd the Program\n")

        # prompting and changing as per menu behaviour
        menu_option = -1
        while menu_option < 0 or (menu_option > 6 and menu_option != 9):
            menu_option = int(input("Enter a menu option or the value to be changed: "))
        if menu_option == 0:
            return 0
        elif menu_option == 1:
            set_default_value()
        elif menu_option == 9:
            return 9
        elif menu_option == 6:
            switch_colours()
        else:
            new_value = input("Enter new value: ")
            if menu_option == 2:
                corner_harris_block_size = int(new_value)
            elif menu_option == 3:
                corner_harris_k_size = int(new_value)
            elif menu_option == 4:
                corner_harris_k = float(new_value)
            elif menu_option == 5:
                dst_percentage = float(new_value)
            else:
                exit(1)


def set_default_value():

    # resetting into default values
    global corner_harris_block_size, corner_harris_k_size, corner_harris_k, dst_percentage, dst_colour, colour_label
    corner_harris_block_size = default_value[0]     # blockSize : size of neighbourhood for C.Detect (default = 2)
    corner_harris_k_size = default_value[1]         # k size    : Aperture parameter for Sobel derivative (default = 3)
    corner_harris_k = default_value[2]              # k         : Harris detector free parameter (default = 0.04)
    dst_percentage = default_value[3]               # threshold : Percentage for the sensitivity of corner (default = 0.01)
    dst_colour = colour_red
    colour_label = "red"


def switch_colours():
    #declare variable
    global  dst_colour, colour_red, colour_blue, colour_green, colour_label

    # show menu
    print("Switch the colour to:")
    print("1:\tRed")
    print("2:\tBlue")
    print("3:\tGreen")

    # prompt user and behaviour
    menu_input = 0
    while menu_input < 1 or menu_input > 3:
        menu_input = int(input("Enter your choice: "))
    if menu_input == 1:
        dst_colour = colour_red
        colour_label = "red"
    elif menu_input == 2:
        dst_colour = colour_blue
        colour_label = "blue"
    elif menu_input == 3:
        dst_colour = colour_green
        colour_label = "green"
    else:
        exit(2)


# parsing the filename into the main function
parser = argparse.ArgumentParser(description="Corner detection of image using Harris Corner Detection")
parser.add_argument("filename", help="Name of the image in jpg")
args = parser.parse_args()

# define variables
default_value = [2, 3, 0.04, 0.01]
colour_red = [0, 0, 255]
colour_green = [0, 255, 0]
colour_blue = [255, 0, 0]

corner_harris_block_size = default_value[0]  # blockSize : size of neighbourhood for C.Detect (default = 2)
corner_harris_k_size = default_value[1]      # k size    : Aperture parameter for Sobel derivative (default = 3)
corner_harris_k = default_value[2]           # k         : Harris detector free parameter (default = 0.04)
dst_percentage = default_value[3]            # threshold : Percentage for the sensitivity of corner (default = 0.01)
dst_colour = colour_red                      # colour    : Colour for corner marking (default = [0,0,255] (RED)
colour_label = "red"

# running main
main(args.filename)

# TODO
# * Fix error messages
