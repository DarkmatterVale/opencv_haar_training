# -*- coding: utf-8 -*-
#
# Copyright 2016 Vale Tolpegin
# Distributed under the terms of the MIT License.

# -- Modules ------------------------------------------------------------------

from optparse import OptionParser


# -- global options -----------------------------------------------------------

global __Options__


# -- getOption ===-------------------------------------------------------------

def getOption(string):
    """
    Fetches an option by name
    """
    return getattr(__Options__, string)


# -- parseOptions -------------------------------------------------------------

def parseOptions():
    """
    Completes command line argument parsing
    """
    parser = OptionParser(usage='usage: %prog [options]', version='0.0.1')
    parser.add_option('-d', '--debug', action='store_true', dest='debug', default=False, help="whether debugging to the console should be on or off")
    parser.add_option('-w', '--width', dest='width', help="cascade target width")
    parser.add_option('-l', '--height', dest='height', help="cascade target height")
    parser.add_option('-i', '--images', dest='images', help="total number of images to use in training")
    parser.add_option('-n', '--num-stages', dest='num_stages', help="number of stages to train the cascade with")

    global __Options__

    (__Options__, args) = parser.parse_args()

    return (__Options__, args)
