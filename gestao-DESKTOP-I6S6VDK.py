# -*- coding: utf-8 -*-
#Atualizacao de arquivos
print('########################################')
print(' Ultima atualizacao 23 de Junho 2017')
print('########################################')

import os, sys,re,zipfile
# import contextlib, zipfile,java
# import stat,urllib,paramiko,getpass,socket, glob,fnmatch
# # biblioteca usada pelo CREAEAR
# from shutil import copytree
# import distutils.dir_util,zipfile,shutil, from distutils.dir_util import copy_tree
# from xml.etree.ElementTree import Element, SubElement, ElementTree,TreeBuilder
# import xml.etree.ElementTree as ET
# from xml.dom.minidom import DOMImplementation, Document,parse

global AdminControl
global AdminConfig
global AdminApp
                        
def listar(arg=0):
    try:
        print('argumento informado %s'%arg)
        cells = AdminConfig.list('Cell').split()    
        apps = AdminApp.list().split()
        for cell in cells:
            variables = AdminConfig.list('VariableSubstitutionEntry',cell).split()
            for variable in variables:
                variableName = AdminConfig.showAttribute(variable,'symbolicName')
                if variableName == 'CELLID':
                    cellValue = AdminConfig.showAttribute(variable,'value')
                    print('ID da Celula %s'%cellValue)
            cellName = AdminConfig.showAttribute(cell,'name')
            print('Nome da Celula: %s'%cellName); arqsys.write('*'*20+'\n')
            arqsys.write('Celula: %s\n' %cellName)
            arqsys.write('*'*20+'\n')
            nodes = AdminConfig.list('Node',cell).split(); clusters = AdminConfig.list('ServerCluster', cell).split(); webservers = AdminTask.listServers('[-serverType WEB_SERVER ]').split()
            arqsys.write('---- Clusters ------\n')
            for cl in clusters:
                clName = AdminConfig.showAttribute(cl,'name')
                print('Cluster | ' + clName)
                arqsys.write('Cluster| ' + clName + '\n')
            arqsys.write('\n-----  Servidores WEB -----\n')
            for web in webservers:
                print('Web Server | ' + web.split('(')[0])            
                arqsys.write('Web Server | ' + web.split('(')[0] + '\n')
            arqsys.write('*'*30+'\n')
            nodes = AdminConfig.list('Node',cell).split()
            print('extraindo as informacoes detalhadas desta celula')
            for node in nodes:
                nodeName = AdminConfig.showAttribute(node,'name')
                arqsys.write('------- Nodes -------\n')                
                arqsys.write('Nome do node: %s\n'%nodeName)
                count = len('Nome do node: %s\n'%nodeName)
                arqsys.write('-'*30+'\n')
                servers = AdminConfig.list('Server',node).split()
                for server in servers:
                    serverName = AdminConfig.showAttribute(server,'name')
                    arqsys.write('| |Servidor %s | | \n'%serverName)
                    apps = AdminApp.list('WebSphere:cell=%s,node=%s,server=%s'%(cellName,nodeName,serverName)).split()
                    for app in apps:
                        arqsys.write('>>> aplicacoes associadas: %s \n'%app)
                        if arg !=0:
                            appmodules(app)
    except:
        print('nao localizado')
      
def listarq():
    cells = AdminConfig.list('Cell').split()
    print('listando arquiteturas associadas as aplicacoes. Iniciando  ...')
    for cell in cells:
        cellName = AdminConfig.showAttribute(cell,'name')
        i = '#' * 50
        arqsys.write(i + '\n')
        arqsys.write('Nome da celula: '+ cellName + '\n')
        arqsys.write(i + '\n')
    nodes = AdminConfig.list('Node',cell).split()
    for node in nodes:
        nodeHostName = AdminConfig.showAttribute(node,'hostName')
        arqsys.write('no: '+nodeHostName+ ' ')
    arqsys.write('\n')
    apps = AdminApp.list().split()
    for app in apps:
        try:
            librs=AdminApp.view(app, '[ -MapSharedLibForMod [[ ]]]' ).split('\n')    
            for lib in librs:
                if lib.startswith('Module:  ') and not lib.endswith('ESCE'):
                    arqsys.write('aplicacao: '+ lib[7:] + ' ; ')
                if lib.startswith('Shared Libraries:'):
                    libraries = lib[19:]
                    libs = libraries.split('+')
                    for library in libs:
                        if len(library) != 0:
                            if not library.startswith('WebSphere:name=API') and not library.startswith('WebSphere:name=ALTAIR')  and not library.startswith('WebSphere:name=AppLibs_SL') and not library.startswith('WebSphere:name=LibreriaArq'):
                                libraryTT = library[15:].split(',')
                                arqsys.write('Arquitetura: '+libraryTT[0]+';')
        except:
            continue
        arqsys.write('\n')
    ct = 0
    for app in apps:
        ct+=1
    print('total de aplicacoes %s'%ct)
    print('....execucao finalizada. Veja o arquivo SystemExit.log gerado neste mesmo caminho')

def listabibl():
    cells = AdminConfig.list('Cell').split()
    print('listando bibliotecas associadas as aplicacoes. Iniciando  ...')
    for cell in cells:
        cellName = AdminConfig.showAttribute(cell,'name')
        i = '#' * 50
        arqsys.write(i + '\n')
        arqsys.write('Nome da celula: '+ cellName + '\n')
        arqsys.write(i + '\n')
    nodes = AdminConfig.list('Node',cell).split()
    for node in nodes:
        nodeHostName = AdminConfig.showAttribute(node,'hostName')
        arqsys.write('no: '+nodeHostName+ ' ')
    arqsys.write('\n')
    apps = AdminApp.list().split()
    for app in apps:
        try:
            librs=AdminApp.view(app, '[ -MapSharedLibForMod [[ ]]]' ).split('\n')    
            for lib in librs:
                if lib.startswith('Module:  ') and not lib.endswith('ESCE'):
                    arqsys.write('aplicacao: '+ lib[7:] + ' ; ')
                if lib.startswith('Shared Libraries:'):
                    libraries = lib[19:]
                    libs = libraries.split('+')
                    for library in libs:
                        if len(library) != 0:
                            libraryTT = library[15:].split(',')
                            arqsys.write('Biblioteca: '+libraryTT[0]+';')
            arqsys.write('\n')
        except:
            continue
    ct = 0
    for app in apps:
        ct+=1
    print('total de aplicacoes %s'%ct)
    print('....execucao finalizada. Veja o arquivo SystemExit.log gerado neste mesmo caminho')
    
def appmodules(app):
    modules=AdminApp.listModules(app,'-server').split('#')
    arqsys.write('-'*20+'\n')
    arqsys.write('Pacote | ' + app + '\n')
    for mod in modules:
        if mod.startswith('WebSphere:cell='):
            mapslice = mod[15:]
            mapps = mapslice.split('+')
            arqsys.write('Mapeamentos\n ')
            for mapp in mapps:
                arqsys.write(mapp.split(',')[1]+ '')
            break
    arqsys.write('\n')
    libraries=AdminApp.view(app, '[ -MapSharedLibForMod [[ ]]]' ).split('\n')    
    for library in libraries:
        if library.startswith('Shared'):
            libs = library[19:]
            libsplit = libs.split('+')
            arqsys.write('Bibliotecas\n ')
            for lib in libsplit:
                if len(lib) != 0:
                    libslice = lib.split(',')[0]
                    arqsys.write(libslice[15:]+ ' ')
                else:
                    arqsys.write('nao ha biblioteca associada neste escopo\n')
        
def exportar(app1,path1):
    if not os.path.exists(path1):
        print('Nao existe o caminho informado')
    else:
        apps = AdminApp.list().split()
        for app in apps:
            if app1 == 'TODOS':
                try:
                    print('voce selecionou a opcao TODOS. sera feito export para o caminho %s' %app)
                    AdminApp.export(app,path1 + app + '.ear', '[-exportToLocal]')
                    print('aplicacao exportada no caminho %s' %path1)
                except:
                    continue
            elif app1 == app:
                if not os.path.exists(os.path.join(path1,app+'.ear')):
                    AdminApp.export(app,path1+'/'+app+'.ear', '[-exportToLocal]')
                    print('export do %s' %app)
                    print('aplicacao exportada no caminho %s' %path1)            
                    
def atualizar(app1,path,pathear):
    arq_ens = open('ens.py','w')
    print('funcao ATUALIZAR acionada')
    print('Atencao, todos os arquivos que foram definidos dentro do caminho %s serao instalados no pacote %s ' %(path,app1))
    cells = AdminConfig.list('Cell').split()    
    apps = AdminApp.list().split()
    for app in apps:
        if app == app1:
            print('App localizado: ' + app)
            for fl in os.listdir(path):
                print(fl)
                str_atualiza = '\''+app1+'\',\'file\',[\'-operation\',  \'update\', \'-contents\',\''+path+''+fl+'\', \'-contenturi\',\'' +pathear+''+fl+'\']'
                print('Arquivo a ser atualizado: %s'%fl)
                arq_ens.write('AdminApp.update(%s)\n' %str_atualiza)
            arq_ens.write('AdminConfig.save();\n')
    arq_ens.close()
    print('Gerado o arquivo ens.py')
    run_atualiza()
    stopapps(app1)
    startapps(app1) 
    
