import json, sys, time, urllib.request, urllib.parse
UA = {"User-Agent": "FrescuraVideoEdit/1.0 (https://github.com/affan57-57/Video-claude-; video editing, CC-licensed media)"}
def get(url, tries=5):
    for k in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(10 * (k + 1)); continue
            raise
    raise SystemExit("gave up " + url)
def info(titles, width):
    q = {"action": "query", "prop": "imageinfo", "iiprop": "url|size|mime|extmetadata", "iiurlwidth": str(width), "format": "json",
         "titles": "|".join("File:" + t for t in titles)}
    return json.loads(get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(q)))["query"]["pages"].values()
if __name__ == "__main__":
    width = int(sys.argv[1]); pairs = [a.split("=", 1) for a in sys.argv[2:]]
    for p in info([t for _, t in pairs], width):
        ii = p["imageinfo"][0]; name = dict((t, n) for n, t in pairs)[p["title"][5:]]
        url = ii["url"] if ii["mime"].startswith("video") else ii["thumburl"]
        open(name, "wb").write(get(url)); print("ok", name, ii["mime"], flush=True); time.sleep(3)
