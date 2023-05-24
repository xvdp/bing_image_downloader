"""
@xvdp mods:
    added versioning : >>> bing_image_downloader.__version__
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
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

def _set_version(name, version):
    with open(f'{name}/version.py', 'w', encoding='utf8') as _fi:
        _fi.write("__version__='"+version+"'")
    return version

def setup_package():
    name="bing_image_downloader"
    metadata = dict(
        name=name,
        version=_set_version(name, version='1.3'),
        author="Guru Prasad Singh_forked xvdp",
        author_email="g.gaurav541@gmail.com_forked",
        description="Python library to download bulk images from Bing.com",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/xvdp/bing_image_downloader",
        keywords=['bing', 'images', 'scraping', 'image download', 'bulk image downloader',],
        packages=['bing_image_downloader'],
        classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
            ]
    )

    setup(**metadata)

if __name__ == '__main__':
    setup_package()
