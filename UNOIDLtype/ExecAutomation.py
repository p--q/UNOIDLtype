#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import officehelper
import traceback
from functools import wraps, partial
import sys
MODE = "Automation"  # 実行モードの選択。マクロモードでもAutomationモードを使う。
UNOIDL = "ObjInsp"  # UNOIDLにしているクラス名。
# MODE = "UNOComponent"
# UNOIDL = "com.blogspot.pq.UnoInsp"
# UNOオブジェクトのインスタンス化はgetUNOComponent[MODE](UNOIDL, args)で行う。argsはタプル。
def testCode(ctx, smgr):  # 引数はデコレーターで受け取る。ctx:サービスマネジャー、smgr: サービスマネジャー
    try:
        pycomp = getUNOComponent[MODE](UNOIDL)
        s = pycomp.stringTypeArg("文字列を渡しました。")
        print(s)
        s = pycomp.stringSeqenceTypeArg(("文字列のタプルを渡しました",))
        print(s)
        s = pycomp.booleanTypeArg(True)
        if s:
            print("Trueが渡されました。")
        else:
            print("Falseが渡されました。")
        s = pycomp.anyTypeArg(smgr)
        print(s)  
        s = pycomp.anyTypeArg("Any型に文字列を渡す")
        print(s)    
    except:
        traceback.print_exc()
        
    try:
        pycomp = getUNOComponent[MODE](UNOIDL, ("withArgs",))
        s = pycomp.getInitArgs()
        print(s)
    except:
        traceback.print_exc()
 
def unoComponent(ctx, smgr, UNOIDL, args=None):  # 拡張機能で定義したUNOIDLのインスタンスを返す。
    print("Running in UNO Component mode\n")
    return smgr.createInstanceWithContext(UNOIDL, ctx) if args is None else smgr.createInstanceWithArgumentsAndContext(UNOIDL, args, ctx)    
def automation(ctx, smgr, unoidl_class, args=None):  # src/pythonpathのcomponent.pyファイルのUNOComponentのインスタンスとなるべきクラスのインスタンスを返す。
    print("Running in Automation mode\n")
    from src.pythonpath import component
    cls = getattr(component, unoidl_class)
    return cls(ctx) if args is None else cls(ctx, args)
# マクロモード用
def printToList(ctx, smgr, prt=None):
    def decorate(func):
        @wraps(func)
        def wrapper():
            print = lambda x: prt.append(x)
            func(ctx, smgr)
        return wrapper
    return decorate
    


def execAsMacro():  # マクロモードで呼び出す関数。
    getUNOComponent = {"Automation": automation}  # マクロモードとオートメーションは同じ。
    prt = ["Running in Macro mode"]
    ctx = XSCRIPTCONTEXT.getComponentContext()
    smgr = ctx.getServiceManager()
    
#     import inspect
#     srclines = inspect.getsource(testCode).splitlines()
    
#     prt.append("\n".join(srclines))

    wrapped = printToList(ctx, smgr, prt)(testCode)
    wrapped()
#     def appendOutput(item):
#         output.append(item)


    
#     ctx = XSCRIPTCONTEXT.getComponentContext()
#     smgr = ctx.getServiceManager()



     
     
#     testCode(ctx, smgr) 
    desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    doc = desktop.loadComponentFromURL("private:factory/swriter", "_blank", 0, ())
    doc.getText().setString("\n".join(prt))
# funcの前後でOffice接続の処理
def connectOffice(func):
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
        getUNOComponent[MODE] = partial(getUNOComponent[MODE], ctx, smgr)  # unoComponentに先にctxとsmgrを渡しておく
        try:
            func(ctx, smgr)  # 引数の関数の実行。
        except:
            traceback.print_exc()
        # soffice.binの終了処理。これをしないとLibreOfficeを起動できなくなる。
        desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
        from com.sun.star.beans import PropertyValue
        prop = PropertyValue(Name="Hidden",Value=True)
        desktop.loadComponentFromURL("private:factory/swriter", "_blank", 0, (prop,))  # バックグラウンドでWriterのドキュメントを開く。
        terminated = desktop.terminate()  # LibreOfficeをデスクトップに展開していない時はエラーになる。
        if terminated:
            print("\nThe Office has been terminated.")  # 未保存のドキュメントがないとき。
        else:
            print("\nThe Office is still running. Someone else prevents termination.")  # 未保存のドキュメントがあってキャンセルボタンが押された時。
    return wrapper
g_exportedScripts = execAsMacro,  # マクロセレクターに表示させる関数を提示。
getUNOComponent = {
    "Automation": automation,
    "UNOComponent": unoComponent
    }
if __name__ == "__main__":
    testCode = connectOffice(testCode)
    testCode()
    