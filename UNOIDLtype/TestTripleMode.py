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

def macroMode():
    ctx = XSCRIPTCONTEXT.getComponentContext()
    smgr = ctx.getServiceManager()
    testCode(ctx, smgr)
    
    
    
g_exportedScripts = macroMode,
if __name__ == "__main__":
    from collections import namedtuple
    MODE = None
#     UNOComponent = namedtuple("UNOComponent", "class_name imple_name service_name")
    
    MODE = "Automation"
    #  class_name imple_name service_name
#     objinsp = UNOComponent("ObjInsp", "UnoInsp", "com.blogspot.pq.UnoInsp")

    objinsp = "ObjInsp", "UnoInsp", "com.blogspot.pq.UnoInsp"
    objinsp2 = "ObjInsp2", "UnoInsp2", "com.blogspot.pq.UnoInsp2"
    UNOCompos = objinsp,objinsp2
    
    
    # Class, IMPLEMENTATION_SERVICE_NAME, SERVICE_NAME


#     SERVICE_NAMES = "UnoInsp", "com.blogspot.pq.UnoInsp"
#     UNO_CLASSS = "ObjInsp",
#     from functools import partial
    from helpers.connectoffice import connectOffice
#     connectOffice = partial(connectOffice, MODE)
#     testCode = connectOffice(objinsp)(testCode)
#     testCode()
    
    with connectOffice(MODE, UNOCompos, testCode) as func:
        func()
        
    
    

