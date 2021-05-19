from selenium import webdriver
import time
import requests
import shutil
import os
import argparse


def save_img(input, image_url, index, directory):
    try:
        filename = f'{input}_{str(index).zfill(5)}.jpg'
        response = requests.get(image_url, stream=True)
        image_path = os.path.join(directory, filename)
        with open(image_path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
    except Exception:
        pass


def find_urls(input, url, driver, directory):
    driver.get(url)
    for _ in range(500):
        driver.execute_script('window.scrollBy(0,10000)')
        try:
            driver.find_element_by_css_selector('.mye4qd').click()
        except:
            continue
        time.sleep(1)
    for index, image_url in enumerate(driver.find_elements_by_css_selector('.rg_i.Q4LuWd')):
        try:
            image_url.click()
            time.sleep(1.5)
            image = driver.find_element_by_xpath(
                '/html/body/div[2]/c-wiz/div[4]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div/div[2]/a/img'
                ).get_attribute("src")
            print(image)
            save_img(input, image, index, directory)
        except:
            pass


def main():
    parser = argparse.ArgumentParser(description='Scrape Google images')
    parser.add_argument(
        '-s', '--search', default='bananas', type=str, help='search term'
        )
    parser.add_argument(
        '-d',
        '--directory',
        default='downloads\\',
        type=str,
        help='save directory'
        )
    args = parser.parse_args()

    driver = webdriver.Chrome('chromedriver.exe')
    directory = args.directory
    search = args.search
    if not os.path.isdir(directory):
        os.makedirs(directory)
    url = f'https://www.google.com/search?q={str(search)}&source=lnms&tbm=isch&sa=X&ved=2ahUKEwie44_AnqLpAhUhBWMBHUFGD90Q_AUoAXoECBUQAw&biw=1920&bih=947'

    find_urls(search, url, driver, directory)

    print('all possible images scraped.')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('quitting...')
        pass
