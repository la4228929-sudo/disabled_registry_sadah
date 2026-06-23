# -*- coding: utf-8 -*-
"""
ملفات إضافية للتطبيق
"""

import os
import json
from datetime import datetime

class FileManager:
    """إدارة الملفات والمرفقات"""
    
    ATTACHMENTS_DIR = "attachments"
    REPORTS_DIR = "reports"
    
    def __init__(self):
        self.create_directories()
    
    def create_directories(self):
        """إنشاء المجلدات المطلوبة"""
        if not os.path.exists(self.ATTACHMENTS_DIR):
            os.makedirs(self.ATTACHMENTS_DIR)
        if not os.path.exists(self.REPORTS_DIR):
            os.makedirs(self.REPORTS_DIR)
    
    def save_attachment(self, person_id, file_path, attachment_type):
        """حفظ المرفق"""
        person_dir = os.path.join(self.ATTACHMENTS_DIR, str(person_id))
        if not os.path.exists(person_dir):
            os.makedirs(person_dir)
        
        return person_dir
    
    def save_report(self, report_name, content):
        """حفظ التقرير"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{report_name}_{timestamp}.html"
        filepath = os.path.join(self.REPORTS_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath


class Logger:
    """نظام تسجيل الأحداث"""
    
    def __init__(self, db):
        self.db = db
    
    def log_action(self, user_id, action, details):
        """تسجيل إجراء"""
        query = '''
            INSERT INTO system_logs (user_id, action, details)
            VALUES (?, ?, ?)
        '''
        return self.db.execute_query(query, (user_id, action, details))
    
    def get_logs(self, limit=100):
        """الحصول على السجلات"""
        query = '''
            SELECT l.*, u.full_name FROM system_logs l
            LEFT JOIN users u ON l.user_id = u.id
            ORDER BY l.timestamp DESC LIMIT ?
        '''
        return self.db.fetch_query(query, (limit,))