def run_atualiza():
    execfile('ens.py')
    sincroniza()

def gerar(arg1):
    arqsrv = open('servidores.sh','w')
    cells = AdminConfig.list('Cell').split()
    for cell in cells:
        cellName = AdminConfig.showAttribute(cell,'name')
        print('Nome da céla ', cellName)
        nodes = AdminConfig.list('Node',cell ).split()
        for node in nodes:
            nodeName = AdminConfig.showAttribute(node,'name')
            nodeHostName = AdminConfig.showAttribute(node,'hostName')
            arqsrv.write('scp -rpC Conf_Aplicaciones/* '+nodeHostName+':/ArquitecturaE-business/Lib/LibRigel/Conf_Aplicaciones/\n')
            arqsrv.write('scp -rpC EarEstatico/* '+nodeHostName+':/ArquitecturaE-business/Html/EarEstatico/\n')
    print('gerado o arquivo servidores.sh com todos os servidores preparados para copiar. Se Atende os devidos escopos ao se copiar')
    arqsrv.close()
        
    print('Arquivo que contenha os pacotes '+ arg1)
    arq_instala = open(arg1,'r')
    ensamblados = arq_instala.readlines()
    print('pasta de trabalho: ', os.getcwd())
    if not os.path.exists('Conf_Aplicaciones'):
        os.mkdir('Conf_Aplicaciones')
    
    for each in ensamblados:
        print(each)
        newone = open('Conf_Aplicaciones/'+each[:-1]+'.properties','w')
        newone.write('#vacio')
        newone.write('#aeb.root.logLevel=VeryHigh\n')
        newone.write('#aeb.root.component.logLevel=VeryHigh\n')
        newone.write('#aeb.root.operation.logLevel=VeryHigh\n')
        newone.write('#aeb.root.operation.internal.logLevel=VeryHigh\n')
        newone.write('#aeb.root.operation.presentation.logLevel=VeryHigh\n')
        newone.write('aeb.loggerManagerDebug=LoggerManagerDebug.xml\n')
        newone.write('aeb.funcional.VeryHigh=true\n')
        newone.write('aeb.AppLogsService.eventLog=false\n')
        newone.write('aeb.independentStaticRoutes=true\n')
        print('Gerando o properties para a aplicacao: ' + each)
        newone.close()

    if not os.path.exists('EarEstatico'):
        os.mkdir('EarEstatico')
    else:
        print('Ja existe a pasta EarEstatico neste caminho')
    for each in ensamblados:
        if not os.path.exists('EarEstatico/'+each):
            os.mkdir('EarEstatico/'+each[:-1])
    print('Gerado nas pastas Conf_Aplicaciones e EarEstatico os arquivos necessarios para o ambiente\n. Neste momento voce deve copiar para todas as maquinas. Futuramente os arquivos serãgerados diretamente em todos os servidores')
    print('copiando arquivos para servidores')
        
def instalar(app1,path,cluster):
    apps = AdminApp.list().split()
    for app in apps:
        if app != app1:
            print(' ')
        else:
            print(app+ 'produto localizado. Escolha a opcao atualizar')
            break
    AdminApp.install(''+path+'','[-appname '+app1+' -cluster '+cluster+']')
    AdminConfig.save()
    configuraear(app1,cluster)
    arq_silent = open('instalar.silent','w')
    arq_silent.write(app1+'\n')
    arq_silent.close()
    os.system('chmod 775 instalar.silent')
    arg1 = 'instalar.silent'
    gerar(arg1)
    mapear(app1,cluster)
    
def appscluster(silent):
    arqsilent = open(silent,'r')
    cluster = [str(cl[8:]).strip() for cl in arqsilent.readlines() if apl.startswith('cluster')]
    cl = str(cluster)
    apls = [str(apl[5:]).strip() for apl in arqsilent.readlines() if apl.startswith('apps=')]
    for a in str(apls).split(','):
        print('aplicacao %s'%a)
    
def configuraear(app1,cluster=0):
    #configurando sessao da aplicacao - Aqui foi usado o script que tinha sido preparado pelo Flavio Monastirscy
    deployments =  AdminConfig.getid('/Deployment:'+app1+'/')
    print('---->mostrando deployments<------')
    print(deployments)
    appDeploy = AdminConfig.showAttribute(deployments, 'deployedObject')
    print(appDeploy)
    #definindo sessao #
    attr0 = ['enable', 'true'] 
    attr1 = ['enableSecurityIntegration', 'false'] 
    attr2 = ['maxWaitTime', '0']
    attr3 = ['enableCookies', 'true'] 
    attr4 = ['allowSerializedSessionAccess', 'false'] 
    attr5 = ['enableSSLTracking', 'false']
    attr6 = ['accessSessionOnTimeout', 'true'] 
    attr7 = ['enableUrlRewriting', 'false'] 
    attr8=  ['enableProtocolSwitchRewriting', 'false'] 
    attbd = ['sessionPersistenceMode', 'DATABASE']
    #tunning
    attr9 =   ['invalidationTimeout', '120']
    attr10 =  ['allowOverflow', 'true']
    attr11 =  ['maxInMemorySessionCount', '1000']
    attr12 =  ['usingMultiRowSchema','true']
    tuningParmsDetailList = [attr9, attr10 ,attr11, attr12]
    tuningParamsList= ['tuningParams', tuningParmsDetailList]
    # BD
    tblSpaceName = ['tableSpaceName','TUPSESSAO']
    pwdList = ['password', 'bks@app2']
    userList = ['userId', 'upsessao']
    rowsize = ['db2RowSize','ROW_SIZE_32KB']
    dsNameList = ['datasourceJNDIName', 'jdbc/Sessions']
    dbPersistenceList = [dsNameList, userList, pwdList,tblSpaceName,rowsize]
    sessionDBPersistenceList = [dbPersistenceList]
    sessionDBPersistenceList = ['sessionDatabasePersistence', dbPersistenceList]
    #cookies
    kuki = ['maximumAge', '-1']
    kukiname= ['name','JSESSIONID_'+app1]
    cookie = [kuki,kukiname]
    cookieSettings = ['defaultCookieSettings', cookie]
    sessionManagerDetailList=[attr0,attr1,attr2,attr3,attr4,attr5,attr6,attr7,attr8,attbd,tuningParamsList, cookieSettings,sessionDBPersistenceList]
    sessionMgr = ['sessionManagement', sessionManagerDetailList]
    id = AdminConfig.create('ApplicationConfig', appDeploy,[sessionMgr], 'configs')
    print('----->mostrando targetMappings<------')
    targetMappings = AdminConfig.showAttribute(appDeploy, 'targetMappings')
    targetMappings = targetMappings[1:len(targetMappings)-1]
    print(targetMappings)
    attrs = ['config', id]
    AdminConfig.modify(targetMappings,[attrs])
    AdminConfig.save()
    print('Efetuado a configuraç de gerenciamento de sessãda aplicacao')
 
def sincroniza():
    arq_sync = open('sync.py','w')
    cells = AdminConfig.list('Cell').split()
    for cell in cells:
        cellName = AdminConfig.showAttribute(cell,'name')
        nodes = AdminConfig.list('Node',cell).split()
        for node in nodes:
            nodeName = AdminConfig.showAttribute(node,'name')
            servers = AdminControl.queryNames('type=Server,cell='+cellName+',node='+nodeName+',*').split()
            # éecessáo criar aqui um processo que verifique se o nótáo ar para poder disparar a sincronizacao full.
            if not nodeName.startswith('Dmgr') and not nodeName.startswith('IHS'):
                arq_sync.write('sync1 = AdminControl.completeObjectName(\'type=NodeSync,process=nodeagent,node='+nodeName+',*\')\n')
                arq_sync.write('AdminControl.invoke(sync1, \'sync\')\n')
    arq_sync.close()
    run_sync()

def run_sync():
    print('sincronizacao em andamento')
    execfile('sync.py')
    
def atualizaear(app1,path,cluster=0):
    AdminApp.update(app1,'app','[-operation update -contents '+path+' -usedefaultbindings -nodeployejb -nouseAutoLink]')
    AdminConfig.save();
    mapear(app1,cluster)
    sincroniza()        

def mapear(app1,cluster):
    '''
    preciso analisar com mais calma mas por mais de uma vez quando se necessita editar um ens eh necessario gerar um arquivo py para que a edicao funcione. 
    Pois se tento fazer a adminapp.edit diretamente do gestao.py apresenta erro informando que um argumento nao foi passado corretamente
    '''
    arqrun = open('run.py','w')
    apps = AdminApp.list().split()
    results = [app for app in apps if app == app1 ]
    if len(results) >0:
        modules=[module[9:] for module in AdminApp.view(app1,'-MapModulesToServers').split('\n') if module.startswith('Module: ')]
        uris=[module[4:] for module in AdminApp.view(app1,'-MapModulesToServers').split('\n') if module.startswith('URI: ')]
        servers=[module[7:] for module in AdminApp.view(app1,'-MapModulesToServers').split('\n') if module.startswith('Server: ')]
        mapmodules=''; mapitems=[]
        for m,u,s in zip(modules,uris,getwebmod(cluster)):
            mapitems.append(m+''+u+' '+getwebmod(cluster))
            mapmodules+=str(mapitems)
            mapitems=[]
        newmapmodules=re.sub('\'','',mapmodules)
        arqrun.write('AdminApp.edit(\''+app1+'\', \'[ -MapModulesToServers ['+newmapmodules+']]\')\n')
        arqrun.write('AdminConfig.save();\n')
    arqrun.close()        
    execfile('run.py')
    print('se voce executou somente a funcao mapear, por favor executar tambem a funcao sincronizar ')
    
