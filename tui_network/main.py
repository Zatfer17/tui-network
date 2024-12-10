from textual.app import App, ComposeResult
from textual.widgets import Footer, DataTable, Input, RichLog
from textual.containers import Container, VerticalGroup, VerticalScroll, HorizontalGroup
from tui_network.features.network_manager.network_manager import NetworkManager
from fortune import fortune

nm = NetworkManager()

class StatusWidget(VerticalScroll):

    BORDER_TITLE = "Status"

    def compose(self) -> ComposeResult:
        yield DataTable(
            header_height=2,
            show_cursor=False,
            cursor_type='row'
        )

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        try:
            table.add_columns(*nm.get_status_header())
            table.add_rows(nm.get_status())
        except Exception:
            print('Wireless is down...')


class NetworksWidget(VerticalScroll):

    BORDER_TITLE = "Networks"

    def compose(self) -> ComposeResult:
        yield DataTable(
            header_height=2,
            cursor_type='row'
        )

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        try:
            table.add_columns(*nm.get_networks_header())
            table.add_rows(nm.get_networks())
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

    BORDER_TITLE = "Fortune"

    def compose(self) -> ComposeResult:
        yield RichLog(wrap=True)

    def on_mount(self):
        self.query_one(RichLog).write(fortune())


class NetworkApp(App):

    BORDER_TITLE = "Network app"
    CSS_PATH = "static/style.tcss"

    BINDINGS = [
        ("ctrl+r", "refresh()", "Refresh"),
        ("ctrl+1", "toggle('off')", "Wifi down"),
        ("ctrl+2", "toggle('on')", "Wifi up"),
    ]

    def compose(self) -> ComposeResult:
        yield Container(
            VerticalGroup(NetworksWidget(can_focus=False), id='networks'),
            VerticalGroup(StatusWidget(can_focus=False, can_focus_children=False), id='status'),
            VerticalGroup(ConnectWidget(), id='connect'),
            VerticalGroup(FortuneWidget(can_focus=False, can_focus_children=False), id='fortune')
        )
        yield Footer()

    def action_refresh(self) -> None:
        nm.rescan()
        self.refresh(recompose=True)

    def action_toggle(self, direction: str) -> None:
        nm.toggle(direction)

def network_app() -> None:
    app = NetworkApp()
    app.run()