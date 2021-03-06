"""
 Princeton University, COS 429, Fall 2020
"""
import os
from glob import glob
import numpy as np
import cv2
from hog36 import hog36


def get_testing_data(n, orientations, wrap180):
    """Reads in examples of faces and nonfaces, and builds a matrix of HoG
       descriptors, ready to pass in to logistic_predict

    Args:
        n: number of face and nonface testing examples (n of each)
        orientations: the number of HoG gradient orientations to use
        wrap180: if true, the HoG orientations cover 180 degrees, else 360

    Returns:
        descriptors: matrix of descriptors for all 2*n testing examples, where
                     each row contains the HoG descriptor for one face or nonface
        classes: vector indicating whether each example is a face (1) or nonface (0)
    """
    testing_faces_dir = 'a2_part2_starter/a2_part2_starter/face_data/testing_faces'
    testing_nonfaces_dir = 'a2_part2_starter/a2_part2_starter/face_data/testing_nonfaces'
    hog_descriptor_size = 100 * orientations

    # Get the names of the first n testing faces
    face_filenames = sorted(glob(os.path.join(testing_faces_dir, '*.jpg')))
    num_face_filenames = len(face_filenames)
    if num_face_filenames > n:
        face_filenames = face_filenames[:n]
    elif num_face_filenames < n:
        n = num_face_filenames

    # Initialize descriptors, classes
    descriptors = np.zeros([2 * n, hog_descriptor_size + 1])
    classes = np.zeros([2 * n])

    # Loop over faces
    for i in range(n):
        # Fill in here
        # Read the next face file
        face = cv2.imread(face_filenames[i], cv2.IMREAD_GRAYSCALE)

        # Compute HoG descriptor
        face_descriptor = hog36(face, orientations, wrap180)
        descriptors[i, 0] = 1
        descriptors[i, 1:] = face_descriptor
        classes[i] = 1

    # Loop over nonfaces
    nonface_filenames = sorted(glob(os.path.join(testing_nonfaces_dir, '*.jpg')))

    for i in range(n, 2 * n):
        # Fill in here
        # Note that unlike in get_training_data, you are not sampling
        # random patches from the nonface images, just reading them in
        # and using them directly.
        # Read the next face file
        face = cv2.imread(nonface_filenames[i-n], cv2.IMREAD_GRAYSCALE)

        # Compute HoG descriptor
        face_descriptor = hog36(face, orientations, wrap180)
        descriptors[i, 0] = 1
        descriptors[i, 1:] = face_descriptor
        classes[i] = 0

    return descriptors, classes
