import subprocess

siti = '..\\tools\\SITI\\bin\\SITI.exe'
param = '--input-file --width --height --color-format'
summary = '{--summary}'
program = f'{siti} {param}'

subprocess.run(siti, shell=True)
