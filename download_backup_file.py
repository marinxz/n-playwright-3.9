import logging
import sys
import os
import shutil
import platform

from configparser import ConfigParser

from playwright.sync_api import Playwright, sync_playwright
from playwright.sync_api import TimeoutError

logger = logging.getLogger(__name__)

def minimal_logger_setup():
    """
    good for testing, just to see debug statuements
    :return:
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(stream_handler)

def get_config(ini_file):
    config = ConfigParser()
    if not os.path.isfile(ini_file):
        return None
    config.read(ini_file)
    return config



def download_backup_file(location, config):

    #   collect input parameters to run download

    timeout = config.getint(location, 'timeout')
    download_timeout = config.getint(location, 'download_timeout')
    headless = config.getboolean(location, 'headless')
    user = config.get(location, 'user')
    password = config.get( location, 'password')
    url = config.get( location, 'url')
    if 'Linux' in platform.system():
        file_destination = config.get(location, 'file_destination_linux')
    elif 'Windows' in platform.system():
        file_destination = config.get(location, 'file_destination_win')
    else:
        logger.error(f"Unknown os: {platform.system()}, exiting")
        return False, None

    file_name = config.get(location, 'file_name')

    #   print parameters
    logger.info(f"{timeout}  {download_timeout} {headless}")
    logger.info (f" User: {user} {password} {url}")
    logger.info(f"File: {file_destination}  {file_name}")

    download_ok = False
    copied_file_path = None

    return False, None
    # open browser
    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(headless=headless, timeout=timeout)
        context = browser.new_context()
        # Open new page
        page = context.new_page()

        page.goto("https://ctfferndale.gingrapp.com/auth/login")
        page.locator("[placeholder=\"E-mail\"]").click()
        page.locator("[placeholder=\"E-mail\"]").fill(user)
        page.locator("[placeholder=\"Password\"]").click()
        page.locator("[placeholder=\"Password\"]").fill(password)

        # Click text=Sign In >> nth=0
        page.locator("text=Sign In").first.click()
        try:
            page.wait_for_url("https://ctfferndale.gingrapp.com/dashboard/index")

            #   we are logged

            # Click .fa >> nth=0
            page.locator(".fa").first.click()
            page.locator("span:has-text(\"Admin\")").click()
            page.wait_for_url("https://ctfferndale.gingrapp.com/admin")
            # Click text=Manage Data
            page.locator("text=Manage Data").click()
            page.wait_for_url("https://ctfferndale.gingrapp.com/admin/manage_data")

            # Click text=Click Here To Backup Your Database

            with page.expect_download(timeout=download_timeout) as download_info:
                page.locator("text=Click Here To Backup Your Database").click()
            download = download_info.value
            download_file_path = download.path()
            logger.info(f"File downloaded: {download_file_path}")
            is_ok = os.path.isfile(download_file_path) and os.path.getsize(download_file_path) > 0
            if not is_ok:
                logger.error("Download is not complete")
                download_ok = False
            else:
                logger.info('Copying file to permanent destination')
                file_dest_path = os.path.join(file_destination, file_name)
                copied_file_path = shutil.copyfile(download_file_path, file_dest_path)
                logger.info(f"copied file name: {copied_file_path}")
                download_ok = True
            page.wait_for_url("https://ctfferndale.gingrapp.com/admin/manage_data")
        except TimeoutError as tex:
            logger.error(f"Timeout while waiting for download {str(tex)}")
            download_ok = False
        except Exception as ex:
            logger.error(f"General error while downloading {str(ex)}")
            download_ok = False

        #   logout

        # Click text=Test Guest Canine To Five Ferndale
        page.locator("text=Test Guest Canine To Five Ferndale").click()
        # Click text=Logout >> nth=1
        page.locator("text=Logout").nth(1).click()

        # close connection
        context.close()
        browser.close()

    return download_ok, copied_file_path


if __name__ == '__main__':

    minimal_logger_setup()
    valid_locations = ['Ferndale', 'Detroit']

    if len(sys.argv) < 2:
        logger.error(f"Location argument is missing: {valid_locations}")
        exit(1)
    else:
        location = sys.argv[1]
    if location not in valid_locations:
        logger.error(f"Invalid location: {location}")
        exit(1)

    ini_file = 'download_backup_file.ini'
    config = get_config(ini_file)
    if config is None:
        logger.info(f"Configuraion file not loaded")
        exit(1)

    logger.info(f"Starting download for location: {location}")

    is_ok, ferndale_file_path = download_backup_file(location, config)
    if is_ok:
        logger.info(f'File downloaded successfully: {ferndale_file_path}')
    else:
        logger.error('Problem downloading file')
    ret_code = 0 if is_ok else 1

    exit(ret_code)