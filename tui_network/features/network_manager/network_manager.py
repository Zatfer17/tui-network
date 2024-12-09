import subprocess


def run(command):
    return subprocess.run(command.split(' '), capture_output=True, text=True).stdout

class NetworkManager():

    STATUS_HEADER = ['device', 'type', 'state', 'connection']
    NETWORKS_HEADER = ['in_use', 'ssid', 'bars', 'security']

    def __init__(self) -> None:
        self.rescan()

    def rescan(self) -> None:
        run('nmcli device wifi rescan')

    def get_format_param(self, header) -> str:
        header = [x.replace('_', '-') for x in header]
        return ','.join(header)

    def get_status_header(self) -> list[str]:
        return self.STATUS_HEADER

    def get_status(self) -> list[list[str]]:
        format_options = self.get_format_param(self.get_status_header())
        output = run(f'nmcli -f {format_options} -t device')
        return [line.split(':') for line in output.split('\n') if line != '']

    def get_networks_header(self) -> list[str]:
        return self.NETWORKS_HEADER

    def get_networks(self) -> list[list[str]]:
        format_options = self.get_format_param(self.get_networks_header())
        output = run(f'nmcli -f {format_options} -t device wifi list --rescan no')
        return [line.split(':') for line in output.split('\n') if line != '']

    def toggle(self, direction) -> None:
        run(f'nmcli radio wifi {direction}')

    def connect(self, name, password) -> None:
        run(f'nmcli device wifi connect {name} password {password}')