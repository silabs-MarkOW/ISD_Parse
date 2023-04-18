import sys
import getopt
import os

BINDIR = "~/bin"
print("BINDIR: '%s'"%(BINDIR))
parsed_options = getopt.getopt(sys.argv[1:],"b:")
for option in parsed_options[0] :
    if '-b' == option[0] :
        BINDIR = option[1]
        continue

if '/' == BINDIR[-1] :
    BINDIR = BINDIR[:-1]

files = parsed_options[1]

if 0 == len(files) :
    print("Usage: install-backend [ -b <bindir> ] script [ script [ ... ]]")
    quit()

try :
    os.scandir('.git')
except FileNotFoundError :
    print('No ".git" folder')
    quit(1)
    
fh = os.popen("git config --get remote.origin.url","r")
text = fh.read()
fh.close()
URL = text.split()[0]

fh = os.popen("git log","r")
text = fh.read()
tokens = text.split()
if "commit" != tokens[0] :
    raise RuntimeError("First token from 'git log' is not 'commit'")
COMMIT = tokens[1]

fh = os.popen("date","r")
text = fh.read()
fh.close()
DATE = text.split('\n')[0]

shell_scripts = []
python_scripts = []

for file in files :
    ext = file[-3:]
    basename = file[:-3]
    if '.sh' == ext :
        shell_scripts.append(basename)
        continue
    if '.py' == ext :
        python_scripts.append(basename)
        continue

print('Shell scripts: [%s]'%(','.join(shell_scripts)))
print('Python scripts: [%s]'%(','.join(python_scripts)))
mode = (7 << 6)|(5 << 3)|5

for file in shell_scripts :
    outpath = BINDIR+"/"+file
    print("processing %s"%(outpath))
    fh_in = open(file+".sh","r")
    fh_out = open(outpath,"w")
    fh_out.write('#! /bin/bash\n#\n')
    fh_out.write('# Installed from %s\n'%(URL))
    fh_out.write('#   commit %s\n'%(COMMIT))
    fh_out.write('#   on %s\n'%(DATE))
    fh_out.write('#\n')
    while 1 :
        buf = fh_in.read()
        if 0 == len(buf) :
                 break
        fh_out.write(buf)
    fh_in.close()
    fh_out.close()
    os.chmod(outpath,mode)
    
for file in python_scripts :
    outpath = BINDIR+"/"+file
    print("processing %s"%(outpath))
    fh_in = open(file+".py","r")
    fh_out = open(outpath,"w")
    fh_out.write('#! /bin/env python3\n#\n')
    fh_out.write('# Installed from %s\n'%(URL))
    fh_out.write('#   commit %s\n'%(COMMIT))
    fh_out.write('#   on %s\n'%(DATE))
    fh_out.write('#\n')
    while 1 :
        buf = fh_in.read()
        if 0 == len(buf) :
                 break
        fh_out.write(buf)
    fh_in.close()
    fh_out.close()
    os.chmod(outpath,mode)
