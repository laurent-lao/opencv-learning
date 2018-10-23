# Author: Laurent Lao
# For: UAV Concordia Sprint Demo on Oct 19 2018
# Date created: Oct 18, 2018
# Purpose: Test different image thresholding as per tutorial on
# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_thresholding/py_thresholding.html#thresholding
# The program:
# Needs a file and a choice (1 or 2) argument, then either shows simple image thresholding or adaptive

import cv2
import numpy as np
import argparse
from matplotlib import pyplot as plt


def main(input_file, simple_or_adaptive):

    # checking arguments to see which threshold to perform and pass the filename
    is_continue = 0
    while is_continue != 9:
        is_continue = display_menu(simple_or_adaptive)
        if is_continue != 9:
            if simple_or_adaptive == 1:
                simple(input_file)
            elif simple_or_adaptive == 2:
                adaptive(input_file)
            else:
                print("Unexpected Error")
    print("End of program")
    exit(0)


def simple(input_file):  # simple uses a global value for Binary, Binary_inv, Trunc, To Zero and To Zero_inv

    # reading the image and threshold via Global values
    # threshold in several ways as to show the differences
    img = cv2.imread(input_file, 0)
    ret,thresh1 = cv2.threshold(img, threshold_number, threshold_max, cv2.THRESH_BINARY)
    ret,thresh2 = cv2.threshold(img, threshold_number, threshold_max, cv2.THRESH_BINARY_INV)
    ret,thresh3 = cv2.threshold(img, threshold_number, threshold_max, cv2.THRESH_TRUNC)
    ret,thresh4 = cv2.threshold(img, threshold_number, threshold_max, cv2.THRESH_TOZERO)
    ret,thresh5 = cv2.threshold(img, threshold_number, threshold_max, cv2.THRESH_TOZERO_INV)

    # creating array for matplotlib
    titles = ["Original Image", "BINARY", "BINARY_INV", "TRUNC", "TOZERO", "TOZERO_INV"]
    images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]

    # creating the matplotlib plot of images
    for i in range(6):
        plt.subplot(2, 3, i + 1), plt.imshow(images[i], "gray")
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])

    plt.show()
    return


def adaptive(input_file):    # in adaptive threshold, image is partitioned and a mean value is used for threshold

    # reading the image and adding a blur
    img = cv2.imread(input_file, 0)
    img = cv2.medianBlur(img, 5)

    # doing both thresholds Mean and Gaussian
    th1 =  cv2.adaptiveThreshold(img, adaptive_thresh_max, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,
                                 adaptive_block_size, adaptive_constant)
    th2 = cv2.adaptiveThreshold(img, adaptive_thresh_max, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,
                                adaptive_block_size, adaptive_constant)

    # creating array for matplotlib
    titles = ["Original Image", "Adaptive Mean Thresholding", "Adaptive Gaussian Thresholding"]
    images = [img, th1, th2]

    # creating the matplotlib plot of images
    for i in range(3):
        plt.subplot(3, 1, i + 1), plt.imshow(images[i], "gray")
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])

    plt.show()
    return


def display_menu(simple_or_adaptive):     # menu for changing variables and such

    # defining string variables
    str_simple_global = "Global Threshold Value"
    str_simple_max = "Max Threshold Value"
    str_adaptive_block_size = "Block Size of Partitions"
    str_adaptive_constant = "Constant substracted from Mean"
    str_adaptive_max = "Max Threshold Value"

    # passing globals
    global threshold_number, threshold_max, adaptive_block_size, adaptive_constant, adaptive_thresh_max

    # check if simple or adaptive
    if simple_or_adaptive == 1:
        str_type = "Simple Thresholding"
    else:
        str_type = "Adaptive Thresholding"

    # menu options
    is_done = -1
    while is_done != 0:
        print("\nMenu options for " + str_type + "\n")
        print("0:\tConfirm value and render")
        print("1:\tReset to default values")
        # menu for simple thresholding
        if simple_or_adaptive == 1:
            print("2:\tThe value for " + "\"" + str_simple_global + "\"" + ": \t" + str(threshold_number) +
                  "\t default: " + str(default_simple[0]))
            print("3:\tThe value for " + "\"" + str_simple_max + "\"" + ": \t\t" + str(threshold_max) +
                  "\t default: " + str(default_simple[1]))
        if simple_or_adaptive == 2:
            print("2:\tThe value for " + "\"" + str_adaptive_block_size + "\"" + ": \t" + str(adaptive_block_size) +
                  "\t default: " + str(default_adaptive[1]))
            print("3:\tThe value for " + "\"" + str_adaptive_constant + "\"" + ": \t" + str(adaptive_constant) +
                  "\t default: " + str(default_adaptive[2]))
            print("4:\tThe value for " + "\"" + str_adaptive_max + "\"" + ": \t" + str(adaptive_thresh_max) +
                  "\t default: " + str(default_adaptive[0]))
        print("9:\tEnd the Program")

        # prompting user for menu option
        print("\n")
        menu_choice = -1
        while((simple_or_adaptive == 1 and (menu_choice < 0 or (menu_choice > 3 and menu_choice != 9))) or
              (simple_or_adaptive == 2 and (menu_choice < 0 or (menu_choice > 4 and menu_choice != 9)))):
            str_menu_choice = input("Enter the menu option or the value you wish to change: ")
            menu_choice = int(str_menu_choice)

        # behaviour according to menu_choice
        if menu_choice == 0:
            return 0
        elif menu_choice == 9:
            return 9
        if simple_or_adaptive == 1:
            if menu_choice == 1:
                threshold_number = default_simple[0]
                threshold_max = default_simple[1]
            else:
                new_value = int(input("New value: "))
                if menu_choice == 2:
                    threshold_number = new_value
                elif menu_choice == 3:
                    threshold_max = new_value
        if simple_or_adaptive == 2:
            if menu_choice == 1:
                adaptive_thresh_max = default_adaptive[0]
                adaptive_block_size = default_adaptive[1]
                adaptive_constant = default_adaptive[2]
            else:
                new_value = int(input("New value: "))
                if menu_choice == 2:
                    adaptive_block_size = new_value
                elif menu_choice == 3:
                    adaptive_constant = new_value
                elif menu_choice == 4:
                    adaptive_thresh_max = new_value


# parsing the filename into the main function
parser = argparse.ArgumentParser(description="Image Threshold")
parser.add_argument("filename", help="Name of the image in jpg")
parser.add_argument("simpleOrAdaptive", type=int, choices=[1, 2], help="Enter 1 for Simple, 2 for Adaptive")
args = parser.parse_args()

# define global variables
default_simple = [127, 255]
default_adaptive = [255, 11, 2]
# defining simple thresholding
threshold_number = default_simple[0]            # number        : threshold of pixel classification
threshold_max = default_simple[1]               # max           : pixel is assigned max if over threshold
# defining adaptive thresholding variables
adaptive_thresh_max = default_adaptive[0]       # max           : pixel value is assigned max if over mean
adaptive_block_size = default_adaptive[1]       # block size    : decides the size of the partition
adaptive_constant = default_adaptive[2]         # C             : constant which is subtracted from the mean values

# adding into main
main(args.filename, args.simpleOrAdaptive)

# TODO
# * fix error message