def getwebmod(cluster):
        cells = AdminConfig.list('Cell').split()
        for cell in cells:
            cName = AdminConfig.showAttribute(cell,'name')
            srvmapping='WebSphere:cell=%s'%cName
            clusters = AdminConfig.list('ServerCluster', cell).split()
            
            for cl in clusters:
                clName = AdminConfig.showAttribute(cl,'name')
                if cluster == clName:
                    srvmapping+=',cluster=%s'%cluster
            nodes = AdminConfig.list('Node',cell).split()
            for node in nodes:
                websrv = AdminConfig.list('WebServer',node)
                if websrv != '':
                    nName = AdminConfig.showAttribute(node,'name')            
                    wName = AdminConfig.showAttribute(websrv,'name')
                    srvmapping+='+WebSphere:cell=%s,node=%s,server=%s'%(cName,nName,wName)
            return srvmapping     
    
def cfgbiblioteca(silent):
    arqsys = open('SystemExit.log','w')
    print('Opcao configurar biblioteca selecionada!')
    print('fazendo a leitura do arquivo .silent no argumento', str(silent))
    arq_silent =open(silent,'r')
    rlines = arq_silent.readlines()
    for line in rlines:
        if line.startswith('biblioteca='):
            bibl = line[11:]
        if line.startswith('arquitetura='):
            arq = line[12:]
    arq_silent.close()
    if len(bibl)==0 or len(arq)==0:
        print('favor verificar argumentos de biblioteca e arquitetura')
        exit
        
    arq_silent =open(silent,'r')
    rlines = arq_silent.readlines()
    for line in rlines:
        if line.startswith('apps='):
            listaens = line.split('=')[1]
            for ens in listaens.split(','):
                print('aplicacao',ens) 
                arqsys.write('aplicacao %s\n' %ens)
                print('arquitetura',arq)
                arqsys.write('arquitetura %s\n' %arq)
                print('biblioteca',bibl)
                arqsys.write('biblioteca %s\n' %bibl)
                cfgbiblioteca2(ens,arq,bibl)
    arq_silent.close()
    arqsys.close()
    AdminConfig.save();
    
def cfgbiblioteca2(ens,arq,bibl):
    arq_con= open('concatena.log','a')
    arq_con.write('*' * 30 + '\n')
    arq2 = arq.strip()
    bibl2 = bibl.strip()
    ens2 = ens.strip()
    arq_con.write('AdminApp.edit('+ens2+', \'[ -MapSharedLibForMod [[ '+ens2+' META-INF/application.xml ARQ_RIGEL_'+arq2+'+'+bibl2+' ]]]\n')

    arq_con.write('*' * 30 + '\n')    
    arq_con.close()
    apps = AdminApp.list().split()
    for app in apps:
        if app == ens:
            print('aplicacao localizada ', app)
            AdminApp.edit(ens2, '[ -MapSharedLibForMod [[ '+ens2+' META-INF/application.xml ARQ_RIGEL_'+arq2+'+'+bibl2+' ]]]')
            librs=AdminApp.view(app, '[ -MapSharedLibForMod [[ ]]]' ).split('\n')    
            for lib in librs:
                if lib.endswith('web.xml'):
                    print(lib[5:])
                    modweb=lib[5:]
                    esce = modweb.split('.')[0]
                    hash = esce + modweb
                    print('hash', hash)
                    AdminApp.edit(app, '[ -MapInitParamForServlet [[ '+hash+' RigelBootStrapServlet bootStrapEncryptConfig null file:/ArquitecturaE-business/Xml/CfgRigel'+arq2+'/gaia/ConfigurationManager.xml ][ '+hash+' RigelBootStrapServlet urlConfig null file:/ArquitecturaE-business/Xml/CfgRigel'+arq2+'/gaia/kernel.xml ][ '+hash+' RigelBootStrapServlet variableConfigPath null /ArquitecturaE-business/Xml/CfgRigel'+arq+'/RigelJars_Configuration ]]]' )
                    AdminApp.edit(app, '[ -MapInitParamForServlet [[ '+hash+' RigelBootStrapServlet bootStrapEncryptConfig null file:/ArquitecturaE-business/Xml/CfgRigel'+arq2+'/gaia/ConfigurationManager.xml ][ '+hash+' RigelBootStrapServlet urlConfig null file:/ArquitecturaE-business/Xml/CfgRigel'+arq2+'/gaia/kernel.xml ][ '+hash+' RigelBootStrapServlet variableConfigPath null /ArquitecturaE-business/Xml/CfgRigel'+bib+'/RigelJars_Configuration ]]]' )
        # AdminConfig.save()                    
    print('alteracao de arquitetura executada')

def configurar(apl,bib):
    apps = AdminApp.list().split()
    for app in apps:
        if app == apl:
            print('aplicacao localizada ', app)
            AdminApp.edit(app, '[ -MapSharedLibForMod [[ '+app+' META-INF/application.xml API+ALTAIR+ARQ_RIGEL_'+bib[8:]+' ]]]' )        
            librs=AdminApp.view(app, '[ -MapSharedLibForMod [[ ]]]' ).split('\n')    
            for lib in librs:
                if lib.endswith('web.xml'):
                    print(lib[5:])
                    modweb=lib[5:]
                    esce = modweb.split('.')[0]
                    hash = esce + modweb
                    print('hash', hash)
                    AdminApp.edit(app, '[ -MapInitParamForServlet [[ '+hash+' RigelBootStrapServlet bootStrapEncryptConfig null file:/ArquitecturaE-business/Xml/'+bib+'/gaia/ConfigurationManager.xml ][ '+hash+' RigelBootStrapServlet urlConfig null file:/ArquitecturaE-business/Xml/'+bib+'/gaia/kernel.xml ][ '+hash+' RigelBootStrapServlet variableConfigPath null /ArquitecturaE-business/Xml/'+bib+'/RigelJars_Configuration ]]]' )
        AdminConfig.save()                    
    print('alteracao de arquitetura executada')
 
def bulkarq(arq):
    arqapps=open('apps.py','w')
    print('gerado o arquivo apps.py com todos os aplicativos desta infra com a configuracao de arquitetura %s' %arq)
    apps = AdminApp.list().split()
    for app in apps:
        arqapps.write('AdminApp.edit(\'%s\', \'[ -MapSharedLibForMod [[ %s META-INF/application.xml API+ALTAIR+ARQ_RIGEL_%s ]]]\' )\n'%(app,app,arq))
        librs=AdminApp.view(app,'[ -MapSharedLibForMod [[ ]]]').split('\n')
        for lib in librs:
            if lib.endswith('web.xml'):
                print(lib[5:])
                modweb=lib[5:]
                esce = modweb.split('.')[0]
                hash = esce + modweb
                print('aplicativo sera atualizado: %s'%hash)   
                arqapps.write('AdminApp.edit(\'%s\',\'[ -MapInitParamForServlet [[ %s RigelBootStrapServlet bootStrapEncryptConfig null file:/ArquitecturaE-business/Xml/CfgRigel%s/gaia/ConfigurationManager.xml ][ %s RigelBootStrapServlet urlConfig null file:/ArquitecturaE-business/Xml/CfgRigel%s/gaia/kernel.xml ][ %s RigelBootStrapServlet variableConfigPath null /ArquitecturaE-business/Xml/CfgRigel%s/RigelJars_Configuration ]]]\')\n' %(app,hash,arq,hash,arq,hash,arq))
    arqapps.write('AdminConfig.save()\n')
    arqapps.close()
    print('gerado o arquivo gerado apps.py com todas as aplicacoes')
    print('Linha da execucao esta comentada.')
    
def stopapps(app1):
    #parando a aplicacao
    cells = AdminConfig.list('Cell').split()    
    for cell in cells:
        cellName = AdminConfig.showAttribute(cell,'name')
        nodes = AdminConfig.list('Node',cell).split()
        for node in nodes:
            nodeName = AdminConfig.showAttribute(node,'name')
            servers = AdminControl.queryNames('type=Server,cell='+cellName+',node='+nodeName+',*').split()
            for server in servers:
                serverName = AdminControl.getAttribute(server,'name')
                apps = AdminApp.list('Websphere:cell='+cellName+',node='+nodeName+',server='+serverName).split()
                for apl in apps:
                    if apl == app1:
                            appManager = AdminControl.queryNames('cell='+cellName+',node='+nodeName+',type=ApplicationManager,process='+serverName+',*')
                            print('aplicacao %s localizada. Processo ira parar a aplicacao no Processo Java %s...' %(apl,appManager.split(',')[1]))
                            objectName = AdminControl.completeObjectName('type=Application,name=' + apl + ',*')
                            if objectName != '':
                                AdminControl.invoke(appManager,'stopApplication',apl)
                                print('aplicacao '+apl+' esta parada ')
                                
