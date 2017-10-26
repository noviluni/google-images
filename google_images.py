import os
import sys
import json
import shutil
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


download_path = 'dataset/'
button_xpath = '//*[@id="smb"]'
images_xpath = '//div[contains(@class,"rg_meta")]'


def create_dir(search_text):
    # We create new dir from search term only if it doesn't exist
    if not os.path.exists(download_path + search_text.replace(' ', '_')):
        os.makedirs(download_path + search_text.replace(' ', '_'))


def init_webdriver():
    profile = webdriver.FirefoxProfile()
    # If you want to set a browser language preference you can uncomment the next 3 code lines.
    # However it seems that doesn't work as expected.

    # locale = 'en-US'
    # profile.set_preference('intl.accept_languages',locale)
    # profile.set_preference('general.useragent.locale',locale)
    return webdriver.Firefox(profile)


def send_infinity_scroll(driver):
    # We send to the browser an infinite and constant scroll.
    driver.execute_script('setInterval(function() {window.scrollBy(0, 1000000)}, 1000);')


def click_element(driver, xpath, timeout=10):
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()


def scroll(driver, img_num_requested):
    # Google show us 100 images and we need to scroll to get more.
    send_infinity_scroll(driver)

    # However, when 400 images are charged appears a button that must be clicked.
    # If we want more than 400 images we should click the button.
    for i in range(img_num_requested//400):
        try:
            # We search for "Show more results button" and click it
            click_element(driver, xpath=button_xpath)
        except TimeoutException:
            # If we can find the button after timeout, we make an advise.
            print('After {} scrolls, there was an error trying to locate the "Show more results" button.'
                  ' If you can see it then you can try changing "button_xpath" variable in code.'.format(i))
            break


def get_images(driver):
    images = driver.find_elements_by_xpath(images_xpath)
    print('Total available images: {}\n'.format(len(images)))
    return images


def get_image_file(image, final_download_path, img_count, downloaded_img_count):
    headers = {'User-Agent':
               'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    img_extensions = {'jpg', 'jpeg', 'png', 'gif'}

    # We get image url and type
    img_url = json.loads(image.get_attribute('innerHTML'))["ou"]
    img_type = json.loads(image.get_attribute('innerHTML'))["ity"]

    if img_type not in img_extensions:
        img_type = 'jpg'

    print('Downloading image {}: {}'.format(img_count, img_url))

    # We download every image and save it on disk
    response = requests.get(img_url, headers=headers, stream=True)
    image_name = '{}/{}.{}'.format(final_download_path, str(downloaded_img_count), img_type)
    with open(image_name, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response


def save_images(images, img_num_requested, final_download_path):
    img_count = 0
    downloaded_img_count = 0

    for image in images:
        img_count += 1
        try:
            get_image_file(image, final_download_path, img_count, downloaded_img_count)
            downloaded_img_count += 1
        except Exception as e:
            print('Download failed: {}\n'.format(e))
        if downloaded_img_count >= img_num_requested:
            break

    print('Total downloaded: {}/{}\n'.format(downloaded_img_count, img_count))


def main():
    search_text = sys.argv[1]  # Search term coming from first argument
    img_num_requested = int(sys.argv[2])  # Number of images coming from second argument

    # We build the url and the directory using search_text
    url = 'https://www.google.com/search?q={}&source=lnms&tbm=isch'.format(search_text)
    final_download_path = '{}{}'.format(download_path, search_text.replace(" ", "_"))

    # We create a directory to put images inside
    create_dir(search_text)

    # We initialize the driver
    driver = init_webdriver()

    # We make a request to the google image website
    driver.get(url)

    # We scroll and click "Show more results" button depending of the number of images requested
    scroll(driver, img_num_requested)

    # We get images URL
    images = get_images(driver)

    # We save requested images
    save_images(images, img_num_requested, final_download_path)
    
    # We stop the driver
    driver.quit()


if __name__ == '__main__':
    main()
