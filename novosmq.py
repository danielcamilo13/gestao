import sys,os

def new_mq(qmanager,queue):
    print('Queue Manager: %s - Queue name(initial): %s'%(qmanager,queue))
    cells = AdminConfig.list('Cell').split()
    for cell in cells:
        cellName = AdminConfig.showAttribute(cell,'name')
        print('Nome da celula a ser modificada: %s' %cellName)
        nodes = AdminConfig.list('Node',cell).split()
        qmfactories = AdminTask.listWMQConnectionFactories(cell).split()
        print('cell factories %s. Scoped by cell'%qmfactories)
        for node in nodes:
            try:
                nodeName = AdminConfig.showAttribute(node,'name')
                nodeHostName = AdminConfig.showAttribute(node,'hostName')
                print('Nome do No: %s'%nodeName.split('.')[0])
                arqsys.write('Nome do No: %s\n'%nodeName.split('.')[0])
                nameSplit = nodeName.split('.')[0]
                nr=nameSplit[-2:]
                getnodeid = AdminConfig.getid('/Node:'+nodeName)
                #Verificando as Connection Factories do ambiente
                # AdminTask.createWMQConnectionFactory(''+getnodeid+'','[-type QCF -name '+qmanager+' -jndiName jms/'+qmanager+' -description "created by Deployment team" -qmgrName QM.BKSBIO.'+nr+' -wmqTransportType BINDINGS_THEN_CLIENT -qmgrHostname '+nodeHostName+' -qmgrPortNumber 1414 -qmgrSvrconnChannel CHANNEL1 ]')
                # AdminTask.createWMQQueue(''+getnodeid+'', '[-name '+queue+' -jndiName jms/'+queue+' -queueName EGR.E.BIO03 -qmgr QM.BKSBIO.'+nr+' -description ]')
                # AdminConfig.save()

                wqms = AdminTask.listWMQConnectionFactories(node).split()
                wqueues = AdminTask.listWMQQueues(node).split()
                print('Connection Factory %s  |  Queues %s'%(wqms,wqueues))
                for wqm in wqms:
                    print(AdminTask.showWMQConnectionFactory(wqm).split(',')[9])
                    # arqsys.write('Connection nao localizada. Efetuando a criacao da Connection %s\n'%qmanager)
                    AdminTask.modifyWMQConnectionFactory(''+wqm+'', '[-persistence NON -priority 6 -expiry UNLIM -ccsid 1208 -useNativeEncoding true -integerEncoding Normal -decimalEncoding Normal -floatingPointEncoding IEEENormal -useRFH2 false -sendAsync QDEF -readAhead QDEF -readAheadClose DELIVERALL ]')

                for wqueue in wqueues:
                    print(AdminTask.showWMQQueue(wqueue).split(',')[4])
                    # arqsys.write('Fila nao localizada. Efetuando a criacao da fila %s\n'%queue)
                    AdminTask.modifyWMQQueue(''+wqueue+'', '[-persistence NON -priority 6 -expiry UNLIM -ccsid 1208 -useNativeEncoding true -integerEncoding Normal -decimalEncoding Normal -floatingPointEncoding IEEENormal -useRFH2 false -sendAsync QDEF -readAhead QDEF -readAheadClose DELIVERALL ]')
                AdminConfig.save()
            except:
                print('nao ha fila de mq neste escopo ou fila ja esta configurada')
                continue
    print('execucao finalizada. Veja o resultado no arquivo SystemExit.log')

