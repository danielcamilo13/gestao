import os,sys,re
global AdminApp, AdminConfig, AdminControl
def view():
    apps = AdminApp.list().split()
    for app in apps:
        libraries = AdminApp.view(app,'[ -MapSharedLibForMod[[]]]')
        initparams = AdminApp.view(app,'[ -MapInitParamForServlet[[]]]')
        modules = AdminApp.view(app,'-MapModulesToServers')
        arqsys.write('#'*40+'\n')
        arqsys.write('Aplicacao %s\n'%app)
        arqsys.write('Bibliotecas %s\n'%libraries)
        arqsys.write('Parametros de inicializacao %s\n'%initparams)
        arqsys.write('Modulos nesta aplicacao %s\n'%modules)
        
arqsys = open('SystemExit.log','w')
view()
arqsys.close()