# OpenCV 3 haar cascade training

This project provides a simple way to generate haar cascades.

## How do I use this?

*Important:* Please read the System Requirements section before attempting to train a classifier to ensure your system meets all of the system requirements to use this application.

First, insert negative images into the *negatives* directory. Then, insert all positive images into the *positives* directory. It is important to note that the negative images *MUST* be larger (in both width and height) than the positive images. Also, this program *DOES NOT* clean the images (i.e. resizing to ensure all the negative and positive images are the same size) so this must be done before training. These are requirements set forth by OpenCV's training system. Finally, to train a HaarCascade, simply run ```python3 train.py```. The generated cascade file as well as each stage file will be placed in the folder *haarcascade*. For details about how the program works, see the "How It Works / Examples" section.

## How It Works / Examples

The following is an example command to use the training software:

```
python3 train.py --width 50 --height 50 --num_stages 10 --images 1000
```

In the above command, a number of the settings for the trainer are being specified:
- The ```width``` and ```height``` options specify the size of the area the trainer will look at. The values specified can be less than the actual width and height of the negative images but never equal or more. The defaults for both the parameters is ```30```
- The ```num_stages``` option specifies the number of stages the training should occur. The longer the number of stages the longer it will take to train the classifier. The default for the ```num_stages``` parameter is ```5```
- The ```images``` parameter specifies the number of positive images to use. By default, this is ```500``` but it should be ~90% of the images in the *positives* directory (given you have a sufficient number of negative images). This parameter also dictates the number of negative images that will be used (default is ```1000```). The number of negatives used is always 2 times that of the positive images, so be sure to set the ```images``` parameter low enough that enough negative images are available. Another consideration when setting this parameter is to ensure that no more than ~90% of negative images are used. Because of the way OpenCV trains classifiers, additional negatives about the number specified will be used which will cause problems if an ```images``` parameter is too high

As an example, lets assume we have 1000 positive images of an apple (images that contain an apple) and 2200 negative images (images that don't contain an apple). All the positive images are sized 50x50 (width x height) and all negative images are 20x20 (width x height). In addition, lets assume that we have a powerful computer that has a strong CPU. The following would be a good set of parameters to provide the trainer with:

```
python3 train.py --width 10 --height 10 --num_stages 10 --images 900
```

Note that although we have 1000 positive images, I only used 900. This is to provide the trainer with a few extras in the event they are needed.

The final generated cascade will be located in the *haarcascade* directory.

## System Requirements

At the moment, there are a number of requirements that must be met to use the system:

1. Python 3.x (I've tested Python 3.5.x and verified it works)
2. Python 2.7.x (the script which merges the vector files requires Python 2.7.x)
2. OpenCV 3.1.x
3. Linux/Mac OSX

## Acknowledgments

A huge thanks to https://github.com/mrnugget for writing ```mergevec.py```.
