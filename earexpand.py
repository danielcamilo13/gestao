# _*_ latin-1 _*__abs__
import sys,os

def earexpand(command,folderbackup,folderlist):
    for folder in os.listdir(folderlist):
        print('pasta %s'%folder)
        arqsys.write('%s -ear %s%s -operationDir %s%s -operation collapse -expansionFlags all\n'%(command,folderbackup,folder,folderlist,folder))
        # ObjShell.run "d:\WebSphere6\AppServer\bin\EARExpander.bat -ear " & target & "\" & objSubfolder.Name & " -operationDir " & objSubfolder.path & " -operation collapse -expansionFlags all"

    # EARExpander.sh -ear /backup/DefaultApplication.ear -operationDir /MyAppsDefaultApplication.ear -operation collapse

command = sys.argv[1]
folderbackup = sys.argv[2]
folderlist = sys.argv[3]

if len(sys.argv)==4:
    arqsys=open('run.sh','w')
    print(command,folderbackup,folderlist)
    print('total de argumentos %s'%len(sys.argv))
    earexpand(command,folderbackup,folderlist)
    arqsys.close()
    os.system('chmod 775 run.sh')
    print('execute a rotina run.sh para fazer o earexpand')
else:
    print('preencha os campos do caminho do comando, pasta de backup e lista de pasta que sera exportada. Exemplos abaixo')
    print('comando=/opt/WebSphere7/AppServer/profiles/Node01/bin/EARExpander.sh')
    print('pasta de backup=xxxxxx')
    print('lista de pasta que sera exportada=/opt/WebSphere7/AppServer/profiles/Node01/installedApps/')
    print('total de argumentos %s'%len(sys.argv))
