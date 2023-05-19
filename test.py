import sys
from bing_image_downloader import downloader

query=sys.argv[1]

    
            
downloader.download(
    query,
    limit=10,
    output_dir="dataset",
    adult_filter_off=True,
    force_replace=False,
    timeout=60,
    verbose=True,
)

