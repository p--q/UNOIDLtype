#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import officehelper
import traceback
from functools import wraps
import sys

def connectOffice(func):  # funcの前後でOffice接続の処理
    @wraps(func)
    def connect():  # LibreOfficeをバックグラウンドで起動してコンポーネントテクストとサービスマネジャーを取得する。
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
            pass
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
    return connect 
@connectOffice
def testCode(ctx, smgr):  # 引数はデコレーターで受け取る。
    # src/pythonpathのcomponent.pyファイルをAutomationで実行
    from src.pythonpath import component
    try:
        pycomp = component.ObjInsp(ctx)
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
        pycomp = component.ObjInsp(ctx, ("withArgs",))  # サービス名か実装名でインスタンス化。
        s = pycomp.getInitArgs()
        print(s)
    except:
        traceback.print_exc()
 
if __name__ == "__main__":
    testCode()
    