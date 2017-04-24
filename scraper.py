import api
import os.path
import ntpath
import argparse

from fuzzywuzzy import fuzz

KEYWORD_LD_RATIO = 85


def _thread_passes(tn, title):
    if not tn:
        return True

    ratio = fuzz.partial_ratio(tn.lower(), title.lower())
    # debug
    # if ratio > KEYWORD_LD_RATIO * 0.8:
    #    print tn, ":", title, "=", ratio
    return ratio >= KEYWORD_LD_RATIO


def get_files(b, pc=3, pf=None, tn=None):
    # use catalog over threads because it has thread info
    t = api.catalog(b)

    recent = [x['threads'] for x in t if x['page'] <= pc]

    threadnos = []

    # todo: refactor
    for xs in recent:
        for st in xs:
            comment = st.get('com', None)
            sub = st.get('sub', None)
            match_comment = comment and _thread_passes(tn, comment)
            match_sub = sub and _thread_passes(tn, sub)
            if match_sub or match_comment:
                print "downloading posts in thread '", sub or comment, "'"
                threadnos.append(st['no'])

    ret = []
    for tn in threadnos:
        posts = api.posts(b, tn)
        file_posts = [p for p in posts if 'ext' in p and (not pf or p['ext'] == pf)]
        links = [api.post_file_url(b, p) for p in file_posts]
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
    parser = argparse.ArgumentParser()
    parser.add_argument("board", help="board shortname, eg 'gif'")
    parser.add_argument("ext", help="file extension to download eg 'webm'")
    parser.add_argument("dir", help="directory to save files to")
    parser.add_argument("--pages", help="number of pages to search, defaults to 5", default=5)
    parser.add_argument("search", help="search term(s) for threads to download", nargs="+")

    args = parser.parse_args()
    ef = _santize_filter(args.ext)
    tn = " ".join(args.search)

    if not os.path.isdir(args.dir):
        print "invalid directory"
        return

    urls = get_files(args.board, args.pages, ef, tn)

    if not urls:
        print "no matching threads found for", tn
        return

    for url in urls:
        _download(url, args.dir)


if __name__ == "__main__":
    main()
