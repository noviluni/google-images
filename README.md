# google-images

Simple script using Python and Selenium that allows to **download images from Google Images**.
This script was developed to get an image database to train a neuronal network (AI).

*Author: Marc Hernández*


### How to use:

Just type in a terminal:

```shell
 python3 google_images.py "cat" 10
```

You can change “cat” by any word or sentence you want to search and “10” by any number of images you want to download.

*Note: Keep in mind that this script allows you to download all the images that google send you, normally less than 1000. Depending of the term you search for, you are going to get more or less results.*


### Requirements

##### System requirements:
- *Python 3*
- *geckodriver* in PATH.

*Note: You can download the geckodriver [here](https://github.com/mozilla/geckodriver/releases). Then you must decompress it and move it into PATH. The simple way in linux to add the executable to the PATH is moving it to /usr/bin and adding it execute permissions (super user required).*


##### Python requirements:
- *requests*
- *selenium*

You can install them using `pip install -r requirements.txt`.


### Limitations and ideas
Normally you can get from *Google Images* less than 1000 images by query.
 If you are going to use this script to download images to train a neural network,
 you can search for the same term in different languages to get more results or run the script several times using similar terms like "smiling cats" and "laughing cats".


### License
You can download, change, adapt and do whatever you want with this code without my explicit permission and without attribution, just in compliance with the GPLv3 license.