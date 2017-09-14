#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import officehelper
import traceback
import sys
from com.sun.star.beans import PropertyValue
from contextlib import contextmanager
from functools import partial
from src.pythonpath.inoxt import component
class Automation:
    def __init__(self, smgr, UNOCompos):
        self.smgr = smgr
        n = len(UNOCompos)
        self.cls = {UNOCompos[i][j]:UNOCompos[i][0] for i in range(n) for j in range(1, 3)}
    def createInstanceWithContext(self, service, ctx):
        if service in self.cls.keys():
            cls = getattr(component, self.cls[service])
            return cls(ctx)
        else:
            return self.smgr.createInstanceWithContext(service, ctx)
    def createInstanceWithArgumentsAndContext(self, service, args, ctx):
        if service in self.cls.keys():
            cls = getattr(component, self.cls[service])
            return cls(ctx, args)
        else:
            return self.smgr.createInstanceWithArgumentsAndContext(service, args, ctx)
def macroMode(XSCRIPTCONTEXT, UNOCompos, func):
    print("Running in Macro mode\n")
    ctx = XSCRIPTCONTEXT.getComponentContext()
    smgr = Automation(ctx.getServiceManager(), UNOCompos)
    with patch("sys.stdout", new=StringIO()) as fake_out:
        func(ctx, smgr)        
        
        
        
# funcの前後でOffice接続の処理
@contextmanager
def connectOffice(MODE, UNOCompos, func):
    '''
    a context manager to switch between Component mode and Automation mode
    :param MODE:  Running mode
    :type MODE: str
    :param services:  UNO service names generated from the source in the src folder
    :type services: tuple
    :param cls_names: class names to become UNO services
    :type cls_names: tuple
    :param func:  A function to verify the behavior of the source in the src folder
    :type func:  Function
    '''
    if MODE is None:
        MODE="UNOComponent"
    ctx = None
    try:
        ctx = officehelper.bootstrap()  # コンポーネントコンテクストの取得。
    except:
        pass
    if not ctx:
        print("Could not establish a connection with a running office.\n")
        sys.exit()
    print("Connected to a running office ...\n")
    smgr = ctx.getServiceManager()  # サービスマネジャーの取得。
    if MODE == "UNOComponent":
        print("Running in UNOcomponent mode\n")
    elif MODE == "Automation":
        print("Running in Automation mode\n")
        smgr = Automation(smgr, UNOCompos)
    func = partial(func, ctx, smgr)
    try:
        yield func
    except:
        traceback.print_exc()
    # soffice.binの終了処理。これをしないとLibreOfficeを起動できなくなる。
    smgr = ctx.getServiceManager()  # サービスマネジャーの取得。
    desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    prop = PropertyValue(Name="Hidden",Value=True)
    desktop.loadComponentFromURL("private:factory/swriter", "_blank", 0, (prop,))  # バックグラウンドでWriterのドキュメントを開く。
    terminated = desktop.terminate()  # LibreOfficeをデスクトップに展開していない時はエラーになる。
    if terminated:
        print("\nThe Office has been terminated.")  # 未保存のドキュメントがないとき。
    else:
        print("\nThe Office is still running. Someone else prevents termination.")  # 未保存のドキュメントがあってキャンセルボタンが押された時。
