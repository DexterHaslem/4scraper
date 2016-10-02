import requests


def _get(ep):
    r = requests.get("http://a.4cdn.org/" + ep)
    return r.json()


def _boards():
    return _get("boards.json")


def _threads(board):
    return _get(board + "/threads.json")


def _posts(b, tn):
    return _get(b + "/thread/" + str(tn) + ".json")['posts']


def download_file(url, path):
    r = requests.get(url, stream=True)
    with open(path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=2048):
            fd.write(chunk)


def get_raw(url):
    r = requests.get(url, stream=True)
    return r.raw


def _post_file_url(b, p):
    if 'ext' not in p:
        return ''
    return "http://i.4cdn.org/" + b + "/" + str(p['tim']) + p['ext']
