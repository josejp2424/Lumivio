#!/usr/bin/env python3
# =============================================================================
# Essora Screen Recorder
# Autor: josejp2424
# Descripción: Grabador de pantalla con control completo para Essora
# Versión: 1.0.0
# Licencia: GPL-3.0
# =============================================================================

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import subprocess
import os
import locale
import signal
import time
from datetime import datetime
import threading


try:
    gi.require_version('AppIndicator3', '0.1')
    from gi.repository import AppIndicator3
    HAS_APPINDICATOR = True
except (ValueError, ImportError):
    HAS_APPINDICATOR = False
    try:
        gi.require_version('AyatanaAppIndicator3', '0.1')
        from gi.repository import AyatanaAppIndicator3 as AppIndicator3
        HAS_APPINDICATOR = True
    except (ValueError, ImportError):
        HAS_APPINDICATOR = False

class ScreenRecorderApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Essora Screen Recorder")
        self.set_default_size(550, 450)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(False)
        

        self.setup_language()
        

        self.sound_file = "/usr/local/Lumivio/camera-shutter.wav"
        self.icon_path = "/usr/local/Lumivio/camera.svg"
        

        if os.path.exists(self.icon_path):
            self.set_icon_from_file(self.icon_path)
        

        self.is_recording = False
        self.is_paused = False
        self.ffmpeg_process = None
        self.current_output = ""
        self.current_screen = ""
        

        self.frame_rate = 25
        self.video_quality = 23
        self.audio_bitrate = 128
        self.output_dir = os.path.expanduser("~")
        self.file_name = "Recording"
        self.file_ext = "mp4"
        

        self.create_ui()
        

        self.indicator = None
        self.setup_indicator()
        
    def setup_language(self):
        """Detectar y configurar idioma del sistema"""
        try:

            try:
                locale.setlocale(locale.LC_ALL, '')
                lang = locale.getlocale()[0]
            except:
                lang = None
            
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
                'title': 'Grabador de Pantalla',
                'screen_prompt': 'Seleccione pantalla',
                'audio_prompt': 'Incluir audio (solo interno)',
                'quality_prompt': 'Calidad de video (0-51, menor=mejor)',
                'framerate_prompt': 'Tasa de frames (fps)',
                'dir_prompt': 'Carpeta destino',
                'name_prompt': 'Nombre del archivo',
                'format_prompt': 'Formato de salida',
                'record_button': '▶️ Iniciar Grabación',
                'stop_button': '⏹ Detener',
                'pause_button': '⏸ Pausar',
                'resume_button': '▶ Reanudar',
                'exit_button': '❌ Salir',
                'open_button': '📂 Abrir carpeta',
                'preview_button': '🎬 Vista previa',
                'close_button': 'Cerrar',
                'recording_title': 'Grabación en curso',
                'complete_title': 'Grabación completada',
                'complete_text': 'Archivo guardado en:',
                'error_title': 'Error',
                'screen_error': 'No se pudo obtener información de la pantalla',
                'no_player_error': 'No se encontró ningún reproductor compatible (mpv, mplayer o ffplay)',
                'select_folder': 'Seleccionar carpeta',
                'recording': 'Grabando',
                'paused': 'Pausado',
                'settings': 'Configuración',
                'back_to_lumivio': '↩️ Volver a Lumivio'
            },
            'en': {
                'title': 'Screen Recorder',
                'screen_prompt': 'Select screen',
                'audio_prompt': 'Include audio (internal only)',
                'quality_prompt': 'Video quality (0-51, lower=better)',
                'framerate_prompt': 'Frame rate (fps)',
                'dir_prompt': 'Destination folder',
                'name_prompt': 'File name',
                'format_prompt': 'Output format',
                'record_button': '▶️ Start Recording',
                'stop_button': '⏹ Stop',
                'pause_button': '⏸ Pause',
                'resume_button': '▶ Resume',
                'exit_button': '❌ Exit',
                'open_button': '📂 Open Folder',
                'preview_button': '🎬 Preview',
                'close_button': 'Close',
                'recording_title': 'Recording in progress',
                'complete_title': 'Recording Complete',
                'complete_text': 'File saved at:',
                'error_title': 'Error',
                'screen_error': 'Could not get screen information',
                'no_player_error': 'No compatible player found (mpv, mplayer or ffplay)',
                'select_folder': 'Select folder',
                'recording': 'Recording',
                'paused': 'Paused',
                'settings': 'Settings',
                'back_to_lumivio': '↩️ Back to Lumivio'
            },
            'fr': {
                'title': 'Enregistreur d\'écran',
                'screen_prompt': 'Sélectionnez l\'écran',
                'audio_prompt': 'Inclure l\'audio (interne seulement)',
                'quality_prompt': 'Qualité vidéo (0-51, plus bas=meilleur)',
                'framerate_prompt': 'Fréquence d\'images (fps)',
                'dir_prompt': 'Dossier de destination',
                'name_prompt': 'Nom du fichier',
                'format_prompt': 'Format de sortie',
                'record_button': '▶️ Démarrer l\'enregistrement',
                'stop_button': '⏹ Arrêter',
                'pause_button': '⏸ Pause',
                'resume_button': '▶ Reprendre',
                'exit_button': '❌ Quitter',
                'open_button': '📂 Ouvrir le dossier',
                'preview_button': '🎬 Aperçu',
                'close_button': 'Fermer',
                'recording_title': 'Enregistrement en cours',
                'complete_title': 'Enregistrement terminé',
                'complete_text': 'Fichier enregistré dans:',
                'error_title': 'Erreur',
                'screen_error': 'Impossible d\'obtenir les informations de l\'écran',
                'no_player_error': 'Aucun lecteur compatible trouvé (mpv, mplayer ou ffplay)',
                'select_folder': 'Sélectionner dossier',
                'recording': 'Enregistrement',
                'paused': 'En pause',
                'settings': 'Paramètres',
                'back_to_lumivio': '↩️ Retour à Lumivio'
            },
            'de': {
                'title': 'Bildschirmrekorder',
                'screen_prompt': 'Bildschirm auswählen',
                'audio_prompt': 'Audio einbeziehen (nur intern)',
                'quality_prompt': 'Videoqualität (0-51, niedriger=besser)',
                'framerate_prompt': 'Bildrate (fps)',
                'dir_prompt': 'Zielordner',
                'name_prompt': 'Dateiname',
                'format_prompt': 'Ausgabeformat',
                'record_button': '▶️ Aufnahme starten',
                'stop_button': '⏹ Stoppen',
                'pause_button': '⏸ Pause',
                'resume_button': '▶ Fortsetzen',
                'exit_button': '❌ Beenden',
                'open_button': '📂 Ordner öffnen',
                'preview_button': '🎬 Vorschau',
                'close_button': 'Schließen',
                'recording_title': 'Aufnahme läuft',
                'complete_title': 'Aufnahme abgeschlossen',
                'complete_text': 'Datei gespeichert in:',
                'error_title': 'Fehler',
                'screen_error': 'Bildschirminformationen konnten nicht abgerufen werden',
                'no_player_error': 'Kein kompatibler Player gefunden (mpv, mplayer oder ffplay)',
                'select_folder': 'Ordner auswählen',
                'recording': 'Aufnahme',
                'paused': 'Pausiert',
                'settings': 'Einstellungen',
                'back_to_lumivio': '↩️ Zurück zu Lumivio'
            },
            'it': {
                'title': 'Registratore Schermo',
                'screen_prompt': 'Seleziona schermo',
                'audio_prompt': 'Includi audio (solo interno)',
                'quality_prompt': 'Qualità video (0-51, più basso=migliore)',
                'framerate_prompt': 'Frame rate (fps)',
                'dir_prompt': 'Cartella destinazione',
                'name_prompt': 'Nome file',
                'format_prompt': 'Formato output',
                'record_button': '▶️ Inizia registrazione',
                'stop_button': '⏹ Ferma',
                'pause_button': '⏸ Pausa',
                'resume_button': '▶ Riprendi',
                'exit_button': '❌ Esci',
                'open_button': '📂 Apri cartella',
                'preview_button': '🎬 Anteprima',
                'close_button': 'Chiudi',
                'recording_title': 'Registrazione in corso',
                'complete_title': 'Registrazione completata',
                'complete_text': 'File salvato in:',
                'error_title': 'Errore',
                'screen_error': 'Impossibile ottenere informazioni sullo schermo',
                'no_player_error': 'Nessun lettore compatibile trovato (mpv, mplayer o ffplay)',
                'select_folder': 'Seleziona cartella',
                'recording': 'Registrazione',
                'paused': 'In pausa',
                'settings': 'Impostazioni',
                'back_to_lumivio': '↩️ Torna a Lumivio'
            },
            'pt': {
                'title': 'Gravador de Tela',
                'screen_prompt': 'Selecione tela',
                'audio_prompt': 'Incluir áudio (apenas interno)',
                'quality_prompt': 'Qualidade de vídeo (0-51, menor=melhor)',
                'framerate_prompt': 'Taxa de quadros (fps)',
                'dir_prompt': 'Pasta destino',
                'name_prompt': 'Nome do arquivo',
                'format_prompt': 'Formato de saída',
                'record_button': '▶️ Iniciar Gravação',
                'stop_button': '⏹ Parar',
                'pause_button': '⏸ Pausar',
                'resume_button': '▶ Retomar',
                'exit_button': '❌ Sair',
                'open_button': '📂 Abrir pasta',
                'preview_button': '🎬 Visualizar',
                'close_button': 'Fechar',
                'recording_title': 'Gravação em andamento',
                'complete_title': 'Gravação concluída',
                'complete_text': 'Arquivo salvo em:',
                'error_title': 'Erro',
                'screen_error': 'Não foi possível obter informações da tela',
                'no_player_error': 'Nenhum reprodutor compatível encontrado (mpv, mplayer ou ffplay)',
                'select_folder': 'Selecionar pasta',
                'recording': 'Gravando',
                'paused': 'Pausado',
                'settings': 'Configurações',
                'back_to_lumivio': '↩️ Voltar ao Lumivio'
            },
            'ru': {
                'title': 'Запись экрана',
                'screen_prompt': 'Выберите экран',
                'audio_prompt': 'Включить звук (только внутренний)',
                'quality_prompt': 'Качество видео (0-51, меньше=лучше)',
                'framerate_prompt': 'Частота кадров (fps)',
                'dir_prompt': 'Папка назначения',
                'name_prompt': 'Имя файла',
                'format_prompt': 'Формат вывода',
                'record_button': '▶️ Начать запись',
                'stop_button': '⏹ Остановить',
                'pause_button': '⏸ Пауза',
                'resume_button': '▶ Продолжить',
                'exit_button': '❌ Выход',
                'open_button': '📂 Открыть папку',
                'preview_button': '🎬 Превью',
                'close_button': 'Закрыть',
                'recording_title': 'Идет запись',
                'complete_title': 'Запись завершена',
                'complete_text': 'Файл сохранен в:',
                'error_title': 'Ошибка',
                'screen_error': 'Не удалось получить информацию об экране',
                'no_player_error': 'Совместимый плеер не найден (mpv, mplayer или ffplay)',
                'select_folder': 'Выбрать папку',
                'recording': 'Запись',
                'paused': 'Приостановлено',
                'settings': 'Настройки',
                'back_to_lumivio': '↩️ Вернуться в Lumivio'
            },
            'ja': {
                'title': '画面録画',
                'screen_prompt': '画面を選択',
                'audio_prompt': '音声を含める（内部のみ）',
                'quality_prompt': 'ビデオ品質（0-51、低いほど良い）',
                'framerate_prompt': 'フレームレート（fps）',
                'dir_prompt': '保存先フォルダ',
                'name_prompt': 'ファイル名',
                'format_prompt': '出力形式',
                'record_button': '▶️ 録画開始',
                'stop_button': '⏹ 停止',
                'pause_button': '⏸ 一時停止',
                'resume_button': '▶ 再開',
                'exit_button': '❌ 終了',
                'open_button': '📂 フォルダを開く',
                'preview_button': '🎬 プレビュー',
                'close_button': '閉じる',
                'recording_title': '録画中',
                'complete_title': '録画完了',
                'complete_text': 'ファイル保存先:',
                'error_title': 'エラー',
                'screen_error': '画面情報を取得できませんでした',
                'no_player_error': '互換性のあるプレーヤーが見つかりません（mpv、mplayer、またはffplay）',
                'select_folder': 'フォルダを選択',
                'recording': '録画中',
                'paused': '一時停止',
                'settings': '設定',
                'back_to_lumivio': '↩️ Lumivioに戻る'
            },
            'zh': {
                'title': '屏幕录制',
                'screen_prompt': '选择屏幕',
                'audio_prompt': '包含音频（仅内部）',
                'quality_prompt': '视频质量（0-51，越低越好）',
                'framerate_prompt': '帧率（fps）',
                'dir_prompt': '目标文件夹',
                'name_prompt': '文件名',
                'format_prompt': '输出格式',
                'record_button': '▶️ 开始录制',
                'stop_button': '⏹ 停止',
                'pause_button': '⏸ 暂停',
                'resume_button': '▶ 恢复',
                'exit_button': '❌ 退出',
                'open_button': '📂 打开文件夹',
                'preview_button': '🎬 预览',
                'close_button': '关闭',
                'recording_title': '正在录制',
                'complete_title': '录制完成',
                'complete_text': '文件已保存至:',
                'error_title': '错误',
                'screen_error': '无法获取屏幕信息',
                'no_player_error': '未找到兼容的播放器（mpv、mplayer或ffplay）',
                'select_folder': '选择文件夹',
                'recording': '录制中',
                'paused': '已暂停',
                'settings': '设置',
                'back_to_lumivio': '↩️ 返回Lumivio'
            },
            'ar': {
                'title': 'مسجل الشاشة',
                'screen_prompt': 'اختر الشاشة',
                'audio_prompt': 'تضمين الصوت (داخلي فقط)',
                'quality_prompt': 'جودة الفيديو (0-51، أقل=أفضل)',
                'framerate_prompt': 'معدل الإطارات (fps)',
                'dir_prompt': 'مجلد الوجهة',
                'name_prompt': 'اسم الملف',
                'format_prompt': 'صيغة الإخراج',
                'record_button': '▶️ بدء التسجيل',
                'stop_button': '⏹ إيقاف',
                'pause_button': '⏸ إيقاف مؤقت',
                'resume_button': '▶ استئناف',
                'exit_button': '❌ خروج',
                'open_button': '📂 فتح المجلد',
                'preview_button': '🎬 معاينة',
                'close_button': 'إغلاق',
                'recording_title': 'جاري التسجيل',
                'complete_title': 'اكتمل التسجيل',
                'complete_text': 'تم حفظ الملف في:',
                'error_title': 'خطأ',
                'screen_error': 'تعذر الحصول على معلومات الشاشة',
                'no_player_error': 'لم يتم العثور على مشغل متوافق (mpv, mplayer أو ffplay)',
                'select_folder': 'اختر المجلد',
                'recording': 'جاري التسجيل',
                'paused': 'متوقف مؤقتاً',
                'settings': 'الإعدادات',
                'back_to_lumivio': '↩️ العودة إلى Lumivio'
            }
        }
        
        return translations.get(lang_code, translations['en'])
    

    def create_ui(self):
        """Crear interfaz de usuario"""

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(main_box)
        

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        main_box.pack_start(scroll, True, True, 0)
        
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        content_box.set_margin_start(16)
        content_box.set_margin_end(16)
        content_box.set_margin_top(16)
        content_box.set_margin_bottom(16)
        scroll.add(content_box)
        

        screen_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        
        screen_label = Gtk.Label(label=self.strings['screen_prompt'])
        screen_label.set_xalign(0)
        screen_content.pack_start(screen_label, False, False, 0)
        
        self.screen_combo = Gtk.ComboBoxText()
        self.populate_screens()
        screen_content.pack_start(self.screen_combo, False, False, 0)
        
        screen_frame = self.create_section_frame("📺 " + self.strings['screen_prompt'], screen_content)
        content_box.pack_start(screen_frame, False, False, 0)
        

        video_content = Gtk.Grid()
        video_content.set_column_spacing(12)
        video_content.set_row_spacing(12)
        

        self.audio_check = Gtk.CheckButton(label=self.strings['audio_prompt'])
        self.audio_check.set_active(True)
        video_content.attach(self.audio_check, 0, 0, 2, 1)
        

        quality_label = Gtk.Label(label=self.strings['quality_prompt'])
        quality_label.set_xalign(0)
        video_content.attach(quality_label, 0, 1, 1, 1)
        
        self.quality_spin = Gtk.SpinButton()
        self.quality_spin.set_range(0, 51)
        self.quality_spin.set_increments(1, 5)
        self.quality_spin.set_value(23)
        self.quality_spin.set_hexpand(True)
        video_content.attach(self.quality_spin, 1, 1, 1, 1)
        

        fps_label = Gtk.Label(label=self.strings['framerate_prompt'])
        fps_label.set_xalign(0)
        video_content.attach(fps_label, 0, 2, 1, 1)
        
        self.fps_spin = Gtk.SpinButton()
        self.fps_spin.set_range(10, 60)
        self.fps_spin.set_increments(1, 5)
        self.fps_spin.set_value(25)
        self.fps_spin.set_hexpand(True)
        video_content.attach(self.fps_spin, 1, 2, 1, 1)
        
        video_frame = self.create_section_frame("   " + self.strings['settings'], video_content)
        content_box.pack_start(video_frame, False, False, 0)
        

        output_content = Gtk.Grid()
        output_content.set_column_spacing(12)
        output_content.set_row_spacing(12)
        

        folder_label = Gtk.Label(label=self.strings['dir_prompt'])
        folder_label.set_xalign(0)
        output_content.attach(folder_label, 0, 0, 1, 1)
        
        folder_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.folder_entry = Gtk.Entry()
        self.folder_entry.set_text(self.output_dir)
        self.folder_entry.set_editable(False)
        self.folder_entry.set_hexpand(True)
        folder_box.pack_start(self.folder_entry, True, True, 0)
        
        folder_btn = Gtk.Button(label="󱅙")
        folder_btn.connect("clicked", self.on_select_folder)
        folder_box.pack_start(folder_btn, False, False, 0)
        output_content.attach(folder_box, 1, 0, 1, 1)
        

        name_label = Gtk.Label(label=self.strings['name_prompt'])
        name_label.set_xalign(0)
        output_content.attach(name_label, 0, 1, 1, 1)
        
        self.name_entry = Gtk.Entry()
        self.name_entry.set_text("Recording")
        self.name_entry.set_hexpand(True)
        output_content.attach(self.name_entry, 1, 1, 1, 1)
        

        format_label = Gtk.Label(label=self.strings['format_prompt'])
        format_label.set_xalign(0)
        output_content.attach(format_label, 0, 2, 1, 1)
        
        self.format_combo = Gtk.ComboBoxText()
        self.format_combo.append_text("mp4")
        self.format_combo.append_text("mkv")
        self.format_combo.append_text("avi")
        self.format_combo.append_text("webm")
        self.format_combo.set_active(0)
        output_content.attach(self.format_combo, 1, 2, 1, 1)
        
        output_frame = self.create_section_frame("󰉔   " + self.strings['dir_prompt'], output_content)
        content_box.pack_start(output_frame, False, False, 0)
        

        self.status_label = Gtk.Label()
        self.status_label.set_margin_top(8)
        content_box.pack_start(self.status_label, False, False, 0)
        

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        button_box.set_margin_start(16)
        button_box.set_margin_end(16)
        button_box.set_margin_top(12)
        button_box.set_margin_bottom(16)
        

        exit_btn = Gtk.Button(label=self.strings['exit_button'])
        exit_btn.connect("clicked", self.on_exit_clicked)
        button_box.pack_start(exit_btn, False, False, 0)
        

        back_btn = Gtk.Button(label=self.strings['back_to_lumivio'])
        back_btn.connect("clicked", self.on_back_to_lumivio)
        button_box.pack_start(back_btn, False, False, 0)
        

        button_box.pack_start(Gtk.Box(), True, True, 0)
        

        self.pause_btn = Gtk.Button(label=self.strings['pause_button'])
        self.pause_btn.connect("clicked", self.on_pause_clicked)
        self.pause_btn.set_sensitive(False)
        button_box.pack_start(self.pause_btn, False, False, 0)
        

        self.stop_btn = Gtk.Button(label=self.strings['stop_button'])
        self.stop_btn.connect("clicked", self.on_stop_clicked)
        self.stop_btn.set_sensitive(False)
        button_box.pack_start(self.stop_btn, False, False, 0)
        

        self.record_btn = Gtk.Button(label=self.strings['record_button'])
        self.record_btn.connect("clicked", self.on_record_clicked)
        button_box.pack_start(self.record_btn, False, False, 0)
        
        main_box.pack_start(button_box, False, False, 0)
    
    def create_section_frame(self, title, content_widget):
        """Crear un marco de sección con título"""
        frame = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        frame.get_style_context().add_class("section-frame")
        

        title_label = Gtk.Label()
        title_label.set_markup(f"<b>{title}</b>")
        title_label.set_xalign(0)
        title_label.get_style_context().add_class("section-title")
        frame.pack_start(title_label, False, False, 0)
        

        frame.pack_start(content_widget, True, True, 0)
        
        return frame
    
    def populate_screens(self):
        """Poblar lista de pantallas disponibles"""
        try:
            result = subprocess.run(
                ['xrandr', '--current'],
                capture_output=True,
                text=True,
                check=True
            )
            
            for line in result.stdout.split('\n'):
                if ' connected' in line:
                    screen_name = line.split()[0]
                    self.screen_combo.append_text(screen_name)
            
            if self.screen_combo.get_active() == -1:
                self.screen_combo.set_active(0)
                
        except subprocess.CalledProcessError:
            self.screen_combo.append_text("HDMI-1")
            self.screen_combo.set_active(0)
    
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
    
    def play_sound(self):
        """Reproducir sonido de captura"""
        if os.path.exists(self.sound_file):
            subprocess.Popen(
                ['aplay', '-q', self.sound_file],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
    
    def on_record_clicked(self, widget):
        """Iniciar grabación"""
        screen = self.screen_combo.get_active_text()
        if not screen:
            self.show_error(self.strings['screen_error'])
            return
        

        try:
            result = subprocess.run(
                ['xrandr', '--current'],
                capture_output=True,
                text=True,
                check=True
            )
            
            screen_info = None
            for line in result.stdout.split('\n'):
                if screen in line and ' connected' in line:
                    import re
                    match = re.search(r'(\d+x\d+\+\d+\+\d+)', line)
                    if match:
                        screen_info = match.group(1)
                        break
            
            if not screen_info:
                self.show_error(self.strings['screen_error'])
                return
            

            parts = screen_info.split('+')
            resolution = parts[0]
            position = f"+{parts[1]},+{parts[2]}" if len(parts) > 2 else "+0,0"
            
        except subprocess.CalledProcessError:
            self.show_error(self.strings['screen_error'])
            return
        

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = self.name_entry.get_text() or "Recording"
        file_ext = self.format_combo.get_active_text()
        self.current_output = os.path.join(
            self.output_dir,
            f"{filename}-{timestamp}.{file_ext}"
        )
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        quality = int(self.quality_spin.get_value())
        fps = int(self.fps_spin.get_value())
        
        cmd = [
            'ffmpeg', '-hide_banner', '-loglevel', 'error',
            '-f', 'x11grab',
            '-video_size', resolution,
            '-framerate', str(fps),
            '-i', f':0.0{position}'
        ]
        

        if self.audio_check.get_active():
            try:
                sink = subprocess.check_output(
                    ['pactl', 'get-default-sink'],
                    text=True
                ).strip()
                cmd.extend([
                    '-f', 'pulse',
                    '-i', f'{sink}.monitor',
                    '-c:a', 'aac',
                    '-b:a', '128k'
                ])
            except:
                pass
        
        cmd.extend([
            '-c:v', 'libx264',
            '-crf', str(quality),
            '-preset', 'veryfast',
            '-pix_fmt', 'yuv420p',
            '-y', self.current_output
        ])
        

        self.ffmpeg_process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        self.is_recording = True
        self.current_screen = screen
        

        self.record_btn.set_sensitive(False)
        self.stop_btn.set_sensitive(True)
        self.pause_btn.set_sensitive(True)
        self.status_label.set_text(f"⏺ {self.strings['recording']}: {screen}")
        

        self.update_indicator()
        

        self.play_sound()
        

        self.iconify()
    
    def on_pause_clicked(self, widget):
        """Pausar/Reanudar grabación"""
        if not self.ffmpeg_process:
            return
        
        if self.is_paused:

            os.kill(self.ffmpeg_process.pid, signal.SIGCONT)
            self.is_paused = False
            self.pause_btn.set_label(self.strings['pause_button'])
            self.status_label.set_text(f"⏺ {self.strings['recording']}: {self.current_screen}")
        else:

            os.kill(self.ffmpeg_process.pid, signal.SIGSTOP)
            self.is_paused = True
            self.pause_btn.set_label(self.strings['resume_button'])
            self.status_label.set_text(f"⏸ {self.strings['paused']}")
        

        self.update_indicator()
        

        self.play_sound()
    
    def on_stop_clicked(self, widget):
        """Detener grabación"""
        if not self.ffmpeg_process:
            return
        

        if self.is_paused:
            os.kill(self.ffmpeg_process.pid, signal.SIGCONT)
            self.is_paused = False
        

        self.ffmpeg_process.send_signal(signal.SIGINT)
        self.ffmpeg_process.wait()
        
        self.is_recording = False
        self.is_paused = False
        

        self.record_btn.set_sensitive(True)
        self.stop_btn.set_sensitive(False)
        self.pause_btn.set_sensitive(False)
        self.pause_btn.set_label(self.strings['pause_button'])
        self.status_label.set_text("")
        

        self.update_indicator()
        

        self.play_sound()
        

        self.present()
        

        if os.path.exists(self.current_output):
            self.show_complete_dialog()
    
    def on_back_to_lumivio(self, widget):
        """Volver a Lumivio"""
        if self.is_recording:
            dialog = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.QUESTION,
                buttons=Gtk.ButtonsType.YES_NO,
                text="¿Detener grabación y volver a Lumivio?"
            )
            response = dialog.run()
            dialog.destroy()
            
            if response == Gtk.ResponseType.YES:
                if self.ffmpeg_process:
                    self.ffmpeg_process.send_signal(signal.SIGINT)
                    self.ffmpeg_process.wait()

                try:
                    subprocess.Popen(["/usr/local/Lumivio/lumivio.py"])
                except:
                    pass
                self.destroy()
        else:

            try:
                subprocess.Popen(["/usr/local/Lumivio/lumivio.py"])
            except:
                pass
            self.destroy()
    
    def on_exit_clicked(self, widget):
        """Salir de la aplicación"""
        if self.is_recording:
            dialog = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.QUESTION,
                buttons=Gtk.ButtonsType.YES_NO,
                text="¿Detener grabación y salir?"
            )
            response = dialog.run()
            dialog.destroy()
            
            if response == Gtk.ResponseType.YES:
                if self.ffmpeg_process:
                    self.ffmpeg_process.send_signal(signal.SIGINT)
                    self.ffmpeg_process.wait()
                self.destroy()
        else:
            self.destroy()
    
    def show_complete_dialog(self):
        """Mostrar diálogo de grabación completada"""
        dialog = Gtk.Dialog(
            title=self.strings['complete_title'],
            transient_for=self,
            flags=0
        )
        dialog.set_default_size(400, 150)
        
        content_area = dialog.get_content_area()
        content_area.set_spacing(12)
        content_area.set_margin_start(16)
        content_area.set_margin_end(16)
        content_area.set_margin_top(16)
        content_area.set_margin_bottom(16)
        
        label = Gtk.Label()
        label.set_markup(f"<b>{self.strings['complete_text']}</b>\n{self.current_output}")
        label.set_line_wrap(True)
        content_area.pack_start(label, True, True, 0)
        

        dialog.add_button(self.strings['close_button'], Gtk.ResponseType.CLOSE)
        dialog.add_button(self.strings['preview_button'], Gtk.ResponseType.YES)
        dialog.add_button(self.strings['open_button'], Gtk.ResponseType.OK)
        
        dialog.show_all()
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            subprocess.Popen(['xdg-open', self.output_dir])
        elif response == Gtk.ResponseType.YES:
            self.preview_video(self.current_output)
        
        dialog.destroy()
    
    def preview_video(self, video_file):
        """Vista previa del video"""
        player = None
        

        if os.path.exists('/usr/local/Oply/Oply-Video.py'):
            player = ['/usr/local/Oply/Oply-Video.py', video_file]

        elif subprocess.run(['which', 'mpv'], capture_output=True).returncode == 0:
            player = ['mpv', '--quiet', '--force-window=immediate', '--loop', '--no-resume-playback', video_file]

        elif subprocess.run(['which', 'mplayer'], capture_output=True).returncode == 0:
            player = ['mplayer', '-quiet', '-loop', '0', video_file]

        elif subprocess.run(['which', 'ffplay'], capture_output=True).returncode == 0:
            player = ['ffplay', '-autoexit', '-window_title', 'Vista previa', video_file]
        else:
            self.show_error(self.strings['no_player_error'])
            return
        
        subprocess.Popen(player, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    def show_error(self, message):
        """Mostrar error"""
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=self.strings['error_title']
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()
    
    def setup_indicator(self):
        """Configurar indicador de systray"""
        if not HAS_APPINDICATOR:
            self.indicator = None
            return
            
        try:
            self.indicator = AppIndicator3.Indicator.new(
                "screen-recorder",
                self.icon_path if os.path.exists(self.icon_path) else "video-display",
                AppIndicator3.IndicatorCategory.APPLICATION_STATUS
            )
            self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
            

            self.indicator_menu = Gtk.Menu()
            self.update_indicator_menu()
            self.indicator.set_menu(self.indicator_menu)
        except Exception as e:
            print(f"No se pudo crear el indicador de systray: {e}")
            self.indicator = None
    
    def update_indicator_menu(self):
        """Actualizar menú del indicador"""
        if not self.indicator:
            return
        

        for item in self.indicator_menu.get_children():
            self.indicator_menu.remove(item)
        

        show_item = Gtk.MenuItem(label="🪟 Mostrar ventana" if not self.get_visible() else "🪟 Ocultar ventana")
        show_item.connect("activate", self.toggle_window_visibility)
        self.indicator_menu.append(show_item)
        
        self.indicator_menu.append(Gtk.SeparatorMenuItem())
        
        if self.is_recording:

            if self.is_paused:
                resume_item = Gtk.MenuItem(label=self.strings['resume_button'])
                resume_item.connect("activate", lambda x: self.on_pause_clicked(None))
                self.indicator_menu.append(resume_item)
            else:
                pause_item = Gtk.MenuItem(label=self.strings['pause_button'])
                pause_item.connect("activate", lambda x: self.on_pause_clicked(None))
                self.indicator_menu.append(pause_item)
            
            stop_item = Gtk.MenuItem(label=self.strings['stop_button'])
            stop_item.connect("activate", lambda x: self.on_stop_clicked(None))
            self.indicator_menu.append(stop_item)
            
            self.indicator_menu.append(Gtk.SeparatorMenuItem())
        

        open_item = Gtk.MenuItem(label=self.strings['open_button'])
        open_item.connect("activate", lambda x: subprocess.Popen(['xdg-open', self.output_dir]))
        self.indicator_menu.append(open_item)
        
        exit_item = Gtk.MenuItem(label=self.strings['exit_button'])
        exit_item.connect("activate", lambda x: self.on_exit_clicked(None))
        self.indicator_menu.append(exit_item)
        
        self.indicator_menu.show_all()
    
    def toggle_window_visibility(self, widget):
        """Mostrar/ocultar ventana"""
        if self.get_visible():
            self.hide()
        else:
            self.present()

        self.update_indicator_menu()
    
    def update_indicator(self):
        """Actualizar estado del indicador"""
        if not self.indicator:
            return
        
        self.update_indicator_menu()


def main():
    app = ScreenRecorderApp()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
