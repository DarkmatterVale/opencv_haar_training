import subprocess
import os
import shutil
from time import sleep
import sys
from utils import parseOptions
from utils import getOption

parseOptions()

DEBUG = getOption("debug")
WIDTH = str(30)
HEIGHT = str(30)
DEFAULT_NEG = 900
DEFAULT_POS = 1800

if getOption("width") != None:
    WIDTH = getOption("width")
if getOption("height") != None:
    HEIGHT = getOption("height")

GEN_FOLDER = "generated"
NEGATIVES_FOLDER = "negatives/"
POSITIVES_FOLDER = "positives/"
DATA_FOLDER = "haarcascade"
SAMPLES_FOLDER = "samples"
VEC_FOLDER = "vectors"

NEG_FILE = "negatives.txt"
POS_FILE = "positives.txt"
INFO_FILE = "info.lst"
VEC_FILE = "positives.vec"

MERGE_VEC_SCRIPT_PATH = "./utils/mergevec.py"

GEN_NORMALIZED_NEGATIVES_FOLDER = "normalized_neg"
GEN_NORMALIZED_POSITIVES_FOLDER = "normalized_pos"

GEN_NEG_FILE = os.path.join(GEN_FOLDER, NEG_FILE)
GEN_INFO_FILE = os.path.join(GEN_FOLDER, INFO_FILE)

GEN_NORMALIZED_NEGATIVES_PATH = os.path.join(GEN_FOLDER, GEN_NORMALIZED_NEGATIVES_FOLDER)
GEN_NORMALIZED_POSITIVES_PATH = os.path.join(GEN_FOLDER, GEN_NORMALIZED_POSITIVES_FOLDER)
GEN_SAMPLES_PATH = os.path.join(GEN_FOLDER, SAMPLES_FOLDER)
GEN_VEC_PATH = os.path.join(GEN_FOLDER, VEC_FOLDER)

CREATE_SAMPLES_COMMAND_EX = "opencv_createsamples -img POS_IMG -bg " + GEN_NEG_FILE + " -info INFO_LOC -pngoutput SAMPLES_PATH -maxxangle 0.5 -maxyangle 0.5 -maxzangle 0.5 -num NUM_IMG"
CREATE_NEG_FILE_EX = 'find ' + GEN_NORMALIZED_NEGATIVES_FOLDER + ' -iname "*.jpg" > ' + NEG_FILE
CREATE_POS_FILE_EX = 'find ' + GEN_NORMALIZED_POSITIVES_FOLDER + ' -iname "*.jpg" > POS_FILE'
CREATE_VEC_COMMAND_EX = "opencv_createsamples -info INFO_LOC -num NUM_IMG -w " + WIDTH + " -h " + HEIGHT + " -vec VEC_FILE"
TRAIN_CASCADE_COMMAND = "opencv_traincascade -data ../" + DATA_FOLDER + " -vec " + VEC_FILE + " -bg " + NEG_FILE + " -numPos 1800 -numNeg 900 -numStages 1 -w " + WIDTH + " -h " + HEIGHT
MERGE_VECTORS_COMMAND_EX = "python " + MERGE_VEC_SCRIPT_PATH + " -v INPUT_FILES -o OUTPUT_FILE"

