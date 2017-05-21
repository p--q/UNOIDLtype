#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import officehelper
def connect():  # LibreOfficeをバックグラウンドで起動してコンポネントテクストを取得する。
    ctx = None
    try:
        ctx = officehelper.bootstrap()
        if ctx:
            print("Connected to a running office ...")
        return ctx
    except:
        pass
    return None
ctx = connect()
if ctx:
    smgr = ctx.getServiceManager()
    print("Using remote servicemanager\n")
    if not smgr:
        print( "ERROR: no service manager" )
        
# PyUnoComponentの実行
try:       
    pycomp = smgr.createInstanceWithContext("com.blogspot.pq.UnoInsp", ctx)  # サービス名か実装名でインスタンス化。
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
    pycomp = smgr.createInstanceWithArgumentsAndContext("com.blogspot.pq.UnoInsp", ("withArgs",), ctx)  # サービス名か実装名でインスタンス化。
    s = pycomp.getInitArgs()
    print(s)
except:
    import traceback
    traceback.print_exc()
# except Exception as e:
#     print(e)

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
     