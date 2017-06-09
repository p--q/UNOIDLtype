#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import unohelper
from com.sun.star.lang import XServiceInfo
from com.blogspot.pq import XToWebHtml
from . import wsgi 
IMPLE_NAME = None
SERVICE_NAME = None
def create(ctx, *args, imple_name, service_name):
    global IMPLE_NAME
    global SERVICE_NAME
    if IMPLE_NAME is None:
        IMPLE_NAME = imple_name 
    if SERVICE_NAME is None:
        SERVICE_NAME = service_name
    return ToWebHtml(ctx, *args)
class ToWebHtml(unohelper.Base, XServiceInfo, XToWebHtml):  
    def __init__(self, ctx, *args):
        self.ctx = ctx
        self.args = args  # 引数がないときもNoneではなくタプルが入る。未使用。
        self.title = ""
    # XToWebHtml
    def openInBrowser(self, html):
        server = wsgi.Wsgi(self.title, html)
        server.wsgiServer()
    def setTitle(self, title):
        self.title = title
    # XServiceInfo
    def getImplementationName(self):
        return IMPLE_NAME
    def supportsService(self, name):
        return name == SERVICE_NAME
    def getSupportedServiceNames(self):
        return (SERVICE_NAME,)
