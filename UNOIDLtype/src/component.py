#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import uno
import unohelper
from com.sun.star.lang import XServiceInfo
from com.blogspot.pq import XUnoInsp
IMPLE_NAME = "UnoInsp"
SERVICE_NAME = "com.blogspot.pq.UnoInsp"
class ObjInsp(unohelper.Base, XServiceInfo, XUnoInsp):  
    def __init__(self, ctx, *args):
        self.ctx = ctx
        self.args = args
    # XUnoInsp
    def stringTypeArg(self,val):  # 文字列を引数にとって文字列を返す。
        return val
    def stringSeqenceTypeArg(self,tp):  # タプルを引数にとってタプルを返す。
        return tp
    def booleanTypeArg(self,boo):  # ブーリアンを引数にとってブーリアンを返す。
        return boo
    def anyTypeArg(self,obj):  # Any型を引数にとって返す。
        return obj
    # XServiceInfo
    def getImplementationName(self):
        return IMPLE_NAME
    def supportsService(self, name):
        return name == SERVICE_NAME
    def getSupportedServiceNames(self):
        return (SERVICE_NAME,)
# Registration
g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(ObjInsp, IMPLE_NAME, (SERVICE_NAME,),)