if __name__ == '__main__':
    # Ensuring the previous build has been removed
    if os.path.exists(GEN_FOLDER):
        if DEBUG:
            print("[*] Removing previous build...")
        shutil.rmtree(GEN_FOLDER)
        if DEBUG:
            print("[*] Previous build has been removed")
        sleep(0.1)

    # Making required folders
    if DEBUG:
        print("[*] Beginning folder creation...")
    subprocess.Popen(["mkdir", GEN_FOLDER]).wait()
    subprocess.Popen(["mkdir", GEN_NORMALIZED_NEGATIVES_PATH]).wait()
    subprocess.Popen(["mkdir", GEN_NORMALIZED_POSITIVES_PATH]).wait()
    subprocess.Popen(["mkdir", GEN_VEC_PATH]).wait()
    if DEBUG:
        print("[*] Completed folder creation")
    sleep(0.1)

    # Copying all negative images into a new folder
    if DEBUG:
        print("[*] Copying all negative images to secondary location...")
    NUM_NEGATIVES = 0
    for file_name in os.listdir(NEGATIVES_FOLDER):
        full_file_name = os.path.join(NEGATIVES_FOLDER, file_name)

        if os.path.isfile(full_file_name):
            if ".jpg" in full_file_name:
                shutil.copy(full_file_name, GEN_NORMALIZED_NEGATIVES_PATH)

                NUM_NEGATIVES += 1
    if DEBUG:
        print("[*] Completed negative image copying")
    sleep(0.1)

    # Generate negative images file (contains all of the negative images)
    if DEBUG:
        print("[*] Generating negative images information file...")
    os.chdir(GEN_FOLDER)
    os.system(CREATE_NEG_FILE_EX)
    os.chdir("../")
    if DEBUG:
        print("[*] Completed negative images information generation")
    sleep(0.1)

    # Copying all positive images into a new folder
    if DEBUG:
        print("[*] Copying all positive images to secondary location...")
    NUM_POSITIVES = 0
    for file_name in os.listdir(POSITIVES_FOLDER):
        full_file_name = os.path.join(POSITIVES_FOLDER, file_name)

        if os.path.isfile(full_file_name):
            if ".jpg" in full_file_name:
                shutil.copy(full_file_name, GEN_NORMALIZED_POSITIVES_PATH)

                NUM_POSITIVES += 1
    if DEBUG:
        print("[*] Completed positive image copying")
    sleep(0.1)

    # Creating samples for the positive images
    counter = 1
    for file_name in os.listdir(GEN_NORMALIZED_POSITIVES_PATH):
        full_file_name = os.path.join(GEN_NORMALIZED_POSITIVES_PATH, file_name)

        if os.path.isfile(full_file_name):
            if ".jpg" in full_file_name:
                if DEBUG:
                    print("[*] Creating samples...")
                subprocess.Popen(["mkdir", (GEN_SAMPLES_PATH + str(counter))]).wait()
                create_samples = CREATE_SAMPLES_COMMAND_EX.replace("POS_IMG", full_file_name).replace("NUM_IMG", str(NUM_NEGATIVES)).replace("SAMPLES_PATH", (GEN_SAMPLES_PATH + str(counter))).replace("INFO_LOC", os.path.join((GEN_SAMPLES_PATH + str(counter)), INFO_FILE))
                process = subprocess.Popen(create_samples.split(" "), stdout=sys.stdout)
                process.wait()
                if DEBUG:
                    print("[*] Finished creating samples")

                # Creating vector file
                if DEBUG:
                    print("[*] Creating vector file...")
                GEN_VEC_FILE = os.path.join(GEN_VEC_PATH, VEC_FILE)
                create_vec_file = CREATE_VEC_COMMAND_EX.replace("NUM_IMG", str(NUM_NEGATIVES)).replace("VEC_FILE", (GEN_VEC_FILE[:-4] + str(counter) + GEN_VEC_FILE[-4:])).replace("INFO_LOC", os.path.join((GEN_SAMPLES_PATH + str(counter)), INFO_FILE))
                os.system(create_vec_file)
                if DEBUG:
                    print("[*] Finished writing vector file")

                counter += 1

                sleep(0.1)

    # Merging vector files into one
    if DEBUG:
        print("[*] Compiling vector files into one single file...")
    merge_command = MERGE_VECTORS_COMMAND_EX.replace("INPUT_FILES", GEN_VEC_PATH).replace("OUTPUT_FILE", os.path.join(GEN_FOLDER, VEC_FILE))
    os.system(merge_command)
    if DEBUG:
        print("[*] Finished compiling vector files into a single file")
    sleep(0.1)

    # Training cascade
    if DEBUG:
        print("[*] Training the cascade...")
    os.chdir(GEN_FOLDER)
    process = subprocess.Popen(TRAIN_CASCADE_COMMAND, shell=True)
    process.wait()
    os.chdir("../")
    if DEBUG:
        print("[*] Finished training the cascade")
    sleep(0.1)
