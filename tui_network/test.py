import subprocess

output = subprocess.run(['nmcli', '-t', 'dev'], capture_output=True, text=True).stdout
output = [x.split(':') for x in output.split('\n') if x != '']
print(output)