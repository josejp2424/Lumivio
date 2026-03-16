#!/usr/bin/env python3
# =============================================================================
# Essora Lumivio
# Autor: josejp2424
# Descripción: Captura de pantalla y GIF con interfaz GTK3 moderna para Essora
# Versión: 1.0.0
# Licencia: GPL-3.0
# =============================================================================

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GdkPixbuf
import subprocess
import os
import locale
import tempfile
from datetime import datetime

class EssoraLumivioApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Essora Lumivio")
        self.set_default_size(650, 550)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(False)
        
        # Detectar idioma del sistema
        self.setup_language()
        
        # Variables de configuración
        self.output_dir = os.path.expanduser("~")
        self.sound_file = "/usr/local/Lumivio/camera-shutter.wav"
        self.icon_path = "/usr/local/Lumivio/camera.svg"
        
        # Configurar icono de ventana
        if os.path.exists(self.icon_path):
            self.set_icon_from_file(self.icon_path)
        
        # Configurar CSS para tema oscuro y estilo moderno
        self.setup_css()
        
        # Crear interfaz
        self.create_ui()
        
    def setup_language(self):
        """Detectar y configurar idioma del sistema"""
        try:
            lang = locale.getdefaultlocale()[0]
            if lang:
                lang_code = lang.split('_')[0].lower()
            else:
                lang_code = 'en'
        except:
            lang_code = 'en'
            
        self.strings = self.get_language_strings(lang_code)
    
    def get_language_strings(self, lang_code):
        """Retorna las cadenas de texto según el idioma"""
        translations = {
            'es': {
                'title': 'Captura de Pantalla',
                'tab_capture': 'Captura',
                'tab_gif': 'GIF/Video',
                'tab_settings': 'Configuración',
                'delay': 'Retardo (segundos)',
                'capture_type': 'Tipo de captura',
                'capture_mode': 'Modo de captura',
                'fullscreen': 'Pantalla completa',
                'window': 'Ventana activa',
                'region': 'Seleccionar región',
                'filename': 'Nombre de archivo',
                'gif_duration': 'Duración del GIF (segundos)',
                'gif_fps': 'Tasa de frames (fps)',
                'gif_quality': 'Calidad (1-30, menor=mejor)',
                'btn_capture': '📸 Capturar',
                'btn_cancel': '❌ Cancelar',
                'btn_recorder': '🎬 Grabador de Pantalla',
                'saved_in': 'Captura guardada en',
                'image': 'Imagen PNG',
                'gif': 'GIF Animado',
                'desc_capture': 'Configure las opciones para capturar pantalla',
                'desc_gif': 'Configure las opciones para crear GIF animado',
                'output_folder': 'Carpeta de salida',
                'select_folder': 'Seleccionar carpeta',
                'play_sound': 'Reproducir sonido al capturar',
                'about': 'Acerca de',
                'about_title': 'Acerca de Essora Lumivio',
                'about_description': 'Herramienta de captura de pantalla y creación de GIF para Essora Linux',
                'version': 'Versión',
                'author': 'Autor',
                'license': 'Licencia',
                'website': 'Sitio web'
            },
            'en': {
                'title': 'Screenshot Capture',
                'tab_capture': 'Capture',
                'tab_gif': 'GIF/Video',
                'tab_settings': 'Settings',
                'delay': 'Delay (seconds)',
                'capture_type': 'Capture type',
                'capture_mode': 'Capture mode',
                'fullscreen': 'Full screen',
                'window': 'Active window',
                'region': 'Select region',
                'filename': 'Filename',
                'gif_duration': 'GIF duration (seconds)',
                'gif_fps': 'Frame rate (fps)',
                'gif_quality': 'Quality (1-30, lower=better)',
                'btn_capture': '📸 Capture',
                'btn_cancel': '❌ Cancel',
                'btn_recorder': '🎬 Screen Recorder',
                'saved_in': 'Capture saved in',
                'image': 'PNG Image',
                'gif': 'Animated GIF',
                'desc_capture': 'Configure screenshot capture options',
                'desc_gif': 'Configure animated GIF creation options',
                'output_folder': 'Output folder',
                'select_folder': 'Select folder',
                'play_sound': 'Play sound on capture',
                'about': 'About',
                'about_title': 'About Essora Lumivio',
                'about_description': 'Screenshot and GIF creation tool for Essora Linux',
                'version': 'Version',
                'author': 'Author',
                'license': 'License',
                'website': 'Website'
            },
            'fr': {
                'title': 'Capture d\'écran',
                'tab_capture': 'Capture',
                'tab_gif': 'GIF/Vidéo',
                'tab_settings': 'Paramètres',
                'delay': 'Délai (secondes)',
                'capture_type': 'Type de capture',
                'capture_mode': 'Mode de capture',
                'fullscreen': 'Plein écran',
                'window': 'Fenêtre active',
                'region': 'Sélectionner région',
                'filename': 'Nom de fichier',
                'gif_duration': 'Durée du GIF (secondes)',
                'gif_fps': 'Taux d\'images (ips)',
                'gif_quality': 'Qualité (1-30, plus bas=meilleur)',
                'btn_capture': '📸 Capturer',
                'btn_cancel': '❌ Annuler',
                'btn_recorder': '🎬 Enregistreur d\'écran',
                'saved_in': 'Capture enregistrée dans',
                'image': 'Image PNG',
                'gif': 'GIF Animé',
                'desc_capture': 'Configurer les options de capture',
                'desc_gif': 'Configurer les options de création de GIF',
                'output_folder': 'Dossier de sortie',
                'select_folder': 'Sélectionner dossier',
                'play_sound': 'Jouer un son lors de la capture',
                'about': 'À propos',
                'about_title': 'À propos d\'Essora Lumivio',
                'about_description': 'Outil de capture d\'écran et de création de GIF pour Essora Linux',
                'version': 'Version',
                'author': 'Auteur',
                'license': 'Licence',
                'website': 'Site web'
            },
            'de': {
                'title': 'Bildschirmfoto',
                'tab_capture': 'Aufnahme',
                'tab_gif': 'GIF/Video',
                'tab_settings': 'Einstellungen',
                'delay': 'Verzögerung (Sekunden)',
                'capture_type': 'Aufnahmetyp',
                'capture_mode': 'Aufnahmemodus',
                'fullscreen': 'Vollbild',
                'window': 'Aktives Fenster',
                'region': 'Region auswählen',
                'filename': 'Dateiname',
                'gif_duration': 'GIF-Dauer (Sekunden)',
                'gif_fps': 'Bildrate (fps)',
                'gif_quality': 'Qualität (1-30, niedriger=besser)',
                'btn_capture': '📸 Aufnehmen',
                'btn_cancel': '❌ Abbrechen',
                'btn_recorder': '🎬 Bildschirmrekorder',
                'saved_in': 'Aufnahme gespeichert in',
                'image': 'PNG-Bild',
                'gif': 'Animiertes GIF',
                'desc_capture': 'Aufnahmeoptionen konfigurieren',
                'desc_gif': 'GIF-Erstellungsoptionen konfigurieren',
                'output_folder': 'Ausgabeordner',
                'select_folder': 'Ordner auswählen',
                'play_sound': 'Ton bei Aufnahme abspielen',
                'about': 'Über',
                'about_title': 'Über Essora Lumivio',
                'about_description': 'Screenshot- und GIF-Erstellungstool für Essora Linux',
                'version': 'Version',
                'author': 'Autor',
                'license': 'Lizenz',
                'website': 'Webseite'
            },
            'it': {
                'title': 'Screenshot',
                'tab_capture': 'Cattura',
                'tab_gif': 'GIF/Video',
                'tab_settings': 'Impostazioni',
                'delay': 'Ritardo (secondi)',
                'capture_type': 'Tipo di cattura',
                'capture_mode': 'Modalità di cattura',
                'fullscreen': 'Schermo intero',
                'window': 'Finestra attiva',
                'region': 'Seleziona regione',
                'filename': 'Nome file',
                'gif_duration': 'Durata GIF (secondi)',
                'gif_fps': 'Frame rate (fps)',
                'gif_quality': 'Qualità (1-30, più basso=migliore)',
                'btn_capture': '📸 Cattura',
                'btn_cancel': '❌ Annulla',
                'btn_recorder': '🎬 Registratore schermo',
                'saved_in': 'Cattura salvata in',
                'image': 'Immagine PNG',
                'gif': 'GIF Animata',
                'desc_capture': 'Configura opzioni di cattura',
                'desc_gif': 'Configura opzioni creazione GIF',
                'output_folder': 'Cartella di output',
                'select_folder': 'Seleziona cartella',
                'play_sound': 'Riproduci suono durante cattura',
                'about': 'Informazioni',
                'about_title': 'Informazioni su Essora Lumivio',
                'about_description': 'Strumento di cattura screenshot e creazione GIF per Essora Linux',
                'version': 'Versione',
                'author': 'Autore',
                'license': 'Licenza',
                'website': 'Sito web'
            },
            'pt': {
                'title': 'Captura de Tela',
                'tab_capture': 'Captura',
                'tab_gif': 'GIF/Vídeo',
                'tab_settings': 'Configurações',
                'delay': 'Atraso (segundos)',
                'capture_type': 'Tipo de captura',
                'capture_mode': 'Modo de captura',
                'fullscreen': 'Tela cheia',
                'window': 'Janela ativa',
                'region': 'Selecionar região',
                'filename': 'Nome do arquivo',
                'gif_duration': 'Duração do GIF (segundos)',
                'gif_fps': 'Taxa de quadros (fps)',
                'gif_quality': 'Qualidade (1-30, menor=melhor)',
                'btn_capture': '📸 Capturar',
                'btn_cancel': '❌ Cancelar',
                'btn_recorder': '🎬 Gravador de Tela',
                'saved_in': 'Captura salva em',
                'image': 'Imagem PNG',
                'gif': 'GIF Animado',
                'desc_capture': 'Configurar opções de captura',
                'desc_gif': 'Configurar opções de criação de GIF',
                'output_folder': 'Pasta de saída',
                'select_folder': 'Selecionar pasta',
                'play_sound': 'Reproduzir som ao capturar',
                'about': 'Sobre',
                'about_title': 'Sobre Essora Lumivio',
                'about_description': 'Ferramenta de captura de tela e criação de GIF para Essora Linux',
                'version': 'Versão',
                'author': 'Autor',
                'license': 'Licença',
                'website': 'Site'
            },
            'ru': {
                'title': 'Скриншот',
                'tab_capture': 'Захват',
                'tab_gif': 'GIF/Видео',
                'tab_settings': 'Настройки',
                'delay': 'Задержка (секунды)',
                'capture_type': 'Тип захвата',
                'capture_mode': 'Режим захвата',
                'fullscreen': 'Весь экран',
                'window': 'Активное окно',
                'region': 'Выбрать область',
                'filename': 'Имя файла',
                'gif_duration': 'Длительность GIF (секунды)',
                'gif_fps': 'Частота кадров (fps)',
                'gif_quality': 'Качество (1-30, меньше=лучше)',
                'btn_capture': '📸 Захватить',
                'btn_cancel': '❌ Отмена',
                'btn_recorder': '🎬 Запись экрана',
                'saved_in': 'Снимок сохранён в',
                'image': 'PNG изображение',
                'gif': 'Анимированный GIF',
                'desc_capture': 'Настроить параметры захвата',
                'desc_gif': 'Настроить параметры создания GIF',
                'output_folder': 'Папка вывода',
                'select_folder': 'Выбрать папку',
                'play_sound': 'Воспроизвести звук при захвате',
                'about': 'О программе',
                'about_title': 'О программе Essora Lumivio',
                'about_description': 'Инструмент для создания скриншотов и GIF для Essora Linux',
                'version': 'Версия',
                'author': 'Автор',
                'license': 'Лицензия',
                'website': 'Веб-сайт'
            },
            'ja': {
                'title': 'スクリーンショット',
                'tab_capture': 'キャプチャ',
                'tab_gif': 'GIF/動画',
                'tab_settings': '設定',
                'delay': '遅延（秒）',
                'capture_type': 'キャプチャタイプ',
                'capture_mode': 'キャプチャモード',
                'fullscreen': '全画面',
                'window': 'アクティブウィンドウ',
                'region': '領域選択',
                'filename': 'ファイル名',
                'gif_duration': 'GIFの長さ（秒）',
                'gif_fps': 'フレームレート（fps）',
                'gif_quality': '品質（1-30、低いほど良い）',
                'btn_capture': '📸 キャプチャ',
                'btn_cancel': '❌ キャンセル',
                'btn_recorder': '🎬 画面録画',
                'saved_in': 'キャプチャ保存先',
                'image': 'PNG画像',
                'gif': 'アニメーションGIF',
                'desc_capture': 'キャプチャオプションを設定',
                'desc_gif': 'GIF作成オプションを設定',
                'output_folder': '出力フォルダ',
                'select_folder': 'フォルダを選択',
                'play_sound': 'キャプチャ時に音を再生',
                'about': 'について',
                'about_title': 'Essora Lumivioについて',
                'about_description': 'Essora Linux用のスクリーンショットとGIF作成ツール',
                'version': 'バージョン',
                'author': '作者',
                'license': 'ライセンス',
                'website': 'ウェブサイト'
            },
            'zh': {
                'title': '屏幕截图',
                'tab_capture': '捕获',
                'tab_gif': 'GIF/视频',
                'tab_settings': '设置',
                'delay': '延迟（秒）',
                'capture_type': '捕获类型',
                'capture_mode': '捕获模式',
                'fullscreen': '全屏',
                'window': '活动窗口',
                'region': '选择区域',
                'filename': '文件名',
                'gif_duration': 'GIF时长（秒）',
                'gif_fps': '帧率（fps）',
                'gif_quality': '质量（1-30，越低越好）',
                'btn_capture': '📸 捕获',
                'btn_cancel': '❌ 取消',
                'btn_recorder': '🎬 屏幕录制',
                'saved_in': '捕获已保存到',
                'image': 'PNG图片',
                'gif': '动画GIF',
                'desc_capture': '配置捕获选项',
                'desc_gif': '配置GIF创建选项',
                'output_folder': '输出文件夹',
                'select_folder': '选择文件夹',
                'play_sound': '捕获时播放声音',
                'about': '关于',
                'about_title': '关于 Essora Lumivio',
                'about_description': 'Essora Linux的屏幕截图和GIF创建工具',
                'version': '版本',
                'author': '作者',
                'license': '许可证',
                'website': '网站'
            }
        }
        
        return translations.get(lang_code, translations['en'])
    
    def setup_css(self):
        """Configurar CSS para tema oscuro moderno"""
        css_provider = Gtk.CssProvider()
        css = """
        window {
            background-color: #1e1e1e;
        }
        
        .notebook {
            background-color: #1e1e1e;
            border: none;
        }
        
        .notebook tab {
            background-color: #2d2d2d;
            color: #ffffff;
            border: none;
            padding: 12px 24px;
            font-weight: 500;
            border-radius: 0;
        }
        
        .notebook tab:checked {
            background-color: #3a3a3a;
            border-bottom: 3px solid #5fb3f6;
        }
        
        .notebook tab:hover {
            background-color: #353535;
        }
        
        .section-frame {
            background-color: #2d2d2d;
            border: 1px solid #3a3a3a;
            border-radius: 8px;
            padding: 16px;
            margin: 8px;
        }
        
        .section-title {
            color: #5fb3f6;
            font-size: 14px;
            font-weight: 600;
            padding: 0 0 8px 0;
        }
        
        label {
            color: #e0e0e0;
            font-size: 13px;
        }
        
        entry {
            background-color: #1e1e1e;
            color: #ffffff;
            border: 1px solid #3a3a3a;
            border-radius: 4px;
            padding: 8px;
            min-height: 32px;
        }
        
        entry:focus {
            border-color: #5fb3f6;
        }
        
        spinbutton {
            background-color: #1e1e1e;
            color: #ffffff;
            border: 1px solid #3a3a3a;
            border-radius: 4px;
        }
        
        spinbutton entry {
            background-color: #1e1e1e;
            border: none;
        }
        
        radiobutton {
            color: #e0e0e0;
        }
        
        radiobutton:checked {
            color: #5fb3f6;
        }
        
        checkbutton {
            color: #e0e0e0;
        }
        
        checkbutton:checked {
            color: #5fb3f6;
        }
        
        combobox button {
            background-color: #1e1e1e;
            color: #ffffff;
            border: 1px solid #3a3a3a;
            border-radius: 4px;
            padding: 8px;
        }
        
        .action-button {
            background: linear-gradient(135deg, #5fb3f6 0%, #4a9fd8 100%);
            color: #ffffff;
            border: none;
            border-radius: 6px;
            padding: 12px 24px;
            font-weight: 600;
            font-size: 14px;
            min-height: 44px;
        }
        
        .action-button:hover {
            background: linear-gradient(135deg, #6ec0ff 0%, #5ab3e8 100%);
        }
        
        .cancel-button {
            background-color: #3a3a3a;
            color: #ffffff;
            border: 1px solid #4a4a4a;
            border-radius: 6px;
            padding: 12px 24px;
            font-weight: 600;
            font-size: 14px;
            min-height: 44px;
        }
        
        .cancel-button:hover {
            background-color: #454545;
        }
        
        .recorder-button {
            background: linear-gradient(135deg, #f65f9a 0%, #d84a7c 100%);
            color: #ffffff;
            border: none;
            border-radius: 6px;
            padding: 12px 24px;
            font-weight: 600;
            font-size: 14px;
            min-height: 44px;
        }
        
        .recorder-button:hover {
            background: linear-gradient(135deg, #ff6ea8 0%, #e85a8c 100%);
        }
        
        .headerbar {
            background-color: #2d2d2d;
            border-bottom: 1px solid #3a3a3a;
        }
        """
        
        css_provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
    
    def create_ui(self):
        """Crear interfaz de usuario"""
        # Crear HeaderBar
        headerbar = Gtk.HeaderBar()
        headerbar.set_show_close_button(True)
        headerbar.set_title("Essora Lumivio")
        headerbar.props.title = "Essora Lumivio"
        self.set_titlebar(headerbar)
        
        # Botón de menú (3 puntos)
        menu_button = Gtk.MenuButton()
        menu_icon = Gtk.Image.new_from_icon_name("open-menu-symbolic", Gtk.IconSize.BUTTON)
        menu_button.set_image(menu_icon)
        
        # Crear menú
        menu = Gtk.Menu()
        
        about_item = Gtk.MenuItem(label=self.strings['about'])
        about_item.connect("activate", self.show_about_dialog)
        menu.append(about_item)
        
        menu.show_all()
        menu_button.set_popup(menu)
        
        headerbar.pack_end(menu_button)
        
        # Contenedor principal
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(main_box)
        
        # Crear notebook para pestañas
        notebook = Gtk.Notebook()
        notebook.set_name("notebook")
        notebook.get_style_context().add_class("notebook")
        main_box.pack_start(notebook, True, True, 0)
        
        # Pestaña 1: Captura
        capture_page = self.create_capture_page()
        notebook.append_page(capture_page, Gtk.Label(label=self.strings['tab_capture']))
        
        # Pestaña 2: GIF/Video
        gif_page = self.create_gif_page()
        notebook.append_page(gif_page, Gtk.Label(label=self.strings['tab_gif']))
        
        # Pestaña 3: Configuración
        settings_page = self.create_settings_page()
        notebook.append_page(settings_page, Gtk.Label(label=self.strings['tab_settings']))
        
        # Botones de acción
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        button_box.set_margin_start(16)
        button_box.set_margin_end(16)
        button_box.set_margin_top(12)
        button_box.set_margin_bottom(16)
        
        # Botón Grabador
        recorder_btn = Gtk.Button(label=self.strings['btn_recorder'])
        recorder_btn.get_style_context().add_class("recorder-button")
        recorder_btn.connect("clicked", self.on_recorder_clicked)
        recorder_btn.set_size_request(200, -1)
        button_box.pack_start(recorder_btn, True, True, 0)
        
        # Botón Capturar
        self.capture_btn = Gtk.Button(label=self.strings['btn_capture'])
        self.capture_btn.get_style_context().add_class("action-button")
        self.capture_btn.connect("clicked", self.on_capture_clicked)
        self.capture_btn.set_size_request(200, -1)
        button_box.pack_start(self.capture_btn, True, True, 0)
        
        # Botón Cancelar
        cancel_btn = Gtk.Button(label=self.strings['btn_cancel'])
        cancel_btn.get_style_context().add_class("cancel-button")
        cancel_btn.connect("clicked", lambda x: self.destroy())
        cancel_btn.set_size_request(200, -1)
        button_box.pack_start(cancel_btn, True, True, 0)
        
        main_box.pack_start(button_box, False, False, 0)
    
    def create_section_frame(self, title, content_widget):
        """Crear un marco de sección con título"""
        frame = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        frame.get_style_context().add_class("section-frame")
        
        # Título de sección
        title_label = Gtk.Label()
        title_label.set_markup(f"<b>{title}</b>")
        title_label.set_xalign(0)
        title_label.get_style_context().add_class("section-title")
        frame.pack_start(title_label, False, False, 0)
        
        # Contenido
        frame.pack_start(content_widget, True, True, 0)
        
        return frame
    
    def create_capture_page(self):
        """Crear página de captura"""
        page_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        page_box.set_margin_start(16)
        page_box.set_margin_end(16)
        page_box.set_margin_top(16)
        page_box.set_margin_bottom(16)
        
        # Sección: Modo de captura
        mode_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        
        self.mode_fullscreen = Gtk.RadioButton(label=self.strings['fullscreen'])
        mode_content.pack_start(self.mode_fullscreen, False, False, 0)
        
        self.mode_window = Gtk.RadioButton(label=self.strings['window'], group=self.mode_fullscreen)
        mode_content.pack_start(self.mode_window, False, False, 0)
        
        self.mode_region = Gtk.RadioButton(label=self.strings['region'], group=self.mode_fullscreen)
        mode_content.pack_start(self.mode_region, False, False, 0)
        
        mode_frame = self.create_section_frame(self.strings['capture_mode'], mode_content)
        page_box.pack_start(mode_frame, False, False, 0)
        
        # Sección: Opciones
        options_content = Gtk.Grid()
        options_content.set_column_spacing(12)
        options_content.set_row_spacing(12)
        
        # Retardo
        delay_label = Gtk.Label(label=self.strings['delay'])
        delay_label.set_xalign(0)
        options_content.attach(delay_label, 0, 0, 1, 1)
        
        self.delay_spin = Gtk.SpinButton()
        self.delay_spin.set_range(0, 30)
        self.delay_spin.set_increments(1, 5)
        self.delay_spin.set_value(1)
        self.delay_spin.set_hexpand(True)
        options_content.attach(self.delay_spin, 1, 0, 1, 1)
        
        # Nombre de archivo
        filename_label = Gtk.Label(label=self.strings['filename'])
        filename_label.set_xalign(0)
        options_content.attach(filename_label, 0, 1, 1, 1)
        
        self.filename_entry = Gtk.Entry()
        self.filename_entry.set_text("screenshot")
        self.filename_entry.set_hexpand(True)
        options_content.attach(self.filename_entry, 1, 1, 1, 1)
        
        options_frame = self.create_section_frame(self.strings['capture_type'], options_content)
        page_box.pack_start(options_frame, False, False, 0)
        
        return page_box
    
    def create_gif_page(self):
        """Crear página de GIF"""
        page_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        page_box.set_margin_start(16)
        page_box.set_margin_end(16)
        page_box.set_margin_top(16)
        page_box.set_margin_bottom(16)
        
        # Sección: Parámetros del GIF
        gif_content = Gtk.Grid()
        gif_content.set_column_spacing(12)
        gif_content.set_row_spacing(12)
        
        # Duración
        duration_label = Gtk.Label(label=self.strings['gif_duration'])
        duration_label.set_xalign(0)
        gif_content.attach(duration_label, 0, 0, 1, 1)
        
        self.gif_duration_spin = Gtk.SpinButton()
        self.gif_duration_spin.set_range(1, 60)
        self.gif_duration_spin.set_increments(1, 5)
        self.gif_duration_spin.set_value(5)
        self.gif_duration_spin.set_hexpand(True)
        gif_content.attach(self.gif_duration_spin, 1, 0, 1, 1)
        
        # FPS
        fps_label = Gtk.Label(label=self.strings['gif_fps'])
        fps_label.set_xalign(0)
        gif_content.attach(fps_label, 0, 1, 1, 1)
        
        self.gif_fps_spin = Gtk.SpinButton()
        self.gif_fps_spin.set_range(1, 60)
        self.gif_fps_spin.set_increments(1, 5)
        self.gif_fps_spin.set_value(10)
        self.gif_fps_spin.set_hexpand(True)
        gif_content.attach(self.gif_fps_spin, 1, 1, 1, 1)
        
        # Calidad
        quality_label = Gtk.Label(label=self.strings['gif_quality'])
        quality_label.set_xalign(0)
        gif_content.attach(quality_label, 0, 2, 1, 1)
        
        self.gif_quality_spin = Gtk.SpinButton()
        self.gif_quality_spin.set_range(1, 30)
        self.gif_quality_spin.set_increments(1, 5)
        self.gif_quality_spin.set_value(15)
        self.gif_quality_spin.set_hexpand(True)
        gif_content.attach(self.gif_quality_spin, 1, 2, 1, 1)
        
        # Nombre de archivo
        filename_label = Gtk.Label(label=self.strings['filename'])
        filename_label.set_xalign(0)
        gif_content.attach(filename_label, 0, 3, 1, 1)
        
        self.gif_filename_entry = Gtk.Entry()
        self.gif_filename_entry.set_text("recording")
        self.gif_filename_entry.set_hexpand(True)
        gif_content.attach(self.gif_filename_entry, 1, 3, 1, 1)
        
        gif_frame = self.create_section_frame(self.strings['gif'], gif_content)
        page_box.pack_start(gif_frame, False, False, 0)
        
        # Sección: Modo de captura para GIF
        mode_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        
        self.gif_mode_fullscreen = Gtk.RadioButton(label=self.strings['fullscreen'])
        mode_content.pack_start(self.gif_mode_fullscreen, False, False, 0)
        
        self.gif_mode_window = Gtk.RadioButton(label=self.strings['window'], group=self.gif_mode_fullscreen)
        mode_content.pack_start(self.gif_mode_window, False, False, 0)
        
        self.gif_mode_region = Gtk.RadioButton(label=self.strings['region'], group=self.gif_mode_fullscreen)
        mode_content.pack_start(self.gif_mode_region, False, False, 0)
        
        mode_frame = self.create_section_frame(self.strings['capture_mode'], mode_content)
        page_box.pack_start(mode_frame, False, False, 0)
        
        return page_box
    
    def create_settings_page(self):
        """Crear página de configuración"""
        page_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        page_box.set_margin_start(16)
        page_box.set_margin_end(16)
        page_box.set_margin_top(16)
        page_box.set_margin_bottom(16)
        
        # Sección: Carpeta de salida
        folder_content = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        
        self.folder_entry = Gtk.Entry()
        self.folder_entry.set_text(self.output_dir)
        self.folder_entry.set_editable(False)
        self.folder_entry.set_hexpand(True)
        folder_content.pack_start(self.folder_entry, True, True, 0)
        
        folder_btn = Gtk.Button(label=self.strings['select_folder'])
        folder_btn.connect("clicked", self.on_select_folder)
        folder_content.pack_start(folder_btn, False, False, 0)
        
        folder_frame = self.create_section_frame(self.strings['output_folder'], folder_content)
        page_box.pack_start(folder_frame, False, False, 0)
        
        # Sección: Opciones de sonido
        sound_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        
        self.play_sound_check = Gtk.CheckButton(label=self.strings['play_sound'])
        self.play_sound_check.set_active(True)
        sound_content.pack_start(self.play_sound_check, False, False, 0)
        
        sound_frame = self.create_section_frame("Audio", sound_content)
        page_box.pack_start(sound_frame, False, False, 0)
        
        return page_box
    
    def on_select_folder(self, widget):
        """Seleccionar carpeta de salida"""
        dialog = Gtk.FileChooserDialog(
            title=self.strings['select_folder'],
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK
        )
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.output_dir = dialog.get_filename()
            self.folder_entry.set_text(self.output_dir)
        
        dialog.destroy()
    
    def on_capture_clicked(self, widget):
        """Manejar clic en botón capturar"""
        # Determinar qué pestaña está activa
        notebook = None
        for child in self.get_children():
            if isinstance(child, Gtk.Box):
                for subchild in child.get_children():
                    if isinstance(subchild, Gtk.Notebook):
                        notebook = subchild
                        break
        
        if notebook:
            current_page = notebook.get_current_page()
            if current_page == 0:
                self.capture_screenshot()
            elif current_page == 1:
                self.capture_gif()
    
    def capture_screenshot(self):
        """Capturar screenshot"""
        delay = int(self.delay_spin.get_value())
        filename = self.filename_entry.get_text() or "screenshot"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(self.output_dir, f"{filename}_{timestamp}.png")
        
        # Minimizar ventana antes de capturar
        self.iconify()
        
        # Determinar modo de captura
        if self.mode_window.get_active():
            mode = "-u"  # Ventana activa
        elif self.mode_region.get_active():
            mode = "-s"  # Selección
        else:
            mode = ""    # Pantalla completa
        
        # Dar tiempo a que la ventana se minimice (300ms)
        GLib.timeout_add(300, self._execute_screenshot, delay, mode, output_file)
    
    def _execute_screenshot(self, delay, mode, output_file):
        """Ejecutar la captura de screenshot"""
        # Ejecutar scrot
        cmd = f"scrot -d {delay} {mode} '{output_file}'"
        
        try:
            subprocess.run(cmd, shell=True, check=True)
            
            # Restaurar ventana
            self.present()
            
            # Reproducir sonido
            if self.play_sound_check.get_active() and os.path.exists(self.sound_file):
                subprocess.Popen(["aplay", self.sound_file], 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
            
            # Mostrar notificación
            self.show_notification(f"{self.strings['saved_in']}\n{output_file}")
            
        except subprocess.CalledProcessError:
            # Restaurar ventana en caso de error
            self.present()
            self.show_error("Error al capturar pantalla")
        
        return False
    
    def capture_gif(self):
        """Capturar GIF"""
        delay = int(self.delay_spin.get_value())
        duration = int(self.gif_duration_spin.get_value())
        fps = int(self.gif_fps_spin.get_value())
        quality = int(self.gif_quality_spin.get_value())
        filename = self.gif_filename_entry.get_text() or "recording"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(self.output_dir, f"{filename}_{timestamp}.gif")
        
        # Minimizar ventana antes de capturar
        self.iconify()
        
        # Crear archivo temporal
        temp_file = tempfile.mktemp(suffix=".mp4")
        
        # Obtener resolución de pantalla
        try:
            screen_res = subprocess.check_output(
                "xrandr | grep '\\*' | awk '{print $1}'",
                shell=True
            ).decode().strip()
        except:
            screen_res = "1920x1080"
        
        # Determinar modo de captura
        mode_cmd = ""
        if self.gif_mode_window.get_active():
            mode_cmd = "window"
        elif self.gif_mode_region.get_active():
            mode_cmd = "region"
        else:
            mode_cmd = "fullscreen"
        
        # Dar tiempo a que la ventana se minimice (300ms) + delay del usuario
        total_delay = delay if delay > 0 else 0
        GLib.timeout_add(300, self._start_gif_capture,
                        mode_cmd, screen_res, fps, duration, 
                        temp_file, output_file, quality, total_delay)
    
    def _start_gif_capture(self, mode_cmd, screen_res, fps, duration, temp_file, output_file, quality, delay):
        """Iniciar captura de GIF después de minimizar"""
        if delay > 0:
            GLib.timeout_add_seconds(delay, self.execute_gif_capture,
                                    mode_cmd, screen_res, fps, duration, 
                                    temp_file, output_file, quality)
        else:
            self.execute_gif_capture(mode_cmd, screen_res, fps, duration,
                                    temp_file, output_file, quality)
        return False
    
    def execute_gif_capture(self, mode, screen_res, fps, duration, temp_file, output_file, quality):
        """Ejecutar captura de GIF"""
        try:
            display = os.environ.get('DISPLAY', ':0.0')
            
            if mode == "fullscreen":
                # Captura pantalla completa
                cmd1 = [
                    'ffmpeg', '-y', '-f', 'x11grab',
                    '-video_size', screen_res,
                    '-framerate', str(fps),
                    '-i', display,
                    '-t', str(duration),
                    temp_file
                ]
                subprocess.run(cmd1, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                
            elif mode == "region":
                # Captura región seleccionada
                slop_output = subprocess.check_output(['slop', '-f', '%x %y %w %h']).decode().strip()
                if slop_output:
                    x, y, w, h = slop_output.split()
                    cmd1 = [
                        'ffmpeg', '-y', '-f', 'x11grab',
                        '-video_size', f'{w}x{h}',
                        '-framerate', str(fps),
                        '-i', f'{display}+{x},{y}',
                        '-t', str(duration),
                        temp_file
                    ]
                    subprocess.run(cmd1, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            
            # Convertir a GIF
            palette_filter = f"fps={fps},scale=iw:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=256:stats_mode=diff[p];[s1][p]paletteuse=dither=bayer:bayer_scale=3"
            
            cmd2 = [
                'ffmpeg', '-y', '-i', temp_file,
                '-vf', palette_filter,
                '-loop', '0',
                '-compression_level', str(quality),
                output_file
            ]
            subprocess.run(cmd2, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            
            # Limpiar archivo temporal
            if os.path.exists(temp_file):
                os.remove(temp_file)
            
            # Restaurar ventana
            self.present()
            
            # Reproducir sonido
            if self.play_sound_check.get_active() and os.path.exists(self.sound_file):
                subprocess.Popen(["aplay", self.sound_file],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
            
            # Mostrar notificación
            self.show_notification(f"{self.strings['saved_in']}\n{output_file}")
            
        except Exception as e:
            # Restaurar ventana en caso de error
            self.present()
            self.show_error(f"Error al crear GIF: {str(e)}")
        
        return False
    
    def on_recorder_clicked(self, widget):
        """Abrir grabador de pantalla"""
        try:
            # Abrir Screen_Recorder.py
            subprocess.Popen(["/usr/local/Lumivio/Screen_Recorder.py"])
            # Cerrar esta ventana
            self.destroy()
        except Exception as e:
            self.show_error(f"No se pudo abrir el grabador de pantalla: {str(e)}")
    
    def show_notification(self, message):
        """Mostrar notificación"""
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=self.strings['title']
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()
    
    def show_error(self, message):
        """Mostrar error"""
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text="Error"
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()
    
    def show_about_dialog(self, widget):
        """Mostrar diálogo About"""
        dialog = Gtk.AboutDialog()
        dialog.set_transient_for(self)
        dialog.set_modal(True)
        
        # Configurar información
        dialog.set_program_name("Essora Lumivio")
        dialog.set_version("1.2.0")
        dialog.set_comments(self.strings['about_description'])
        dialog.set_copyright("Copyright © 2025 josejp2424")
        dialog.set_authors(["josejp2424"])
        dialog.set_license_type(Gtk.License.GPL_3_0)
        dialog.set_website("https://github.com/josejp2424")
        dialog.set_website_label("GitHub")
        
        # Configurar logo/icono
        if os.path.exists(self.icon_path):
            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    self.icon_path, 128, 128, True
                )
                dialog.set_logo(pixbuf)
            except:
                pass
        
        dialog.run()
        dialog.destroy()


def main():
    app = EssoraLumivioApp()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
