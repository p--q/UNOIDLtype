#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
from wsgiref.simple_server import make_server
import webbrowser
_resp = '''\
<html>
  <head>
     <title>{0}</title>
   </head>
   <body>
     {1}
   </body>
</html>'''
class Wsgi:
    def __init__(self, title, html):
        self.resp = _resp.format(title, html)
    def app(self, environ, start_response):  # WSGIアプリ。引数はWSGIサーバから渡されるデフォルト引数。
        start_response('200 OK', [ ('Content-type','text/html; charset=utf-8')])  # charset=utf-8'がないと文字化けする時がある
        yield self.resp.encode()  # デフォルトエンコードはutf-8
    def wsgiServer(self): 
        host, port = "localhost", 8080  # サーバが受け付けるポート番号を設定。
        httpd = make_server(host, port, self.app)  # appへの接続を受け付けるWSGIサーバを生成。
        url = "http://localhost:{}".format(port)  # 出力先のurlを取得。
        webbrowser.open_new_tab(url)   # デフォルトブラウザでurlを開く。
        httpd.handle_request()  # リクエストを1回だけ受け付けたらサーバを終了させる