def statusapps():
    #Status das aplicaçs
    cells = AdminConfig.list('Cell').split()    
    for cell in cells:
        cellName = AdminConfig.showAttribute(cell,'name')
        nodes = AdminConfig.list('Node',cell).split()
        for node in nodes:
            nodeName = AdminConfig.showAttribute(node,'name')
            servers = AdminControl.queryNames('type=Server,cell='+cellName+',node='+nodeName+',*').split()
            for server in servers:
                serverName = AdminControl.getAttribute(server,'name')
                apps = AdminApp.list('Websphere:cell='+cellName+',node='+nodeName+',server='+serverName).split()
                for app in apps:
                    print('Pacote:', app)
                    arqsys.write('Pacote: '+app+'\n')
                    objNames = AdminControl.queryNames('type=Application,name='+app+',*').split()
                    if len(objNames)!=0:
                        ct = 0
                        for objName in objNames:
                            ct+=1
                            arqsys.write('mbean: '+ objName+ '\n')
                        print('mbeans ativos %s'%ct)
                        arqsys.write('Processos mbeans ativos: '+ str(ct)+'\n')
                        arqsys.write('aplicacao em execucao')
                    else:
                        print('aplicacao parada')
                        arqsys.write('aplicacao parada')
                                
def startapps(app1):    
    #iniciando a aplicacao
    cellName = [AdminConfig.showAttribute(cell,'name') for cell in AdminConfig.list('Cell').split()][0]
    cellID = [cell for cell in AdminConfig.list('Cell').split()][0]
    cellID2 = cell.replace('\'','');cellID2=cellID2.replace('[','');cellID2=cellID2.replace(']','')
    nodeNames = str([AdminConfig.showAttribute(node,'name') for node in AdminConfig.list('Node',cellID2).split()])
    print('ID Celula %s \nCelula %s \nNodes %s'%(cellID, cellName, nodeNames.replace('\'','')))
    for nodeName in nodeNames.split():
        try:
            nName = nodeName.replace('[','');nName = nName.replace(']','');nName = nName.replace('\'','');nName = nName.replace(',','')
            arqsys.write('No: %s\n'%nName)
            # #Este metodo de pesquisa de servidores busca somente os que estao ativos. Preciso confirmar mas este é um gerenciamento de JMX
            servers = AdminControl.queryNames('type=Server,cell='+cellName+',node='+nName+',*').split()
            for server in servers:
                serverName = AdminControl.getAttribute(server,'name')
                apps = AdminApp.list('Websphere:cell='+cellName+',node='+nName+',server='+serverName).split()
                arqsys.write('Servidor %s\n'%serverName)
                arqsys.write('apps %s\n'%apps)
                for app in apps:
                    if app == app1:
                        print('Aplicacao localizada %s'%app);arqsys.write('Aplicacao Localizada %s\n'%app)
                        appManager = AdminControl.queryNames('cell='+cellName+',node='+nName+',type=ApplicationManager,process='+serverName+',*')
                        objName = AdminControl.completeObjectName('type=Application,name=' + app + ',*')
                        print('Processo hospedeiro: %s \nNome do processo do APP %s '%(appManager,app1))
                        if objName == '':
                            AdminControl.invoke(appManager,'startApplication',app1)
                            print('realizado o start na aplicacao %s no %s'%(app1,appManager.split(',')[1]))
                        else:
                            print('Nenhuma acao realizada. Processo aparentemente ativo')
        except:
            continue
                                
def coleta_servidores():
    arqsrv = open('servidores.silent','w')
    cells = AdminConfig.list('Cell').split()
    for cell in cells:
        cellName = AdminConfig.showAttribute(cell,'name')
        print('Nome da celula ', cellName)
        nodes = AdminConfig.list('Node',cell ).split()
        for node in nodes:
            nodeName = AdminConfig.showAttribute(node,'name')
            nodeHostName = AdminConfig.showAttribute(node,'hostName')
            print('No: '+ nodeName + ' -- hostname '+  nodeHostName)
            arqsrv.write(nodeHostName+'\n')        
    arqsrv.close()
    print('gerado o arquivo servidores.silent com todos os nós deste ambiente')

def sgs(usr,pwd):
    print('funcao SGS acionada')
    print('este metodo ira gerar duas rotinas. SERVIDORES.SH para o restart - necessario passar usuario e senha e uma rotina que usa o  paramiko para execucao no windows. ambas sao automaticas')
    coleta_servidores()
    arqsrv=open('servidores.silent','r')
    arqrestart = open('servidores.py','w')
    arqrun = open('servidores.sh','w')
    arqrestart.write('import os,subprocess\n')
    try:
        for servidor in arqsrv.readlines():
            server=str(servidor).strip()
            arqrun.write('ssh -t %s@%s \'sudo /export/arqsrv/bin/./ARQSRV.sh restart\'\n'%(usr,server))
            arqrestart.write('subprocess.call(\'ssh -t %s@%s \'sudo /export/arqsrv/bin/./ARQSRV.sh restart\',shell=True) \n' %(usr,server))
        arqrestart.close()
        arqrun.close()
    except IOError:
        print('Arquivo nao localizado')   
    os.system('chmod 775 servidores.py')
    os.system('python servidores.py')
    
    
    arq_run = open('run_windows.py','w')
    arq_run.write('arqsys = open(\'SystemExit.log\',\'w\') \n')
    arq_run.write('import paramiko,getpass,socket \n')
    arq_run.write('ssh = paramiko.SSHClient() \n')
    arq_run.write('ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) \n')
    arq_run.write('usr1 = \'%s\' \n'%usr)
    arq_run.write('pwd1 = \'%s\' \n'%pwd)
    arq_run.write('arq_read = open(\'servidores.silent\',\'r\')\n')
    arq_run.write('arq_readlns = arq_read.readlines()\n')
    arq_run.write('for readln in arq_readlns:\n')
    arq_run.write('    try:\n')
    arq_run.write('        print(\'servidores\',readln.strip())\n')
    arq_run.write('        server = readln.strip()\n')
    arq_run.write('        ssh.connect(server,username=usr1,password=pwd1,timeout=3.0)\n')
    arq_run.write('        chan=ssh.get_transport().open_session()\n')
    arq_run.write('        chan.get_pty()\n')
    arq_run.write('        f = chan.makefile()\n')
    arq_run.write('        chan.exec_command(\'sudo /export/arqsrv/bin/./ARQSRV.sh stop\')\n')
    arq_run.write('        print(f.read())\n')
    arq_run.write('        ssh.close()\n')
    arq_run.write('        ssh.connect(server,username=usr1,password=pwd1,timeout=3.0)\n')
    arq_run.write('        chan=ssh.get_transport().open_session()\n')
    arq_run.write('        chan.get_pty()\n')
    arq_run.write('        f = chan.makefile()\n')
    arq_run.write('        chan.exec_command(\'sudo /export/arqsrv/bin/./ARQSRV.sh start\')\n')
    arq_run.write('        print(f.read())\n')
    arq_run.write('        ssh.close()\n')
    arq_run.write('    except:\n')
    arq_run.write('        continue\n')
    arq_run.write('for readln in arq_readlns:\n')
    arq_run.write('    try:\n')
    arq_run.write('        print(\'servidores\',readln.strip())\n')
    arq_run.write('        server = readln.strip()\n')
    arq_run.write('        ssh.connect(server,username=usr1,password=pwd1,timeout=3.0)\n')
    arq_run.write('        chan=ssh.get_transport().open_session()\n')
    arq_run.write('        chan.get_pty()\n')
    arq_run.write('        f = chan.makefile()\n')
    arq_run.write('        chan.exec_command(\'sudo /export/arqsrv/bin/./ARQSRV.sh status\')\n')
    arq_run.write('        arqsys.write(\' Status %s\' % chan.recv_exit_status())\n')
    arq_run.write('        print(f.read())\n')
    arq_run.write('        ssh.close()\n')
    arq_run.write('    except:\n')
    arq_run.write('        continue\n')
    arq_run.write('arqsys.close()\n')
    arq_run.close()   
    print('gerado o arquivo servidores.silent. Favor executar o arquivos run.py para restart do serviçde SGS')

