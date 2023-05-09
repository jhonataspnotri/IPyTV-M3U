import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import vlc

class IPTVPlayer(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(IPTVPlayer, self).__init__(parent)
        self.setWindowTitle("IPTV Player")
        self.setWindowIcon(QtGui.QIcon("logo-iptv.png"))
        self.resize(800, 600)
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Criação dos widgets
        self.treeview = QtWidgets.QTreeView()
        self.treeview.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.treeview.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeview.setHeaderHidden(True)
        self.search_edit = QtWidgets.QLineEdit()
        self.search_edit.setPlaceholderText("Pesquisar...")
        self.filter_edit = QtWidgets.QLineEdit()
        self.filter_edit.setPlaceholderText("Filtrar...")
        self.play_button = QtWidgets.QPushButton("Play")
        self.stop_button = QtWidgets.QPushButton("Stop")
        self.volume_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(100)

        # Criação dos layouts
        self.search_layout = QtWidgets.QHBoxLayout()
        self.search_layout.addWidget(self.search_edit)
        self.search_layout.addWidget(self.filter_edit)
        self.play_layout = QtWidgets.QHBoxLayout()
        self.play_layout.addWidget(self.play_button)
        self.play_layout.addWidget(self.stop_button)
        self.volume_layout = QtWidgets.QHBoxLayout()
        self.volume_layout.addWidget(self.volume_slider)
        self.tree_layout = QtWidgets.QVBoxLayout()
        self.tree_layout.addLayout(self.search_layout)
        self.tree_layout.addWidget(self.treeview)
        self.tree_layout.addLayout(self.play_layout)
        self.tree_layout.addLayout(self.volume_layout)
        self.central_widget.setLayout(self.tree_layout)

        # Inicialização da biblioteca VLC
        self.instance = vlc.Instance()
        self.media_player = self.instance.media_player_new()

        # Carregamento dos canais
        self.channels = self.load_channels_from_file("canais.m3u")
        self.channel_model = QtGui.QStandardItemModel()
        self.populate_channel_model()
        self.treeview.setModel(self.channel_model)

        # Conexão dos sinais
        self.search_edit.textChanged.connect(self.filter_treeview)
        self.filter_edit.textChanged.connect(self.filter_treeview)
        if self.treeview:
            self.treeview.selectionModel().selectionChanged.connect(self.handle_treeview_selection)
        else:
            print("Erro: widget QTreeView não foi criado corretamente.")
        self.play_button.clicked.connect(self.play_selected_channel)
        self.stop_button.clicked.connect(self.stop_playback)
        self.volume_slider.valueChanged.connect(self.set_volume)

    def load_channels_from_file(self, file_path):
        channels = []
        with open(file_path, "r") as f:
            for line in f.readlines():
                line = line.strip()
                if line.startswith("#EXTINF:"):
                    channel_name = line.split(",")[1]
                elif line.startswith("http"):
                    channel_url = line
                    channels.append({"name": channel_name, "url": channel_url})
        return channels

    def populate_channel_model(self):
        self.channel_model.clear()
        for channel in self.channels:
            item = QtGui.QStandardItem(channel["name"])
            item.setData(channel["url"], role=QtCore.Qt.UserRole)
            self.channel_model.appendRow(item)

    def handle_treeview_selection(self):
        self.play_button.setEnabled(True)
        self.stop_button.setEnabled(True)

    def play_selected_channel(self):
        selected_items = self.treeview.selectedIndexes()
        if selected_items:
            selected_item = selected_items[0]
            channel_url = selected_item.data(QtCore.Qt.UserRole)
            media = self.instance.media_new(channel_url)
            self.media_player.set_media(media)
            self.media_player.play()

    def stop_playback(self):
        self.media_player.stop()

    def set_volume(self, value):
        self.media_player.audio_set_volume(value)

    def filter_treeview(self, text):
        search_text = self.search_edit.text().lower()
        filter_text = self.filter_edit.text().lower()

        for i in range(self.channel_model.rowCount()):
            item = self.channel_model.item(i)
            channel_name = item.text().lower()
            if search_text in channel_name and filter_text in channel_name:
                self.treeview.setRowHidden(i, QtCore.QModelIndex(), False)
            else:
                self.treeview.setRowHidden(i, QtCore.QModelIndex(), True)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    player = IPTVPlayer()
    player.show()
    sys.exit(app.exec_())
