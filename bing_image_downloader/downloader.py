"""
@xvdp 
mods: 
    default output_dir -> '.'
    default adult_filter_off -> False
    added filter args: img_type, color, size, aspect, people
    added runaway search tag: max_pages
    adeed query to folder renaming: remove_tags

    names files as md5_hash(urllink).<extension>
    traces attributions with a dict saved to f"output_dir{/bing_dl.json}"
    keys: md5hash(url_link)
        {"url": url_link, 
         "size": [h, w], 
         "parent": subfolder, 
         "ext": extension, 
         "fullname": relative path to output_dir}

"""
from typing import Optional, Union
import os
import shutil
from pathlib import Path

try:
    from bing import Bing
except ImportError:  # Python 3
    from .bing import Bing


def download(query: str,
             limit: int = 100,
             output_dir: str = '.',
             adult_filter_off: bool = False,
             force_replace: bool = False,
             timeout: int = 60,
             img_type: Optional[str] = None, # filters
             color: Optional[str] = None, # filters
             size: Optional[str] = None,
             aspect: Optional[str] = None,
             people: Optional[str] = None,
             max_pages:  Optional[int] = 50,
             remove_tags: Union[str, tuple, None] = None,
             verbose: bool = True,) -> None:
    """
    Args
        query       (str) any image query
        limit       (int [100]) max images
        output_dir  (str ['.'])
        audlt_filter_off    (bool [False]) # to enable adult images, set to True
        force_replace:      (bool [False]) if True Deletes search folder
        timeaout    (int [60]) seconds. prevent handing

    Args in this fork
        max_pages           int(20) prevent endless loop if not enough unique images found.
            if None, search until 'limit'
        remove_tags   (str, tuple [None]) tags to remove from query in naming folder

     filter args ( replace 'filter' with mostly complete filterning)
        color       None(all) or color, bw, RED, ORANGE, GREEN, YELLOW, TEAL, BLUE,
                                    PURPLE, BROWN, BLACK, GRAY, WHITE
            img_type, size and aspect can either be full name or first initial
        img_type    None(all) or [l]inedrawing, [p]hoto, [c]lipart, [g]if | [a]nimatedgif, [t]ransparent
        size        None(all) [w]allpaper, [l]arge, [m]edium, [s]mall
        aspect      None(all) [s]quare [w]ide [t]all
        people      None(all) [f]face [p]portrait

    Examples:
    >>> from bing_image_downloader.downloader import download
    # downlaods 10, 'w' wallpaper' sized,  'bw' black and white, 'p' photos, 'f' face images, to folder './Claudia_Shiffer
    >>> download("Claudia+Schiffer", **dict(img_type='p', size='w', people='f', color='bw', aspect=None, output_dir=".", limit=10)

    >>> download("AOC+politician", **dict(img_type='p', size='w', people='p', aspect=None, output_dir=".", limit=10, remove_tags='politician'))
    # downlaods 10, 'w' wallpaper' sized, 'p' photos, 'f' face images, to folder './AOC
        """
    # engine = 'bing'
    adult = 'off' if adult_filter_off else 'on'

    folder = folder_name_from_query(query, remove_tags)
    if not folder:
        folder = query
    image_dir = Path(output_dir).joinpath(folder).absolute()

    if force_replace and Path.is_dir(image_dir):
        shutil.rmtree(image_dir)
    os.makedirs(image_dir, exist_ok=True)

    print(f"[%] Downloading Images to {image_dir.absolute()}")
    bing = Bing(query, limit, image_dir, adult, timeout, img_type=img_type, color=color,
                size=size, aspect=aspect, people=people, max_pages=max_pages, verbose=verbose)
    bing.run()


def folder_name_from_query(query, remove_tags: Union[str, tuple, None] = None) -> str:
    """ converts ' ' and '+' to '_'
    removes query tags in 'remove_tags' on folder naming 
    """
    folder = query
    if remove_tags is not None:
        if isinstance(remove_tags, str):
            remove_tags = (remove_tags,)
        for tag in remove_tags:
            folder = folder.replace(tag, '')
    folder =  "_".join(folder.replace("+", " ").split())
    folder = folder.rstrip().lstrip()
    return folder


if __name__ == '__main__':
    download('dog', output_dir="cat", limit=10, timeout=1)