def repliweb(usr,pwd):
    print('este metodo ira gerar duas rotinas. SERVIDORES.SH para o restart - necessario passar usuario e senha e uma rotina que usa o  paramiko para execucao no windows. ambas sao automaticas')
    print('atualmente ela disponivel somente onde ha a biblioteca paramiko')
    coleta_servidores()
    arqrestart = open('servidores.sh','w')
    arqrestart.write('#/bin/sh\n')
    arqsrv=open('servidores.silent','r')
    try:
        for servidor in arqsrv.readlines():
            server=str(servidor).strip()
            arqrestart.write('ssh -tt %s@%s \'sudo /etc/init.d/./xinetd restart\'\n'%(usr,server))
            os.system('ssh -tt %s@%s \'sudo /etc/init.d/./xinetd restart\''%(usr,server))
            arqrestart.write('ssh -tt %s@%s \'sudo /usr/bin/repliweb_scheduler start\'\n'%(usr,server))
            os.system('ssh -tt %s@%s \'sudo /usr/bin/repliweb_scheduler start\''%(usr,server))
        arqrestart.close()
    except IOError:
        print('Arquivo nao localizado')
        
    arq_run = open('run.py','w')
    arq_run.write('arqsys = open(\'SystemExit.log\',\'w\') \n')
    arq_run.write('import paramiko,getpass,socket \n')
    arq_run.write('ssh = paramiko.SSHClient() \n')
    arq_run.write('ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) \n')
    arq_run.write('usr1 = \''+usr+'\' \n')
    arq_run.write('pwd1 = \''+pwd+'\' \n')
    arq_run.write('arq_read = open(\'servidores.silent\',\'r\')\n')
    arq_run.write('arq_readlns = arq_read.readlines()\n')
    arq_run.write('for readln in arq_readlns:\n')
    arq_run.write('    try:\n')
    arq_run.write('        print(\'servidores\',readln.strip())\n')
    arq_run.write('        arqsys.write(\'servidores: \' +readln.strip()+\' fim\')\n')
    arq_run.write('        server = readln.strip()\n')
    arq_run.write('        ssh.connect(server,username=usr1,password=pwd1,timeout=3.0)\n')
    arq_run.write('        chan=ssh.get_transport().open_session()\n')
    arq_run.write('        chan.get_pty()\n')
    arq_run.write('        f = chan.makefile()\n')
    arq_run.write('        chan.exec_command(\'sudo /etc/init.d/./xinetd restart\')\n')
    arq_run.write('        ssh.close()\n')
    arq_run.write('    except:\n')
    arq_run.write('        continue\n')
    arq_run.write('arq_read.close()\n')    
    arq_run.close()   
    print('gerado o arquivo SERVIDORES.SH para executar manualmente ')
    
def creaear(app1,silent):
    bibliotecas()
    print('Aplicacao a ser criada %s e sera usado o arquivo %s com os dados pertinentes para execucao' %(app1,silent))
    arq_sil = open(silent,'r')
    contents = arq_sil.readlines()
    for ln in contents:
        if ln.startswith('creaear='):
            count = len('creaear=')
            templ = ln[count:]
            print('caminho do template '+templ)

    if not os.path.exists('swap'):
        os.mkdir('swap')
    if not os.path.exists('swap/'+app1):
        os.mkdir('swap/'+app1)
    print('criando a estrutura de pastas')
    for dirname,subdirs,files in os.walk('template'):
        for subdir in subdirs:
            if not os.path.exists('swap/'+app1+'/'+os.path.join(dirname,subdir)):
                os.makedirs('swap/'+app1+'/'+os.path.join(dirname,subdir))
    print('copiando arquivos')
    for dirname,subdirs,files in os.walk('template'):
        local = os.getcwd()
        for file in files:
            origem = os.path.join(dirname,file)
            destino = os.path.join('swap',app1,dirname,file)
            shutil.copy2(origem,destino)
        # distutils.dir_util.copy_tree(direc,'swap/'+app1+'/')
        
    modifica_xml(app1)
    zip_ear(path,jar)
    input('clique em ENTER para finalizar o processo')

def zip_ear(app1,path1,path3=0,jar=0):
    if jar !=0:
        print('valor do jar %s' %jar)
    else:
        print('valor diferente do jar %s'%jar)
    print('caminho %s'%path1)
    arqzip=open('extrair.py','w')
    arqzip.write('import os,sys,contextlib, zipfile\n')
    arqzip.write('zipf = zipfile.ZipFile(\'%sswap/%s\',\'w\')\n'%(path1,jar))
    arqzip.write('os.chdir(\'%s\')\n'%(path3))
    arqzip.write('for dirname,subdirs,files in os.walk(\'.\'):\n')
    arqzip.write('    for file in files:\n')
    arqzip.write('        zipf.write(os.path.join(dirname,file))\n')
    arqzip.write('zipf.close()\n')
    arqzip.write('print(\'Jar %s compactado. Consultar o arquivo no caminho %s/swap. Aplicacao %s\')\n'%(jar,path1,app1))
    arqzip.close()
    os.system('chmod 775 extrair.py')
    os.system('python extrair.py')    
    
def modifica_xml(app1):
    print('modificando xmls')
    arq_modifica = open('SystemExit.log','w')
    os.chdir('swap/'+app1+'/template/META-INF')

    domapp = parse('application.xml')
    doctype =  [no for no in domapp.childNodes if no.nodeType == domapp.DOCUMENT_TYPE_NODE]
    for tipo in doctype:
        print('base', tipo.systemId)
        print('System ID',tipo.name)
        tipo.systemId = 'http://java.sun.com/dtd/application_1_3.dtd'
        print('Public ID',tipo.publicId)
        tipo.publicId = '-//Sun Microsystems, Inc.//DTD J2EE Application 1.3//EN'

    childs =  [no for no in domapp.childNodes if no.nodeType == domapp.ELEMENT_NODE]
    for parent in childs:
        print('pai: %s'%parent.nodeName + ' ID: %s'%parent.getAttribute('id') )
        childs2 = [no for no in parent.childNodes if no.nodeType == domapp.ELEMENT_NODE]
        for child in childs2:
            print('Nivel 1: '+str(child.nodeName) + ' ID: ' + str(child.getAttribute('id')) +' texto: '+ node_text(child))
            if node_text(child) == 'ABB_LANPRO_ENS':
                child.firstChild.replaceWholeText(app1)
            childs3 = [no for no in child.childNodes if no.nodeType == domapp.ELEMENT_NODE]
            for child_new in childs3:
                print('Nivel 2 ',child_new.nodeName)
                childs4 = [no for no in child_new.childNodes if no.nodeType == domapp.ELEMENT_NODE]
                for child_grand in childs4:
                    print('Nivel 3 ', child_grand.nodeName)
                    print('text localizado ', node_text(child_grand))
                    if node_text(child_grand) == 'ABB_LANPRO_ENS.war':
                        child_grand.firstChild.replaceWholeText(app1+'.war')
                    if node_text(child_grand) == 'ABB_LANPRO_ENS':
                        child_grand.firstChild.replaceWholeText(app1)                    
    domapp.writexml(open('novo_application.xml','w'), addindent='  ',newl='')
    os.remove('application.xml')
    os.rename('novo_application.xml','application.xml')
    print(os.getcwd())
    os.chdir('../war/WEB-INF/')

    dom = parse("web.xml")
    doctype =  [no for no in dom.childNodes if no.nodeType == dom.DOCUMENT_TYPE_NODE]
    for tipo in doctype:
        print('base', tipo.systemId)
        tipo.systemId = 'http://java.sun.com/dtd/web-app_2_3.dtd'
        print('System ID',tipo.name)
        tipo.name = 'web-app'
        print('Public ID',tipo.publicId)
        tipo.publicId = '-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN'

        
    childs =  [no for no in dom.childNodes if no.nodeType == dom.ELEMENT_NODE]
    for parent in childs:
        childs2 = [no for no in parent.childNodes if no.nodeType == dom.ELEMENT_NODE]
        for node in dom.getElementsByTagName('display-name'):
            childs2 = [no for no in parent.childNodes if no.nodeType == dom.ELEMENT_NODE]
            for child in childs2:
                if node_text(child) == 'ABB_LANPRO_ENS':
                    node.firstChild.replaceWholeText(app1)
        (node_text(child))
    dom.writexml(open('novo_web.xml','w'), addindent=' ',newl='')
    os.remove('web.xml')
    os.rename('novo_web.xml','web.xml')
    arq_modifica.close()

def node_text(node):
    text = ''
    for child in node.childNodes:
        if child.nodeType is child.TEXT_NODE:
            text += child.data
        return text 
    
def bulk(file=0):
    #Localizando web servers#
    webservers = AdminConfig.list('WebServer').split()
    for webserver in webservers:
        webName = AdminConfig.showAttribute(webserver,'server')
        webName2 = AdminConfig.showAttribute(webserver,'name')
        wserver = 'WebSphere:cell=' + webName.split('/')[1] +',node='+ webName.split('/')[3] +',server='+ webName2
    print(wserver)

