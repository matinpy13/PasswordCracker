import sys
import os
import rarfile
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import time
import itertools
import string
import json
import pyzipper
import pikepdf

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

CONFIG_FILE = resource_path("config.json")

if hasattr(sys, '_MEIPASS'):
    unrar_exe_path_in_bundle = resource_path("UnRAR.exe")
    if os.path.exists(unrar_exe_path_in_bundle):
        rarfile.UNRAR_TOOL = unrar_exe_path_in_bundle
    else:
        print("FATAL: UnRAR.exe not found in bundle!")


LANGUAGES = {
    "en": {
        "app_title": "ZIP, RAR, PDF Password Cracker",
        "about_button_text": "About",
        "language_label_text": "Language:",
        "target_file_label": "Target File:",
        "browse_button_text": "Browse",
        "charset_label": "Character Set:",
        "charset_numbers": "Numbers (0-9)",
        "charset_lowercase": "Lowercase (a-z)",
        "charset_uppercase": "Uppercase (A-Z)",
        "charset_lower_numbers": "Lowercase + Numbers",
        "charset_all_letters": "All Letters (a-z, A-Z)",
        "charset_all_letters_numbers": "All Letters + Numbers",
        "charset_all_letters_numbers_symbols": "All Letters + Numbers + Symbols",
        "min_length_label": "Min Length:",
        "max_length_label": "Max Length:",
        "start_button_text": "Start Cracking",
        "stop_button_text": "Stop Cracking",
        "status_idle": "Status: Idle",
        "status_cracking_zip": "Status: Cracking ZIP...",
        "status_cracking_rar": "Status: Cracking RAR...",
        "status_cracking_pdf": "Status: Cracking PDF...",
        "status_stopping": "Status: Stopping...",
        "status_stopped_user": "Status ({file_type}): Stopped by user.",
        "status_password_found": "Status ({file_type}): Password Found!",
        "status_password_not_found": "Status ({file_type}): Password not found.",
        "attempts_time_format": "Attempts: {attempts:,} | Time: {elapsed_time:.2f}s",
        "log_selected_file": "Selected file: {filepath}",
        "log_starting_crack": "Starting crack for: {filepath} (Type: {file_type})",
        "log_charset_length": "Charset: '{charset_key}' (Size: {charset_size}), Length: {min_len}-{max_len}",
        "log_stop_signal_sent": "Stop signal sent. Waiting for thread to finish...",
        "log_stopping_at_length": "Stopping at length {length} due to user request.",
        "log_trying_length": "[*] Trying passwords of length {length} for {file_type}...",
        "log_file_error_halting": "File error with {filepath}. Halting for this file.",
        "log_success_password_is": "\nSUCCESS! Password is: {password}",
        "log_password_not_found_constraints": "\nPassword not found within the given constraints.",
        "log_unrar_not_found": "Error: 'unrar' tool not found. Please install it and ensure it's in your PATH, or set rarfile.UNRAR_TOOL.",
        "log_rar_cracking_disabled": "RAR cracking disabled for this session.",
        "log_rar_no_password_needed": "Info: '{filename}' does not seem to be password protected by RAR.",
        "log_multivolume_rar_unsupported": "Error: Multi-volume RAR archives are not supported for cracking.",
        "log_pdf_not_encrypted": "Info: '{filename}' is not encrypted.",
        "error_title": "Error",
        "error_select_file_msg": "Please select a valid target file.",
        "error_invalid_length_msg": "Invalid min/max length values.",
        "error_length_must_be_int_msg": "Min/max length must be integers.",
        "error_unsupported_file_type_msg": "Unsupported file type: {file_extension}. Only ZIP, RAR, PDF are supported.",
        "error_no_cracker_for_file": "Error: No cracker available for {file_extension}",
        "error_cracking_loop_title": "Cracking Loop Error",
        "error_unexpected_dispatcher": "An unexpected error occurred in dispatcher: {error}",
        "error_critical_dispatcher": "Critical Error during cracking dispatcher: {error}",
        "warning_title": "Warning",
        "warning_long_op_title": "Potentially Long Operation",
        "warning_long_op_msg": "Warning: Large character set ('{charset_key}') and/or max length ({max_len}). This could take an extremely long time. Continue?",
        "success_title": "Success!",
        "success_password_found_msg": "Password found: {password}",
        "result_title": "Result",
        "result_password_not_found_msg": "Password not found with the current settings.",
        "restart_required_title": "Restart Required",
        "restart_required_message": "The language has been changed. Please restart the application for the changes to take full effect.",
        "ok_button": "OK",
        "about_window_title": "About Program",
        "about_app_name_label": "Password Cracker",
        "about_info_text": "Developed by: MatinPy13\n\nTelegram: @MatinPy13\n\nVersion: 1.0.0\n© 2025",
        "back_button_text": "Back",
        "loading_info_text": "This program was developed by MatinPy13.",
        "loading_warning_text": "The user is responsible for any misuse of this tool.\nPlease use this program in compliance with laws and ethics.",
        "error_generic_title": "An Error Occurred",
        "error_generic_message": "Something went wrong. Please try again or contact the developer.",
        "supported_archives_filter": "Supported Archives",
        "select_target_file_title": "Select Target File",
    },
    "fa": {
        "app_title": "رمزگشای فایل‌های ZIP, RAR, PDF",
        "about_button_text": "درباره ؟",
        "language_label_text": "زبان:",
        "target_file_label": "فایل هدف:",
        "browse_button_text": "انتخاب",
        "charset_label": "مجموعه کاراکتر:",
        "charset_numbers": "اعداد (0-9)",
        "charset_lowercase": "حروف کوچک (a-z)",
        "charset_uppercase": "حروف بزرگ (A-Z)",
        "charset_lower_numbers": "حروف کوچک + اعداد",
        "charset_all_letters": "تمام حروف (a-z, A-Z)",
        "charset_all_letters_numbers": "تمام حروف + اعداد",
        "charset_all_letters_numbers_symbols": "تمام حروف + اعداد + نمادها",
        "min_length_label": "حداقل طول:",
        "max_length_label": "حداکثر طول:",
        "start_button_text": "شروع شکستن رمز",
        "stop_button_text": "توقف شکستن رمز",
        "status_idle": "وضعیت: آماده",
        "status_cracking_zip": "وضعیت: در حال شکستن رمز ZIP...",
        "status_cracking_rar": "وضعیت: در حال شکستن رمز RAR...",
        "status_cracking_pdf": "وضعیت: در حال شکستن رمز PDF...",
        "status_stopping": "وضعیت: در حال توقف...",
        "status_stopped_user": "وضعیت ({file_type}): توسط کاربر متوقف شد.",
        "status_password_found": "وضعیت ({file_type}): رمز عبور پیدا شد!",
        "status_password_not_found": "وضعیت ({file_type}): رمز عبور پیدا نشد.",
        "attempts_time_format": "تلاش‌ها: {attempts:,} | زمان: {elapsed_time:.2f} ثانیه",
        "log_selected_file": "فایل انتخاب شده: {filepath}",
        "log_starting_crack": "شروع شکستن رمز برای: {filepath} (نوع: {file_type})",
        "log_charset_length": "مجموعه کاراکتر: '{charset_key}' (اندازه: {charset_size})، طول: {min_len}-{max_len}",
        "log_stop_signal_sent": "سیگنال توقف ارسال شد. در انتظار پایان ریسه...",
        "log_stopping_at_length": "توقف در طول {length} به درخواست کاربر.",
        "log_trying_length": "[*] تلاش برای رمزهای با طول {length} برای {file_type}...",
        "log_file_error_halting": "خطا در فایل {filepath}. عملیات برای این فایل متوقف می‌شود.",
        "log_success_password_is": "\nموفقیت! رمز عبور: {password}",
        "log_password_not_found_constraints": "\nرمز عبور با محدودیت‌های داده شده پیدا نشد.",
        "log_unrar_not_found": "خطا: ابزار 'unrar' یافت نشد. لطفاً آن را نصب کرده و از وجود آن در PATH سیستم اطمینان حاصل کنید، یا rarfile.UNRAR_TOOL را تنظیم کنید.",
        "log_rar_cracking_disabled": "شکستن رمز RAR برای این جلسه غیرفعال شد.",
        "log_rar_no_password_needed": "اطلاعات: به نظر می‌رسد فایل '{filename}' با RAR رمزگذاری نشده است.",
        "log_multivolume_rar_unsupported": "خطا: آرشیوهای RAR چند قسمتی برای شکستن رمز پشتیبانی نمی‌شوند.",
        "log_pdf_not_encrypted": "اطلاعات: فایل '{filename}' رمزگذاری نشده است.",
        "error_title": "خطا",
        "error_select_file_msg": "لطفاً یک فایل هدف معتبر انتخاب کنید.",
        "error_invalid_length_msg": "مقادیر حداقل/حداکثر طول نامعتبر است.",
        "error_length_must_be_int_msg": "حداقل/حداکثر طول باید عدد صحیح باشد.",
        "error_unsupported_file_type_msg": "نوع فایل پشتیبانی نمی‌شود: {file_extension}. فقط ZIP، RAR، PDF پشتیبانی می‌شوند.",
        "error_no_cracker_for_file": "خطا: رمزگشایی برای {file_extension} موجود نیست",
        "error_cracking_loop_title": "خطا در حلقه شکستن رمز",
        "error_unexpected_dispatcher": "یک خطای غیرمنتظره در دیسپچر رخ داد: {error}",
        "error_critical_dispatcher": "خطای بحرانی هنگام اجرای دیسپچر: {error}",
        "warning_title": "هشدار",
        "warning_long_op_title": "عملیات بالقوه طولانی",
        "warning_long_op_msg": "هشدار: مجموعه کاراکتر بزرگ ('{charset_key}') و/یا حداکثر طول ({max_len}). این عملیات ممکن است زمان بسیار زیادی طول بکشد. ادامه می‌دهید؟",
        "success_title": "موفقیت!",
        "success_password_found_msg": "رمز عبور پیدا شد: {password}",
        "result_title": "نتیجه",
        "result_password_not_found_msg": "رمز عبور با تنظیمات فعلی پیدا نشد.",
        "restart_required_title": "نیاز به راه‌اندازی مجدد",
        "restart_required_message": "زبان تغییر کرده است. لطفاً برای اعمال کامل تغییرات، برنامه را مجدداً راه‌اندازی کنید.",
        "ok_button": "باشه",
        "about_window_title": "درباره برنامه",
        "about_app_name_label": "Password Cracker",
        "about_info_text": "توسعه یافته توسط: MatinPy13\n\nتلگرام: @MatinPy13\n\nنسخه: 1.0.0\n© 2025",
        "back_button_text": "بازگشت",
        "loading_info_text": "این برنامه توسط MatinPy13 توسعه یافته است.",
        "loading_warning_text": "مسئولیت هرگونه استفاده نادرست از این ابزار بر عهده کاربر می‌باشد.\nلطفاً با رعایت قوانین و اخلاق از این برنامه استفاده کنید.",
        "error_generic_title": "خطایی رخ داد",
        "error_generic_message": "مشکلی پیش آمد. لطفاً مجدداً تلاش کنید و یا به توسعه دهنده اطلاع دهید.",
        "supported_archives_filter": "آرشیوهای پشتیبانی شده",
        "select_target_file_title": "انتخاب فایل هدف",
    }
}

