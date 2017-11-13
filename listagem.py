
def listar( ):
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
        print('Nome da Celula: %s'%cellName)
        nodes = AdminConfig.list('Node',cell).split(); clusters = AdminConfig.list('ServerCluster', cell).split(); webservers = AdminTask.listServers('[-serverType WEB_SERVER ]').split()
        for cl in clusters:
            clName = AdminConfig.showAttribute(cl,'name')
            print('Cluster | ' + clName)
        print('\n-----  Servidores WEB -----')
        for web in webservers:
            print('Web Server | ' + web.split('(')[0])            
        nodes = AdminConfig.list('Node',cell).split()
        print('extraindo as informacoes detalhadas desta celula')
        for node in nodes:
            nodeName = AdminConfig.showAttribute(node,'name')
            print('Nome do node: %s'%nodeName)
            count = len('Nome do node: %s\n'%nodeName)
            servers = AdminControl.queryNames('WebSphere:type=Server,cell=%s,node=%s,*'%(cellName,nodeName)).split()
            for server in servers:
                sname = AdminControl.getAttribute(server, 'name')
                ptype = AdminControl.getAttribute(server, 'processType')
                pid   = AdminControl.getAttribute(server, 'pid')
                state = AdminControl.getAttribute(server, 'state')
                jvm = AdminControl.queryNames('type=JVM,cell=%s,node=%s,process=%s',*'%(cellName,nodeName,sname))
                osname = AdminControl.invoke(jvm, 'getProperty', 'os.name')
                print(" " + sname + " " +  ptype + " has pid " + pid + ";state: " + state + "; on " + osname)
            
listar()