def embeddor():
    print('Esta opcao faz a extracao do conteudo de CELLID configurado e realiza o embeddor das aplicações')
    print('Esta sendo usada a biblioteca urllib pois é a ultima disponivel na versao do jython atualmente instalada')
    arqemb = open('embeddor.log','w')

    cells = AdminConfig.list('Cell').split()
    for cell in cells:
        cellName = AdminConfig.showAttribute(cell,'name')
        variables = AdminConfig.list('VariableSubstitutionEntry',cell).split()
        for variable in variables:
            variableName = AdminConfig.showAttribute(variable,'symbolicName')
            apps = AdminApp.list().split()
            if variableName == 'CELLID':
                cellValue = AdminConfig.showAttribute(variable,'value')
                print('Valor da varíavel CELLID desta célula %s' %cellValue)
                for app in apps:
                    try:
                        print('%s/%s/Embeddor'%(cellValue,app))
                        arqemb.write('%s/%s/Embeddor\n'%(cellValue,app))
                    except:
                        continue
    arqemb.close()

    arqrun = open('run.py','w')    
    arqrun.write('import urllib\n')
    arqrun.write('arqemb=open(\'embeddor.log\',\'r\')\n')
    arqrun.write('arqres=open(\'embeddor_result.log\',\'w\')\n')
    arqrun.write('for rd in arqemb.readlines():\n')
    arqrun.write('    try:\n')
    arqrun.write('        response = urllib.urlopen(rd)\n')
    arqrun.write('        data_response = response.read()\n')
    arqrun.write('        data_response = str(data_response)\n')
    arqrun.write('        print(\'status %s\'%data_response)\n')
    # arqrun.write('        data_response = re.sub(r\'([a-z][A-Z])\',\'\',data_response)\n')
    arqrun.write('        arqres.write(\'%s\\n\'%rd)\n')
    arqrun.write('        arqres.write(\'status %s\\n\'%data_response)\n')
    arqrun.write('    except:\n')
    arqrun.write('        continue\n')
    arqrun.write('    finally:\n')
    arqrun.write('        arqres.close()\n')
    arqrun.write('        arqemb.close()\n')
    arqrun.close()    
    os.system('python run.py')
    print('gerado o arquivo embeddor_result.log com o resultado do embeddor')
    
def extrair(app1,path1,jar,env,camada):
    print('A funcao EXTRAIR exporta a aplicacao, extrai o arquivo que esta no argumento do arquivo .jar e modifica o conteudo de acordo com o ambiente e a camada')
    print('Argumentos informados: \naplicacao=%s \ncaminho=%s \njar=%s \nambiente=%s \ncamada=%s'%(app1,path1,jar,env,camada))
    print('Atenção, neste momento esta funcao esta preparada para modificar somente de HG para qualquer outra opcao')
    exportar(app1,path1)
    if not os.path.exists(path1+'swap/extracao'): #and not os.path.exists(path+'/swap/extracao/extracao-%s'%jar):
        os.system('mkdir %s/swap/extracao/extracao_%s -p'%(path1,jar))
        path2=path1+'swap/extracao'
        path3=path1+'swap/extracao/extracao_%s'%jar
        print('Pasta %s/swap/extracao criada'%path1)
    else:
        os.system('rm -rf %s/swap/'%path1)
        os.system('mkdir %s/swap/extracao/extracao_%s -p'%(path1,jar))
        path2=path1+'swap/extracao'
        path3=path1+'swap/extracao/extracao_%s'%jar
        print('Pasta swap re-criada')
        
    arqzip=open('extrair.py','w')
    arqzip.write('print(\'Primeira etapa: descompactando o ensamblado\')\n')
    arqzip.write('import os,sys,contextlib, zipfile \n\n')
    arqzip.write('with contextlib.closing(zipfile.ZipFile(\'%s/%s.ear\',\'r\')) as unz:\n'%(path1,app1))
    arqzip.write('    unz.extractall(\'%s\')\n\n'%path2)
    arqzip.close()
    os.system('chmod 775 extrair.py')
    os.system('python extrair.py')

    arqzip=open('extrair.py','w')
    arqzip.write('print(\'Segunda etapa: descompactando o jar\')\n')    
    arqzip.write('import os,sys,contextlib, zipfile \n\n')
    arqzip.write('with contextlib.closing(zipfile.ZipFile(\'%s/%s\',\'r\')) as unz:\n'%(path2,jar))
    arqzip.write('    unz.extractall(\'%s\')\n\n'%(path3))
    arqzip.write('print(\'Pacote extraido no caminho %s\')\n'%(path3))
    arqzip.close()
    os.system('chmod 775 extrair.py')
    os.system('python extrair.py') 
    
    if jar == 'SEGOP_CeControloperativoBrb_LN.jar':
        modifica_segop(path3,jar,env)        
    elif jar =='resource.jar':
        bla=0
        modifica_resource(path3,jar,camada)
    zip_ear(app1,path1,path3,jar)

def modifica_resource(path3,jar,camada):    
    print('para esta ação indifere para qual ambiente voce esta configurando\n Atualmente apenas os arquivos applicationSettings.xml e variableCfgSelector.xml estao sendo modificados \n Terceira etapa: Modificar o jar %s\')\n'%jar)
    
    arqmod=open('extrair.py','w')
    arqmod.write('# _*_ coding:utf-8 _*_\n')
    arqmod.write('import os,re,sys\n')
    arqmod.write('from xml.dom.minidom import DOMImplementation, Document,parse \n')
    arqmod.write('for dirname,subdirs,files in os.walk(\'%s%s\'):\n'%(path,jar))  
    arqmod.write('    for filename in files:\n')  
    arqmod.write('        if filename == \'applicationSettings.xml\':\n')  
    arqmod.write('            print(\'Arquivo atualmente sendo alterado: applicationSettings.xml \')\n')  
    arqmod.write('            domapp=parse(\'%s%s/applicationSettings.xml\')\n'%(path,jar))  
    arqmod.write('            childs = [node for node in domapp.childNodes if node.nodeType == domapp.ELEMENT_NODE]\n')  
    arqmod.write('            for parent in childs:\n')  
    arqmod.write('                childs2 = [node for node in parent.childNodes if node.nodeType == domapp.ELEMENT_NODE]\n')  
    arqmod.write('                for child in childs2:\n')  
    arqmod.write('                    if child.getAttribute(\'id\')==\'aeb.external.entity.alias\':\n')  
    arqmod.write('                        print(\'ID \'+child.getAttribute(\'id\')+ \' - Valor antes da modificacao: \'+child.firstChild.data)\n')  
    arqmod.write('                        child.firstChild.replaceWholeText(\'%sBrasil\')\n'%camada)  
    arqmod.write('                        print(\'ID \'+child.getAttribute(\'id\')+ \' - Valor APOS da modificacao: \'+child.firstChild.data)\n')  
    arqmod.write('        elif filename == \'variableCfgSelector.xml\':\n')  
    arqmod.write('            arqvar=open(\'%s%s/variableCfgSelector.xml\',\'r+\')\n'%(path,jar))  
    arqmod.write('            arqvard=open(\'%s%s/novo_variableCfgSelector.xml\',\'w\')\n'%(path,jar))  
    arqmod.write('            print(\'Arquivo atualmente sendo alterado: variableCfgSelector.xml \')\n')      
    arqmod.write('            lines = arqvar.readlines()\n')      
    arqmod.write('            for line in lines:\n')      
    arqmod.write('                pattern=r\'<environment>\'\n')      
    arqmod.write('                if re.search(pattern,line):\n')
    arqmod.write('                    print(\'Valor anterior %s\'%line)\n')
    arqmod.write('                    newvalue=re.sub(line,\'<environment>%s</environment>\',line)\n'%camada)
    arqmod.write('                    arqvard.write(newvalue.strip()+\'\\n\')\n')
    arqmod.write('                    print(\'Valor modificado %s\'%newvalue)\n')
    arqmod.write('                else:\n')
    arqmod.write('                    arqvard.write(line.strip()+\'\\n\')\n')      
    arqmod.write('            arqvar.close()\n')
    arqmod.write('            arqvard.close()\n')
    arqmod.write('domapp.writexml(open(\'%s%s/novo_applicationSettings.xml\',\'w\'),addindent=\'\',newl=\'\')\n'%(path,jar))
    arqmod.write('domapp.unlink()\n')
    arqmod.write('os.remove(\'%s%s/applicationSettings.xml\')\n'%(path,jar))
    arqmod.write('os.rename(\'%s%s/novo_applicationSettings.xml\',\'%s%s/applicationSettings.xml\')\n'%(path,jar,path,jar))
    arqmod.write('os.remove(\'%s%s/variableCfgSelector.xml\')\n'%(path,jar))
    arqmod.write('os.rename(\'%s%s/novo_variableCfgSelector.xml\',\'%s%s/variableCfgSelector.xml\')\n'%(path,jar,path,jar))
    arqmod.write('os.system(\'chmod -R 775 %s%s\')\n'%(path,jar))
    arqmod.close()
    os.system('chmod 775 extrair.py')
    os.system('python extrair.py') 
 
