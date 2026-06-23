# -*- coding: utf-8 -*-
"""
خدمات البيانات والعمليات
"""

from app.database import Database
from datetime import datetime

class DisabledPersonService:
    """خدمة إدارة المستفيدين"""
    
    def __init__(self):
        self.db = Database()
    
    def add_person(self, data):
        """إضافة مستفيد جديد"""
        query = '''
            INSERT INTO disabled_people (
                daily_number, case_number, registration_date, disability_type,
                name, nickname, gender, birth_year, birthplace, governorate,
                district, subdivision, village, landmark, phone1, phone2,
                marital_status, children_count, education_level, health_status,
                disease_type, other_disabled, provider_type, provider_name,
                id_type, id_number, status, researcher_name, operator_name, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        values = (
            data.get('daily_number'),
            data.get('case_number'),
            data.get('registration_date', datetime.now().strftime('%Y-%m-%d')),
            data.get('disability_type'),
            data.get('name'),
            data.get('nickname'),
            data.get('gender'),
            data.get('birth_year'),
            data.get('birthplace'),
            data.get('governorate'),
            data.get('district'),
            data.get('subdivision'),
            data.get('village'),
            data.get('landmark'),
            data.get('phone1'),
            data.get('phone2'),
            data.get('marital_status'),
            data.get('children_count'),
            data.get('education_level'),
            data.get('health_status'),
            data.get('disease_type'),
            data.get('other_disabled'),
            data.get('provider_type'),
            data.get('provider_name'),
            data.get('id_type'),
            data.get('id_number'),
            data.get('status'),
            data.get('researcher_name'),
            data.get('operator_name'),
            data.get('notes')
        )
        
        return self.db.execute_query(query, values)
    
    def get_all_people(self):
        """الحصول على جميع المستفيدين"""
        query = 'SELECT * FROM disabled_people ORDER BY id DESC'
        return self.db.fetch_query(query)
    
    def get_person_by_id(self, person_id):
        """الحصول على بيانات مستفيد"""
        query = 'SELECT * FROM disabled_people WHERE id = ?'
        result = self.db.fetch_query(query, (person_id,))
        return result[0] if result else None
    
    def update_person(self, person_id, data):
        """تحديث بيانات مستفيد"""
        set_clause = ', '.join([f'{key} = ?' for key in data.keys()])
        query = f'UPDATE disabled_people SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?'
        
        values = list(data.values()) + [person_id]
        return self.db.execute_query(query, values)
    
    def delete_person(self, person_id):
        """حذف مستفيد"""
        query = 'DELETE FROM disabled_people WHERE id = ?'
        return self.db.execute_query(query, (person_id,))
    
    def search_people(self, search_term):
        """البحث عن مستفيدين"""
        query = '''
            SELECT * FROM disabled_people WHERE
            name LIKE ? OR case_number LIKE ? OR phone1 LIKE ? OR
            governorate LIKE ? OR disability_type LIKE ?
            ORDER BY id DESC
        '''
        search_pattern = f'%{search_term}%'
        return self.db.fetch_query(query, (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern))
    
    def get_statistics(self):
        """الحصول على الإحصائيات"""
        stats = {}
        
        # إجمالي المسجلين
        query = 'SELECT COUNT(*) as total FROM disabled_people'
        result = self.db.fetch_query(query)
        stats['total'] = result[0][0] if result else 0
        
        # الذكور
        query = "SELECT COUNT(*) as males FROM disabled_people WHERE gender = 'ذكر'"
        result = self.db.fetch_query(query)
        stats['males'] = result[0][0] if result else 0
        
        # الإناث
        query = "SELECT COUNT(*) as females FROM disabled_people WHERE gender = 'أنثى'"
        result = self.db.fetch_query(query)
        stats['females'] = result[0][0] if result else 0
        
        # توزيع الإعاقات
        query = 'SELECT disability_type, COUNT(*) as count FROM disabled_people GROUP BY disability_type'
        result = self.db.fetch_query(query)
        stats['disabilities'] = [(row[0], row[1]) for row in (result or [])]
        
        # السندات المصدرة
        query = 'SELECT COUNT(*) as vouchers FROM service_vouchers'
        result = self.db.fetch_query(query)
        stats['vouchers'] = result[0][0] if result else 0
        
        return stats


class DisabilityService:
    """خدمة إدارة الإعاقات"""
    
    def __init__(self):
        self.db = Database()
    
    def add_disability(self, person_id, description, medical_report):
        """إضافة إعاقة"""
        query = '''
            INSERT INTO disabilities_list (person_id, disability_description, medical_report)
            VALUES (?, ?, ?)
        '''
        return self.db.execute_query(query, (person_id, description, medical_report))
    
    def get_disabilities_by_person(self, person_id):
        """الحصول على إعاقات المستفيد"""
        query = 'SELECT * FROM disabilities_list WHERE person_id = ?'
        return self.db.fetch_query(query, (person_id,))
    
    def update_received_card(self, disability_id):
        """تحديث حالة البطاقة المستلمة"""
        query = 'UPDATE disabilities_list SET received_card = 1 WHERE id = ?'
        return self.db.execute_query(query, (disability_id,))


class NeedService:
    """خدمة إدارة الاحتياجات"""
    
    def __init__(self):
        self.db = Database()
    
    def add_need(self, person_id, need_type, description, priority='متوسط'):
        """إضافة احتياج"""
        query = '''
            INSERT INTO needs_list (person_id, need_type, description, priority)
            VALUES (?, ?, ?, ?)
        '''
        return self.db.execute_query(query, (person_id, need_type, description, priority))
    
    def get_needs_by_person(self, person_id):
        """الحصول على احتياجات المستفيد"""
        query = 'SELECT * FROM needs_list WHERE person_id = ?'
        return self.db.fetch_query(query, (person_id,))
    
    def update_need_status(self, need_id, status):
        """تحديث حالة الاحتياج"""
        query = 'UPDATE needs_list SET status = ? WHERE id = ?'
        return self.db.execute_query(query, (status, need_id))


class ServiceVoucherService:
    """خدمة إدارة سندات الخدمة"""
    
    def __init__(self):
        self.db = Database()
    
    def create_voucher(self, person_id, voucher_number, service_type, amount, issued_by):
        """إنشاء سند خدمة"""
        query = '''
            INSERT INTO service_vouchers (person_id, voucher_number, service_type, amount, issued_date, issued_by)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        issued_date = datetime.now().strftime('%Y-%m-%d')
        return self.db.execute_query(query, (person_id, voucher_number, service_type, amount, issued_date, issued_by))
    
    def get_vouchers_by_person(self, person_id):
        """الحصول على سندات المستفيد"""
        query = 'SELECT * FROM service_vouchers WHERE person_id = ?'
        return self.db.fetch_query(query, (person_id,))
    
    def get_all_vouchers(self):
        """الحصول على جميع السندات"""
        query = 'SELECT * FROM service_vouchers ORDER BY id DESC'
        return self.db.fetch_query(query)
