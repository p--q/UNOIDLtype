#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import traceback
def testCode(ctx, smgr):  # 引数はデコレーターで受け取る。ctx:サービスマネジャー、smgr: サービスマネジャー

    try:
        pycomp = smgr.createInstanceWithContext("UnoInsp", ctx)  # サービス名か実装名でインスタンス化。
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

objinsp = "ObjInsp", "UnoInsp", "com.blogspot.pq.UnoInsp"
UNOCompos = objinsp,
func = testCode

from helpers.connectoffice import connectOffice, macroMode
def macro():
    macroMode(XSCRIPTCONTEXT, UNOCompos, func)
g_exportedScripts = macro,
MODE = None
if __name__ == "__main__":
    MODE = "Automation"
    from helpers.connectoffice import connectOffice
    with connectOffice(MODE, UNOCompos, func) as fn:
        fn()