def modifica_segop(path3,jar,env):    
    if env=='PRE':
        env='MQCICK'
    elif env=='PRO':
        env='MQCICP'
    arqmod=open('extrair.py','w')
    arqmod.write('print(\'Terceira etapa: Modificar o jar %s\')\n'%jar)
    arqmod.write('import os,re,sys\n')
    arqmod.write('env = \'%s\'\n'%env)  
    arqmod.write('new=\'\'\n')  
    arqmod.write('amb=r\'MQCICG\'\n')  
    arqmod.write('ambq=r\'MQCICK\'\n')  
    arqmod.write('ambp=r\'MQCICP\'\n')  
    arqmod.write('for dirname,subdirs,files in os.walk(\'%s\'):\n'%(path3))  
    arqmod.write('    for filename in files:\n')  
    arqmod.write('        if filename == \'SEGOP_ControlOperativo.properties\':\n')  
    arqmod.write('            newfile = open(dirname+\'/SEGOP_ControlOperativo.properties1\',\'w\')\n')
    arqmod.write('            with open(dirname+\'/\'+filename,\'r+\') as segop:\n')  
    arqmod.write('                linhas = segop.readlines()\n')  
    arqmod.write('                for linha in linhas:\n')
    arqmod.write('                    if re.search(ambq,linha):\n')
    arqmod.write('                        print(\'achei %s\'%linha)\n')
    arqmod.write('                        newfile.write(re.sub(ambq,env,linha))\n')
    arqmod.write('                    elif re.search(amb,linha):\n')
    arqmod.write('                        print(\'achei %s\'%linha)\n')
    arqmod.write('                        newfile.write(re.sub(amb,env,linha))\n')
    arqmod.write('                    else:\n')
    arqmod.write('                        newfile.write(linha)\n')
    arqmod.write('            newfile.close()\n')
    # arqmod.write('            os.system(\'rm SEGOP_ControlOperativo.properties\')\n')
    arqmod.write('            os.rename(dirname+\'/SEGOP_ControlOperativo.properties1\',dirname+\'/SEGOP_ControlOperativo.properties\')\n')
    arqmod.write('            print(\'arquivo modificado %s/%s\'%(dirname,filename))\n')
    arqmod.close()
    os.system('chmod 775 extrair.py')
    os.system('python extrair.py') 

def transacao():
    print('estao opcao foi preparada para aumentar em tempo de timeout de tempo de vida de transacao')
    cells = AdminConfig.list('Cell').split()    
    for cell in cells:
        cellName = AdminConfig.showAttribute(cell,'name')
        print('Nome da Celula ', cellName)
        nodes = AdminConfig.list('Node',cell).split()
        for node in nodes:
            nodeName = AdminConfig.showAttribute(node,'name')
            print('Nome do No: '+nodeName)
            servers = AdminControl.queryNames('type=Server,cell='+cellName+',node='+nodeName+',*').split()
            for server in servers:
                serverName = AdminControl.getAttribute(server,'name')
                print('nome do servidor ', serverName)
                ts = AdminControl.completeObjectName('cell='+cellName+',node='+nodeName+',process='+serverName+',type=TransactionService,*')
                print('Limites de tempo de transacao'+ ts)
                if ts != '':
                    AdminControl.setAttributes(ts, [['clientInactivityTimeout', 600],  ['totalTranLifetimeTimeout', 1200]])

def mod_amb(jarx2,ambx):
    arq_ema = open('ema.py','w')
    arq_ema.write('# _*_ coding:utf-8 _*_\n')
    arq_ema.write('from xml.dom.minidom import DOMImplementation, Document,parse \n')
    arq_ema.write('import os, sys, contextlib, zipfile \n')    
    arq_ema.write('for jars in os.listdir(\'/tmp/swap/\'):\n')
    arq_ema.write('    if jars == \''+jarx2+'\': \n')
    arq_ema.write('        domapp = parse(\'/tmp/swap/'+jarx2+'/applicationSettings.xml\')\n')
    arq_ema.write('        childs = [no for no in domapp.childNodes if no.nodeType == domapp.ELEMENT_NODE]\n')
    arq_ema.write('        for parent in childs:\n')
    arq_ema.write('            childs2 = [no for no in parent.childNodes if no.nodeType == domapp.ELEMENT_NODE]\n')
    arq_ema.write('            for child in childs2:\n')
    arq_ema.write('                if child.getAttribute(\'id\')==\'aeb.external.entity.alias\':\n')
    arq_ema.write('                    print(\'valor localizado \',child.firstChild.data)\n')
    arq_ema.write('                    child.firstChild.replaceWholeText(\''+ambx+'Brasil\')\n')
    arq_ema.write('                    print(\'valor alterado \',child.firstChild.data)\n')    
    arq_ema.write('        domapp.writexml(open(\'/tmp/swap/'+jarx2+'/novo_applicationSettings.xml\',\'w\'), addindent=\'  \',newl=\'\')\n')
    arq_ema.write('        doc = Document()                                                                                         \n')
    arq_ema.write('        root = doc.createElement(\'VariableCfgSelection\')                                                       \n')
    arq_ema.write('        ent = doc.createElement(\'entity\')                                                                      \n')
    arq_ema.write('        env = doc.createElement(\'environment\')                                                                 \n')
    arq_ema.write('        tpais = doc.createTextNode(\'Brasil\')                                                                   \n')
    arq_ema.write('        tinternet = doc.createTextNode(\'%s\')                                                             \n'%ambx)
    arq_ema.write('        doc.appendChild(root)                                                                                    \n')
    arq_ema.write('        root.appendChild(ent)                                                                                    \n')
    arq_ema.write('        root.appendChild(env)                                                                                    \n')
    arq_ema.write('        ent.appendChild(tpais)                                                                                   \n')
    arq_ema.write('        env.appendChild(tinternet)                                                                               \n')
    arq_ema.write('        doc.writexml(open(\'/tmp/swap/%s/novo_variableCfgSelector.xml\',\'w\'), addindent=\'  \', newl=\'\\n\')\n'%ambx)
    arq_ema.write('        doc.unlink()                                                \n')
    arq_ema.write('        os.remove(\'/tmp/swap/%s/applicationSettings.xml\')                                                \n'%ambx)
    arq_ema.write('        os.remove(\'/tmp/swap/%s/variableCfgSelector.xml\')                                                \n'%ambx)
    arq_ema.write('        os.rename(\'/tmp/swap/%s/novo_variableCfgSelector.xml\',\'/tmp/swap/%s/variableCfgSelector.xml\')\n'%(ambx,ambx))
    arq_ema.write('        os.rename(\'/tmp/swap/%s/novo_applicationSettings.xml\',\'/tmp/swap/%s/applicationSettings.xml\')\n'%(ambx,ambx))
    arq_ema.write('    elif jars==\'SEGOP_CeControloperativoBrb_LN\': \n')
    arq_ema.write('        bla=0\n')
    arq_ema.write('zf=zipfile.ZipFile(\'/tmp/swap/'+jarx2+'.jar\',\'w\')         \n')  
    arq_ema.write('os.chdir(\'/tmp/swap/'+jarx2+'\')\n')  
    arq_ema.write('for dirname,subdirs,files in os.walk(\'.\'): \n')
    arq_ema.write('    for file in files:                            \n')
    arq_ema.write('        zf.write(os.path.join(dirname,file))      \n')
    arq_ema.write('zf.close() \n')      
    arq_ema.close()
    os.system('python ema.py')
       
