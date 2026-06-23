#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام صندوق رعاية وتأهيل المعاقين - فرع صعدة
Disabled Registry Management System
"""

import tkinter as tk
from tkinter import messagebox
import os
import sys
from pathlib import Path

# إضافة المسار للمكتبات المحلية
sys.path.insert(0, str(Path(__file__).parent))

from app.database import Database
from app.ui.login_window import LoginWindow

def main():
    """نقطة الدخول الرئيسية للتطبيق"""
    try:
        # التحقق من وجود قاعدة البيانات وإنشاؤها إن لزم
        db = Database()
        db.init_database()
        
        # إنشاء نافذة تسجيل الدخول
        root = tk.Tk()
        root.withdraw()  # إخفاء النافذة الرئيسية مؤقتاً
        
        login_window = LoginWindow(root)
        root.deiconify()  # إظهار النافذة
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("خطأ", f"حدث خطأ عند بدء التطبيق:\n{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
