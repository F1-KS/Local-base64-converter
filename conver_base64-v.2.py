import tkinter as tk
from tkinter import messagebox, StringVar, OptionMenu, Scrollbar
import base64
import json
import os

# Файл для хранения настроек
CONFIG_FILE = "config.json"

# Словари для локализации
translations = {
    'ru': {
        'title': "Base64 и Base64url Кодировщик/Декодировщик",
        'version': "- версия 2.0.0",
        'input_label': "Исходный текст:",
        'output_label': "Результат:",
        'encode_base64': "Кодировать Base64",
        'decode_base64': "Декодировать Base64",
        'encode_base64url': "Кодировать Base64url",
        'decode_base64url': "Декодировать Base64url",
        'encoding_label': "Кодировка:",
        'characters': "Символов:",
        'cursor_at': "Курсор на:",
        'line_number_label': "Номер строки:",
        'input_placeholder': "Введите текст для кодирования...",
        'output_placeholder': "Результат будет здесь...",
        'warning': "Предупреждение",
        'enter_text': "Введите текст для кодирования.",
        'error': "Ошибка",
        'encoding_error': "Ошибка кодирования: {error}",
        'decoding_error': "Ошибка декодирования: {error}",
        'language': "Язык:",
        'language_ru': "Русский",
        'language_en': "English",
        'language_zh': "中文"
    },
    'en': {
        'title': "Base64 and Base64url Encoder/Decoder",
        'version': "- version 2.0.0",
        'input_label': "Input text:",
        'output_label': "Result:",
        'encode_base64': "Encode Base64",
        'decode_base64': "Decode Base64",
        'encode_base64url': "Encode Base64url",
        'decode_base64url': "Decode Base64url",
        'encoding_label': "Encoding:",
        'characters': "Characters:",
        'cursor_at': "Cursor at:",
        'line_number_label': "Line number:",
        'input_placeholder': "Enter text to encode...",
        'output_placeholder': "Result will appear here...",
        'warning': "Warning",
        'enter_text': "Enter text to encode.",
        'error': "Error",
        'encoding_error': "Encoding error: {error}",
        'decoding_error': "Decoding error: {error}",
        'language': "Language:",
        'language_ru': "Russian",
        'language_en': "English",
        'language_zh': "Chinese"
    },
    'zh': {
        'title': "Base64 和 Base64url 编码器/解码器",
        'version': "- 版本 2.0.0",
        'input_label': "输入文本:",
        'output_label': "结果:",
        'encode_base64': "编码 Base64",
        'decode_base64': "解码 Base64",
        'encode_base64url': "编码 Base64url",
        'decode_base64url': "解码 Base64url",
        'encoding_label': "编码:",
        'characters': "字符数:",
        'cursor_at': "光标位置:",
        'line_number_label': "行号:",
        'input_placeholder': "输入要编码的文本...",
        'output_placeholder': "结果将显示在这里...",
        'warning': "警告",
        'enter_text': "请输入要编码的文本。",
        'error': "错误",
        'encoding_error': "编码错误: {error}",
        'decoding_error': "解码错误: {error}",
        'language': "语言:",
        'language_ru': "俄语",
        'language_en': "英语",
        'language_zh': "中文"
    }
}

# Получение текущей локализации
def get_current_language():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('language', 'ru')
        except:
            return 'ru'
    return 'ru'

# Сохранение текущего языка
def save_language(language):
    try:
        config = {}
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
        config['language'] = language
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving language: {e}")

# Получаем текущий язык
current_language = get_current_language()
current_translations = translations[current_language]

# Функции для кодирования и декодирования
def encode_base64():
    input_text = input_text_area.get("1.0", tk.END).strip()
    encoding = encoding_var.get()
    if input_text:
        try:
            encoded_text = base64.b64encode(input_text.encode(encoding)).decode('utf-8')
            output_text_area.delete("1.0", tk.END)
            output_text_area.insert(tk.END, encoded_text)
            update_output_counter()
        except Exception as e:
            messagebox.showerror(current_translations['error'], current_translations['encoding_error'].format(error=str(e)))
    else:
        messagebox.showwarning(current_translations['warning'], current_translations['enter_text'])

def decode_base64():
    input_text = input_text_area.get("1.0", tk.END).strip()
    encoding = encoding_var.get()
    if input_text:
        normalized_input = input_text.rstrip('=')
        padding_needed = len(normalized_input) % 4
        if padding_needed:
            normalized_input += '=' * (4 - padding_needed)

        try:
            decoded_text = base64.b64decode(normalized_input).decode(encoding)
            output_text_area.delete("1.0", tk.END)
            output_text_area.insert(tk.END, decoded_text)
            update_output_counter()
        except Exception as e:
            messagebox.showerror(current_translations['error'], current_translations['decoding_error'].format(error=str(e)))
    else:
        messagebox.showwarning(current_translations['warning'], current_translations['enter_text'])

