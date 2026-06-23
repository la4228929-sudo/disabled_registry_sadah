# -*- coding: utf-8 -*-
"""
خوارزميات التقارير والطباعة
"""

from datetime import datetime
import os

class ReportGenerator:
    """مولد التقارير"""
    
    @staticmethod
    def generate_html_report(people_data):
        """إنشاء تقرير HTML"""
        html_content = '''
        <!DOCTYPE html>
        <html dir="rtl" lang="ar">
        <head>
            <meta charset="UTF-8">
            <title>تقرير المستفيدين</title>
            <style>
                body { font-family: Arial, sans-serif; background-color: #f5f5f5; }
                .header { background-color: #1a5276; color: white; padding: 20px; text-align: center; }
                .header h1 { margin: 0; }
                .header p { margin: 5px 0; font-size: 12px; }
                table { width: 100%; border-collapse: collapse; background-color: white; margin: 20px 0; }
                th { background-color: #85c1e9; color: #0a3d5c; padding: 10px; text-align: right; }
                td { padding: 8px; border-bottom: 1px solid #ddd; text-align: right; }
                tr:hover { background-color: #f0f0f0; }
                .footer { text-align: center; font-size: 12px; color: #666; margin-top: 20px; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>نظام صندوق رعاية وتأهيل المعاقين</h1>
                <p>فرع صعدة - تقرير المستفيدين</p>
                <p>التاريخ: ''' + datetime.now().strftime('%Y-%m-%d') + '''</p>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>م</th>
                        <th>الاسم</th>
                        <th>نوع الإعاقة</th>
                        <th>المحافظة</th>
                        <th>الهاتف</th>
                        <th>الحالة</th>
                    </tr>
                </thead>
                <tbody>
        '''
        
        for idx, person in enumerate(people_data, 1):
            html_content += f'''
                <tr>
                    <td>{idx}</td>
                    <td>{person[4] if len(person) > 4 else ''}</td>
                    <td>{person[3] if len(person) > 3 else ''}</td>
                    <td>{person[9] if len(person) > 9 else ''}</td>
                    <td>{person[14] if len(person) > 14 else ''}</td>
                    <td>{person[26] if len(person) > 26 else ''}</td>
                </tr>
            '''
        
        html_content += '''
                </tbody>
            </table>
            <div class="footer">
                <p>تم إنشاء هذا التقرير بواسطة نظام صندوق رعاية المعاقين</p>
            </div>
        </body>
        </html>
        '''
        
        return html_content
    
    @staticmethod
    def generate_excel_report(people_data, filename='report.xlsx'):
        """إنشاء تقرير Excel"""
        try:
            import xlsxwriter
            
            workbook = xlsxwriter.Workbook(filename)
            worksheet = workbook.add_worksheet('المستفيدون')
            
            # تنسيق الرأس
            header_format = workbook.add_format({
                'bg_color': '#1a5276',
                'font_color': 'white',
                'bold': True,
                'align': 'right',
                'border': 1
            })
            
            # تنسيق الخلايا
            cell_format = workbook.add_format({
                'align': 'right',
                'border': 1
            })
            
            # أسماء الأعمدة
            headers = ['م', 'الاسم', 'نوع الإعاقة', 'المحافظة', 'المديرية', 'الهاتف', 'الحالة']
            
            for col, header in enumerate(headers):
                worksheet.write(0, col, header, header_format)
            
            # البيانات
            for row, person in enumerate(people_data, 1):
                worksheet.write(row, 0, row, cell_format)
                worksheet.write(row, 1, person[4] if len(person) > 4 else '', cell_format)
                worksheet.write(row, 2, person[3] if len(person) > 3 else '', cell_format)
                worksheet.write(row, 3, person[9] if len(person) > 9 else '', cell_format)
                worksheet.write(row, 4, person[10] if len(person) > 10 else '', cell_format)
                worksheet.write(row, 5, person[14] if len(person) > 14 else '', cell_format)
                worksheet.write(row, 6, person[26] if len(person) > 26 else '', cell_format)
            
            workbook.close()
            return True
        except Exception as e:
            print(f'خطأ في إنشاء التقرير: {e}')
            return False
    
    @staticmethod
    def generate_id_card(person_data):
        """إنشاء بطاقة هوية"""
        card_html = f'''
        <html dir="rtl" lang="ar">
        <head>
            <meta charset="UTF-8">
            <title>بطاقة هوية - {person_data[4] if len(person_data) > 4 else 'المستفيد'}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
                .card {{
                    width: 300px;
                    height: 200px;
                    border: 2px solid #1a5276;
                    border-radius: 10px;
                    padding: 15px;
                    background: linear-gradient(135deg, #e0f0f8 0%, #d0e8f4 100%);
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    font-size: 12px;
                }}
                .header {{ color: #1a5276; font-weight: bold; text-align: center; border-bottom: 2px solid #1a5276; padding-bottom: 10px; margin-bottom: 10px; }}
                .field {{ margin: 5px 0; }}
                .label {{ font-weight: bold; color: #0a3d5c; }}
                .value {{ color: #1a5276; }}
                .footer {{ text-align: center; margin-top: 15px; font-size: 10px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="card">
                <div class="header">بطاقة المستفيد</div>
                <div class="field">
                    <span class="label">الاسم:</span>
                    <span class="value">{person_data[4] if len(person_data) > 4 else ''}</span>
                </div>
                <div class="field">
                    <span class="label">رقم الحالة:</span>
                    <span class="value">{person_data[2] if len(person_data) > 2 else ''}</span>
                </div>
                <div class="field">
                    <span class="label">نوع الإعاقة:</span>
                    <span class="value">{person_data[3] if len(person_data) > 3 else ''}</span>
                </div>
                <div class="field">
                    <span class="label">الهاتف:</span>
                    <span class="value">{person_data[14] if len(person_data) > 14 else ''}</span>
                </div>
                <div class="footer">
                    <p>صندوق رعاية وتأهيل المعاقين - فرع صعدة</p>
                </div>
            </div>
        </body>
        </html>
        '''
        return card_html
