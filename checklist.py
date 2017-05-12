# -*- coding: utf-8 -*-

############################################################################################################################
##  Data de modificação 20/04/2017                                                                                        ##
############################################################################################################################



import os, sys, java

global AdminApp
global AdminControl
global AdminConfig

def listar():
    cells = AdminConfig.list('Cell').split()
    for cell in cells:
        variables = AdminConfig.list('VariableSubstitutionEntry',cell).split()
        cellName = AdminConfig.showAttribute(cell,'name')
        print('#' * 98)
        print('Checklist do ambiente. Nome da celula %s'%cellName)
        print('#' * 98)
        arqsys.write('#' * 98)
        arqsys.write('\n########  Checklist do ambiente. Nome da celula '+cellName+' ##########\n')
        arqsys.write('#'*84+'\n')    
        for variable in variables:
            variableLinkName = AdminConfig.showAttribute(variable,'symbolicName')
            variableName = AdminConfig.showAttribute(variable,'value')
            if variableLinkName == 'CELLID':
                arqsys.write('Variavel CELLID: %s\n'%variableName)
        nodes = AdminConfig.list('Node',cell).split()
        arqsys.write('*** Nodes & HostNames ***\n')        
        for node in nodes:
            nodeName = AdminConfig.showAttribute(node,'name')
            nodehostName = AdminConfig.showAttribute(node,'hostName')
            arqsys.write('Node name: %s | hostName: %s \n'%(nodeName,nodehostName))
        arqsys.write('\n')
        webservers = AdminConfig.list('WebServer',cell).split()
        arqsys.write('*** Servidores WEB ***\n')        
        for webserver in webservers:
            webName = AdminConfig.showAttribute(webserver,'name')
            arqsys.write('servidor WEB ' + webName + '\n')
        arqsys.write('\n')
        clusters = AdminConfig.list('ServerCluster', cell).split()
        arqsys.write('*** Clusters ***\n')
        for cluster in clusters:
            clusterName = AdminConfig.showAttribute(cluster,'name')
            arqsys.write('Cluster ' + clusterName + '\n')
        arqsys.write('\n')
        arqsys.write('*'*90+'\n')
        arqsys.write('--- Configuracao de HA, MQ e JVM Arguments ---\n')
        arqsys.write('*'*90+'\n')
        for node in nodes:
            nodeName = AdminConfig.showAttribute(node,'name')
            nodehostName = AdminConfig.showAttribute(node,'hostName')
            arqsys.write('_'*90)
            arqsys.write('\n|Node name: %s | hostName: %s |\n'%(nodeName,nodehostName))
            arqsys.write('_'*90+'\n')
            try:
                servers = AdminControl.queryNames('type=Server,cell='+cellName+',node='+nodeName+',*').split()
                wfactories = AdminTask.listWMQConnectionFactories(node).split()
                wqueues = AdminTask.listWMQQueues(node).split()
                has = AdminConfig.list('HAManagerService',node).split()
                if wfactories != '':
                    arqsys.write('\n*** MQ Connection Factories ***\n')
                    for wfactory in wfactories:
                        wfactoryName = AdminTask.showWMQConnectionFactory(wfactory)
                        arqsys.write('Connection Factory: %s' %wfactoryName.split(',')[33]+ '\n')
                        arqsys.write('Connection Factory - detalhado %s\n' %wfactoryName)
                arqsys.write('\n*** MQ Queues ***\n')
                if wqueues != '':
                    for wqueue in wqueues:
                        wqueueName = AdminTask.showWMQQueue(wqueue)
                        arqsys.write('MQ queue %s\n'%wqueueName.split(',')[12])
                        arqsys.write('MQ queue - detalhado %s\n '%wqueueName)
                arqsys.write('\n*** Configuracao de HA - Alta disponibilidade ***\n ')
                if has != '':
                    for ha in has:
                        en1 = AdminConfig.showAttribute(ha,'enable');en2 = AdminConfig.showAttribute(ha,'activateEnabled');tp = AdminConfig.showAttribute(ha,'threadPool')
                        if en1 == 'true' or en2 == 'true':
                            arqsys.write('Processo Java: ' + tp.split('/')[5]+ '\n')
                            arqsys.write('-'* 50 + '\n')
                            arqsys.write('<<<<<\'HA\' esta HABILITADO neste NO. Favor rever configuracao>>>>>\n')
                            arqsys.write('-'* 50 + '\n')
                        else:
                            arqsys.write('Processo Java: ' + tp.split('/')[5])
                            arqsys.write('\'HA\' DESABILITADO neste NO\n')
                arqsys.write('\n*** Configuracao JVM Arguments ***\n')
                for server in servers:
                    serverName = AdminControl.getAttribute(server,'name')
                    jvmprops = AdminTask.showJVMProperties('[-serverName '+serverName+' -nodeName '+nodeName+' -propertyName genericJvmArguments]')
                    arqsys.write('Servidor: %s Argumento JVM: %s\n'%(serverName,jvmprops))
                    arqsys.write('\n*** Portas***\n')
                    ports = AdminConfig.list('NamedEndPoint', node).split()
                    for port in ports:
                        endp = AdminConfig.showAttribute(port,'endPoint')
                        portName = AdminConfig.showAttribute(port,'endPointName')
                        pt = AdminConfig.showAttribute(endp,'port')
                        portHost = AdminConfig.showAttribute(endp,'host')
                        if portHost != '*':
                            arqsys.write('Portas: '+ str(portHost)+ ' | '+ str(portName) + ' | ' + pt+'\n')                
            except:
                arqsys.write('%s = HA, MQ ou argumento de processo Java nao localizada neste escopo \n'%nodeName)
                continue
                    
        # clusters = AdminConfig.list('ServerCluster', cell).split()
        # arqsys.write('*** Configuracao de Clusters ***\n')
        # for cluster in clusters:
            # clusterName = AdminConfig.showAttribute(cluster,'name')
            # print(clusterName)
            # arqsys.write('Cluster ' + clusterName + '\n')
            # wmqs = AdminTask.listWMQQueues(cluster).split()
            # if wmqs != '':
                # for wmq in wmqs:
                    # wmqName = AdminTask.showWMQQueue(wmq)
                    # print('Filas ', wmqName)
                    # arqsys.write('MQ connection ' + wmqName.split(',')[12] + '\n')
            # else:
                # arqsys.write('Nao ha configuracao de MQ neste processo \n')
    