def encode_base64url():
    input_text = input_text_area.get("1.0", tk.END).strip()
    encoding = encoding_var.get()
    if input_text:
        try:
            encoded_text = base64.urlsafe_b64encode(input_text.encode(encoding)).decode('utf-8')
            output_text_area.delete("1.0", tk.END)
            output_text_area.insert(tk.END, encoded_text)
            update_output_counter()
        except Exception as e:
            messagebox.showerror(current_translations['error'], current_translations['encoding_error'].format(error=str(e)))
    else:
        messagebox.showwarning(current_translations['warning'], current_translations['enter_text'])

def decode_base64url():
    input_text = input_text_area.get("1.0", tk.END).strip()
    encoding = encoding_var.get()
    if input_text:
        normalized_input = input_text.rstrip('=')
        padding_needed = len(normalized_input) % 4
        if padding_needed:
            normalized_input += '=' * (4 - padding_needed)

        try:
            decoded_text = base64.urlsafe_b64decode(normalized_input).decode(encoding)
            output_text_area.delete("1.0", tk.END)
            output_text_area.insert(tk.END, decoded_text)
            update_output_counter()
        except Exception as e:
            messagebox.showerror(current_translations['error'], current_translations['decoding_error'].format(error=str(e)))
    else:
        messagebox.showwarning(current_translations['warning'], current_translations['enter_text'])

def update_input_counter(event=None):
    # Используем len() напрямую на содержимом текстового поля
    input_content = input_text_area.get("1.0", tk.END)
    input_count = len(input_content) - 1  # Вычитаем 1, чтобы исключить символ новой строки в конце
    input_counter_label.config(text=f"{current_translations['characters']} {input_count}")

def update_output_counter(event=None):
    output_content = output_text_area.get("1.0", tk.END)
    output_count = len(output_content) - 1  # Вычитаем 1, чтобы исключить символ новой строки в конце
    output_counter_label.config(text=f"{current_translations['characters']} {output_count}")

def update_cursor_position(event=None):
    cursor_index = input_text_area.index(tk.INSERT)
    cursor_position_label.config(text=f"{current_translations['cursor_at']} {cursor_index}")

def update_output_cursor_position(event=None):
    cursor_index = output_text_area.index(tk.INSERT)
    output_cursor_position_label.config(text=f"{current_translations['cursor_at']} {cursor_index}")

def change_language(language):
    global current_language, current_translations
    current_language = language
    current_translations = translations[language]
    save_language(language)
    
    # Обновляем тексты на интерфейсе
    root.title(f"{current_translations['title']} {current_translations['version']}")
    input_label.config(text=current_translations['input_label'])
    output_label.config(text=current_translations['output_label'])
    encode_button.config(text=current_translations['encode_base64'])
    decode_button.config(text=current_translations['decode_base64'])
    encode_url_button.config(text=current_translations['encode_base64url'])
    decode_url_button.config(text=current_translations['decode_base64url'])
    
    # Обновляем счетчики
    update_input_counter()
    update_output_counter()
    cursor_position_label.config(text=f"{current_translations['cursor_at']} 1.0")
    output_cursor_position_label.config(text=f"{current_translations['cursor_at']} 1.0")
    language_label.config(text=current_translations['language'])

# Функция для изменения цвета кнопок при наведении
def on_enter(e):
    e.widget['background'] = '#5DADE2'  # Цвет при наведении

def on_leave(e):
    e.widget['background'] = '#3498DB'  # Исходный цвет

# Создаем главное окно
root = tk.Tk()
root.title(f"{current_translations['title']} {current_translations['version']}")
root.geometry("700x630")
root.configure(background='#EAEDED')  # Цвет фона приложения

# Устанавливаем логотип
# Получаем путь к текущему исполнимому файлу EXE
exe_path = os.path.dirname(os.path.abspath(__file__))
# Путь к иконке, встроенной в EXE
icon_path = os.path.join(exe_path, 'f1-ks.ico')
# Устанавливаем логотип
root.wm_iconbitmap(icon_path)

# Создаем панель для кнопок и выбора кодировки
button_frame = tk.Frame(root)
button_frame.pack(pady=(10, 0), fill=tk.X)

# Выбор кодировки
encoding_var = StringVar(root)
encoding_var.set("UTF-8")  # Установить значение по умолчанию
encodings = ["UTF-8", "ASCII", "ISO-8859-1", "UTF-16"]
encoding_menu = OptionMenu(button_frame, encoding_var, *encodings)
encoding_menu.config(font=('Arial', 12))
encoding_menu.grid(row=0, column=0, padx=5)

# Кнопки для Base64
button_color = '#3498DB'
button_font = ('Arial', 12)

encode_button = tk.Button(button_frame, text=current_translations['encode_base64'], command=encode_base64, bg=button_color, fg='white', font=button_font, width=20)
encode_button.grid(row=0, column=1, padx=5)

decode_button = tk.Button(button_frame, text=current_translations['decode_base64'], command=decode_base64, bg=button_color, fg='white', font=button_font, width=20)
decode_button.grid(row=0, column=2, padx=5)

encode_url_button = tk.Button(button_frame, text=current_translations['encode_base64url'], command=encode_base64url, bg=button_color, fg='white', font=button_font, width=20)
encode_url_button.grid(row=1, column=1, padx=5, pady=(5,0))

