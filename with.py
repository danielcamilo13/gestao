with open('gestao.silent', 'r') as f:
    data = f.readlines()
 
for line in data:
    words = line.split()
    print(words)