# -*- coding: utf-8 -*-
"""
النافذة الرئيسية
"""

import tkinter as tk
from tkinter import messagebox, ttk
from app.config import *
from app.database import Database

class MainWindow:
    """النافذة الرئيسية للتطبيق"""
    
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.db = Database()
        
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        
        # تمركز النافذة
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
        """إنشاء الواجهة الرئيسية"""
        # الإطار العلوي
        header_frame = tk.Frame(self.root, bg=COLOR_PRIMARY, height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # عنوان التطبيق
        title_label = tk.Label(
            header_frame,
            text="نظام صندوق رعاية وتأهيل المعاقين - فرع صعدة",
            font=("Arial", 14, "bold"),
            bg=COLOR_PRIMARY,
            fg=COLOR_WHITE
        )
        title_label.pack(pady=10)
        
        # معلومات المستخدم
        user_info = f"المستخدم: {self.user[3]} | الدور: {USER_ROLES.get(self.user[4], 'غير محدد')}"
        user_label = tk.Label(
            header_frame,
            text=user_info,
            font=("Arial", 10),
            bg=COLOR_SECONDARY,
            fg=COLOR_WHITE
        )
        user_label.pack(fill=tk.X, padx=10, pady=5)
        
        # الإطار الرئيسي
        main_frame = tk.Frame(self.root, bg=COLOR_LIGHT)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # شريط الأدوات
        toolbar_frame = tk.Frame(main_frame, bg=COLOR_LIGHTER, height=50)
        toolbar_frame.pack(fill=tk.X, padx=5, pady=5)
        toolbar_frame.pack_propagate(False)
        
        # أزرار الأدوات
        buttons_data = [
            ("إضافة مستفيد", self.add_disabled_person),
            ("عرض المستفيدين", self.view_disabled_people),
            ("البحث", self.search),
            ("التقارير", self.reports),
        ]
        
        # إضافة أزرار إضافية حسب الصلاحيات
        if self.user[4] == "admin":
            buttons_data.extend([
                ("إدارة المستخدمين", self.manage_users),
                ("سجل النظام", self.view_logs)
            ])
        
        for btn_text, btn_command in buttons_data:
            btn = tk.Button(
                toolbar_frame,
                text=btn_text,
                font=("Arial", 10, "bold"),
                bg=COLOR_PRIMARY,
                fg=COLOR_WHITE,
                padx=10,
                pady=5,
                command=btn_command
            )
            btn.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # زر الخروج
        logout_btn = tk.Button(
            toolbar_frame,
            text="خروج",
            font=("Arial", 10, "bold"),
            bg=COLOR_ERROR,
            fg=COLOR_WHITE,
            padx=10,
            pady=5,
            command=self.logout
        )
        logout_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # منطقة المحتوى
        self.content_frame = tk.Frame(main_frame, bg=COLOR_LIGHT)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # عرض الشاشة الرئيسية
        self.show_home()
    
    def clear_content(self):
        """مسح منطقة المحتوى"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_home(self):
        """عرض الشاشة الرئيسية"""
        self.clear_content()
        
        welcome_frame = tk.Frame(self.content_frame, bg=COLOR_LIGHT)
        welcome_frame.pack(fill=tk.BOTH, expand=True)
        
        welcome_label = tk.Label(
            welcome_frame,
            text=f"مرحباً بك {self.user[3]}!",
            font=("Arial", 18, "bold"),
            bg=COLOR_LIGHT,
            fg=COLOR_PRIMARY
        )
        welcome_label.pack(pady=50)
        
        info_label = tk.Label(
            welcome_frame,
            text="اختر أحد الخيارات من أعلى الشاشة للبدء",
            font=("Arial", 12),
            bg=COLOR_LIGHT,
            fg=COLOR_SECONDARY
        )
        info_label.pack()
    
    def add_disabled_person(self):
        """إضافة مستفيد جديد"""
        self.clear_content()
        tk.Label(self.content_frame, text="إضافة مستفيد جديد", font=("Arial", 14, "bold"), bg=COLOR_LIGHT).pack(pady=20)
        tk.Label(self.content_frame, text="سيتم تطوير هذه الميزة", bg=COLOR_LIGHT).pack()
    
    def view_disabled_people(self):
        """عرض المستفيدين"""
        self.clear_content()
        tk.Label(self.content_frame, text="عرض المستفيدين", font=("Arial", 14, "bold"), bg=COLOR_LIGHT).pack(pady=20)
        
        # جدول المستفيدين
        tree_frame = tk.Frame(self.content_frame, bg=COLOR_LIGHT)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("رقم الحالة", "الاسم", "الإعاقة", "المحافظة", "الهاتف")
        tree = ttk.Treeview(tree_frame, columns=columns, height=15)
        tree.column("#0", width=50)
        tree.heading("#0", text="م")
        
        for col in columns:
            tree.column(col, width=100)
            tree.heading(col, text=col)
        
        tree.pack(fill=tk.BOTH, expand=True)
    
    def search(self):
        """البحث"""
        self.clear_content()
        tk.Label(self.content_frame, text="البحث", font=("Arial", 14, "bold"), bg=COLOR_LIGHT).pack(pady=20)
        tk.Label(self.content_frame, text="سيتم تطوير هذه الميزة", bg=COLOR_LIGHT).pack()
    
    def reports(self):
        """التقارير"""
        self.clear_content()
        tk.Label(self.content_frame, text="التقارير والإحصائيات", font=("Arial", 14, "bold"), bg=COLOR_LIGHT).pack(pady=20)
        tk.Label(self.content_frame, text="سيتم تطوير هذه الميزة", bg=COLOR_LIGHT).pack()
    
    def manage_users(self):
        """إدارة المستخدمين"""
        self.clear_content()
        tk.Label(self.content_frame, text="إدارة المستخدمين", font=("Arial", 14, "bold"), bg=COLOR_LIGHT).pack(pady=20)
        tk.Label(self.content_frame, text="سيتم تطوير هذه الميزة", bg=COLOR_LIGHT).pack()
    
    def view_logs(self):
        """عرض السجلات"""
        self.clear_content()
        tk.Label(self.content_frame, text="سجل النظام", font=("Arial", 14, "bold"), bg=COLOR_LIGHT).pack(pady=20)
        tk.Label(self.content_frame, text="سيتم تطوير هذه الميزة", bg=COLOR_LIGHT).pack()
    
    def logout(self):
        """تسجيل الخروج"""
        if messagebox.askyesno("تأكيد", "هل تريد تسجيل الخروج؟"):
            self.root.destroy()
            import tkinter as tk
            new_root = tk.Tk()
            from app.ui.login_window import LoginWindow
            LoginWindow(new_root)
            new_root.mainloop()
