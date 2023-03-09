import requests
import os
from bs4 import BeautifulSoup
import urllib3
from config import HEADERS

urllib3.disable_warnings()


class SciHub:
    """
    SciHub class to download PDF files

    Parameters
    ----------
    doi_list : list
        List of DOIs to download
    path : str
        Path to save the PDF files

    Methods
    -------
    download(doi, path= None)
        Download the PDF file

    Examples
    --------
    >>> from scihub import SciHub
    >>> doi_list = ["10.1016/j.biomaterials.2015.01.027", "10.1007/978-90-481-9145-1_6"]
    >>> SciHub(doi_list)
    """

    def __init__(self, doi_list, path= None): 
        self.req = requests.Session()
        self.req.headers = HEADERS
        self.available_scihub_urls = self._get_available_scihub_urls()

        for doi in doi_list:
            print("Processing DOI: {}".format(doi))
            self.download(doi, path)

    def _get_available_scihub_urls(self):
        """
        Get a list of all available SciHub URLs   
        """
        resp = self.req.get("https://sci-hub.now.sh/")
        soup = self._get_soup(resp.content)

        return [a["href"] + "/" for a in soup.find_all("a", href=True) 
                if "sci-hub." in a["href"]]

    def _get_soup(self, soup):
        """
        Get the BeautifulSoup object
        """
        return BeautifulSoup(soup, "html.parser")

    def _parse_path(self, doi, path= None):
        """
        Parse the path to save the PDF file
        """
        if path:
            return os.join.path(path, doi.replace("/", "_") + ".pdf")
        
        else:
            abs_path = os.path.dirname(__file__)
            download_path = os.path.join(abs_path, "Downloads")
            if os.path.isdir(download_path):
                return os.path.join(download_path, doi.replace("/", "_") + ".pdf")
            else:
                os.mkdir(download_path)
                return os.path.join(download_path, doi.replace("/", "_") + ".pdf")

    def _save_pdf(self, path, resp):
        """
        Save the PDF file
        """
        with open(path, "wb") as f:
            f.write(resp)

    def _get_download_url(self, soup):
        """
        Get the download URL
        """
        iframe = soup.find("iframe")
        embed = soup.find("embed")
        if iframe:
            url_download = iframe.get("src")
        if embed:
            url_download = "https:" + embed.get("src")

        return url_download

    def download(self, doi, path= None):
        """
        Download the PDF file
        """

        for available_url in self.available_scihub_urls:
            url = available_url + doi
            try:
                resp = self.req.get(url, verify= False)
            except:
                continue

            soup = self._get_soup(resp.content)
            url_download = self._get_download_url(soup)
            if url_download:
                break

        resp = self.req.get(url_download, verify= False)
        if resp.headers["Content-Type"] != "application/pdf":
            print("Paper not found in Sci-Hub: {}".format(doi))
        
        else:
            path = self._parse_path(doi, path)
            self._save_pdf(path, resp.content)
            print("Downloaded: {}".format(doi))
            

if __name__ == "__main__":
    SciHub(["10.1007/978-90-481-9145-1_6"])