# -*- coding: utf-8 -*-
"""
نافذة تسجيل الدخول
"""

import tkinter as tk
from tkinter import messagebox, ttk
from app.config import *
from app.database import Database
from app.ui.main_window import MainWindow

class LoginWindow:
    """نافذة تسجيل الدخول"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        self.db = Database()
        self.current_user = None
        
        # تمركز النافذة في منتصف الشاشة
        self.center_window()
        
        # إنشاء الواجهة
        self.create_ui()
    
    def center_window(self):
        """تمركز النافذة في منتصف الشاشة"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"+{x}+{y}")
    
    def create_ui(self):
        """إنشاء واجهة تسجيل الدخول"""
        # الإطار الرئيسي
        main_frame = tk.Frame(self.root, bg=COLOR_LIGHT)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # العنوان
        title_frame = tk.Frame(main_frame, bg=COLOR_PRIMARY)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title = tk.Label(
            title_frame,
            text="نظام صندوق رعاية المعاقين",
            font=("Arial", 16, "bold"),
            bg=COLOR_PRIMARY,
            fg=COLOR_WHITE
        )
        title.pack(pady=15)
        
        # إطار المدخلات
        input_frame = tk.Frame(main_frame, bg=COLOR_LIGHT)
        input_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # اسم المستخدم
        tk.Label(input_frame, text="اسم المستخدم:", font=("Arial", 11), bg=COLOR_LIGHT).pack(anchor="e", pady=(0, 5))
        self.username_entry = tk.Entry(input_frame, font=("Arial", 11), width=30)
        self.username_entry.pack(fill=tk.X, pady=(0, 15))
        self.username_entry.focus()
        
        # كلمة المرور
        tk.Label(input_frame, text="كلمة المرور:", font=("Arial", 11), bg=COLOR_LIGHT).pack(anchor="e", pady=(0, 5))
        self.password_entry = tk.Entry(input_frame, font=("Arial", 11), width=30, show="*")
        self.password_entry.pack(fill=tk.X, pady=(0, 20))
        self.password_entry.bind("<Return>", lambda e: self.login())
        
        # أزرار
        button_frame = tk.Frame(input_frame, bg=COLOR_LIGHT)
        button_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(
            button_frame,
            text="دخول",
            font=("Arial", 11, "bold"),
            bg=COLOR_PRIMARY,
            fg=COLOR_WHITE,
            width=15,
            command=self.login
        ).pack(side=tk.RIGHT, padx=5)
        
        tk.Button(
            button_frame,
            text="خروج",
            font=("Arial", 11, "bold"),
            bg=COLOR_ERROR,
            fg=COLOR_WHITE,
            width=15,
            command=self.root.quit
        ).pack(side=tk.LEFT, padx=5)
        
        # معلومات المستخدمين الافتراضيين
        info_frame = tk.Frame(main_frame, bg=COLOR_LIGHTER)
        info_frame.pack(fill=tk.X, padx=20, pady=20)
        
        info_text = """المستخدمون الافتراضيون:
اسم: مدير الفرع | كلمة المرور: 123456 | الدور: مدير
اسم: admin | كلمة المرور: admin | الدور: باحث"""
        
        tk.Label(
            info_frame,
            text=info_text,
            font=("Arial", 9),
            bg=COLOR_LIGHTER,
            justify=tk.RIGHT
        ).pack(fill=tk.BOTH, padx=10, pady=10)
    
    def login(self):
        """معالجة تسجيل الدخول"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("تحذير", "الرجاء إدخال اسم المستخدم وكلمة المرور")
            return
        
        # التحقق من بيانات المستخدم
        query = "SELECT * FROM users WHERE username = ? AND active = 1"
        result = self.db.fetch_query(query, (username,))
        
        if not result:
            messagebox.showerror("خطأ", "بيانات المستخدم غير صحيحة")
            return
        
        user = result[0]
        hashed_password = Database.hash_password(password)
        
        if user[2] != hashed_password:  # التحقق من كلمة المرور
            messagebox.showerror("خطأ", "كلمة المرور غير صحيحة")
            return
        
        # تسجيل الدخول بنجاح
        self.current_user = dict(user)
        messagebox.showinfo("نجح", f"مرحباً {user[3]}!")
        
        # فتح النافذة الرئيسية
        self.open_main_window()
    
    def open_main_window(self):
        """فتح النافذة الرئيسية"""
        self.root.destroy()
        new_root = tk.Tk()
        MainWindow(new_root, self.current_user)
        new_root.mainloop()
