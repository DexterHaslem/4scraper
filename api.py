import requests

_API = "https://a.4cdn.org/"
_CDN = "https://i.4cdn.org/"


def _get(ep):
    r = requests.get(_API + ep)
    return r.json()


def boards():
    return _get("boards.json")


def threads(b):
    return _get(b + "/threads.json")


def catalog(b):
    return _get(b + "/catalog.json")


def posts(b, tn):
    return _get(b + "/thread/" + str(tn) + ".json")['posts']


def download_file(url, path):
    r = requests.get(url, stream=True)
    with open(path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=2048):
            fd.write(chunk)


def get_raw(url):
    r = requests.get(url, stream=True)
    return r.raw


def post_file_url(b, p):
    if 'ext' not in p:
        return ''
    return _CDN + b + "/" + str(p['tim']) + p['ext']
