import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import vlc
import tkinter as tk
import requests
from PIL import ImageTk, Image
from io import BytesIO


class IPTVPlayer(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(IPTVPlayer, self).__init__(parent)
        self.setWindowTitle("IPTV Player 4.8")
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
        # Carregar imagend dos icones do player
        button_icons = {"play":"python/sprite/control2.png", "pause":"python/sprite/control3.png", "stop":"python/sprite/control10.png", "anterior":"python/sprite/control5.png", "proximo":"python/sprite/control4.png", "forward":"python/sprite/control9.png", "backward":"python/sprite/control8.png"}
        self.search_edit.setPlaceholderText("Pesquisar...")
        self.filter_edit = QtWidgets.QLineEdit()
        self.filter_edit.setPlaceholderText("Filtrar...")
        
        # Bt Play
        self.play_button = QtWidgets.QPushButton()
        play_icon = QtGui.QIcon(button_icons["play"])
        self.play_button.setIcon(play_icon) 
        
        # Bt stop       
        self.stop_button = QtWidgets.QPushButton()
        stop_icon = QtGui.QIcon(button_icons["stop"])
        self.stop_button.setIcon(stop_icon)
        
        # Bt Pause
        self.pause_button = QtWidgets.QPushButton()
        pause_icon = QtGui.QIcon(button_icons["pause"])
        self.pause_button.setIcon(pause_icon)
        
        # Bt Anterior        
        self.previous_button = QtWidgets.QPushButton()
        ant_icon = QtGui.QIcon(button_icons["anterior"])
        self.previous_button.setIcon(ant_icon)        
        
        # Bt Proximo
        self.next_button = QtWidgets.QPushButton()
        prox_icon = QtGui.QIcon(button_icons["proximo"])
        self.next_button.setIcon(prox_icon)        
        
        # Bt Avançar
        self.forward_button = QtWidgets.QPushButton()
        forward_icon = QtGui.QIcon(button_icons["forward"])
        self.forward_button.setIcon(forward_icon)        
        
        # Bt Retroceder
        self.backward_button = QtWidgets.QPushButton()
        backward_icon = QtGui.QIcon(button_icons["backward"])        
        self.backward_button.setIcon(backward_icon)
                
        self.volume_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(100)
        
        # Criação do evento de teclas pressionadas
        self.treeview.keyPressEvent = self.play_on_return

        # Criação dos layouts
        self.search_layout = QtWidgets.QHBoxLayout()
        self.search_layout.addWidget(self.search_edit)
        self.search_layout.addWidget(self.filter_edit)
        self.play_layout = QtWidgets.QHBoxLayout()
        self.play_layout.addWidget(self.play_button)
        self.play_layout.addWidget(self.stop_button)
        self.play_layout.addWidget(self.pause_button)
        self.play_layout.addWidget(self.previous_button)
        self.play_layout.addWidget(self.next_button)
        self.play_layout.addWidget(self.backward_button)
        self.play_layout.addWidget(self.forward_button)        
        self.volume_layout = QtWidgets.QHBoxLayout()
        self.volume_layout.addWidget(self.volume_slider)
        self.tree_layout = QtWidgets.QVBoxLayout()
        self.tree_layout.addLayout(self.search_layout)
        self.tree_layout.addWidget(self.treeview)
        self.tree_layout.addLayout(self.play_layout)
        self.tree_layout.addLayout(self.volume_layout)
        self.central_widget.setLayout(self.tree_layout)

        # Botão para selecionar o arquivo m3u
        self.select_file_button = QtWidgets.QPushButton("Selecionar arquivo")
        self.tree_layout.addWidget(self.select_file_button)
        self.select_file_button.clicked.connect(self.select_file)

        # Inicialização da biblioteca VLC
        self.instance = vlc.Instance("--no-xlib")
        self.media_player = self.instance.media_player_new()

        # Criação da lista de canais vazia
        self.channels = []        
        self.channel_model = QtGui.QStandardItemModel()
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
        self.pause_button.clicked.connect(self.pause_playback)
        self.volume_slider.valueChanged.connect(self.set_volume)
        self.previous_button.clicked.connect(self.play_previous_channel)
        self.next_button.clicked.connect(self.play_next_channel)
        self.forward_button.clicked.connect(self.forward)
        self.backward_button.clicked.connect(self.backward)        

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Selecionar arquivo', './Vídeos', 'Arquivos M3U (*.m3u)')
        if file_path:
            self.channels = self.load_channels_from_file(file_path)
            self.populate_channel_model()            

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

    def pause_playback(self):
        self.media_player.pause()
    
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

    def play_previous_channel(self):
        current_index = self.treeview.selectedIndexes()[0]
        previous_index = current_index.sibling(current_index.row() - 1, current_index.column())
        if previous_index.isValid():
            self.treeview.selectionModel().select(previous_index, QtCore.QItemSelectionModel.ClearAndSelect)
            self.play_selected_channel()

    def play_next_channel(self):
        current_index = self.treeview.selectedIndexes()[0]
        next_index = current_index.sibling(current_index.row() + 1, current_index.column())
        if next_index.isValid():
            self.treeview.selectionModel().select(next_index, QtCore.QItemSelectionModel.ClearAndSelect)
            self.play_selected_channel()

    def play_on_return(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.play_selected_channel()
            
    def forward(self):
        self.media_player.set_time(self.media_player.get_time() + 10000)

    def backward(self):
        self.media_player.set_time(self.media_player.get_time() - 10000)
            
    def QCloseEvent(self, event):
    	if self.media_process is not None:
        	self.media_process.kill()
        	self.media_player.stop()
    	event.accept()

if __name__ == "__main__":
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = "./platforms"
    app = QtWidgets.QApplication(sys.argv)
    player = IPTVPlayer()
    player.show()
    sys.exit(app.exec_())
