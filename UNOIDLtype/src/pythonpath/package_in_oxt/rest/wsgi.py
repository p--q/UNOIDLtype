from . import resty
from wsgiref.simple_server import make_server
import webbrowser

_resp = '''\
<html>
  <head>
     <title>output</title>
   </head>
   <body>
     <h1>output {arg}!</h1>
   </body>
</html>'''

def wsgiApp1(environ, start_response):
    start_response('200 OK', [ ('Content-type','text/html; charset=utf-8')])
    params = environ['params']
    resp = _resp.format(arg=params.get('arg'))
    yield resp.encode('utf-8')

def wsgiServer(arg):
    dispatcher = resty.PathDispatcher()
    path1 = '/argoutput'
    dispatcher.register('GET', path1, wsgiApp1)
    port = 8080  # サーバが受け付けるポート番号を設定。
    httpd = make_server("", port, dispatcher)  # appへの接続を受け付けるWSGIサーバを生成。
    url = "http://localhost:{}{}?arg={}".format(port, path1, arg)  # 出力先のurlを取得。
#     webbrowser.get('firefox').open_new_tab(url) 
    webbrowser.open_new_tab(url)  # デフォルトのブラウザでurlを開く。
    httpd.handle_request()  # リクエストを1回だけ受け付けたらサーバを終了させる