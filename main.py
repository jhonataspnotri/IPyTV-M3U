import os
import time
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget, QLineEdit
import vlc
import tkinter as tk
import requests
from PIL import ImageTk, Image, ImageOps, ImageEnhance
import numpy as np
import colorsys
from PIL.ImageQt import ImageQt
from io import BytesIO
#import keyboard


class IPTVPlayer(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(IPTVPlayer, self).__init__(parent)
        self.setWindowTitle("IPTV Player 4.8")
        self.setWindowIcon(QtGui.QIcon("images/logo/logo-iptv.png"))
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
        self.filter_edit = QtWidgets.QComboBox()
        root = tk.Tk()
        self.filter_edit.setFixedWidth( (root.winfo_screenwidth() // 2 - 300) // 2)
        #self.filter_edit.setPlaceholderText("Filtrar...")
        self.itens = [""]
        
        # Carregar imagend dos icones do player
        button_icons = {"play":"images/np4/control1.png",
                        "pause":"images/np4/control17.png",
                        "stop":"images/np4/control18.png",
                        "anterior":"images/np4/control22.png",
                        "proximo":"images/np4/control23.png",
                        "backward":"images/np4/control20.png",
                        "forward":"images/np4/control21.png",                        
                        "ratio":"images/np4/control39.png",}
        
        # Var bt_visible = False
        self.bt_visible = False
        
        # Bt Play
        self.play_button = QtWidgets.QPushButton()
        play_icon = QtGui.QIcon(button_icons["play"])
        icon_size = play_icon.actualSize(QtCore.QSize(32, 32)) # define o tamanho do ícone como 32x32 pixels
        self.play_button.setIconSize(icon_size)
        self.play_button.setIcon(play_icon)
        self.play_button.setEnabled(False)                

        # Bt stop       
        self.stop_button = QtWidgets.QPushButton()
        stop_icon = QtGui.QIcon(button_icons["stop"])
        icon_size = stop_icon.actualSize(QtCore.QSize(32, 32)) # define o tamanho do ícone como 32x32 pixels
        self.stop_button.setIconSize(icon_size)
        self.stop_button.setIcon(stop_icon)
        self.stop_button.setEnabled(False)

        # Bt Pause
        self.pause_button = QtWidgets.QPushButton()
        pause_icon = QtGui.QIcon(button_icons["pause"])
        icon_size = pause_icon.actualSize(QtCore.QSize(32, 32)) # define o tamanho do ícone como 32x32 pixels
        self.pause_button.setIconSize(icon_size)
        self.pause_button.setIcon(pause_icon)
        self.pause_button.setEnabled(False)        

        # Bt Anterior        
        self.previous_button = QtWidgets.QPushButton()
        ant_icon = QtGui.QIcon(button_icons["anterior"])
        icon_size = ant_icon.actualSize(QtCore.QSize(32, 32)) # define o tamanho do ícone como 32x32 pixels
        self.previous_button.setIconSize(icon_size)
        self.previous_button.setIcon(ant_icon)
        self.previous_button.setEnabled(False)

        # Bt Proximo
        self.next_button = QtWidgets.QPushButton()
        prox_icon = QtGui.QIcon(button_icons["proximo"])
        icon_size = prox_icon.actualSize(QtCore.QSize(32, 32)) # define o tamanho do ícone como 32x32 pixels
        self.next_button.setIconSize(icon_size)
        self.next_button.setIcon(prox_icon)
        self.next_button.setEnabled(False)

        # Bt Avançar
        self.forward_button = QtWidgets.QPushButton()
        forward_icon = QtGui.QIcon(button_icons["forward"])
        icon_size = forward_icon.actualSize(QtCore.QSize(32, 32)) # define o tamanho do ícone como 32x32 pixels
        self.forward_button.setIconSize(icon_size)
        self.forward_button.setIcon(forward_icon)
        self.forward_button.setEnabled(False)

        # Bt Retroceder
        self.backward_button = QtWidgets.QPushButton()
        backward_icon = QtGui.QIcon(button_icons["backward"]) 
        icon_size = backward_icon.actualSize(QtCore.QSize(32, 32)) # define o tamanho do ícone como 32x32 pixels
        self.backward_button.setIconSize(icon_size)
        self.backward_button.setIcon(backward_icon)
        self.backward_button.setEnabled(False)
        
        # Bt Aspect Ratio
        self.ratio_button = QtWidgets.QPushButton()
        ratio_icon = QtGui.QIcon(button_icons["ratio"])
        icon_size = ratio_icon.actualSize(QtCore.QSize(32, 32)) # define o tamanho do ícone como 32x32 pixels
        self.ratio_button.setIconSize(icon_size)
        self.ratio_button.setIcon(ratio_icon)
        self.ratio_button.setEnabled(False)         
        
        # Volume slider
        self.volume_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(100)
        
        # Tempo slider
        self.tempo_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.tempo_slider.setRange(0, 100)
        
        
        # Criação dos layouts
        self.search_layout = QtWidgets.QHBoxLayout()
        self.search_layout.addWidget(self.search_edit)        
        self.play_layout = QtWidgets.QHBoxLayout()        
        self.play_layout.addWidget(self.backward_button)
        self.play_layout.addWidget(self.previous_button)
        self.play_layout.addWidget(self.pause_button)
        self.play_layout.addWidget(self.play_button)
        self.play_layout.addWidget(self.stop_button)
        self.play_layout.addWidget(self.next_button)        
        self.play_layout.addWidget(self.forward_button)
        self.play_layout.addWidget(self.ratio_button)
        self.volume_layout = QtWidgets.QHBoxLayout()
        self.volume_layout.addWidget(self.volume_slider)        
        self.tree_layout = QtWidgets.QVBoxLayout()
        
        self.tree_layout.addWidget(self.treeview)
        self.tree_layout.addWidget(self.tempo_slider)
        # Adicione o QLabel ao layout
        self.logo_label = QtWidgets.QLabel()
        #self.logo_label.setFixedSize(300, 250)
        
        #self.tree_layout.addWidget(self.logo_label)       
        self.search_layout.addWidget(self.logo_label)
        self.search_layout.addWidget(self.filter_edit)
                       
        self.tree_layout.addLayout(self.play_layout)
        self.tree_layout.addLayout(self.search_layout)
        self.tree_layout.addLayout(self.volume_layout)        
        self.central_widget.setLayout(self.tree_layout)

        # Botão para selecionar o arquivo m3u
        self.select_file_button = QtWidgets.QPushButton("Selecionar arquivo")
        self.tree_layout.addWidget(self.select_file_button)
        self.select_file_button.clicked.connect(self.select_file)

        # Inicialização da biblioteca VLC
        self.instance = vlc.Instance("--no-xlib")
        self.media_player = self.instance.media_player_new()
        self.media_player.set_fullscreen(True)
        self.aspect_ratio = "16:9"  # Proporção de aspecto desejada (exemplo: 16:9)
        self.media_player.video_set_aspect_ratio(self.aspect_ratio)
        self.change = 0

        # Criação da lista de canais vazia        
        self.channels = []        
        self.channel_model = QtGui.QStandardItemModel()
        self.treeview.setModel(self.channel_model)

        # Conexão dos sinais        
        # Criação do evento de teclas pressionadas
        self.search_edit.returnPressed.connect(lambda: self.filter_treeview(self.search_edit.text()))
        self.filter_edit.activated[str].connect(lambda item: self.filter_treeview(item))
        #self.filter_edit.returnPressed.connect(lambda: self.filter_treeview(self.filter_edit.text()))        
        self.treeview.keyPressEvent = self.keyPressEvent
        #keyboard.on_press(self.handle_key_press)        
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
        self.ratio_button.clicked.connect(self.change_ratio) 
        # Configura o temporizador para verificar o fim do vídeo
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.check_media_end)
        self.timer.start(1000)  # verifica a cada segundo 
        self.tempo_slider.sliderReleased.connect(self.set_tempo)
        #self.tempo_slider.sliderPressed.connect(self.slider_pressed)        
        #self.tempo_slider.sliderPressed = False
        #self.tempo_slider.sliderMoved.connect(self.slider_Moved)         

    def select_file(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, 'Selecionar arquivo', os.path.expanduser("~/Vídeos"), 'Arquivos M3U (*.m3u)')
            if file_path:
                self.channels = self.load_channels_from_file(file_path)
                self.populate_channel_model()
                self.filter_edit.addItems(self.itens) 
        except Exception as e:
            print(e)
                
    def load_channels_from_file(self, file_path):
        channels = []        
        with open(file_path, "r") as f:
            for line in f.readlines():
                line = line.strip()
                if line.startswith("#EXTINF:"):
                    channel_name = line.split("=")[2].rstrip(" tvg-logo").strip("\"")
                    channel_logo = line.split("=")[3].rstrip(" group-title").strip("\"")
                    channel_group = line.rsplit("group-title=")[1]                                        
                    channel_group = channel_group.split(",")[0].strip("\"")
                    if not channel_group in self.itens:
                        self.itens.append(channel_group)                    
                    #print(channel_group)
                elif line.startswith("http"):
                    channel_url = line                    
                    channels.append({"name": channel_group +": "+channel_name, "url": channel_url, "logo": channel_logo})                   
        return channels        

    def populate_channel_model(self):
        self.channel_model.clear()
        for channel in self.channels:
            item = QtGui.QStandardItem(channel["name"])
            item.setData(channel["url"], role=QtCore.Qt.UserRole)
            item.setData(channel["logo"], role=QtCore.Qt.UserRole+1)
            self.channel_model.appendRow(item)

    def handle_treeview_selection(self):
        try:
            if not self.bt_visible:
                self.play_button.setEnabled(True)
                self.stop_button.setEnabled(True)
                self.pause_button.setEnabled(True)
                self.previous_button.setEnabled(True)
                self.next_button.setEnabled(True)
                self.forward_button.setEnabled(True)
                self.backward_button.setEnabled(True)
                self.ratio_button.setEnabled(True)
                self.bt_visible = True
            #print(self.bt_visible)    
            
            # mudar a imagem exibida conforme a linha selecionada
            selected_items = self.treeview.selectedIndexes()
            if selected_items:
                selected_item = selected_items[0]
                channel_url = selected_item.data(QtCore.Qt.UserRole)
                channel_logo_url = selected_item.data(QtCore.Qt.UserRole + 1)            
                response = requests.get(channel_logo_url)
                # Carrega a imagem e redimensiona
                img = Image.open(BytesIO(response.content)).convert("RGBA")
                img = img.resize((300, 250), Image.Resampling.LANCZOS)            
                # Define uma máscara que seleciona apenas as áreas dentro da borda de 5 pixels
                mask = Image.new('L', img.size, 255)
                borda = 16
                for x in range(img.size[0]):
                    for y in range(img.size[1]):
                        if x < borda or x >= img.size[0]-borda or y < borda or y >= img.size[1]-borda:
                            mask.putpixel((x, y), 0)                        
                # Aplica a máscara na imagem
                img = ImageOps.fit(img, mask.size, centering=(1.6, 1.6))
                img.putalpha(mask)            
                # Converte a imagem para um QPixmap e exibe no QLabel
                pixmap = QtGui.QPixmap.fromImage(ImageQt(img))
                self.logo_label.setPixmap(pixmap)
        except Exception as e:
            print(e)

    def play_selected_channel(self):
        selected_items = self.treeview.selectedIndexes()
        if selected_items:
            selected_item = selected_items[0]
            channel_url = selected_item.data(QtCore.Qt.UserRole)
            media = self.instance.media_new(channel_url)
            self.media_player.set_media(media)
            self.media_player.play()            
            # Aguarda até que o vídeo comece a ser reproduzido ou ocorra um erro
            while not vlc.State.Playing:
                time.sleep(1)            
            # Tenta reproduzir o vídeo até 3 vezes caso ocorra um erro
                for i in range(3):
                    try:
                        self.media_player.play()
                        break
                    except Exception as e:
                        print("Erro ao reproduzir vídeo:", e)
                        print("Tentando novamente em 3 segundos...")
                        time.sleep(3)
                else:
                    print("Não foi possível reproduzir o vídeo após 3 tentativas.")

    def change_ratio(self):        
        if self.change == 0:  # muda para 4:3
            self.aspect_ratio = "4:3"
            self.media_player.video_set_aspect_ratio(self.aspect_ratio)
            self.change += 1
        elif self.change == 1:  # muda para 1:1
            self.aspect_ratio = "1:1"
            self.media_player.video_set_aspect_ratio(self.aspect_ratio)
            self.change += 1
        elif self.change == 2:  # muda para 16:9
            self.aspect_ratio = "16:9"
            self.media_player.video_set_aspect_ratio(self.aspect_ratio)
            self.change += 1 
        elif self.change == 3:  # muda para 16:10
            self.aspect_ratio = "16:10"
            self.media_player.video_set_aspect_ratio(self.aspect_ratio)
            self.change = 0        
        print(self.aspect_ratio)
    
    def stop_playback(self):
        self.media_player.stop()

    def pause_playback(self):
        self.media_player.pause()

    def set_volume(self, value):
        self.media_player.audio_set_volume(value)
        
    def set_tempo(self):
        novoValue = self.tempo_slider.value() * 1000
        self.media_player.set_time(novoValue) 
        #self.tempo_slider.sliderPressed = False
        #self.tempo_slider.sliderMoved = False   
        
    #def slider_pressed(self):
        #self.tempo_slider.sliderPressed = True                 
    
    #def slider_Moved(self):
        #self.tempo_slider.sliderMoved = True       

    def filter_treeview(self, text):
        search_text = self.search_edit.text().lower()
        #filter_text = self.filter_edit.text().lower()
        filter_text = self.filter_edit.currentText().lower()
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
            viewport_rect = self.treeview.viewport().rect()
            item_rect = self.treeview.visualRect(previous_index)
            if not viewport_rect.contains(item_rect):                    
            #if next_index.row() == self.treeview.selectionModel().rowCount() - 1:
                self.treeview.scrollTo(previous_index, QtWidgets.QAbstractItemView.PositionAtTop)            
            self.play_selected_channel()

    def play_next_channel(self):
        current_index = self.treeview.selectedIndexes()[0]
        next_index = current_index.sibling(current_index.row() + 1, current_index.column())
        if next_index.isValid():
            self.treeview.selectionModel().select(next_index, QtCore.QItemSelectionModel.ClearAndSelect)
            viewport_rect = self.treeview.viewport().rect()
            item_rect = self.treeview.visualRect(next_index)
            if not viewport_rect.contains(item_rect):                    
            #if next_index.row() == self.treeview.selectionModel().rowCount() - 1:
                self.treeview.scrollTo(next_index, QtWidgets.QAbstractItemView.PositionAtBottom)            
            self.play_selected_channel()

    #def handle_key_press(self, event):
        ## trata o evento de tecla pressionada
        #print("Tecla pressionada:", event.name)
        #if event.name == "enter":
            #self.play_selected_channel()
            
        #if event.name == "right":
            #current_index = self.treeview.selectedIndexes()[0]
            #next_index = current_index.sibling(current_index.row() + 1, current_index.column())
            #if next_index.isValid():
                #self.treeview.selectionModel().select(next_index, QtCore.QItemSelectionModel.ClearAndSelect)
                #viewport_rect = self.treeview.viewport().rect()
                #item_rect = self.treeview.visualRect(next_index)
                #if not viewport_rect.contains(item_rect):                    
                ##if next_index.row() == self.treeview.selectionModel().rowCount() - 1:
                    #self.treeview.scrollTo(next_index, QtWidgets.QAbstractItemView.PositionAtBottom)            
                #self.play_selected_channel()                       
        
        #if event.name == "left":
            #current_index = self.treeview.selectedIndexes()[0]
            #previous_index = current_index.sibling(current_index.row() - 1, current_index.column())
            #if previous_index.isValid():
                #self.treeview.selectionModel().select(previous_index, QtCore.QItemSelectionModel.ClearAndSelect)
                #viewport_rect = self.treeview.viewport().rect()
                #item_rect = self.treeview.visualRect(previous_index)
                #if not viewport_rect.contains(item_rect):                    
                ##if next_index.row() == self.treeview.selectionModel().rowCount() - 1:
                    #self.treeview.scrollTo(previous_index, QtWidgets.QAbstractItemView.PositionAtTop)            
                #self.play_selected_channel()            
        
    def keyPressEvent(self, event):
        # Ao pressionar <ENTER>
        if event.key() == QtCore.Qt.Key_Return:
            self.play_selected_channel()
    
        # Ao pressionar <Key_Down>
        if event.key() == QtCore.Qt.Key_Down:
            selected_indexes = self.treeview.selectedIndexes()
            if selected_indexes:
                current_index = selected_indexes[0]
                current_row = current_index.row()
                next_row = current_row + 1
    
                while next_row < self.channel_model.rowCount():
                    next_index = self.channel_model.index(next_row, current_index.column())
                    if self.treeview.isRowHidden(next_row, QtCore.QModelIndex()):
                        next_row += 1
                        self.treeview.scrollTo(next_index, QtWidgets.QAbstractItemView.PositionAtBottom)
                    else:
                        self.treeview.selectionModel().select(next_index, QtCore.QItemSelectionModel.ClearAndSelect)
                        self.treeview.selectionModel().setCurrentIndex(next_index, QtCore.QItemSelectionModel.ClearAndSelect)                        
                        break
    
        # Ao pressionar <Key_Up>
        if event.key() == QtCore.Qt.Key_Up:
            selected_indexes = self.treeview.selectedIndexes()
            if selected_indexes:
                current_index = selected_indexes[0]
                current_row = current_index.row()
                next_row = current_row - 1
    
                while next_row >= 0:
                    next_index = self.channel_model.index(next_row, current_index.column())
                    if self.treeview.isRowHidden(next_row, QtCore.QModelIndex()):
                        next_row -= 1
                        self.treeview.scrollTo(next_index, QtWidgets.QAbstractItemView.PositionAtTop)
                    else:
                        self.treeview.selectionModel().select(next_index, QtCore.QItemSelectionModel.ClearAndSelect)
                        self.treeview.selectionModel().setCurrentIndex(next_index, QtCore.QItemSelectionModel.ClearAndSelect)                        
                        break

                    
    def forward(self):
        #self.media_player.set_time(self.media_player.get_length() - 10000)
        self.media_player.set_time(self.media_player.get_time() + self.media_player.get_length() // 8)

    def backward(self):
        self.media_player.set_time(self.media_player.get_time() - self.media_player.get_length() // 8)

    def QCloseEvent(self, event):
        if self.media_process is not None:
            self.media_process.kill()
            self.media_player.stop()
        event.accept()

    def check_media_end(self):
        if self.media_player.get_state() == vlc.State.Ended and self.media_player.get_time() > 10000:
            self.play_next_channel()
        if self.media_player.get_state() == vlc.State.Playing:
            #self.handle_treeview_selection()
            if not self.tempo_slider.underMouse():
                self.tempo_slider.setRange(0, self.media_player.get_length()//1000)    
                self.tempo_slider.setValue(self.media_player.get_time()//1000)         
        #DEBUG:    
        #print(self.media_player.get_state())
        #print(self.media_player.get_time()//1000)
        #print(self.tempo_slider.sliderMoved)
        #if self.tempo_slider.underMouse():
            # O ponteiro do mouse está sobre o tempo_slider
        #   print("O ponteiro do mouse está sobre o tempo_slider")
        #else:
            # O ponteiro do mouse não está sobre o tempo_slider
        #    print("O ponteiro do mouse não está sobre o tempo_slider")              
            
if __name__ == "__main__":
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = "./platforms"
    #os.environ["QT_QPA_PLATFORM"] = "wayland"
    #os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = "/usr/lib/qt5/plugins/platforms/"
    app = QtWidgets.QApplication(sys.argv)
    player = IPTVPlayer()
    player.show()
    sys.exit(app.exec_())

