## 4scraper

### About
this is a simple utility to download all files from a 4chan thread.


### usage
>$ python scraper.py -h

    usage: scraper.py [-h] [--pages PAGES] board ext dir search [search ...]

    positional arguments:
      board          board shortname, eg 'gif'
      ext            file extension to download eg 'webm'
      dir            directory to save files to
      search         search term(s) for threads to download

    optional arguments:
      -h, --help     show this help message and exit
      --pages PAGES  number of pages to search, defaults to 5


examples:

download all webm from any threads in 'ck' matching the title/subject of 'pizza' into a folder called 'savedwebm':
> $ python scraper.py ck webm savedwebm pizza

