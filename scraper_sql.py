import api
import os.path
import ntpath
import sys
import mysql.connector
import zlib
import time


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


def _insert(url):
    __, fn = ntpath.split(url)
    # dont send full thing in, just tim
    f, ext = os.path.splitext(fn)

    cnx = mysql.connector.connect(user='rq3', password='eB6rW4RMeV', host='gib.space', database='rq3_fcs')
    cursor = cnx.cursor()

    check_sql = ("select id from reqs where fn = %(fn)s")
    add_entry_sql = ("insert into reqs (fn, fc) values (%s, %s)")
    cursor.execute(check_sql, {'fn': f})
    rows = cursor.fetchall()

    if not rows:  # cursor.rowcount < 1: # returns -1 on no records for some reason
        fc = api.get_raw(url)
        compressed = zlib.compress(fc.data)
        bytesize = sys.getsizeof(compressed)
        megsize = bytesize / (1024 * 1024)
        if megsize < 4:
            try:
                cursor.execute(add_entry_sql, (f, compressed))
                cnx.commit()
                print "uploaded", f + ext
            except mysql.connector.errors.OperationalError as e:
                print "WARN: insert failed - ", e

    cursor.close()
    cnx.close()


def _santize_filter(f):
    if not f:
        return None
    if f[0] != '.':
        return '.' + f
    # maybe consider validating its one of 4chans supported file exts
    return f


def main():
    ac = len(sys.argv)
    if ac < 3:
        print "usage:", sys.argv[0], " <boardname> <page count>"
        print "\t boardname - short board name, eg 'k' for weapons board"
        print "\t page count - how many pages back to download. max is 10, recommend less than 5"
        return

    b = sys.argv[1]
    pc = int(sys.argv[2])
    # ef = _santize_filter(sys.argv[3])
    ef = '.webm'
    urls = get_files(b, pc, ef)

    print "got", len(urls), "files..."

    for url in urls:
        # lot of broken pipe errors.. hmm..
        time.sleep(0.625)
        _insert(url)


if __name__ == "__main__":
    main()
