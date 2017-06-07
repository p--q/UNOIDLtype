#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import unohelper
from com.sun.star.lang import XServiceInfo
from com.blogspot.pq import XUnoInsp
from pythonpath.package_in_oxt.rest.output import invokeRest
IMPLE_NAME = None
SERVICE_NAME = None
def create(ctx, *args, imple_name, service_name):
    global IMPLE_NAME
    global SERVICE_NAME
    if IMPLE_NAME is None:
        IMPLE_NAME = imple_name 
    if SERVICE_NAME is None:
        SERVICE_NAME = service_name
    return ObjInsp(ctx, *args)

# _hello_resp = '''\
# <html>
#   <head>
#      <title>Hello {name}</title>
#    </head>
#    <body>
#      <h1>Hello {name}!</h1>
#    </body>
# </html>'''
# 
# def getTxt(environ, start_response):
#     start_response('200 OK', [ ('Content-type','text/html')])
#     params = environ['params']
#     resp = _hello_resp.format(name=params.get('name'))
#     yield resp.encode('utf-8')



class ObjInsp(unohelper.Base, XServiceInfo, XUnoInsp):  
    def __init__(self, ctx, *args):
        self.ctx = ctx
        self.args = args  # 引数がないときもNoneではなくタプルが入る。
    # XUnoInsp
    def stringTypeArg(self,val):  # 文字列を引数にとって文字列を返す。
        return val
    def stringSeqenceTypeArg(self,tp):  # タプルを引数にとってタプルを返す。
        return tp
    def booleanTypeArg(self,boo):  # ブーリアンを引数にとってブーリアンを返す。
        return boo
    def anyTypeArg(self,obj):  # Any型を引数にとって返す。
        return obj
    def getInitArgs(self):  # createInstanceWithArgumentsAndContext()で取得した引数（タプル)を返す。
        return self.args
    def invokeWebbrowser(self, txt):
        
        from .rest import output
        output.invokeRest(txt)
#         from .rest import resty
#         from wsgiref.simple_server import make_server
#         import webbrowser
#         dispatcher = resty.PathDispatcher()
#         path = '/txt'
#         dispatcher.register('GET', path, getTxt)
#         port = 8080  # サーバが受け付けるポート番号を設定。
#         httpd = make_server("", port, dispatcher)  # appへの接続を受け付けるWSGIサーバを生成。
#         url = "http://localhost:{}{}?name={}".format(port, path, txt)  # 出力先のurlを取得。
#         webbrowser.open_new_tab(url)  # デフォルトのブラウザでurlを開く。
#         httpd.handle_request()  # リクエストを1回だけ受け付けたらサーバを終了させる
    # XServiceInfo
    def getImplementationName(self):
        return IMPLE_NAME
    def supportsService(self, name):
        return name == SERVICE_NAME
    def getSupportedServiceNames(self):
        return (SERVICE_NAME,)
