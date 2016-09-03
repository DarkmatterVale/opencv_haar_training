# OpenCV 3 haar cascade training

This project provides a simple way to generate haar cascades.

## How do I use this?

*Important:* Please read the System Requirements section before attempting to train a classifier to ensure your system meets all of the system requirements to use this application.

First, insert negative images into the *negatives* directory. Then, insert all positive images into the *positives* directory. It is important to note that the negative images *MUST* be larger (in both width and height) than the positive images. Also, this program *DOES NOT* clean the images (i.e. resizing to ensure all the negative and positive images are the same size) so this must be done before training. These are requirements set forth by OpenCV's training system. Finally, to train a HaarCascade, simply run ```python3 train.py```. The generated cascade file as well as each stage file will be placed in the folder *haarcascade*. For details about how the program works, see the "How It Works" section.

## System Requirements

At the moment, there are a number of requirements that must be met to use the system:

1. Python 3.x (I've tested Python 3.5.x and verified it works)
2. Python 2.7.x (the script which merges the vector files requires Python 2.7.x)
2. OpenCV 3.1.x
3. Linux/Mac OSX

## Acknowledgments

A huge thanks to https://github.com/mrnugget for writing ```mergevec.py```.
