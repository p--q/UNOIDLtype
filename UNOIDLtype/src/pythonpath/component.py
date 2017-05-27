#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import unohelper
from com.sun.star.lang import XServiceInfo
from com.blogspot.pq import XUnoInsp
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
    # XServiceInfo
    def getImplementationName(self):
        return IMPLE_NAME
    def supportsService(self, name):
        return name == SERVICE_NAME
    def getSupportedServiceNames(self):
        return (SERVICE_NAME,)
