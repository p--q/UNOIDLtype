#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import officehelper
import traceback
import sys
from com.sun.star.beans import PropertyValue
from contextlib import contextmanager
from functools import partial
class Automation:
    def __init__(self, smgr, services, cls_name):
        from src.pythonpath import component
        self.smgr = smgr
        self.services = services
        self.cls = getattr(component, cls_name)
    def createInstanceWithContext(self, service, ctx):
        if service in self.services:
            return self.cls(ctx)
        else:
            return self.smgr.createInstanceWithContext(service, ctx)
    def createInstanceWithArgumentsAndContext(self, service, args, ctx):
        if service in self.services:
            return self.cls(ctx, args)
        else:
            return self.smgr.createInstanceWithArgumentsAndContext(service, args, ctx)
# funcの前後でOffice接続の処理
@contextmanager
def connectOffice(MODE, services, cls_name, func):
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
        smgr = Automation(smgr, services, cls_name)
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
