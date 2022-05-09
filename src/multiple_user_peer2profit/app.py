"""
Allow multiple users to use the same peer2profit account and reward them according to time spent
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import subprocess


class MultipleUserPeer2Profit(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        self.earned = 0
        self.running = False
        self.p2p_process = None
        self.on_exit = self.end_all
        main_box = toga.Box(style=Pack(direction=COLUMN))

        inp_box = toga.Box(style=Pack(direction=ROW, padding=5))
        discord_id_label = toga.Label(
            'Discord ID:', style=Pack(padding=(0, 5)))
        self.discord_id_input = toga.TextInput(style=Pack(flex=1))
        inp_box.add(discord_id_label)
        inp_box.add(self.discord_id_input)

        self.info_box = toga.Box(style=Pack(
            direction=COLUMN, padding=5, alignment="center"))
        status_label = toga.Label(
            f"Status: {self.determine_if_running()}", style=Pack(padding=(0, 5)))
        earned_label = toga.Label(
            f"Earned this session: {self.earned}", style=Pack(padding=(0, 5)))
        self.info_box.add(status_label)
        self.info_box.add(earned_label)

        self.start_button = toga.Button(
            'Start Earning!', on_press=self.start_p2p, style=Pack(padding=5))
        self.stop_button = toga.Button(
            'Stop', on_press=self.stop_p2p, style=Pack(padding=5), enabled=False)

        main_box.add(inp_box)
        main_box.add(self.info_box)
        main_box.add(self.start_button)
        main_box.add(self.stop_button)

        self.main_window = toga.MainWindow(
            title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def start_p2p(self, widget):
        print(f"Starting P2P client. {self.discord_id_input.value}")
        self.p2p_process = subprocess.Popen(
            ["p2pclient", "--login", self.discord_id_input.value])
        widget.enabled = False
        self.stop_button.enabled = True
        widget.refresh()
        self.stop_button.refresh()
        self.earned += 1
        self.running = True
        self.info_box.refresh()

    def stop_p2p(self, widget):
        print(f"Stopping P2P client. {self.discord_id_input.value}")
        self.p2p_process.terminate()
        widget.enabled = False
        self.start_button.enabled = True
        self.start_button.refresh()
        widget.refresh()

    def end_all(self):
        print("Stopping p2p if runnin.")
        if self.p2p_process is not None:
            self.p2p_process.terminate()
        self.running = False

    def determine_if_running(self):
        if self.running:
            return "Running"
        else:
            return "Stopped"


def main():
    return MultipleUserPeer2Profit()
