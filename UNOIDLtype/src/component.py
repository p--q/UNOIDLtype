#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import uno
import unohelper
from com.sun.star.lang import XServiceInfo
from com.sun.star.test import XSomethingB
IMPLE_NAME = "TestComponentB"
SERVICE_NAME = "com.sun.star.test.SomethingB"
class TestComponentB(unohelper.Base, XServiceInfo, XSomethingB):  
    # unohelperを使わない方法はよくわからないので略。
    def __init__(self, ctx, *args):
        self.ctx = ctx
        self.args = args
    # XSomethingB
    def methodTwo(self,val):
        return val + " by Python UNO Component"
    # XServiceInfo
    def getImplementationName(self):
        return IMPLE_NAME
    def supportsService(self, name):
        return name == SERVICE_NAME
    def getSupportedServiceNames(self):
        return (SERVICE_NAME,)
# Registration
g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(TestComponentB, IMPLE_NAME, (SERVICE_NAME,),)
