#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import officehelper
import traceback
from functools import wraps, partial
import sys
from com.sun.star.beans import PropertyValue
from .replacefunc import replaceFunc

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




# funcの前後でOffice接続の処理
def connectOffice(func):
    
    
#     func = replaceFunc(print=replacedPrint)(func)



    @wraps(func)
    def wrapper():  # LibreOfficeをバックグラウンドで起動してコンポーネントテクストとサービスマネジャーを取得する。
        ctx = None
        try:
            ctx = officehelper.bootstrap()  # コンポーネントコンテクストの取得。
        except:
            pass
        if not ctx:
            print("Could not establish a connection with a running office.")
            sys.exit()
        print("Connected to a running office ...")
        smgr = ctx.getServiceManager()  # サービスマネジャーの取得。
        if not smgr:
            print( "ERROR: no service manager" )
            sys.exit()
        print("Using remote servicemanager\n") 
        try:
            func(ctx, smgr)  # 引数の関数の実行。
        except:
            traceback.print_exc()
        # soffice.binの終了処理。これをしないとLibreOfficeを起動できなくなる。
        desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
        prop = PropertyValue(Name="Hidden",Value=True)
        desktop.loadComponentFromURL("private:factory/swriter", "_blank", 0, (prop,))  # バックグラウンドでWriterのドキュメントを開く。
        terminated = desktop.terminate()  # LibreOfficeをデスクトップに展開していない時はエラーになる。
        if terminated:
            print("\nThe Office has been terminated.")  # 未保存のドキュメントがないとき。
        else:
            print("\nThe Office is still running. Someone else prevents termination.")  # 未保存のドキュメントがあってキャンセルボタンが押された時。
    return wrapper