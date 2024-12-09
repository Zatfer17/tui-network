import subprocess

def run(command):
    return subprocess.run(command.split(' '), capture_output=True, text=True).stdout


class NetworkManager():

    def __init__(self):
        self.rescan()

    def rescan(self):
        run('nmcli device wifi rescan')

    def get_format_param(self, header):
        header = [x.replace('_', '-') for x in header]
        return ','.join(header)

    def get_status_header(self):
        return ['device', 'type', 'state', 'connection']

    def get_status(self):
        format_options = self.get_format_param(self.get_status_header())
        output = run(f'nmcli -f {format_options} -t device')
        return [line.split(':') for line in output.split('\n') if line != '']

    def get_networks_header(self):
        return ['in_use', 'ssid', 'bars', 'security']

    def get_networks(self):
        format_options = self.get_format_param(self.get_networks_header())
        output = run(f'nmcli -f {format_options} -t device wifi list --rescan no')
        print(output)
        return [line.split(':') for line in output.split('\n') if line != '']

    def toggle(self, direction):
        run(f'nmcli radio wifi {direction}')

    def connect(self, name, password):
        run(f'nmcli device wifi connect {name} password {password}')