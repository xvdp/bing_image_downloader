'''
Python api to download image form Bing.
Author: Guru Prasad (g.gaurav541@gmail.com)

@xvdp mod: added filters
added attribution json file, containing name:link
minor linting
'''
import warnings
import time
from typing import Optional, Union
import os.path as osp
import urllib
import urllib.request
import re
import imghdr
import posixpath
from pathlib import Path
import hashlib
import json
from PIL import Image


def md5(data):
    m = hashlib.md5()
    if isinstance(data, str):
        m.update(data.encode())
    else:
        m.update(data)
    return m.hexdigest()

class Bing:
    def __init__(self,
                 query: str,
                 limit: int,
                 output_dir: Union[Path, str],
                 adult: str,
                 timeout: int,
                 *,
                 img_type: Optional[str] = None, # filters
                 color: Optional[str] = None, # filters
                 size: Optional[str] = None, # filters
                 aspect: Optional[str] = None, # filters
                 people: Optional[str] = None, # filters
                 max_pages: Optional[int] = 50, 
                 verbose: bool = True) -> None:
        """
        query       (str)  any image query
        limit       (int)  max images
        output_dir  (str)
        adult       (str) 'off | on
        timeaout    (int) seconds. prevent handing

        keyword args: added u firj fork
            max_pages   int(20) prevent endless loop if not enough unique images found.

          filter args ( replace 'filter' with mostly complete filterning)
            color       None(all) or color, bw, RED, ORANGE, GREEN, YELLOW, TEAL, BLUE,
                                        PURPLE, BROWN, BLACK, GRAY, WHITE
                img_type, size and aspect can either be full name or first initial
            img_type    None(all) or [l]inedrawing, [p]hoto, [c]lipart, [g]if | [a]nimatedgif, [t]ransparent
            size        None(all) [w]allpaper, [l]arge, [m]edium, [s]mall
            aspect      None(all) [s]quare [w]ide [t]all
            people      None(all) [f]face [p]portrait


            

        """
        assert isinstance(limit, int), f"limit must be integer, got {limit}"
        assert isinstance(timeout, int), f"timeout must be integer, got {timeout}"

        self.download_count = 0
        self.query = query
        self.output_dir = output_dir if isinstance(output_dir, Path) else Path(output_dir)
        self.adult = adult
        self.verbose = verbose
        self.seen = set()
        self.limit = limit
        self.timeout = timeout
        self.max_pages = max_pages

        self.filters = self.get_filters(img_type, color, size, aspect, people)
        self.atribution_fname = osp.join(osp.dirname(output_dir), "bing_dl.json")
        self.attribution = {}

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
        """ most standard bing image filters"""
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
            _s = size.lower()[0]
            if _s in _sizes:
                out += f"+filterui:imagesize-{_sizes[_s]}"
            else:
                warnings.warn(f"ignoring, image size: {size} not found in {_sizes.values()}")
        if aspect is not None:
            _aspects = {'s':'square', 'w':'wide', 't':'tall'}
            _a = aspect.lower()[0]
            if _a in _aspects:
                out += f"+filterui:aspect-{_aspects[_a]}"
        if people is not None:
            _peoples = {'p':'portrait', 'f':'face'}
            _p = people.lower()[0]
            if _p in _peoples:
                out += f"+filterui:face-{_peoples[_p]}"
        return out


    def add_atribution(self, link, filepath, size):
        """ @xvdp basic traceability info relating the saved file to url
        TODO: change naming &  to :
        
        """
        # {'url': url, 'size': im.size, 'parent': new_folder, ext: ext, 'fullname': osp.join(new_folder, new_key+ext)}
        if osp.isfile(self.atribution_fname):
            with open(self.atribution_fname, 'r', encoding='utf8') as _fi:
                self.attribution = json.load(_fi)
        # self.attribution[name] = link

        parent, name  = osp.split(filepath)
        name, ext = osp.splitext(name)

        self.attribution[name] = {'url': link, 'size':size, 'parent': parent, 'ext': ext, 'fullname': filepath}
        with open(self.atribution_fname, 'w', encoding='utf8') as _fi:
            json.dump(self.attribution, _fi)


    def save_image(self, link, file_path):
        """ @xvdp added dict storing name:url
        """
        request = urllib.request.Request(link, None, self.headers)
        image = urllib.request.urlopen(request, timeout=self.timeout).read()
        if not imghdr.what(None, image):
            raise ValueError(f'   Invalid image, not saving {link}')
        with open(file_path, 'wb') as _f:
            _f.write(image)


    def download_image(self, link):
        """ downloader
            xvdp - changed naming scheme to name_{mdhash(link)}
        """
        self.download_count += 1
        # Get the image link
        try:
            path = urllib.parse.urlsplit(link).path
            filename = posixpath.basename(path).split('?')[0]
            name, file_type = osp.splitext(osp.basename(filename))
            if file_type.lower() not in ["jpe", "jpeg", "jfif", "exif", "tiff",
                                         "gif", "bmp", "png", "webp", "jpg"]:
                file_type = "jpg"

            # file_path =  str(self.output_dir.joinpath(f"{name}_{md5(link)}.{file_type}"))
            file_path =  str(self.output_dir.joinpath(f"{md5(link)}.{file_type}"))
            self.save_image(link, file_path)
            size = Image.open(file_path).size
            name =  osp.join(osp.basename(self.output_dir), f"{md5(link)}.{file_type}")

            self.add_atribution(link, name, size)
            if self.verbose:
                print(f"    Downloaded: {link} -> {name}" )

        except Exception as _e:
            self.download_count -= 1
            print(f"[!] Issue getting: {link}\n[!] Error:: {_e}")


    def run(self):
        _errors = 0
        _max_errors = 20
        while self.download_count < self.limit and self.page_counter < self.max_pages:
            # Parse the page source and download pics
            request_url = 'https://www.bing.com/images/async?q=' + urllib.parse.quote_plus(self.query) \
                          + '&first=' + str(self.page_counter) + '&count=' + str(self.limit) \
                          + '&adlt=' + self.adult + '&qft=' + self.filters
            try:
                request = urllib.request.Request(request_url, None, headers=self.headers)
                response = urllib.request.urlopen(request)
                if response.status == 200:
                    html = response.read().decode('utf8')
                    if html ==  "":
                        print(f"[%] No more images are available {request_url}")
                        break
                    links = re.findall('murl&quot;:&quot;(.*?)&quot;', html)
                    if self.verbose:
                        print(f"[%] Indexed {len(links)} Images on Page {self.page_counter + 1}")

                    for link in links:
                        if self.download_count < self.limit and link not in self.seen:
                            self.seen.add(link)
                            self.download_image(link)

                    self.page_counter += 1
                else:
                    print(f" url status: {response.status}, {response.reason}, {request_url}")
                    break
            except Exception as _e:
                print(f"url request Exception {_e} request{request_url }\n response {response.status} {request_url}")
                _errors += 1
                time.sleep(1)
                if _errors >= _max_errors:
                    print("\nmax-errors 5, sleeping 4 seconds...\n")
                    time.sleep(4)
                    break
        search = request_url.split('q=')[1].replace('&', ' ').replace('filterui:', ' ').replace('qft=+', 'filters:').replace('+', ',')
        print(f"[%] Done. Downloaded {self.download_count} images: {search}")


