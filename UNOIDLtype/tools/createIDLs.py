#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
from settings import getDIC, createBK
import os
import glob
def defineIDLs():
    # com.blogspot.pq.UnoInspの定義
    unoinsp = UNOIDL("com.blogspot.pq.UnoInsp")
    unoinsp.include("XUnoInsp")
    unoinsp.super("XUnoInsp")
    yield unoinsp
    # com.blogspot.pq.XUnoInspの定義
    xunoinsp = UNOIDL("com.blogspot.pq.XUnoInsp")
    xunoinsp.include("com.sun.star.uno.XInterface")
    xunoinsp.sub(
        "string stringTypeArg([in] string value)",
        "sequence <string> stringSeqenceTypeArg([in] sequence <string> values)",
        "boolean booleanTypeArg([in] boolean boo)",
        "any anyTypeArg([in] any obj)",
        "sequence <any> getInitArgs()"
        )
    yield xunoinsp
class UNOIDL:
    def __init__(self, name):
        self.name = name
        self.includes = tuple()
        self.subs = tuple() 
        self.super = None
    def include(self, *args):
        self._args(args, "includes")
    def sub(self, *args):   
        self._args(args, "subs")     
    def super(self, super):
        self.super = super
    def _args(self, args, attr):
        if isinstance(args, tuple) and len(args) > 0:
            setattr(self, attr, args)  
            
            
            
def createIDL(DIC=None):
    if DIC is None:
        DIC = getDIC()
    myidl_path = os.path.join(DIC["SRC_PATH"],"idl")  # PyDevプロジェクトのidlフォルダへの絶対パスを取得。
    if not os.path.exists(myidl_path):  # idlフォルダがないとき
        os.mkdir(myidl_path)  # idlフォルダを作成
    os.chdir(myidl_path)  # idlフォルダに移動     
    for f in glob.iglob("*.idl"):
        createBK(f, DIC["BACKUP"])  # 既存のidlファイルを削除。
    for idl in defineIDLs():
        ms = idl.name.split(".")
        b = ms.pop()
        main = "    " 
        main += "interface " if b.startswith("X") else "service "
        if idl.super:
            main += " :  " + idl.super.replace(".", "::")
        with open(b + ".idl", "w", encoding="utf-8") as f:
            lines = list()
            s = "_" + idl.name.replace(".", "_") + "_"  
            lines.append("#ifndef " + s)
            lines.append("#define " + s)
            lines.append("")
            for inc in idl.includes:
                s = inc.replace(".", "/") + ".idl"
                lines.append("#include <" + s + ">")  
            lines.append("")
            
            
            
            
            
            f.write("\n".join(lines))
            
            

#             
#             
#             s = "" 
#             for m in ms:
#                 s += "module " + m + " { "
                
    
    
        

        
        
 
        
if __name__ == "__main__":
    createIDL()        