def modificar():
    print('opcao disponivel somente desabilitar HA')
    cells = AdminConfig.list('Cell').split()    
    for cell in cells:
        cellName = AdminConfig.showAttribute(cell,'name')      
        nodes = AdminConfig.list('Node',cell).split()
        for node in nodes:
            try:
                nodeName = AdminConfig.showAttribute(node,'name')

                wmqs = AdminTask.listWMQQueues(node).split()
                for wmq in wmqs:
                    print('queues ', wmqs)
                    arqsys.write('MQ connection ' + wmq + '\n')
                    AdminTask.modifyWMQQueue(wmq, '[-persistence APP -priority APP -expiry APP -ccsid 1208 -useNativeEncoding true -integerEncoding Normal -decimalEncoding Normal -floatingPointEncoding IEEENormal -useRFH2 false -sendAsync QDEF -readAhead QDEF -readAheadClose DELIVERALL ]')
                    AdminConfig.save()
                # AdminTask.modifyWMQQueue('ReceiveQueue(cells/waspaypvlbr14/nodes/waspaypvlbr13Node01|resources.xml#MQQueue_1472308052343)', '[-persistence APP -priority APP -expiry APP -ccsid 1208 -useNativeEncoding true -integerEncoding Normal -decimalEncoding Normal -floatingPointEncoding IEEENormal -useRFH2 true -sendAsync QDEF -readAhead QDEF -readAheadClose DELIVERALL ]')

                HAs = AdminConfig.list('HAManagerService',node).split()
                count = 0
                for ha in HAs:
                    count+=1
                    print(ha , count)
                    AdminConfig.modify(ha, '[[isAlivePeriodSec "120"] [transportBufferSize "10"] [enable "false"] [activateEnabled "false"]]')
                    AdminConfig.save()
                
                if not nodeName.startswith('Dmgr') and nodeName.startswith('IHS'):
                    print('Neste no não sera modificado o HA ' +nodeName)
                    sync1 = AdminControl.completeObjectName('type=NodeSync,process=nodeagent,node='+nodeName+',*')
                    print(sync1)
            except:
                continue

