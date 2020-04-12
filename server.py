import pafy
import urllib
import re
from pydub import AudioSegment
import os
from multiprocessing import Process
import importlib
from bottle import route,request,response, run, get, post, static_file, hook


download_path = './downloads/'


def Validate(links):
    query_string = urllib.parse.urlencode({"search_query" : links})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    vid = pafy.new("http://www.youtube.com/watch?v=" + search_results[0])
    aud = vid.getbestaudio()
    print(aud)
    aud.download(filepath=download_path)
    return "done"
@route("/", method="GET")
def youtube():
    return '''<form action="/nice" method="post">
 <input name="url" type="text" value=""/>
 <input value="Download" type="submit" /></form>'''
@route("/nice", method = 'POST')
def youtube_accept():
    link = request.forms.get("url")
    a = Process(target=Validate,args=(link,))  # need faster net speed
    a.start()
    a.join()
    s = os.listdir(path=download_path)
    AudioSegment.from_file(download_path+s[0], 'webm').export(download_path+(s[0].split('.')[0]) + '.mp3', format='mp3')
    s = os.listdir(path=download_path)

    print(s)
    @hook('after_request')
    def delFiles():
        for i in s:
            os.remove(download_path+i)

    return static_file(s[0], root=download_path, download=s[0])
def star():
    run()
if __name__ == "__main__":
    b = Process(target=star)
    b.start()
