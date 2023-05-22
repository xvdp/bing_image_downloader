import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bing_image_downloader",
    version="1.2.0",
    author="Guru Prasad Singh_forked",
    author_email="g.gaurav541@gmail.com_forked",
    description="Python library to download bulk images from Bing.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gurugaurav/bing_image_downloader",
    keywords=['bing', 'images', 'scraping', 'image download', 'bulk image downloader',],
    packages=['bing_image_downloader'],
    classifiers=[
	"Programming Language :: Python :: 3",
	"License :: OSI Approved :: MIT License",
	"Operating System :: OS Independent",
        ]
)
