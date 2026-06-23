# -*- coding: utf-8 -*-
"""
ملف الإعدادات والثوابت
"""

# معلومات قاعدة البيانات
DB_FILE = "registry.db"
DB_PATH = f"./{DB_FILE}"

# إعدادات الواجهة
WINDOW_TITLE = "نظام صندوق رعاية وتأهيل المعاقين - فرع صعدة"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 600

# الألوان
COLOR_PRIMARY = "#1a5276"  # الكحلي الملكي
COLOR_SECONDARY = "#0a3d5c"  # أزرق داكن
COLOR_LIGHT = "#e0f0f8"  # أزرق فاتح
COLOR_LIGHTER = "#d0e8f4"  # أزرق أفتح
COLOR_ACCENT = "#85c1e9"  # أزرق متوسط
COLOR_WHITE = "#ffffff"
COLOR_BLACK = "#000000"
COLOR_SUCCESS = "#27ae60"
COLOR_ERROR = "#e74c3c"
COLOR_WARNING = "#f39c12"

# أنواع المستخدمين والصلاحيات
USER_ROLES = {
    "admin": "مدير النظام والفرع",
    "researcher": "باحث اجتماعي إداري",
    "operator": "مدخل بيانات"
}

ROLE_PERMISSIONS = {
    "admin": ["view_all", "add", "edit", "delete", "reports", "users", "sync"],
    "researcher": ["view_all", "add", "edit", "reports"],
    "operator": ["view", "add", "edit"]
}

# أنواع الإعاقات
DISABILITY_TYPES = [
    "حركية",
    "بصرية",
    "سمعية",
    "عقلية",
    "نطقية",
    "نفسية",
    "أخرى"
]

# أنواع الخدمات
SERVICE_TYPES = [
    "أجهزة مساعدة",
    "رعاية طبية",
    "دعم مادي",
    "تأهيل",
    "تعليم",
    "أخرى"
]

# أنواع الاحتياجات
NEEDS_TYPES = [
    "أجهزة مساعدة",
    "رعاية طبية",
    "دعم مادي",
    "تأهيل",
    "تعليم",
    "سكن",
    "نقل",
    "أخرى"
]

# الحقول الأساسية للمستفيدين
BASIC_FIELDS = [
    "daily_number",      # رقم اليومية
    "case_number",       # رقم الحالة
    "registration_date", # تاريخ التسجيل
    "disability_type",   # نوع الإعاقة
    "name",              # الاسم الرباعي
    "nickname",          # اللقب
    "gender",            # الجنس
    "birth_year",        # سنة الميلاد
    "birthplace",        # محل الميلاد
    "governorate",       # المحافظة
    "district",          # المديرية
    "subdivision",       # العزلة
    "village",           # القرية
    "landmark",          # معلم بارز
    "phone1",            # رقم الهاتف
    "phone2",            # رقم هاتف آخر
    "marital_status",    # الحالة الاجتماعية
    "children_count",    # عدد الأولاد
    "education_level",   # الحالة التعليمية
    "health_status",     # الحالة الصحية
    "disease_type",      # نوع المرض
    "other_disabled",    # معاقين آخرين
    "provider_type",     # صفة المعيل
    "provider_name",     # اسم المعيل
    "id_type",           # نوع الهوية
    "id_number",         # رقم الهوية
    "status",            # حالة المعاق
    "researcher_name",   # اسم الباحث
    "operator_name",     # مدخل البيانات
    "notes"              # ملاحظات
]

# الملفات المرفقة
ATTACHMENTS_TYPES = [
    "هوية المعاق",
    "شهادة ميلاد",
    "هوية المعيل",
    "تخطيط سمع",
    "تقرير طبي",
    "بطاقة صندوق",
    "بطاقة جمعية",
    "فحص نظر",
    "صورة 4×6"
]