def jvmargs():
    cells = AdminConfig.list('Cell').split()
    for cell in cells:
        cellName = AdminConfig.showAttribute(cell,'name')
        print('Nome da célula ', cellName)
        nodes = AdminConfig.list('Node',cell ).split()
        for node in nodes:
            nodeName = AdminConfig.showAttribute(node,'name')
            nodeHostName = AdminConfig.showAttribute(node,'hostName')
            print('>>>>>>> Nome do No: ', nodeName)
            print('Nome do Host: ', nodeHostName)
            print('--------------------------------')
            clusters = AdminConfig.list('ServerCluster',cell).split()
            for cluster in clusters:
                clusterName = AdminConfig.showAttribute(cluster,'name')
                members = AdminConfig.list('ClusterMember',cluster).split()
                # print('Nome do cluster: ', clusterName)
                for member in members:
                    memberName = AdminConfig.showAttribute(member,'memberName')
                    # print('Membro ', memberName)
                    servers = AdminControl.queryNames('type=Server,cell='+cellName+',node='+nodeName+',*').split()
            for server in servers:
                serverName = AdminControl.getAttribute(server,'name')
                if not serverName.startswith('nodeagent') or not serverName.startswith('dmgr'):
                    print('Servidor | ' + serverName)
                    # jvmprops = AdminTask.showJVMProperties('[-serverName '+serverName+' -nodeName '+nodeName+'  -propertyName genericJvmArguments]').split('[]')  
                    
                    AdminTask.setJVMProperties('[-serverName '+serverName+' -nodeName '+nodeName+' -verboseModeClass false -verboseModeGarbageCollection true -verboseModeJNI false -initialHeapSize 1024 -maximumHeapSize 2048 -runHProf false -hprofArguments -debugMode false -debugArgs "-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=7777" -genericJvmArguments "-Daeb.CELLNAME=$(CELLID) -Daeb.iiop=${iiopVar} -Daeb.ldapServer.server=${ldapVar} -Dclient.encoding.override=ISO-8859-1 -Daeb.usuario.ALTAIR=${USER_ALTAIR}-Daeb.metricas=${METRICAS_BKS} -Dcom.ibm.websphere.servlet.temp.dir=/opt/WebSphere7/tmpjsp -Dcom.wily.introscope.agentProfile=/opt/wily/wilyAgent/core/config/IntroscopeAgent.profile -Dfile.encoding=ISO-8859-1 -Dsun.rmi.dgc.server.gcInterval=1800000 -javaagent:/opt/wily/wilyAgent/AgentNoRedefNoRetrans.jar -DserverName=${WAS_SERVER_NAME} -Dwebsphere.workspace.root=/opt/WebSphere7/AppServer/wstemp -Xverbosegclog:${SERVER_LOG_ROOT}/gc#.txt,10,1000 -Xdump:stack:events=allocation,filter=#1m -Xdump:java:defaults:file=javacore.${WAS_SERVER_NAME}.%H%M%S.txt -Xnocompressedrefs -Xgcpolicy:gencon"]') 
                    print(jvmprops)
                    AdminConfig.save()

