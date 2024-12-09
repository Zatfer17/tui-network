from textual.app import App, ComposeResult
from textual.widgets import Footer, DataTable, Input, RichLog
from textual.containers import Container, VerticalGroup, VerticalScroll, HorizontalGroup
from tui_network.features.network_manager.network_manager import NetworkManager


nm = NetworkManager()

class StatusWidget(VerticalGroup):

    BORDER_TITLE = "Status"

    def compose(self) -> ComposeResult:
        yield DataTable(
            header_height=2,
            show_cursor=False,
            cursor_type='row'
        )

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        status = nm.get_status()
        try:
            table.add_columns(*status[0].keys())
            table.add_rows([x.values() for x in status])
        except:
            print('Wireless is down...')

class AvailableNetworksWidget(VerticalScroll):

    BORDER_TITLE = "Available networks"

    def compose(self) -> ComposeResult:
        yield DataTable(
            header_height=2,
            cursor_type='row'
        )

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        networks = nm.get_networks()
        try:
            table.add_columns(*networks[0].keys())
            table.add_rows([x.values() for x in networks])
        except:
            print('Wireless is down...')

    def on_data_table_row_selected(self, message: DataTable.RowSelected) -> None:
        self.app.query_one('#network_name').insert_text_at_cursor(message.data_table.get_row_at(message.cursor_row)[0])
        self.app.query_one('#network_passphrase').focus()

class ConnectWidget(HorizontalGroup):

    BORDER_TITLE = "Connect"

    def compose(self) -> ComposeResult:
        yield Input(placeholder='Network name', id='network_name')
        yield Input(placeholder='Network passphrase', password=True, id='network_passphrase')

    def on_input_submitted(self, message: Input.Submitted) -> None:
        if message.input.id == 'network_name':
            self.screen.focus_next()
        if message.input.id == 'network_passphrase':
            network_name = self.parent.query_one('#network_name').value
            network_passphrase = message.value
            nm.connect(network_name, network_passphrase)

class FortuneWidget(VerticalScroll):

    BORDER_TITLE = "Some wisdom"

    def compose(self) -> ComposeResult:
        yield RichLog()

    def on_mount(self) -> None:
        text = self.query_one(RichLog)
        text.write(fortune())

class NetworkApp(App):

    BORDER_TITLE = "Network app"
    CSS_PATH = "assets/NetworkApp.tcss"

    BINDINGS = [
        ("ctrl+s", "scan()", "Scan"),  
        ("ctrl+r", "refresh()", "Refresh"),
        ("ctrl+u", "toggle(True)", "Wireless up"),
        ("ctrl+d", "toggle(False)", "Wireless down"),
    ]

    def compose(self) -> ComposeResult:
        yield Container(
            VerticalGroup(AvailableNetworksWidget(), id='p1'),
            VerticalGroup(DevicesWidget(), id='p2'),
            VerticalGroup(StatusWidget(), id='p3'),
            VerticalGroup(ConnectWidget(), id='p4'),
        )
        yield Footer()

    def action_scan(self) -> None:
        nm.scan()

    def action_refresh(self) -> None:
        nm.update_info()
        self.refresh(recompose=True)

    def action_toggle(self, up: bool):
        nm.toggle(up)

def network_app():
    app = NetworkApp()
    app.run()