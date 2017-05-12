# -*- coding: latin-1 -*-
import sys, os, re

def main(arg):
    arqfile = open(sys.argv[1],'r+')
    arqshadow = open(sys.argv[1]+'_novo','w')
    patt=r'PCCGCM_ENS'
    for line in arqfile.readlines():
        arqshadow.write(line)
        if re.search(patt,line):
            changes = re.sub(line,'Alias /PCCGCM_ENS /ArquitecturaE-business/Html\nAlias /CCCAAR_ENS /ArquitecturaE-business/Html\n',line))
            arqshadow.write(changes)
            print('arquivo localizado')
            print(line)
    arqshadow.close()
    arqfile.close()
    print('realizado um backup')
arg = sys.argv[1]
main(arg)

#Exemplo python modificahttp.py arquivo.conf parametro#