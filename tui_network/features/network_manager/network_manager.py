import subprocess

def run(command):
    return subprocess.run(command.split(' '), capture_output=True, text=True).stdout         


class NetworkManager():

    def __init__(self):
        pass

    def get_status_header(self):
        return ['device', 'type', 'state', 'connection']

    def get_status(self):
        output = run('nmcli -t dev')
        return [line.split(':') for line in output.split('\n') if line != '']

    def get_networks(self):
        pass

    def connect(self):
        pass