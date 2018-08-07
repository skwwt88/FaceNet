import os
import zipfile
from multiprocessing import Pool

import cv2 as cv
from tqdm import tqdm

from config import identity_annot_filename, image_folder, img_size
from utils import ensure_folder, get_bbox


def extract(folder):
    filename = '{}.zip'.format(folder)
    print('Extracting {}...'.format(filename))
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall('data')


def check_one_image(line):
    line = line.strip()
    if len(line) > 0:
        tokens = line.split(' ')
        image_name = tokens[0].strip()
        bbox = bboxes[image_name]
        x1, y1, w, h = bbox
        filename = os.path.join(image_folder, image_name)
        original = cv.imread(filename)
        try:
            cropped = original[y1:y1 + h, x1:x1 + w]
            resized = cv.resize(cropped, (img_size, img_size), cv.INTER_CUBIC)
        except cv.error as err:
            print(filename)
            print('x1={}, y1={}, w={}, h={}'.format(x1, y1, w, h))
            print('original.shape: ' + str(original.shape))
            print('cropped.shape: ' + str(cropped.shape))
            print('resized.shape: ' + str(resized.shape))



def check_image():
    with open(identity_annot_filename, 'r') as file:
        lines = file.readlines()
    pool = Pool(1)
    for _ in tqdm(pool.imap_unordered(check_one_image, lines), total=len(lines)):
        pass
    pool.close()
    pool.join()


if __name__ == '__main__':
    # parameters
    ensure_folder('data')

    if not os.path.isdir(image_folder):
        extract(image_folder)

    bboxes = get_bbox()
    check_image()
