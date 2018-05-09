import json
import math
import os
import re

import requests
from tqdm import tqdm


class ChanDownloader:
    uri = ''
    JSON = ''
    urls = []
    board = ''
    thread = ''

    def __init__(self, url):
        self.uri = url
        self.getLinksFromJSON()

    def getJSON(self):
        """
        Requests the JSON from Chan and assign it as a decoded json to self.JSON
        :return: Void
        """
        self.verifiesLink()
        funcJson = requests.get('https://a.4cdn.org/' + self.board + '/thread/' + self.thread + '.json')
        self.JSON = json.loads(funcJson.text)

    def getLinksFromJSON(self):
        """
        Filters the JSON for the media URL and appends them to self.urls
        This method is called in the initializer and has to be called to work with this module
        in other python called.
        :return: Void
        """
        self.getJSON()
        for posts in self.JSON['posts']:
            try:
                self.urls.append(
                    [f'https://i.4cdn.org/{self.board}/{posts["tim"]}{posts["ext"]}', self.board, posts['tim'],
                     posts["ext"]])
            except:
                pass

    def verifiesPath(self):
        """
        Verifes the path for the download function.
        """
        path = input('Please enter your desired path: ')
        normPath = os.path.normpath(path + f'/{self.JSON["posts"][0]["semantic_url"]}')

        if os.path.exists(normPath):
            print('Folder already exisit!')
        else:
            os.mkdir(normPath)
            print('Folder was created!')
        return normPath

    def download(self):
        """
        Checks the the filepath and if folders have to created, normalizes then the path.
        Downloads the Images/Gifs/webm from the given *chan thread to the computer.

        :return: Void
        """
        counter = 0
        normPath = self.verifiesPath()

        print('Starting Download!')

        for content in self.urls:
            r = None
            total_size = 0

            print('Connecting:')
            try:
                r = requests.get(content[0], timeout=6.0, stream=True)
                total_size = int(r.headers.get('content-length', 0))
            except (ConnectionRefusedError, TimeoutError, ConnectionError, ConnectionAbortedError) as error:
                print(error)

            if r:
                with open(os.path.normcase(f'{normPath}/{content[2]}{content[3]}'), 'wb') as handle:
                    for data in tqdm(r.iter_content(), total=math.ceil(total_size), ascii=True,
                                     desc=f'Download: {counter} of {len(self.urls)}', unit='KB', unit_scale=True):
                        handle.write(data)
            counter += 1
        print('Finished Download!')

    def verifiesLink(self):
        """
        Verifies the links which is given by the constructor of the class.
        """
        regex = r'boards\.4chan\.org\/(\w*)\/thread\/(\d*)'
        matches = re.search(regex, self.uri)

        if matches is None:
            print('Please enter a valid URL!')
            exit()
        else:
            print('Your URL is valid!')

            self.board = matches.group(1)
            self.thread = matches.group(2)
