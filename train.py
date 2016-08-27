import subprocess
import os
import shutil
from time import sleep
import sys

NEGATIVES_PATH = "negatives/"
POSITIVES_PATH = "positives/"
GEN_FOLDER = "generated"
DATA_FOLDER = "../haarcascade"
GEN_NORMALIZED_NEGATIVES_FOLDER = "normalized_neg"
GEN_NORMALIZED_NEGATIVES_PATH = "generated/normalized_neg/"
GEN_SAMPLES_PATH = "generated/samples/"
NEG_FILE = "negatives.txt"
INFO_FILE = "samples/info.lst"
GEN_NEG_FILE = os.path.join(GEN_FOLDER, NEG_FILE)
GEN_INFO_FILE = os.path.join(GEN_FOLDER, INFO_FILE)
VEC_FILE = "positives.vec"
GEN_VEC_FILE = os.path.join(GEN_FOLDER, VEC_FILE)

DEBUG = True

CREATE_SAMPLES_COMMAND_EX = "opencv_createsamples -img POS_IMG -bg NEG_FILE -info INFO_LOC -pngoutput OUT_LOC -maxxangle 0.5 -maxyangle 0.5 -maxzangle 0.5 -num 1950"
CREATE_NEG_FILE_EX = 'find DIR -iname "*.jpg" > NEG_FILE'
CREATE_VEC_COMMAND_EX = "opencv_createsamples -info INFO_LOC -num 1950 -w 20 -h 20 -vec VEC_FILE"
TRAIN_CASCADE_COMMAND = "opencv_traincascade -data " + DATA_FOLDER + " -vec " + VEC_FILE + " -bg " + NEG_FILE + " -numPos 1800 -numNeg 900 -numStages 5 -w 20 -h 20"

if __name__ == '__main__':
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
    for file_name in os.listdir(NEGATIVES_PATH):
        full_file_name = os.path.join(NEGATIVES_PATH, file_name)

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
    create_neg_file = CREATE_NEG_FILE_EX.replace("DIR", GEN_NORMALIZED_NEGATIVES_FOLDER).replace("NEG_FILE", NEG_FILE)
    os.system(create_neg_file)
    os.chdir("../")
    if DEBUG:
        print("[*] Completed negative images information generation")
    sleep(0.1)

    # Creating samples for the positive images
    if DEBUG:
        print("[*] Creating samples...")
    made_samples = False
    for file_name in os.listdir(POSITIVES_PATH):
        if made_samples == False:
            full_file_name = os.path.join(POSITIVES_PATH, file_name)

            if (os.path.isfile(full_file_name)):
                if ".jpg" in full_file_name:
                    create_samples = CREATE_SAMPLES_COMMAND_EX.replace("POS_IMG", full_file_name).replace("NEG_FILE", GEN_NEG_FILE).replace("INFO_LOC", GEN_INFO_FILE).replace("OUT_LOC", GEN_SAMPLES_PATH)
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
    create_vec_file = CREATE_VEC_COMMAND_EX.replace("INFO_LOC", GEN_INFO_FILE).replace("VEC_FILE", GEN_VEC_FILE)
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
