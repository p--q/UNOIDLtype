from . import resty
from wsgiref.simple_server import make_server
import webbrowser

_resp = '''\
<html>
  <head>
     <title>Hello {name}</title>
   </head>
   <body>
     <h1>Hello {name}!</h1>
   </body>
</html>'''

def getTxt(environ, start_response):
    start_response('200 OK', [ ('Content-type','text/html')])
    params = environ['params']
    resp = _resp.format(name=params.get('name'))
    yield resp.encode('utf-8')

def invokeRest(val):
    dispatcher = resty.PathDispatcher()
    path = '/txt'
    dispatcher.register('GET', path, getTxt)
    port = 8080  # サーバが受け付けるポート番号を設定。
    httpd = make_server("", port, dispatcher)  # appへの接続を受け付けるWSGIサーバを生成。
    url = "http://localhost:{}{}?name={}".format(port, path, val)  # 出力先のurlを取得。
    webbrowser.open_new_tab(url)  # デフォルトのブラウザでurlを開く。
    httpd.handle_request()  # リクエストを1回だけ受け付けたらサーバを終了させる