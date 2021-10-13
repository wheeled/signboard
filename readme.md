# `signboard`

## Overview
`signboard` is a Python utility to optimally rescale .jpg images of any size for the Electroboard sign.

The ``downscale`` module takes each input image and, using the default (LANCZOS) filter, rescales it to 320 x 160 pixels to fit on the raster of the signboard. If the image has an aspect ratio other than 2 x 1, the image is rescaled and centred on a black raster such that the entire image appears on the sign.

## Important Note
Images need to be placed in the directory "raw_images" before running the script - if that directory does not exist it will be created the first time the script is run.

## Installation
The `signboard` repo is not presently published so that it can not be found by `pip`, `brew` or `easy-install`.  Installation involves cloning the repo onto your machine and then installing from there:

    git clone https://github.com/wheeled/signboard
    pip3 install -e /path/to/your/local/repo

## Usage
Once installed, the `downscale` module can be run from the command line with no arguments.

Example:

    $ python3 /path/to/your/local/repo/signboard/downscale.py 

13-Oct-2021