import warnings
from typing import Optional
from pathlib import Path
import urllib.request
import urllib
import imghdr
import posixpath
import re

'''
Python api to download image form Bing.
Author: Guru Prasad (g.gaurav541@gmail.com)
'''


class Bing:
    def __init__(self,
                 query: str,
                 limit: int,
                 output_dir: str,
                 adult: str,
                 timeout: int,
                 img_type: Optional[str] = None, # filters
                 color: Optional[str] = None, # filters
                 size: Optional[str] = None, # filters
                 aspect: Optional[str] = None, # filters
                 people: Optional[str] = None, # filters
                 verbose: bool = True) -> None:
        """
        added filter args
        filter args:
            color       None(all) or color, bw, RED, ORANGE, GREEN, YELLOW, TEAL, BLUE,
                                        PURPLE, BROWN, BLACK, GRAY, WHITE
                img_type, size and aspect can either be full name or first initial
            img_type    None(all) or [l]inedrawing, [p]hoto, [c]lipart, [g]if | [a]nimatedgif, [t]ransparent
            size        None(all) [w]allpaper, [l]arge, [m]edium, [s]mall
            aspect      None(all) [s]quare [w]ide [t]all
            people      None(all) [f]face [p]portrait
            

        """
        self.download_count = 0
        self.query = query
        self.output_dir = output_dir
        self.adult = adult
        self.filters = self.get_filters(img_type, color, size, aspect, people)
        self.verbose = verbose
        self.seen = set()

        assert type(limit) == int, "limit must be integer"
        self.limit = limit
        assert type(timeout) == int, "timeout must be integer"
        self.timeout = timeout

        # self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}
        self.page_counter = 0
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
      'AppleWebKit/537.11 (KHTML, like Gecko) '
      'Chrome/23.0.1271.64 Safari/537.11',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'}


    @staticmethod
    def get_filters(img_type, color, size, aspect, people):
        """ multiple image filters"""
        out = ''
        if img_type is not None:
            _types = {'l':'linedrawing', 'p':'photo', 'g':'animatedgif', 'a':'animatedgif',
                      't':'transparent'}
            _t = img_type.lower()[0]
            if _t in _types:
                out += f"+filterui:photo-{_types[_t]}"
            else:
                warnings.warn(f"ignoring, image type: {img_type} not found in {_types.values()}")
        if color is not None:
            _colors=("RED", "ORANGE", "YELLOW", "GREEN", "TEAL", "BUE", "PURPLE", "BROWN",
                     "BLACK", "GRAY", "WHITE")
            if color.upper() in _colors:
                out += f"+filterui:color2-FGcls_{color.upper()}"
            elif color.lower() in ("color", "bw"):
                out += f"+filterui:color2-{color.lower()}"
            else:
                _colors = list(_colors) + ['color', 'bw']
                warnings.warn(f"ignoring, image color: {color} not found in {_colors}")
        if size is not None:
            _sizes = {'w':'wallpaper', 'l':'large', 'm':'medium', 's':'small'}
            if size.lower()[0] in _sizes:
                out += f"+filterui:imagesize-{_sizes[size.lower()]}"
            else:
                warnings.warn(f"ignoring, image size: {size} not found in {_sizes.values()}")
        if aspect is not None:
            _aspects = {'s':'square', 'w':'wide', 't':'tall'}
            if aspect.lower()[0] in _aspects:
                out += f"+filterui:aspect-{_aspects[aspect.lower()]}"
        if people is not None:
            _peoples = {'p':'portrait', 'f':'face'}
            if people.lower()[0] in _peoples:
                out += f"+filterui:face-{_peoples[people.lower()[0]]}"
        return out


    def save_image(self, link, file_path):
        request = urllib.request.Request(link, None, self.headers)
        image = urllib.request.urlopen(request, timeout=self.timeout).read()
        if not imghdr.what(None, image):
            print('[Error]Invalid image, not saving {}\n'.format(link))
            raise ValueError('Invalid image, not saving {}\n'.format(link))
        with open(str(file_path), 'wb') as f:
            f.write(image)

    def download_image(self, link):
        self.download_count += 1
        # Get the image link
        try:
            path = urllib.parse.urlsplit(link).path
            filename = posixpath.basename(path).split('?')[0]
            file_type = filename.split(".")[-1]
            if file_type.lower() not in ["jpe", "jpeg", "jfif", "exif", "tiff",
                                         "gif", "bmp", "png", "webp", "jpg"]:
                file_type = "jpg"

            if self.verbose:
                # Download the image
                print("[%] Downloading Image #{} from {}".format(self.download_count, link))

            self.save_image(link, self.output_dir.joinpath("Image_{}.{}".format(
                str(self.download_count), file_type)))
            if self.verbose:
                print("[%] File Downloaded !\n")

        except Exception as e:
            self.download_count -= 1
            print("[!] Issue getting: {}\n[!] Error:: {}".format(link, e))

    
    def run(self):
        while self.download_count < self.limit:
            if self.verbose:
                print('\n\n[!!]Indexing page: {}\n'.format(self.page_counter + 1))
            # Parse the page source and download pics
            request_url = 'https://www.bing.com/images/async?q=' + urllib.parse.quote_plus(self.query) \
                          + '&first=' + str(self.page_counter) + '&count=' + str(self.limit) \
                          + '&adlt=' + self.adult + '&qft=' + self.filters
            request = urllib.request.Request(request_url, None, headers=self.headers)
            response = urllib.request.urlopen(request)
            html = response.read().decode('utf8')
            if html ==  "":
                print("[%] No more images are available")
                break
            links = re.findall('murl&quot;:&quot;(.*?)&quot;', html)
            if self.verbose:
                print("[%] Indexed {} Images on Page {}.".format(len(links), self.page_counter + 1))
                print("\n===============================================\n")

            for link in links:
                if self.download_count < self.limit and link not in self.seen:
                    self.seen.add(link)
                    self.download_image(link)

            self.page_counter += 1
        print("\n\n[%] Done. Downloaded {} images.".format(self.download_count))
