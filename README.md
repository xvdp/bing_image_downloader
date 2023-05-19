![GitHub top language](https://img.shields.io/github/languages/top/gurugaurav/bing_image_downloader)
![GitHub](https://img.shields.io/github/license/gurugaurav/bing_image_downloader)
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fgurugaurav%2Fbing_image_downloader&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)
## Bing Image Downloader
<hr>

Python library to download bulk of images form Bing.com.
This package uses async url, which makes it very fast while downloading.<br/>


### Disclaimer<br />

This program lets you download tons of images from Bing.
Please do not download or use any image that violates its copyright terms. 

### Installation <br />
```sh
pip install bing-image-downloader
```

or 
```bash
git clone https://github.com/gurugaurav/bing_image_downloader
cd bing_image_downloader
pip install .
```



### Usage <br />
```python
from bing_image_downloader import downloader
downloader.download(query_string, limit=100,  output_dir='dataset', adult_filter_off=True, force_replace=False, timeout=60, verbose=True)
downloader.download(query_string, limit=100,  output_dir='.', size='w') # dowloads large images 'wallpaper
downloader.download(query_string, limit=100,  output_dir='.', color='bw') # only grayscale images
downloader.download(query_string, limit=100,  output_dir='.', aspect='square') # square images
downloader.download(query_string, limit=100,  output_dir='.', img_type='photo') # photographs
downloader.download(query_string, limit=100,  output_dir='.', people='face') # faces only
```

`query_string` : String to be searched.<br />
`limit` : (optional, default is 100) Number of images to download.<br />
`output_dir` : (optional, default is 'dataset') Name of output dir.<br />
`adult_filter_off` : (optional, default is True) Enable of disable adult filteration.<br />
`force_replace` : (optional, default is False) Delete folder if present and start a fresh download.<br />
`timeout` : (optional, default is 60) timeout for connection in seconds<br />
Filter args: replaces `filter` arg which only affected image type with more filters @xvdp added. not include in original repo<br />
`color`:       None(all) or color, bw, RED, ORANGE, GREEN, YELLOW, TEAL, BLUE, PURPLE, BROWN, BLACK, GRAY, WHITE<br />
`img_type`:    None(all) or [l]inedrawing, [p]hoto, [c]lipart, [g]if | [a]nimatedgif, [t]ransparent # can either be full name or first initial<br />
`size`:        None(all) [w]allpaper, [l]arge, [m]edium, [s]mall # can either be full name or first initial<br />
`people`:      None(all) [p]ortrait, [f]ace  # can either be full name or first initial<br />
`aspect`:      None(all) [s]quare [w]ide [t]all # can either be full name or first initial<br />
`verbose` : (optional, default is True) Enable downloaded message.<br />


You can also test the programm by runnning `test.py keyword`


### PyPi <br />
https://pypi.org/project/bing-image-downloader/

###note: pypi version does not contain the extended filters 'color, size, aspect, img_type' @xvdp



</br>

### Donate
You can buy me a coffee if this project was helpful to you.</br>

[<img src="https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-1.svg" alt="Show your support" width="180"/>](https://www.buymeacoffee.com/gurugaurav)
  



