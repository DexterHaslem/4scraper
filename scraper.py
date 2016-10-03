import api
import os.path
import ntpath
import sys

from fuzzywuzzy import fuzz

KEYWORD_LD_RATIO = 50


def _thread_passes(tn, title):
    if not tn:
        return True

    ratio = fuzz.ratio(tn, title)

    if ratio > KEYWORD_LD_RATIO * 0.5:
        print tn, ":", title, "=", ratio

    return ratio >= KEYWORD_LD_RATIO * 0.75
    # for kw in kws:
    #     ratio = fuzz.token_set_ratio(title, kw)
    #     if ratio > KEYWORD_LD_RATIO:
    #         return True


def get_files(b, pc=3, pf=None, tn=None):
    # use catalog over threads because it has thread info
    # t = api._threads(b)
    t = api._catalog(b)

    recent = [x['threads'] for x in t if x['page'] <= pc]

    threadnos = []

    # todo: refactor
    for xs in recent:
        for st in xs:
            title = st.get('com', None)
            if title and _thread_passes(tn, title):
                print "downloading posts in thread '", title, "' due to match"
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
    if ac < 5:
        print "usage:", sys.argv[0], " <boardname - required> <page count> <ext filter> <dest dir> <thread search>"
        print "\t boardname - short board name, eg 'k' for weapons board"
        print "\t page count - how many pages back to download. max is 10, recommend less than 5"
        print "\t ext filter - which file types to download, eg '.webm'. defaults to all"
        print "\t destdir - destination directory to download files"
        print "\t thread name - optional thread title to try to include threads by"
        return

    b = sys.argv[1]
    pc = int(sys.argv[2])
    ef = _santize_filter(sys.argv[3])
    dest = sys.argv[4]
    tn = None
    if ac > 4:
        tn = " ".join(sys.argv[5:])

    if not os.path.isdir(dest):
        print "invalid directory"
        return

    urls = get_files(b, pc, ef, tn)
    for url in urls:
        _download(url, dest)


if __name__ == "__main__":
    main()
