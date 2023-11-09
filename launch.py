import sys
import os
import configparser
import subprocess
from pathlib import Path
from PyQt5 import QtWidgets, QtGui
from PyQt5.uic import loadUi

BASEDIR = os.path.dirname(__file__)

class KatanaLauncher(QtWidgets.QMainWindow):
    """class representing the main launcher UI"""

    def __init__(self):
        super(KatanaLauncher, self).__init__()
        loadUi(os.path.join(BASEDIR, "assets/KatanaLauncher.ui"), self)
        self.setWindowIcon(QtGui.QIcon(os.path.join(BASEDIR, "assets/Katana.ico")))
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join(BASEDIR, "config.ini"))
        self.populate()
        self.refresh_BTN.clicked.connect(self.populate)
        self.renderer_CB.currentTextChanged.connect(self.renderer_changed)
        self.katana_version_CB.currentTextChanged.connect(self.renderer_changed)
        self.editScripts_BTN.pressed.connect(self.edit_scripts)
        self.settings_BTN.pressed.connect(self.open_settings)
        self.run_BTN.pressed.connect(self.launch)

    def center_on_screen(self):
        """Centers the window to the users screen."""
        qt_rectangle = self.frameGeometry()
        center_point = QtWidgets.QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

    def renderer_changed(self, index):
        """After the combobox changes, find and populate the versions for chosen renderer"""
        index = self.renderer_CB.currentText()
        katana_line = self.katana_version_CB.currentText()[0:3]
        self.renderer_version_CB.clear()
        self.renderer_version_CB.setEnabled(False)
        if index == "3Delight":
            self.renderer_version_CB.addItem("Katana Version")
            self.renderer_version_CB.setCurrentIndex(0)
        elif index == "RenderMan":
            renderman_path = self.config.get("RenderMan", "Path")
            renderman_versions = [
                file.split("-")[1]
                for file in os.listdir(renderman_path)
                if "RenderManForKatana" in file
                and os.path.isdir(renderman_path + "/" + file)
            ]
            renderman_versions.reverse()
            self.renderer_version_CB.addItems(renderman_versions)
            self.renderer_version_CB.setEnabled(True)
        elif index == "Arnold":
            arnold_path = self.config.get("Arnold", "Path")
            arnold_versions = [
                file.split("-")[1]
                for file in os.listdir(arnold_path)
                if "kat" + katana_line in file
                and "ktoa" in file
                and os.path.isdir(arnold_path + "/" + file)
            ]
            arnold_versions.reverse()
            self.renderer_version_CB.addItems(arnold_versions)
            self.renderer_version_CB.setEnabled(True)
        else:
            self.renderer_version_CB.setEnabled(False)

    def populate(self):
        """populates the UI with versions found"""
        # clear scripts
        while self.scripts_layout.count():
            child = self.scripts_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # clear versions
        self.katana_version_CB.clear()
        self.renderer_CB.clear()

        self.config.read(os.path.join(BASEDIR, "config.ini"))
        if self.validate_paths():
            # get versions
            katana_path = self.config.get("Katana", "Path")
            katana_versions = [
                file[6:]
                for file in os.listdir(katana_path)
                if os.path.isfile(katana_path + "/" + file + "/bin/katanaBin")
            ]
            renderers = [
                file[0:-3]
                for file in os.listdir((os.path.join(BASEDIR, "scripts/Renderers")))
                if file.endswith(".sh")
            ]
            scripts = [
                file[0:-3]
                for file in os.listdir((os.path.join(BASEDIR, "scripts")))
                if file.endswith(".sh")
            ]
            # get scripts
            for script in scripts:
                check_box = QtWidgets.QCheckBox(script)
                self.scripts_layout.addWidget(check_box)
            self.scripts_layout.addStretch()

            # add to UI
            katana_versions.reverse()
            self.katana_version_CB.addItems(katana_versions)
            self.renderer_CB.addItems(renderers)

    def launch(self):
        """Gather all environment variables, combine, and run a single .sh, launching Katana"""
        # Gather user input
        katana_version = self.katana_version_CB.currentText()
        os.environ["KATANA_VERSION"] = katana_version
        os.environ["KATANA_LINE"] = katana_version[:3]
        os.environ["KATANA_ROOT"] = (
            self.config.get("Katana", "Path") + "Katana" + katana_version
        )
        os.environ["RENVER"] = self.renderer_version_CB.currentText()
        renderer = self.renderer_CB.currentText()
        # Sanity check inputs
        print("KATANA VERSION: " + katana_version)
        print("RENDERER VERSION: " + renderer)

        if katana_version == "" or renderer == "":
            QtWidgets.QMessageBox.critical(
                None,
                "Error",
                "No Katana version or renderer selected.",
                QtWidgets.QMessageBox.Ok,
            )
            return
        # Create and launch script
        optional_scripts = (self.scripts_layout.itemAt(i).widget() for i in range(self.scripts_layout.count()-1)
                             if self.scripts_layout.itemAt(i).widget().isChecked())
        cmd = ''
        for script in optional_scripts:
            cmd += Path('scripts/' + script.text() + '.sh').read_text()

        cmd += Path('scripts/Renderers/' + renderer + '.sh').read_text()
        cmd += "\n$KATANA_ROOT/katana"
        # Temp bat file deletes itself when Katana closes
        cmd += "\nrm temp.sh"
        # Create temporary file with all commands
        with open("temp.sh", "w") as f:
            f.write(cmd)

        os.system('gnome-terminal --window -- bash -c \"bash -i temp.sh;bash\"')

    def edit_scripts(self):
        """Open a notepad of user selected scripts to be edited"""
        optional_scripts = (
            self.scripts_layout.itemAt(i).widget()
            for i in range(self.scripts_layout.count() - 1)
            if self.scripts_layout.itemAt(i).widget().isChecked()
        )
        for script in optional_scripts:
            subprocess.Popen(
                "notepad.exe "
                + os.path.join(BASEDIR, "scripts/" + script.text() + ".sh")
            )

    def open_settings(self):
        """Open the settings config notepad"""
        subprocess.Popen("notepad.exe " + os.path.join(BASEDIR, "config.ini"))

    def validate_paths(self):
        """Ensure all paths in config file exist"""
        for section in self.config.sections():
            path = self.config.get(section, "Path")
            if not os.path.exists(path):
                QtWidgets.QMessageBox.critical(
                    None,
                    "Error",
                    "One or more of your paths are not valid, please modify your config.ini file.",
                    QtWidgets.QMessageBox.Ok,
                )
                return False
        return True


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = KatanaLauncher()
    ui.center_on_screen()
    ui.show()
    app.exec_()