######## menu principal ##########
try:
    arqsys = open('SystemExit.log','w')
    if len(sys.argv)==0:
        print('Nenhum argumento informado')
        print('argumentos disponiveis: ATUALIZAR, ATUALIZAEAR, BIBLIOTECA, BULK, CONFIGURAR, CREAREAR, EMA, EMBEDDOR, EXPORTAR, GERAR, INICIAR, INSTALAR, LISTARQ,LISTAR, PARAR, SESSAO, SGS, SINCRONIZAR e TRANSACAO. para AJUDA nao use argumentos')  
    elif sys.argv[0] == 'LISTAR':
        if len(sys.argv) == 2:
            arg = sys.argv[1]
            print('informado argumento. extracao detalhada sera adicionada em SystemOut.log')
            listar(arg)
        else:
            print('nenhum argumento informado')
            listar()
    elif sys.argv[0] == 'UNSESSION':
        unsession()
    elif sys.argv[0]=='EXPORTAR':
        if len(sys.argv) == 3:
            if sys.argv[1]=='TODOS':
                app1 = 'TODOS'
                path = sys.argv[2]
            elif sys.argv[1]!='':
                app1=sys.argv[1]
                path = sys.argv[2]
            exportar(app1,path)
        else:
            print('informar nome do ensamblado e o caminho para exportar')
    elif sys.argv[0]=='ATUALIZAR':
        if len(sys.argv)==4:
            app1 = sys.argv[1]; path = sys.argv[2];pathear = sys.argv[3]
            print('Ensamblado: ' + app1 + ' - Caminho origem: ' + path + ' - Caminho destino: ' + pathear)
            atualizar(app1,path,pathear)
        else:
            print('nãofoi informado os argumentos necessáos')        
    elif sys.argv[0]=='GERAR':
        if len(sys.argv) == 2:
            arg1 = sys.argv[1]
            gerar(arg1)
        else:
            print('informar nome do arquivo')               
    elif sys.argv[0] == 'INSTALAR':
        if len(sys.argv)==4:
            app1 = sys.argv[1]; path = sys.argv[2]; cluster = sys.argv[3]
            instalar(app1,path,cluster)        
        else:
            print('favor informar a aplicacao e o cluster a ser instalado')
    elif sys.argv[0] == 'SINCRONIZAR':
        if len(sys.argv)==1:
            sincroniza()        
        else:
            print('favor informar a aplicacao e o cluster a ser instalado')
    elif sys.argv[0] == 'ATUALIZAEAR':
        if len(sys.argv)==4:
            print('opcao escolhida %s' %sys.argv[0])
            print('app %s. caminho %s. Cluster %s' %(sys.argv[1],sys.argv[2],sys.argv[3]))
            app1 = sys.argv[1]; path = sys.argv[2]; cluster = sys.argv[3]
            atualizaear(app1,path,cluster)        
        else:
            print('favor informar a aplicacao e o cluster a ser instalado')
    elif sys.argv[0] == 'CONFIGURAR':
        print('opcao escolhida', sys.argv[0])
        if len(sys.argv)==3:
            apl = sys.argv[1]
            bib = sys.argv[2]
            configurar(apl,bib)
        else:
            print('favor informar o pacote e a biblioteca com as configuracoes')        
    elif sys.argv[0] == 'CONFIGURA_BIBLIOTECA':
        print('opcao escolhida', sys.argv[0])
        if len(sys.argv)==2:
            silent = sys.argv[1]
            cfgbiblioteca(silent)
        else:
            print('favor informar o arquivo silent para configurao de bibliotecas de forma nao-assistidas')
    elif sys.argv[0] == 'CONFIGURA_MAPEAMENTO':
        print('opcao indisponivel', sys.argv[0])
    elif sys.argv[0] == 'BULK':
        file = sys.argv[1]
        bulk(file)
    elif sys.argv[0] == 'SGS':
        if len(sys.argv)==3:
            usr=sys.argv[1]
            pwd=sys.argv[2]
            sgs(usr,pwd)
        else:
            print('Execucao nao realizada. Favor informar o usuario e senha')
    elif sys.argv[0] == 'SESSAO':
        app1 = sys.argv[1]
        configuraear(app1)
    elif sys.argv[0] == 'LISTARQ':
        listarq()
    elif sys.argv[0] == 'LISTALIB':
        listabibl()    
    elif sys.argv[0] == 'TRANSACAO':
        transacao()
    elif sys.argv[0] == 'INICIAR':
        app1 = sys.argv[1]
        startapps(app1)
    elif sys.argv[0] == 'PARAR':
        app1 = sys.argv[1]
        stopapps(app1)
    elif sys.argv[0] == 'STATUS':
        statusapps()
    elif sys.argv[0] == 'EMBEDDOR':
        embeddor()
    elif sys.argv[0] == 'EXTRAIR':
        if len(sys.argv)==6:
            app1 = sys.argv[1]; path1 = sys.argv[2]; jar = sys.argv[3]; env = sys.argv[4]; camada = sys.argv[5]
            extrair(app1,path1,jar,env,camada)
        else:
            print('argumentos: ensamblado, caminho, jar, ambiente (PRE/PRO) e camada (Internet/Intranet/Internet) \n Arquivos pre-definidos para modificacao: SEGOP_CeControloperativoBrb_LN.jar, resource.jar e langs em andamento')
    elif sys.argv[0] == 'REPLIWEB':
        if len(sys.argv)==3:
            usr=sys.argv[1]
            pwd=sys.argv[2]
            repliweb(usr,pwd)
        else:
            print('Favor informar usuario e senha')
    elif sys.argv[0] == 'UPDARQ':
        if len(sys.argv)==2:
            arq = sys.argv[1]
            bulkarq(arq)
        else:
            print('necessário informar arquitetura que alterara todas as aplicações do ambiente ')
    elif sys.argv[0] == 'CREAEAR':
        app1 = sys.argv[1]
        silent = sys.argv[2]
        creaear(app1,silent)
    elif sys.argv[0] == 'MAPEAR':
        if len(sys.argv)== 3:
            app1 = sys.argv[1]
            cluster = sys.argv[2]
            mapear(app1,cluster)
    elif sys.argv[0] == 'APPCLUSTER':
        if len(sys.argv)==1:
            silent = sys.argv[1]
            appscluster(silent)           
        else:
            print('necessario informar o arquivo silent para instalacao')
    elif sys.argv[0]== 'AJUDA':
        print('*'* 120)
        print('Favor informar como parametro uma das opcoes: ATUALIZAR, ATUALIZAEAR, BIBLIOTECA, BULK, CONFIGURA_BIBLIOTECA, CONFIGURA_MAPEAR, CONFIGURAR, CREAEAR, INSTALAR, EXPORTAR, GERAR, LISTALIB, LISTARQ,LISTAR, MAPEAR ou SINCRONIZAR')
        print('### Rotina criada para uso da equipe de gestao de cambios / configuracao e despliegue       ###')
        print('### permite atualizar, exportar, instalar,gerar, listar e sincronizar as aplicacoes         ###')
        print('### abaixo exemplo de sintaxe                                                               ###')
        print('###-----------------------------------------------------------------------------------------###')
        print('### gestao.py ATUALIZAR ENS_ENS CAMINHO_ARQ CAMINHO_EAR   | ens_ens (ensamblado) CAMINHO_ARQ (arquivo atualizado), CAMINHO_EAR (dentro ENS)###')
        print('### Atencao: para esta opcao quando for na raiz do ENS coloque /, caso contrario inicie o caminho completo com pasta xxx_ESCE.was/subpasta ###')
        print('### gestao.py ATUALIZAEAR ENS_ENS CAMINHO_ARQ CAMINHO_EAR | ens_ens (ensamblado) CAMINHO_ARQ (arquivo atualizado), CAMINHO_EAR (dentro ENS)###')
        print('### gestao.py APPSCLUSTER silent                          | ens_ens (ensamblado) CAMINHO_ARQ (arquivo atualizado), CAMINHO_EAR (dentro ENS)###')
        print('### gestao.py CREAEAR ENS_ENS                             | necessita de um arquivo gestao.silent com o caminho template                   ###')
        print('### gestao.py BIBLIOTECA arquivo.silent*                  | extrai aplicacoes e bibliotecas associadas                                     ###')
        print('### gestao.py BULK arquivo.silent                         | arquivo com configuracoes de sessao, biblioteca e mapeamento                   ###')
        print('### gestao.py UPDARQ V36SP04F09                           | configura todas as aplicacoes na arquitetura informada como argumento          ###')
        print('### gestao.py CONFIGURA_BIBLIOTECA ENS_ENS BIBLIOTECA     | Alterar a biblioteca da aplicacao - instalacao nao-assistida                   ###')
        print('### gestao.py CONFIGURA_MAPEAR ENS_ENS BIBLIOTECA         | Alterar o mapeamento da aplicacao - instalacao nao-assistida                   ###')
        print('### gestao.py EMBEDDOR                                    |                                                                                ###')
        print('### gestao.py EXPORTAR TODOS /CAMINHO                     | exporta todos os pacotes instalados neste ambiente para o caminho              ###')
        print('### gestao.py EXPORTAR ENS_ENS /CAMINHO                    | exporta somente o arquivo informado colocando                                 ###')
        print('### gestao.py EXTRAIR ensamblado caminho jar ambiente (PRE/PRO) camada (Internet/Intranet/Internet)                                        ###')
        print('### >>> para esta opcao temos mapeados as alteracoes para as seguintes opcoes:                                                             ###')
        print('### >>>     SEGOP_CeControloperativoBrb_LN.jar                                                                                             ###')
        print('### >>>     resource.jar                                                                                                                   ###')
        print('### gestao.py GERAR ARQUIVO                               | ex.: esta opcao gera o properties e a pasta de EarEstatico do pacote desejado  ###')
        print('###                                                       | E necessario que tenha um arquivo com os pacotes a serem gerados               ###')
        print('### gestao.py INICIAR ENS_ENS                             | iniciar a aplicacao                                                            ###')
        print('### gestao.py INSTALAR ENS_ENS CAMINHO_ARQ CAMINHO_EAR    | ens_ens (ensamblado) CAMINHO_ARQ (arquivo atualizado), CAMINHO_EAR (dentro ENS)###')
        print('### gestao.py LISTAR                                      | lista aplicacoes do ambiente distribuidos                                      ###')
        print('### gestao.py LISTAR xxx                                  | lista aplicacoes do ambiente distribuidos por clusters e suas bibliotecas     ###')
        print('### gestao.py LISTA-BIBLIOTECAS                           | lista bibliotecas associadas as aplicacoes do ambiente                         ###')
        print('### gestao.py LISTA-ARQUITETURAS                          | lista aplicacoes do ambiente distribuidos por clusters e suas bibliotecas      ###')
        print('### gestao.py MAPEAR                                      | mapear bibliotecas e arquituras nas aplicacoes no arquivo gestao.silent        ###')   
        print('### gestao.py PARAR ENS_ENS                               | para a aplicacao                                                               ###')
        print('### gestao.py RESTARTAR ENS_ENS                           | para a aplicacao                                                               ###')
        print('### gestao.py SESSAO ENS_ENS                              | sincronizacao de todo o ambiente                                               ###')
        print('### gestao.py SINCRONIZAR                                 | sincronizacao de todo o ambiente                                               ###')
        print('*'* 120)
    else:  
        print('Nenhum argumento localizado')
finally:
    arqsys.close()
