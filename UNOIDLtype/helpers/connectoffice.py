#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import officehelper
import traceback
import sys
from com.sun.star.beans import PropertyValue
from .replacefunc import replaceFunc
from contextlib import contextmanager
from functools import partial

def replacedPrint(arg):
    print("置換された関数で出力 {}".format(arg))

# def unoComponent(ctx, smgr, UNOIDL, args=None):  # 拡張機能で定義したUNOIDLのインスタンスを返す。
# #     print("\nRunning in UNO Component mode\n")
#     return smgr.createInstanceWithContext(UNOIDL, ctx) if args is None else smgr.createInstanceWithArgumentsAndContext(UNOIDL, args, ctx)    
# def automation(ctx, smgr, unoidl_class, args=None):  # src/pythonpathのcomponent.pyファイルのUNOComponentのインスタンスとなるべきクラスのインスタンスを返す。
# #     print("Running in Automation mode\n")
#     from src.pythonpath import component
#     cls = getattr(component, unoidl_class)
#     return cls(ctx) if args is None else cls(ctx, args)


def automation():
    from src.pythonpath import component
    pass


# funcの前後でOffice接続の処理
@contextmanager
def connectOffice(MODE, func):
    
    if MODE == "Automation":
        print("Running in Automation mode\n")
        kwargs = {
            "smgr.createInstanceWithContext": "automation",
            "smgr.createInstanceWithArgumentsAndContext": "automation"
        }
        
        func = replaceFunc(**kwargs)(func, debug=True)
    
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
