"""
@xvdp added filter args
mod default output_dir
"""
from typing import Optional
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
             adult_filter_off: bool = True,
             force_replace: bool = False,
             timeout: int = 60,
             img_type: Optional[str] = None, # filters
             color: Optional[str] = None, # filters
             size: Optional[str] = None,
             aspect: Optional[str] = None,
             people: Optional[str] = None,
             verbose: bool = True) -> None:
    """
    filter args:
        color       None(all) or color, bw, RED, ORANGE, GREEN, YELLOW, TEAL, BLUE,
                                    PURPLE, BROWN, BLACK, GRAY, WHITE
            img_type, size and aspect can either be full name or first initial
        img_type    None(all) or [l]inedrawing, [p]hoto, [c]lipart, [g]if | [a]nimatedgif, [t]ransparent
        size        None(all) [w]allpaper, [l]arge, [m]edium, [s]mall
        aspect      None(all) [s]quare [w]ide [t]all
        people      None(all) [f]face [p]portrait

        """
    # engine = 'bing'
    adult = 'off' if adult_filter_off else 'on'

    image_dir = Path(output_dir).joinpath(query).absolute()

    if force_replace and Path.is_dir(image_dir):
        shutil.rmtree(image_dir)
    os.makedirs(image_dir, exist_ok=True)

    print(f"[%] Downloading Images to {image_dir.absolute()}")
    bing = Bing(query, limit, image_dir, adult, timeout, img_type, color,
                size, aspect, people, verbose)
    bing.run()


if __name__ == '__main__':
    download('dog', output_dir="cat", limit=10, timeout=1)
