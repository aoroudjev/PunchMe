import wget
import zipfile
import os

from win32com.client import Dispatch

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def get_version_via_com():
    parser = Dispatch("Scripting.FileSystemObject")
    version = parser.GetFileVersion(chrome_path)
    return version


def download_driver(version: str = None):
    if version:
        download_url = (
                "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/"
                + version
                + "/win64/chromedriver-win64.zip"
        )
    else:
        download_url = (
                "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/"
                + get_version_via_com()
                + "/win64/chromedriver-win64.zip"
        )

    latest_driver_zip = wget.download(download_url, 'chromedriver.zip')
    dir = './ChromeDriver'
    if not os.path.exists(dir):
        os.makedirs(dir)
    with zipfile.ZipFile(latest_driver_zip, 'r') as zip_ref:
        zip_ref.extractall(path=dir)

    os.remove(latest_driver_zip)
