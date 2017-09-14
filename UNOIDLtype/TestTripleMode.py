#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import traceback
def testCode(ctx, smgr):  # 引数はデコレーターで受け取る。ctx:サービスマネジャー、smgr: サービスマネジャー


    try:
        pycomp = smgr.createInstanceWithContext("pq.UnoInsp", ctx)  # サービス名か実装名でインスタンス化。
        s = pycomp.stringTypeArg("文字列を渡しました。")
        print(s)
        s = pycomp.stringSeqenceTypeArg(("文字列のタプルを渡しました",))
        print(s)
        s = pycomp.booleanTypeArg(True)
        if s:
            print("Trueが渡されました。")
        else:
            print("Falseが渡されました。")
        s = pycomp.anyTypeArg(ctx)
        print(s)  
        s = pycomp.anyTypeArg("Any型に文字列を渡す")
        print(s)    
    except:
        traceback.print_exc()
            
    try:
        pycomp = smgr.createInstanceWithArgumentsAndContext("com.blogspot.pq.UnoInsp", ("withArgs",), ctx)  # サービス名か実装名でインスタンス化。
        s = pycomp.getInitArgs()
        print(s)
    except:
        traceback.print_exc()


# Service information to be instantiated instead of UNO component when in automation mode
# Class name, Implementation name, Service name
objinsp = "ObjInsp", "UnoInsp", "com.blogspot.pq.UnoInsp"
# Tuple of replacement service information
UNOCompos = objinsp,
# Function for test the source
func = testCode

# Function to call from macro
def macro():
    ctx = XSCRIPTCONTEXT.getComponentContext()
    smgr = ctx.getServiceManager()
    from unittest.mock import patch
    from io import StringIO
    with patch("sys.stdout", new=StringIO()) as fake_out:  # 標準出力をリダイレクト。
        func(ctx, smgr)
    page = smgr.createInstanceWithContext("pq.ToWebHtml", ctx)
    page.setTitle("From Macro")
    page.openInBrowser(fake_out.getvalue().replace("\n", "</br>"))
g_exportedScripts = macro,
MODE = None
if __name__ == "__main__":
    MODE = "Automation"
    from helpers.connectoffice import connectOffice
    with connectOffice(MODE, UNOCompos, func) as fn:
        fn()