def new_mq(qmanager,queue):
    print('Queue Manager: %s - Queue name(initial): %s'%(qmanager,queue))
    cells = AdminConfig.list('Cell').split()
    for cell in cells:
        cellName = AdminConfig.showAttribute(cell,'name')
        nodes = AdminConfig.list('Node',cell).split()
        qmfactories = AdminTask.listWMQConnectionFactories(cell).split()
        print('Nome da celula a ser modificada: %s' %cellName)
        print('cell factories %s. Scoped by cell'%qmfactories)
        for node in nodes:
            try:
                nodeName = AdminConfig.showAttribute(node,'name')
                nodeHostName = AdminConfig.showAttribute(node,'hostName')
                arqsys.write('Nome do No: %s\n'%nodeName.split('.')[0])
                nameSplit = nodeName.split('.')[0]
                nr=nameSplit[-2:]
                getnodeid = AdminConfig.getid('/Node:'+nodeName)
                #Verificando as Connection Factories do ambiente
                AdminTask.createWMQConnectionFactory(''+getnodeid+'','[-type QCF -name '+qmanager+' -jndiName jms/'+qmanager+' -description " " -qmgrName QM.BKSBIO.'+nr+' -wmqTransportType BINDINGS_THEN_CLIENT -qmgrHostname '+nodeHostName+' -qmgrPortNumber 1414 -qmgrSvrconnChannel CHANNEL1 ]')
                AdminTask.createWMQQueue(''+getnodeid+'', '[-name '+queue+' -jndiName jms/'+queue+' -queueName EGR.E.BIO03 -qmgr QM.BKSBIO.'+nr+' -description ]')
                AdminConfig.save()

                wqms = AdminTask.listWMQConnectionFactories(node).split()
                wqueues = AdminTask.listWMQQueues(node).split()
                print('Connection Factory %s  |  Queues %s'%(wqms,wqueues))
                for wqm in wqms:
                    try:
                        print(AdminTask.showWMQConnectionFactory(wqm).split(',')[9])
                        # arqsys.write('Connection nao localizada. Efetuando a criacao da Connection %s\n'%qmanager)
                        AdminTask.modifyWMQConnectionFactory(''+wqm+'', '[-persistence NON -priority 6 -expiry UNLIM -ccsid 1208 -useNativeEncoding true -integerEncoding Normal -decimalEncoding Normal -floatingPointEncoding IEEENormal -useRFH2 false -sendAsync QDEF -readAhead QDEF -readAheadClose DELIVERALL ]')
                    except:
                        print('algum erro ocorreu ao executar a criacao da factory. Favor verificar ')
                        continue
                for wqueue in wqueues:
                    try:
                        print(AdminTask.showWMQQueue(wqueue).split(',')[4])
                        # arqsys.write('Fila nao localizada. Efetuando a criacao da fila %s\n'%queue)
                        AdminTask.modifyWMQQueue(''+wqueue+'', '[-persistence NON -priority 6 -expiry UNLIM -ccsid 1208 -useNativeEncoding true -integerEncoding Normal -decimalEncoding Normal -floatingPointEncoding IEEENormal -useRFH2 false -sendAsync QDEF -readAhead QDEF -readAheadClose DELIVERALL ]')
                    except:
                        print('algum erro ocorreu ao executar a criacao da fila. Favor verificar ')
                        continue
                AdminConfig.save()
            except:
                print('%s nao ha connection neste escopo'%node)
                    
arqsys = open('SystemExit.log','w')
if len(sys.argv)==0:
    print('E necessário informar um argumento')
    print('opcoes disponiveis: ARGUMENTO,CRIARMQ,LISTAR ou MODIFICAR')
elif sys.argv[0]=='LISTAR':
    listar()
elif sys.argv[0]=='MODIFICAR':
    modificar()
elif sys.argv[0] == 'ARGUMENTO':
    jvmargs()
elif sys.argv[0] == 'CRIARMQ':
    if len(sys.argv)==3:
        qmanager = sys.argv[1]
        queue=sys.argv[2]
        new_mq(qmanager,queue)
    else:
        print('necessario informar a connection Factory e a fila. Exemplo jms/Factory jms/Send')
print('execucao finalizada. Veja o log gerado no SystemExit.log')    
arqsys.close()