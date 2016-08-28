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

if getOption("width") != None:
    WIDTH = getOption("width")
if getOption("height") != None:
    HEIGHT = getOption("height")

GEN_FOLDER = "generated"
NEGATIVES_FOLDER = "negatives/"
POSITIVES_FOLDER = "positives/"
DATA_FOLDER = "haarcascade"
SAMPLES_FOLDER = "samples"

NEG_FILE = "negatives.txt"
INFO_FILE = "samples/info.lst"
VEC_FILE = "positives.vec"

GEN_NORMALIZED_NEGATIVES_FOLDER = "normalized_neg"

GEN_NEG_FILE = os.path.join(GEN_FOLDER, NEG_FILE)
GEN_INFO_FILE = os.path.join(GEN_FOLDER, INFO_FILE)
GEN_VEC_FILE = os.path.join(GEN_FOLDER, VEC_FILE)

GEN_NORMALIZED_NEGATIVES_PATH = "generated/normalized_neg/"
GEN_SAMPLES_PATH = os.path.join(GEN_FOLDER, SAMPLES_FOLDER)

CREATE_SAMPLES_COMMAND_EX = "opencv_createsamples -img POS_IMG -bg " + GEN_NEG_FILE + " -info " + GEN_INFO_FILE + " -pngoutput " + GEN_SAMPLES_PATH + " -maxxangle 0.5 -maxyangle 0.5 -maxzangle 0.5 -num 1950"
CREATE_NEG_FILE_EX = 'find ' + GEN_NORMALIZED_NEGATIVES_FOLDER + ' -iname "*.jpg" > ' + NEG_FILE
CREATE_VEC_COMMAND_EX = "opencv_createsamples -info " + GEN_INFO_FILE + " -num 1950 -w " + WIDTH + " -h " + HEIGHT + " -vec " + GEN_VEC_FILE
TRAIN_CASCADE_COMMAND = "opencv_traincascade -data ../" + DATA_FOLDER + " -vec " + VEC_FILE + " -bg " + NEG_FILE + " -numPos 1800 -numNeg 900 -numStages 1 -w " + WIDTH + " -h " + HEIGHT

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
    subprocess.Popen(["mkdir", GEN_SAMPLES_PATH]).wait()
    if DEBUG:
        print("[*] Completed folder creation")
    sleep(0.1)

    # Copying all negative images into a new folder
    if DEBUG:
        print("[*] Copying all negative images to secondary location...")
    for file_name in os.listdir(NEGATIVES_FOLDER):
        full_file_name = os.path.join(NEGATIVES_FOLDER, file_name)

        if (os.path.isfile(full_file_name)):
            if ".jpg" in full_file_name:
                shutil.copy(full_file_name, GEN_NORMALIZED_NEGATIVES_PATH)
    if DEBUG:
        print("[*] Completed negative image copying")
    sleep(0.1)

    # Generate negative images file (contains all of the negative images)
    if DEBUG:
        print("[*] Generating negative images information file...")
    os.chdir(GEN_FOLDER)
    create_neg_file = CREATE_NEG_FILE_EX
    os.system(create_neg_file)
    os.chdir("../")
    if DEBUG:
        print("[*] Completed negative images information generation")
    sleep(0.1)

    # Creating samples for the positive images
    if DEBUG:
        print("[*] Creating samples...")
    made_samples = False
    for file_name in os.listdir(POSITIVES_FOLDER):
        if made_samples == False:
            full_file_name = os.path.join(POSITIVES_FOLDER, file_name)

            if (os.path.isfile(full_file_name)):
                if ".jpg" in full_file_name:
                    create_samples = CREATE_SAMPLES_COMMAND_EX.replace("POS_IMG", full_file_name)
                    process = subprocess.Popen(create_samples.split(" "), stdout=sys.stdout)
                    process.wait()

                    made_samples = True
        else:
            break
    if DEBUG:
        print("[*] Finished creating samples")
    sleep(0.1)

    # Creating vector file
    if DEBUG:
        print("[*] Creating vector file...")
    create_vec_file = CREATE_VEC_COMMAND_EX
    os.system(create_vec_file)
    if DEBUG:
        print("[*] Finished writing vector file")
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
