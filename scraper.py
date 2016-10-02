import api
import os.path
import ntpath
import sys
from os import getcwd


def get_files(b, pc=3, pf=None):
    t = api._threads(b)

    recent = [x['threads'] for x in t if x['page'] <= pc]

    threadnos = []

    # todo: refactor
    for xs in recent:
        for st in xs:
            threadnos.append(st['no'])

    ret = []
    for tn in threadnos:
        posts = api._posts(b, tn)
        file_posts = [p for p in posts if 'ext' in p and (not pf or p['ext'] == pf)]
        links = [api._post_file_url(b, p) for p in file_posts]
        for link in links:
            ret.append(link)

    return ret


def _download(url, dest):
    try:
        __, fn = ntpath.split(url)
        fp = os.path.join(dest, fn)
        if not os.path.isfile(fp):
            api.download_file(url, fp)
    except IOError as ioe:
        print "failed to download", url, ioe


def _santize_filter(f):
    if not f:
        return None
    if f[0] != '.':
        return '.' + f
    # maybe consider validating its one of 4chans supported file exts
    return f


def main():
    ac = len(sys.argv)
    if ac < 2:
        print "usage:", sys.argv[0], " <boardname - required> <page count> <ext filter>"
        print "\t boardname - short board name, eg 'k' for weapons board"
        print "\t page count - how many pages back to download. default is 2"
        print "\t ext filter - which file types to download, eg '.webm'. defaults to all"
        return

    pc = 2
    ef = None
    b = sys.argv[1]

    if ac > 2:
        pc = int(sys.argv[2])
    if ac > 3:
        ef = _santize_filter(sys.argv[3])

    urls = get_files(b, pc, ef)
    for url in urls:
        _download(url, getcwd())

if __name__ == "__main__":
    main()
