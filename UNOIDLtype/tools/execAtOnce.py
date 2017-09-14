from createIDLs import createIDLs
from createRDB import createRDB
from createXCUs import createXCUs
from createXMLs import createXMLs
from createOXT import createOXT
from deployOXT import deployOXT
from settings import getDIC
if __name__ == '__main__':
    # シェルコマンドのエラーでは止まらないのでログを最初から確認する必要あり。
    DIC = getDIC()
    DIC["BACKUP"] = False
    
#     print("\ncreateIDLs\n")
#     createIDLs(DIC)   
   
#     print("\ncreateRDB\n")
#     createRDB(DIC)
 
#     print("\ncreateXCUs\n")
#     createXCUs(DIC)

#     print("\ncreateXMLs\n")
#     createXMLs(DIC)
    
    print("\ncreateOXT\n")
    createOXT(DIC)
    
    print("\ndeployOXT\n")
    deployOXT(DIC)
    
    print("By running TestPyUnoComponent.py, you can check the operation of the created oxt file.")