decode_url_button = tk.Button(button_frame, text=current_translations['decode_base64url'], command=decode_base64url, bg=button_color, fg='white', font=button_font, width=20)
decode_url_button.grid(row=1, column=2, padx=5, pady=(5,0))

# Привязываем события для кнопок
for button in button_frame.winfo_children():
    if isinstance(button, tk.Button):
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

# Метка для поля ввода
input_label = tk.Label(root, text=current_translations['input_label'], bg='#EAEDED', font=('Arial', 12))
input_label.pack(pady=(10, 0))

# Создаем фрейм для поля ввода и полосы прокрутки
input_frame = tk.Frame(root)
input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

# Полоса прокрутки для поля ввода
input_scroll = Scrollbar(input_frame)
input_scroll.pack(side=tk.RIGHT, fill=tk.Y)

# Текстовое поле для ввода
input_text_area = tk.Text(input_frame, height=10, bg='#FFFFFF', fg='#000000', font=('Arial', 12), yscrollcommand=input_scroll.set, wrap=tk.WORD)
input_text_area.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)

# Привязываем полосу прокрутки к текстовому полю
input_scroll.config(command=input_text_area.yview)

# Обработчики событий для поля ввода
# Для обновления счетчика символов
input_text_area.bind("<KeyRelease>", update_input_counter)
# Для обновления позиции курсора
input_text_area.bind("<ButtonRelease-1>", update_cursor_position)
input_text_area.bind("<Button-1>", update_cursor_position)
# Добавлено для отслеживания нажатий клавиш (включая Enter)
input_text_area.bind("<Key>", update_cursor_position)

# Добавляем счетчик символов и позиции курсора для ввода
input_counter_frame = tk.Frame(root, bg='#EAEDED')
input_counter_frame.pack(fill=tk.X, padx=10, pady=(0, 5))

input_counter_label = tk.Label(input_counter_frame, text=f"{current_translations['characters']} 0", bg='#EAEDED', font=('Arial', 10))
input_counter_label.pack(side=tk.LEFT, padx=(10, 0))

cursor_position_label = tk.Label(input_counter_frame, text=f"{current_translations['cursor_at']} 1.0", bg='#EAEDED', font=('Arial', 10))
cursor_position_label.pack(side=tk.RIGHT, padx=(0, 10))

output_label = tk.Label(root, text=current_translations['output_label'], bg='#EAEDED', font=('Arial', 12))
output_label.pack(pady=(10, 0))

# Создаем фрейм для поля вывода и полосы прокрутки
output_frame = tk.Frame(root)
output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

# Полоса прокрутки для поля вывода
output_scroll = Scrollbar(output_frame)
output_scroll.pack(side=tk.RIGHT, fill=tk.Y)

# Текстовое поле для вывода
output_text_area = tk.Text(output_frame, height=10, bg='#FFFFFF', fg='#000000', font=('Arial', 12), yscrollcommand=output_scroll.set, wrap=tk.WORD)
output_text_area.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)

# Привязываем полосу прокрутки к текстовому полю
output_scroll.config(command=output_text_area.yview)

# Обработчики событий для поля вывода
output_text_area.bind("<KeyRelease>", update_output_counter)
output_text_area.bind("<ButtonRelease-1>", update_output_cursor_position)
output_text_area.bind("<Button-1>", update_output_cursor_position)

# Добавляем счетчики для вывода
output_counter_frame = tk.Frame(root, bg='#EAEDED')
output_counter_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

output_counter_label = tk.Label(output_counter_frame, text=f"{current_translations['characters']} 0", bg='#EAEDED', font=('Arial', 10))
output_counter_label.pack(side=tk.LEFT, padx=(10, 0))

output_cursor_position_label = tk.Label(output_counter_frame, text=f"{current_translations['cursor_at']} 1.0", bg='#EAEDED', font=('Arial', 10))
output_cursor_position_label.pack(side=tk.RIGHT, padx=(0, 10))

# Поле для выбора языка
language_frame = tk.Frame(root, bg='#EAEDED')
language_frame.pack(fill=tk.X, padx=10, pady=(0, 5))

# Выбор языка
language_var = StringVar(root)
language_var.set(current_language)

def language_changed(event):
    selected_lang = language_var.get()
    if selected_lang == 'ru':
        change_language('ru')
    elif selected_lang == 'en':
        change_language('en')
    elif selected_lang == 'zh':
        change_language('zh')

language_menu = OptionMenu(language_frame, language_var, 'ru', 'en', 'zh', command=language_changed)
language_menu.config(font=('Arial', 10))
language_menu.pack(side=tk.RIGHT, padx=(10, 0))

language_label = tk.Label(language_frame, text=current_translations['language'], bg='#EAEDED', font=('Arial', 10))
language_label.pack(side=tk.RIGHT, padx=(10, 0))

# Инициализируем счетчики при запуске
update_input_counter()
update_output_counter()

# Запускаем главный цикл
root.mainloop()
