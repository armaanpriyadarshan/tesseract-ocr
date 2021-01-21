#!/usr/bin/env python
# coding: utf-8
"""
Optical Character Recognition with OpenCV and Tesseract
=====================================
"""

import cv2
import pytesseract
import argparse
from pytesseract import Output
import numpy as np
import re

parser = argparse.ArgumentParser()
parser.add_argument('--image', help='Path to your image', required=True)
parser.add_argument('--threshold', help='Minimum confidence threshold', default=60)

args = parser.parse_args()

image_path = args.image
min_conf_thresh = int(args.threshold)
image = cv2.imread(image_path)

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)   
# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)

    
scale_percent = (1000/image.shape[0])*100
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)

# resize image
image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
gray_image = get_grayscale(image)

d = pytesseract.image_to_data(gray_image, output_type=Output.DICT) 
#print(d)
date_pattern = '^(202[12])(-)(0[1-9]|1[012])(-)(0[1-9]|[12][0-9]|3[01])$'
id_pattern = '^([ABCDEFGHIJKLMNOPQRSTUVWXYZ]|[0-9])([ABCDEFGHIJKLMNOPQRSTUVWXYZ]|[0-9])([ABCDEFGHIJKLMNOPQRSTUVWXYZ]|[0-9])([ABCDEFGHIJKLMNOPQRSTUVWXYZ]|[0-9])([ABCDEFGHIJKLMNOPQRSTUVWXYZ]|[0-9])([ABCDEFGHIJKLMNOPQRSTUVWXYZ]|[0-9])([ABCDEFGHIJKLMNOPQRSTUVWXYZ]|[0-9])([ABCDEFGHIJKLMNOPQRSTUVWXYZ]|[0-9])([ABCDEFGHIJKLMNOPQRSTUVWXYZ]|[0-9])$'
n_boxes = len(d['text'])
for i in range(n_boxes):
    if int(d['conf'][i]) >= min_conf_thresh and re.match(date_pattern, d['text'][i]):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        print("The date of your test was " + d['text'][i])
    if int(d['conf'][i]) >= min_conf_thresh and re.match(id_pattern, d['text'][i]):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        print("Your test ID is " + d['text'][i])
    if int(d['conf'][i]) >= min_conf_thresh and d['text'][i] == 'cd' or d['text'][i] == 'c' or d['text'][i] == 'C4':
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        positive_width = (x + x + w)/2
        positive_height = (y + y + h)/2
        #print("Positive Test Result Coordinates: (" + str(positive_width) + ", " + str(positive_height) + ")")
        #print(image[int(positive_height), int(positive_width+50)])
        if 182 <= image [int(positive_height), int(positive_width+50)][0] <= 190 and 133 <= image[int(positive_height), int(positive_width+50)][1] <= 140 and 110 <= image[int(positive_height), int(positive_width+50)][2] <= 120:
            print("You have tested positive for COVID-19")
    if int(d['conf'][i]) >= min_conf_thresh and d['text'][i] == 'v4' or d['text'][i] == 'TH' or d['text'][i] == '4' or d['text'][i] == 'Td':
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        unsure_width = (x + x + w)/2
        unsure_height = (y + y + h)/2
        #print("Unsure Test Result Coordinates: (" + str(unsure_width) + ", " + str(unsure_height) + ")")
        #print(image[int(unsure_height), int(unsure_width+50)])
        if 182 <= image [int(unsure_height), int(unsure_width+50)][0] <= 190 and 133 <= image[int(unsure_height), int(unsure_width+50)][1] <= 140 and 110 <= image[int(unsure_height), int(unsure_width+50)][2] <= 120:
            print("Your test results didn't conclude anything")
    if int(d['conf'][i]) >= min_conf_thresh and d['text'][i] == 'nc4' or d['text'][i] == 'Nc4' or d['text'][i] == 'ncq' or d['text'][i] == 'Ncq' or d['text'][i] == 'NC4':
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        negative_width = (x + x + w)/2
        negative_height = (y + y + h)/2
        #print("Negative Test Result Coordinates: (" + str(negative_width) + ", " + str(negative_height) + ")")
        #print(image[int(negative_height), int(negative_width+50)])
        if 182 <= image [int(negative_height), int(negative_width+50)][0] <= 190 and 133 <= image[int(negative_height), int(negative_width+50)][1] <= 140 and 110 <= image[int(negative_height), int(negative_width+50)][2] <= 120:
            print("You have tested negative for COVID-19")
            

cv2.imshow('output', image)
cv2.waitKey(0)