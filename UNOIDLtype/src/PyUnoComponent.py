#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
IMPLE_NAME = "UnoInsp"
SERVICE_NAME = "com.blogspot.pq.UnoInsp"
def create(ctx, *args):    
    
    import component
#     return component.create(IMPLE_NAME, SERVICE_NAME, ctx, *args)
    return component.create(IMPLE_NAME, ctx, *args)




# Registration
import unohelper
g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(create, IMPLE_NAME, (SERVICE_NAME,),)
