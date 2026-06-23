# -*- coding: utf-8 -*-
"""
إدارة قاعدة البيانات
"""

import sqlite3
from pathlib import Path
import hashlib
from datetime import datetime
from app.config import DB_PATH, ATTACHMENTS_TYPES

class Database:
    """فئة إدارة قاعدة البيانات"""
    
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.connection = None
    
    def connect(self):
        """الاتصال بقاعدة البيانات"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            return self.connection
        except sqlite3.Error as e:
            print(f"خطأ في الاتصال: {e}")
            return None
    
    def disconnect(self):
        """قطع الاتصال بقاعدة البيانات"""
        if self.connection:
            self.connection.close()
    
    def execute_query(self, query, params=()):
        """تنفيذ استعلام"""
        conn = self.connect()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.lastrowid
            except sqlite3.Error as e:
                print(f"خطأ في الاستعلام: {e}")
                return None
            finally:
                conn.close()
    
    def fetch_query(self, query, params=()):
        """جلب النتائج من استعلام"""
        conn = self.connect()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query, params)
                return cursor.fetchall()
            except sqlite3.Error as e:
                print(f"خطأ في الاستعلام: {e}")
                return None
            finally:
                conn.close()
    
    def init_database(self):
        """إنشاء جداول قاعدة البيانات"""
        conn = self.connect()
        if not conn:
            return False
        
        cursor = conn.cursor()
        
        # جدول المستخدمين
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT NOT NULL,
                email TEXT,
                role TEXT NOT NULL,
                active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول المستفيدين
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS disabled_people (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                daily_number TEXT UNIQUE,
                case_number TEXT UNIQUE,
                registration_date TEXT,
                disability_type TEXT,
                name TEXT NOT NULL,
                nickname TEXT,
                gender TEXT,
                birth_year INTEGER,
                birthplace TEXT,
                governorate TEXT,
                district TEXT,
                subdivision TEXT,
                village TEXT,
                landmark TEXT,
                phone1 TEXT,
                phone2 TEXT,
                marital_status TEXT,
                children_count INTEGER,
                education_level TEXT,
                health_status TEXT,
                disease_type TEXT,
                other_disabled TEXT,
                provider_type TEXT,
                provider_name TEXT,
                id_type TEXT,
                id_number TEXT,
                status TEXT,
                researcher_name TEXT,
                operator_name TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول الإعاقات الفرعية
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS disabilities_list (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER NOT NULL,
                disability_description TEXT,
                medical_report TEXT,
                received_card INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (person_id) REFERENCES disabled_people(id)
            )
        ''')
        
        # جدول الاحتياجات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS needs_list (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER NOT NULL,
                need_type TEXT,
                description TEXT,
                priority TEXT DEFAULT 'متوسط',
                status TEXT DEFAULT 'مسجل',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (person_id) REFERENCES disabled_people(id)
            )
        ''')
        
        # جدول الخدمات المقدمة
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS provided_services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER NOT NULL,
                service_type TEXT,
                service_description TEXT,
                amount REAL,
                funded_by TEXT,
                received_by TEXT,
                service_date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (person_id) REFERENCES disabled_people(id)
            )
        ''')
        
        # جدول سندات الخدمة
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS service_vouchers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER NOT NULL,
                voucher_number TEXT UNIQUE,
                service_type TEXT,
                amount REAL,
                issued_date TEXT,
                issued_by TEXT,
                status TEXT DEFAULT 'صادر',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (person_id) REFERENCES disabled_people(id)
            )
        ''')
        
        # جدول المرفقات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attachments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER NOT NULL,
                attachment_type TEXT,
                file_path TEXT,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (person_id) REFERENCES disabled_people(id)
            )
        ''')
        
        # جدول سجل النظام
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT,
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # إضافة المستخدمين الافتراضيين
        cursor.execute('SELECT COUNT(*) FROM users')
        if cursor.fetchone()[0] == 0:
            admin_password = hashlib.sha256("123456".encode()).hexdigest()
            researcher_password = hashlib.sha256("admin".encode()).hexdigest()
            
            cursor.execute('''
                INSERT INTO users (username, password, full_name, role)
                VALUES (?, ?, ?, ?)
            ''', ("مدير الفرع", admin_password, "مدير فرع صعدة", "admin"))
            
            cursor.execute('''
                INSERT INTO users (username, password, full_name, role)
                VALUES (?, ?, ?, ?)
            ''', ("admin", researcher_password, "باحث اجتماعي", "researcher"))
        
        conn.commit()
        conn.close()
        return True
    
    @staticmethod
    def hash_password(password):
        """تشفير كلمة المرور"""
        return hashlib.sha256(password.encode()).hexdigest()