arqsys = open('SystemExit.log','w')                
qmanager = sys.argv[0]
queue=sys.argv[1]
new_mq(qmanager,queue)
arqsys.close()



                        # print('Factory existente '+AdminTask.showWMQConnectionFactory(wqm))
                        # print('desativando o cabecalho RFH ')
                        # AdminTask.modifyWMQConnectionFactory(wqm, '[-persistence APP -priority APP -expiry APP -ccsid 1208 -useNativeEncoding true -integerEncoding Normal -decimalEncoding Normal -floatingPointEncoding IEEENormal -useRFH2 false -sendAsync QDEF -readAhead QDEF -readAheadClose DELIVERALL ]')
                        # AdminConfig.save()
                # else:
                    # print('criando fila e modificando')
                    # AdminTask.createWMQConnectionFactory(''+getnodeid+'','[-type QCF -name PLPLBI_qcf -jndiName jms/PLPLBI_qcf -description "created by Despliegue team" -qmgrName QM.BKSBIO.'+nr+' -wmqTransportType BINDINGS_THEN_CLIENT -qmgrHostname '+nodeHostName+' -qmgrPortNumber 1414 -qmgrSvrconnChannel CHANNEL1 ]')
                    # AdminTask.modifyWMConnectionFactory(wqm, '[-persistence APP -priority APP -expiry APP -ccsid 1208 -useNativeEncoding true -integerEncoding Normal -decimalEncoding Normal -floatingPointEncoding IEEENormal -useRFH2 false -sendAsync QDEF -readAhead QDEF -readAheadClose DELIVERALL ]')
                    # AdminConfig.save()
                # wqueues = AdminTask.listWMQQueues(node).split()
                # print('estas sao as filas criadas')
                # if wqueues !='':
                    # for wqueue in wqueues:
                        # nameQueue = AdminTask.showWMQQueue(wqueue).split(',')[4]
                        # AdminTask.modifyWMQQueue(wqueue, '[-persistence NON -priority 6 -expiry UNLIM -ccsid 1208 -useNativeEncoding true -integerEncoding Normal -decimalEncoding Normal -floatingPointEncoding IEEENormal -useRFH2 false -sendAsync QDEF -readAhead QDEF -readAheadClose DELIVERALL ]')
                        # print('nome da fila>>>>>>> %s'%nameQueue)
                        # AdminConfig.save()
                # else:
                    # AdminTask.createWMQQueue(''+getnodeid+'', '[-name PLPLBI_RequestQueue -jndiName jms/PLPLBI_RequestQueue -queueName EGR.E.BIO03 -qmgr QM.BKSBIO.'+nr+' -description ]')
                    # AdminConfig.save()
                    
# AdminTask.createWMQConnectionFactory('"WebSphere MQ JMS Provider(cells/gerH/nodes/wasbioivlbr06.bs.br.bschNode|resources.xml#builtin_mqprovider)"', '[-type QCF -name name -jndiName jndi_name -description "created by routine" -qmgrName qm_name -wmqTransportType BINDINGS_THEN_CLIENT -qmgrHostname server -qmgrPortNumber 1414 -qmgrSvrconnChannel CHANNEL1 ]')
# AdminTask.createWMQQueue('wasbioivlbr06(cells/gerH/nodes/wasbioivlbr06.bs.br.bschNode/servers/wasbioivlbr06|server.xml)', '[-name name -jndiName jndi_name -queueName queue_name -qmgr qm_name -description ]')


# AdminTask.modifyWMQQueue('PLPLBI_RequestQueue(cells/Real_gerenciador/nodes/wasbioivlbr32.bs.br.bschNode|resources.xml#MQQueue_1492541214805)', '[-persistence NON -priority 6 -expiry UNLIM -ccsid 1208 -useNativeEncoding true -integerEncoding Normal -decimalEncoding Normal -floatingPointEncoding IEEENormal -useRFH2 false -sendAsync QDEF -readAhead QDEF -readAheadClose DELIVERALL ]') 
# AdminTask.modifyWMQConnectionFactory('PLPLBI_qcf(cells/Real_gerenciador/nodes/wasbioivlbr12.bs.br.bschNode|resources.xml#MQQueueConnectionFactory_1492542346658)', '[-modelQueue SYSTEM.DEFAULT.MODEL.QUEUE -tempQueuePrefix -rescanInterval 5000 -msgRetention TRUE -replyWithRFH2 AS_REPLY_DEST -pollingInterval 5000 -ccsid 819 -maxBatchSize 10 -compressHeaders NONE -compressPayload NONE -failIfQuiescing true ]') 
# AdminTask.modifyWMQConnectionFactory('MQJMSFactory(cells/Shadow_PortalBKSCell02|resources.xml#MQQueueConnectionFactory_1413316432480)', '[-name MQJMSFactory -jndiName jms/Factory -description -qmgrName QM.BIO.01 -wmqTransportType BINDINGS_THEN_CLIENT -qmgrHostname SRVBIOPVWBR01 -qmgrPortNumber 1414 -qmgrSvrconnChannel CHANNEL1 -sslType NONE -clientId -providerVersion -mappingAlias DefaultPrincipalMapping -containerAuthAlias -componentAuthAlias -xaRecoveryAuthAlias -support2PCProtocol true ]') 