def load_language_setting():
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config.get("language", "en")
    except (FileNotFoundError, json.JSONDecodeError):
        return "en"

def save_language_setting(lang_code):
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump({"language": lang_code}, f, ensure_ascii=False, indent=4)
    except IOError:
        print(f"Warning: Could not save language setting to {CONFIG_FILE}")


class AboutWindow(ctk.CTkToplevel):
    def __init__(self, master, strings):
        super().__init__(master)
        self.strings = strings
        self.title(self.strings["about_window_title"])
        self.geometry("400x270")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        master_x = master.winfo_x()
        master_y = master.winfo_y()
        master_width = master.winfo_width()
        master_height = master.winfo_height()
        x_pos = master_x + (master_width // 2) - (400 // 2)
        y_pos = master_y + (master_height // 2) - (270 // 2)
        self.geometry(f"+{x_pos}+{y_pos}")
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        about_font_title = ("Tahoma", 16, "bold")
        about_font_text = ("Tahoma", 13)
        ctk.CTkLabel(main_frame, text=self.strings["about_app_name_label"], font=about_font_title).pack(pady=(0,10))
        ctk.CTkLabel(main_frame, text=self.strings["about_info_text"], font=about_font_text, justify="center", wraplength=350).pack(pady=10)
        back_button = ctk.CTkButton(main_frame, text=self.strings["back_button_text"], command=self.destroy, width=100)
        back_button.pack(pady=(15,0))
        self.protocol("WM_DELETE_WINDOW", self.destroy)

class LoadingScreen(ctk.CTkToplevel):
    def __init__(self, master, strings):
        super().__init__(master)
        self.strings = strings
        self.overrideredirect(True)
        self.geometry("600x300")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_pos = (screen_width // 2) - (600 // 2)
        y_pos = (screen_height // 2) - (300 // 2)
        self.geometry(f"+{x_pos}+{y_pos}")
        try:
            bg_color_from_theme = ctk.ThemeManager.theme["CTkFrame"]["fg_color"]
            applied_bg_color = self._apply_appearance_mode(bg_color_from_theme)
            self.configure(fg_color=applied_bg_color)
        except (KeyError, AttributeError, TypeError):
            fallback_bg = ("#ECECEC", "#2B2B2B")
            self.configure(fg_color=self._apply_appearance_mode(fallback_bg))
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(expand=True, fill="both", padx=25, pady=25)
        info_font = ("Tahoma", 16)
        warning_font = ("Tahoma", 13, "italic")
        self.info_label = ctk.CTkLabel(content_frame, text="", font=info_font, wraplength=550, justify="center")
        self.info_label.pack(pady=(15, 10))
        self.warning_label = ctk.CTkLabel(content_frame, text="", font=warning_font, wraplength=550, justify="center")
        self.warning_label.pack(pady=10)
        self.canvas_size = 60
        try:
            canvas_bg_color_tuple_or_str = ctk.ThemeManager.theme["CTkFrame"]["fg_color"]
            canvas_bg = self._apply_appearance_mode(canvas_bg_color_tuple_or_str)
            if canvas_bg is None:
                 canvas_bg = "#2B2B2B" if ctk.get_appearance_mode() == "Dark" else "#ECECEC"
        except (KeyError, AttributeError, TypeError):
            canvas_bg = "#2B2B2B" if ctk.get_appearance_mode() == "Dark" else "#ECECEC"
        self.canvas = ctk.CTkCanvas(content_frame, width=self.canvas_size, height=self.canvas_size,
                                    bg=canvas_bg,
                                    highlightthickness=0)
        self.canvas.pack(pady=(15,0))
        self.angle = 0
        self.animate_loading_id = None
        self.text_to_type_info = self.strings["loading_info_text"]
        self.text_to_type_warning = self.strings["loading_warning_text"]
        self.current_char_info_index = 0
        self.current_char_warning_index = 0
        self.typing_phase = "info"
        self.after_id_typing = None
        self.type_next_char()

    def type_next_char(self):
        if self.typing_phase == "info":
            if self.current_char_info_index < len(self.text_to_type_info):
                self.info_label.configure(text=self.text_to_type_info[:self.current_char_info_index + 1])
                self.current_char_info_index += 1
                self.after_id_typing = self.after(70, self.type_next_char)
            else:
                self.typing_phase = "warning"
                self.after_id_typing = self.after(300, self.type_next_char)
        elif self.typing_phase == "warning":
            if self.current_char_warning_index < len(self.text_to_type_warning):
                self.warning_label.configure(text=self.text_to_type_warning[:self.current_char_warning_index + 1])
                self.current_char_warning_index += 1
                self.after_id_typing = self.after(50, self.type_next_char)
            else:
                self.start_loading_animation()
                self.after_id_typing = self.after(2500, self.close_splash)

    def start_loading_animation(self):
        self.canvas.delete("all")
        self.angle = (self.angle + 15) % 360
        try:
            theme_color_tuple_or_str = ctk.ThemeManager.theme["CTkButton"]["hover_color"]
            arc_color = self._apply_appearance_mode(theme_color_tuple_or_str)
            if arc_color is None:
                arc_color = "#569DE5"
        except (KeyError, AttributeError, TypeError):
            arc_color = self._apply_appearance_mode(("#569DE5", "#569DE5"))
        self.canvas.create_arc(
            5, 5, self.canvas_size - 5, self.canvas_size - 5,
            start=self.angle, extent=150, style=ctk.ARC,
            outline=arc_color, width=5
        )
        self.animate_loading_id = self.after(40, self.start_loading_animation)

    def close_splash(self):
        if self.after_id_typing: self.after_cancel(self.after_id_typing)
        if self.animate_loading_id: self.after_cancel(self.animate_loading_id)
        self.destroy()
        if self.master and hasattr(self.master, 'deiconify'): self.master.deiconify()


class SimpleCrackerApp(ctk.CTk):
    def __init__(self, fg_color=None, **kwargs):
        super().__init__(fg_color=fg_color, **kwargs)
        self.current_lang_code = load_language_setting()
        self.strings = LANGUAGES[self.current_lang_code]
        self.title(self.strings["app_title"])
        self.geometry("700x600")
        self.minsize(650, 550)
        self.target_filepath_var = ctk.StringVar()
        self.stop_event = threading.Event()
        self.crack_thread = None
        self.attempt_count = 0
        self.start_time_crack = None
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(pady=10, padx=20, fill="both", expand=True)
        title_bar_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        title_bar_frame.pack(fill="x", pady=(0, 10))
        app_title_font = ("Tahoma", 18, "bold")
        self.app_title_label = ctk.CTkLabel(title_bar_frame, text=self.strings["app_title"], font=app_title_font)
        self.app_title_label.pack(side="left", padx=(0,10))
        control_buttons_frame = ctk.CTkFrame(title_bar_frame, fg_color="transparent")
        control_buttons_frame.pack(side="right")
        self.lang_option_var = ctk.StringVar(value="English" if self.current_lang_code == "en" else "فارسی")
        language_options = ["English", "فارسی"]
        self.language_menu = ctk.CTkOptionMenu(control_buttons_frame, variable=self.lang_option_var,
                                               values=language_options, command=self.change_language_ui, width=100)
        self.language_menu.pack(side="right", padx=(5,0))
        self.language_label = ctk.CTkLabel(control_buttons_frame, text=self.strings["language_label_text"])
        self.language_label.pack(side="right")
        self.about_button = ctk.CTkButton(control_buttons_frame, text=self.strings["about_button_text"],
                                          command=self.show_about_window, width=80)
        self.about_button.pack(side="right", padx=(10,5))
        file_frame = ctk.CTkFrame(main_frame)
        file_frame.pack(pady=5, padx=10, fill="x")
        label_font = ("Arial", 13)
        self.target_file_text_label = ctk.CTkLabel(file_frame, text=self.strings["target_file_label"], font=label_font)
        self.target_file_text_label.pack(side="left", padx=5)
        self.file_entry = ctk.CTkEntry(file_frame, textvariable=self.target_filepath_var, width=350)
        self.file_entry.pack(side="left", padx=5, expand=True, fill="x")
        self.browse_button = ctk.CTkButton(file_frame, text=self.strings["browse_button_text"], command=self.browse_file)
        self.browse_button.pack(side="left", padx=5)
        config_frame = ctk.CTkFrame(main_frame)
        config_frame.pack(pady=5, padx=10, fill="x")
        self.charset_text_label = ctk.CTkLabel(config_frame, text=self.strings["charset_label"], font=label_font)
        self.charset_text_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        all_symbols = string.punctuation
        self.charset_option_keys_map = {
            "charset_numbers": string.digits,
            "charset_lowercase": string.ascii_lowercase,
            "charset_uppercase": string.ascii_uppercase,
            "charset_lower_numbers": string.ascii_lowercase + string.digits,
            "charset_all_letters": string.ascii_letters,
            "charset_all_letters_numbers": string.ascii_letters + string.digits,
            "charset_all_letters_numbers_symbols": string.ascii_letters + string.digits + all_symbols,
        }
        self.translated_charset_options = [self.strings[key] for key in self.charset_option_keys_map.keys()]
        self.charset_var = ctk.StringVar(value=self.strings["charset_numbers"])
        self.charset_menu = ctk.CTkOptionMenu(config_frame, variable=self.charset_var, values=self.translated_charset_options)
        self.charset_menu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.min_len_text_label = ctk.CTkLabel(config_frame, text=self.strings["min_length_label"], font=label_font)
        self.min_len_text_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.min_len_var = ctk.StringVar(value="1")
        self.min_len_entry = ctk.CTkEntry(config_frame, textvariable=self.min_len_var, width=50)
        self.min_len_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.max_len_text_label = ctk.CTkLabel(config_frame, text=self.strings["max_length_label"], font=label_font)
        self.max_len_text_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.max_len_var = ctk.StringVar(value="4")
        self.max_len_entry = ctk.CTkEntry(config_frame, textvariable=self.max_len_var, width=50)
        self.max_len_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        config_frame.columnconfigure(1, weight=1)
        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(pady=5, padx=10, fill="x")
        self.start_button = ctk.CTkButton(controls_frame, text=self.strings["start_button_text"], command=self.start_cracking_ui)
        self.start_button.pack(side="left", padx=10, pady=10)
        self.stop_button = ctk.CTkButton(controls_frame, text=self.strings["stop_button_text"], command=self.stop_cracking_ui, state="disabled")
        self.stop_button.pack(side="left", padx=10, pady=10)
        status_frame = ctk.CTkFrame(main_frame)
        status_frame.pack(pady=5, padx=10, fill="both", expand=True)
        self.status_label_var = ctk.StringVar(value=self.strings["status_idle"])
        self.status_label_widget = ctk.CTkLabel(status_frame, textvariable=self.status_label_var, font=label_font)
        self.status_label_widget.pack(pady=5, anchor="w")
        self.attempts_label_var = ctk.StringVar(value=self.strings["attempts_time_format"].format(attempts=0, elapsed_time=0.00))
        self.attempts_label_widget = ctk.CTkLabel(status_frame, textvariable=self.attempts_label_var, font=label_font)
        self.attempts_label_widget.pack(pady=5, anchor="w")
        self.log_textbox = ctk.CTkTextbox(status_frame, height=180, state="disabled", font=("Consolas", 11))
        self.log_textbox.pack(pady=5, fill="both", expand=True)

    def show_generic_error_message(self, specific_error_details=None):
        if specific_error_details:
            self.after(0, self.log_message, f"Internal Error Detail: {specific_error_details}")
        def _show_msgbox():
            messagebox.showerror(
                self.strings["error_generic_title"],
                self.strings["error_generic_message"]
            )
        if threading.current_thread() is threading.main_thread():
            _show_msgbox()
        else:
            self.after(0, _show_msgbox)

    def change_language_ui(self, selected_language_display_name):
        new_lang_code = "fa" if selected_language_display_name == "فارسی" else "en"
        if new_lang_code != self.current_lang_code:
            save_language_setting(new_lang_code)
            temp_strings = LANGUAGES[new_lang_code]
            title = temp_strings.get("restart_required_title", LANGUAGES["en"]["restart_required_title"])
            message = temp_strings.get("restart_required_message", LANGUAGES["en"]["restart_required_message"])
            if messagebox.showinfo(title, message):
                 self.destroy()

    def show_about_window(self):
        if hasattr(self, "_about_window") and self._about_window.winfo_exists():
            self._about_window.focus()
        else:
            self._about_window = AboutWindow(master=self, strings=self.strings)

    def browse_file(self):
        filetypes = (
            (self.strings["supported_archives_filter"], "*.zip *.rar *.pdf"),
            ("ZIP files", "*.zip"),
            ("RAR files", "*.rar"),
            ("PDF files", "*.pdf"),
            ("All files", "*.*")
        )
        filepath = filedialog.askopenfilename(title=self.strings["select_target_file_title"], filetypes=filetypes)
        if filepath:
            self.target_filepath_var.set(filepath)
            self.log_message(self.strings["log_selected_file"].format(filepath=filepath))

    def log_message(self, message, clear_first=False):
        self.log_textbox.configure(state="normal")
        if clear_first:
            self.log_textbox.delete("1.0", "end")
        self.log_textbox.insert("end", message + "\n")
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")

    def update_status_bar(self, attempts, elapsed_time):
        self.attempts_label_var.set(self.strings["attempts_time_format"].format(attempts=attempts, elapsed_time=elapsed_time))

    def start_cracking_ui(self):
        target_filepath = self.target_filepath_var.get()
        if not target_filepath or not os.path.exists(target_filepath):
            messagebox.showerror(self.strings["error_title"], self.strings["error_select_file_msg"])
            return
        try:
            min_len = int(self.min_len_var.get())
            max_len = int(self.max_len_var.get())
            if min_len <= 0 or max_len < min_len:
                messagebox.showerror(self.strings["error_title"], self.strings["error_invalid_length_msg"])
                return
        except ValueError:
            messagebox.showerror(self.strings["error_title"], self.strings["error_length_must_be_int_msg"])
            return
        selected_charset_display_name = self.charset_var.get()
        charset_key_selected = ""
        for key, val_str_map in self.charset_option_keys_map.items():
            if self.strings[key] == selected_charset_display_name:
                charset_key_selected = key
                break
        if not charset_key_selected:
            messagebox.showerror(self.strings["error_title"], "Internal charset selection error.")
            return
        charset = self.charset_option_keys_map[charset_key_selected]
        file_extension = os.path.splitext(target_filepath)[1].lower()
        if file_extension not in [".zip", ".rar", ".pdf"]:
            messagebox.showerror(self.strings["error_title"], self.strings["error_unsupported_file_type_msg"].format(file_extension=file_extension))
            return
        if len(charset) > 70 and max_len > 4 or len(charset) > 50 and max_len > 5 :
            warn_msg = self.strings["warning_long_op_msg"].format(charset_key=selected_charset_display_name, max_len=max_len)
            if not messagebox.askyesno(self.strings["warning_long_op_title"], warn_msg):
                return
        self.log_message(self.strings["log_starting_crack"].format(filepath=target_filepath, file_type=file_extension.upper()), clear_first=True)
        self.log_message(self.strings["log_charset_length"].format(charset_key=selected_charset_display_name, charset_size=len(charset), min_len=min_len, max_len=max_len))
        self.start_button.configure(state="disabled")
        self.browse_button.configure(state="disabled")
        self.charset_menu.configure(state="disabled")
        self.min_len_entry.configure(state="disabled")
        self.max_len_entry.configure(state="disabled")
        self.stop_button.configure(state="normal")
        status_key = f"status_cracking_{file_extension[1:]}"
        self.status_label_var.set(self.strings.get(status_key, "Status: Cracking..."))
        self.attempt_count = 0
        self.start_time_crack = time.time()
        self.update_status_bar(0, 0)
        self.stop_event.clear()
        self.crack_thread = threading.Thread(
            target=self.run_crack_logic_dispatcher,
            args=(target_filepath, file_extension, charset, min_len, max_len),
            daemon=True
        )
        self.crack_thread.start()

    def stop_cracking_ui(self):
        if self.crack_thread and self.crack_thread.is_alive():
            self.stop_event.set()
            self.log_message(self.strings["log_stop_signal_sent"])
            self.status_label_var.set(self.strings["status_stopping"])

    def _on_crack_complete(self, password_found, found_password_value=None, file_type_ext="File"):
        self.start_button.configure(state="normal")
        self.browse_button.configure(state="normal")
        self.charset_menu.configure(state="normal")
        self.min_len_entry.configure(state="normal")
        self.max_len_entry.configure(state="normal")
        self.stop_button.configure(state="disabled")
        file_type_display = file_type_ext.replace(".","").upper() if file_type_ext else "File"
        if self.stop_event.is_set() and not password_found:
             self.status_label_var.set(self.strings["status_stopped_user"].format(file_type=file_type_display))
             if not hasattr(self, 'critical_error_flag_for_session') or not self.critical_error_flag_for_session:
                self.log_message(self.strings["status_stopped_user"].format(file_type=file_type_display).replace(f"Status ({file_type_display}): ", ""))
        elif password_found:
            self.status_label_var.set(self.strings["status_password_found"].format(file_type=file_type_display))
            self.log_message(self.strings["log_success_password_is"].format(password=found_password_value))
            messagebox.showinfo(self.strings["success_title"], self.strings["success_password_found_msg"].format(password=found_password_value))
        else:
            if not (hasattr(self, 'critical_error_flag_for_session') and self.critical_error_flag_for_session):
                self.status_label_var.set(self.strings["status_password_not_found"].format(file_type=file_type_display))
                self.log_message(self.strings["log_password_not_found_constraints"])
                messagebox.showinfo(self.strings["result_title"], self.strings["result_password_not_found_msg"])
        elapsed_time = time.time() - self.start_time_crack if self.start_time_crack else 0
        self.update_status_bar(self.attempt_count, elapsed_time)
        self.crack_thread = None
        if hasattr(self, 'critical_error_flag_for_session'):
            del self.critical_error_flag_for_session

    def run_crack_logic_dispatcher(self, filepath, file_extension, charset, min_length, max_length):
        password_found_flag = False
        identified_password = None
        self.critical_error_flag_for_session = False
        cracker_function = None
        if file_extension == ".zip": cracker_function = self._crack_zip
        elif file_extension == ".rar": cracker_function = self._crack_rar
        elif file_extension == ".pdf": cracker_function = self._crack_pdf
        if not cracker_function:
            self.after(0, self.log_message, self.strings["error_no_cracker_for_file"].format(file_extension=file_extension))
            self.critical_error_flag_for_session = True
            self.after(0, self._on_crack_complete, False, None, file_extension)
            return
        try:
            file_type_display = file_extension.replace(".","").upper()
            for length in range(min_length, max_length + 1):
                if self.stop_event.is_set(): break
                self.after(0, self.log_message, self.strings["log_trying_length"].format(length=length, file_type=file_type_display))
                for password_tuple in itertools.product(charset, repeat=length):
                    if self.stop_event.is_set(): break
                    password_str = "".join(password_tuple)
                    self.attempt_count += 1
                    if self.attempt_count % 2000 == 0:
                        elapsed = time.time() - self.start_time_crack
                        self.after(0, self.update_status_bar, self.attempt_count, elapsed)
                    result = cracker_function(filepath, password_str)
                    if result == "found":
                        identified_password = password_str
                        password_found_flag = True; break
                    elif result == "wrong_password": continue
                    elif result == "file_error":
                        self.after(0, self.log_message, self.strings["log_file_error_halting"].format(filepath=os.path.basename(filepath)))
                        self.stop_event.set()
                        break
                if password_found_flag or self.stop_event.is_set(): break
        except rarfile.NoCrackerToolError:
            self.after(0, self.log_message, self.strings["log_unrar_not_found"])
            self.after(0, self.log_message, self.strings["log_rar_cracking_disabled"])
            self.critical_error_flag_for_session = True
            self.stop_event.set()
        except (pyzipper.zipfile.BadZipFile, rarfile.BadRarFile, pikepdf.PdfError) as e_file_corruption:
            self.after(0, self.log_message, f"Error: File appears to be corrupted or is not a valid {file_extension.upper()} file: {os.path.basename(filepath)}. Details: {e_file_corruption}")
            self.critical_error_flag_for_session = True
            self.stop_event.set()
        except Exception as e_general_dispatcher:
            self.after(0, self.log_message, self.strings["error_critical_dispatcher"].format(error=e_general_dispatcher))
            self.show_generic_error_message(specific_error_details=f"Dispatcher: {e_general_dispatcher}")
            password_found_flag = False
            self.critical_error_flag_for_session = True
            self.stop_event.set()
        finally:
            self.after(0, self._on_crack_complete, password_found_flag, identified_password, file_extension)

    def _crack_zip(self, filepath, password_str):
        try:
            with pyzipper.AESZipFile(filepath, 'r') as zf:
                zf.setpassword(password_str.encode('utf-8'))
                if zf.testzip() is None: return "found"
                else: return "wrong_password"
        except RuntimeError as e:
            if 'Bad password' in str(e) or 'password incorrect' in str(e) or 'CRC error' in str(e):
                return "wrong_password"
            raise
        except pyzipper.zipfile.BadZipFile as e:
            raise
        except Exception: return "wrong_password"

    def _crack_rar(self, filepath, password_str):
        try:
            rf = rarfile.RarFile(filepath)
            rf.setpassword(password_str)
            if rf.needs_password():
                _ = rf.infolist()
                return "found"
            else:
                self.after(0, self.log_message, self.strings["log_rar_no_password_needed"].format(filename=os.path.basename(filepath)))
                self.stop_event.set()
                return "file_error"
        except rarfile.NoCrackerToolError:
            raise
        except (rarfile.BadRarFile, rarfile.NeedFirstVolume) as e_rar_specific :
            if isinstance(e_rar_specific, rarfile.NeedFirstVolume):
                 self.after(0, self.log_message, self.strings["log_multivolume_rar_unsupported"])
                 self.stop_event.set()
                 return "file_error"
            raise
        except (rarfile.PasswortIncorrect, rarfile.NoPassword):
            return "wrong_password"
        except RuntimeError as e:
            if "bad password" in str(e).lower() or "wrong password" in str(e).lower() or "crc check failed" in str(e).lower():
                return "wrong_password"
            raise
        except Exception: return "wrong_password"

    def _crack_pdf(self, filepath, password_str):
        try:
            pdf = pikepdf.Pdf.open(filepath, password=password_str)
            if not pdf.is_encrypted:
                self.after(0, self.log_message, self.strings["log_pdf_not_encrypted"].format(filename=os.path.basename(filepath)))
                self.stop_event.set(); pdf.close(); return "file_error"
            _ = len(pdf.pages); pdf.close(); return "found"
        except pikepdf.PasswordError: return "wrong_password"
        except (pikepdf.PdfError, IOError, ValueError, TypeError, AttributeError) as e:
            raise
        except Exception: return "wrong_password"

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    current_lang = load_language_setting()
    app_strings = LANGUAGES[current_lang]
    app = SimpleCrackerApp()
    app.withdraw()
    splash = LoadingScreen(master=app, strings=app_strings)
    app.mainloop()