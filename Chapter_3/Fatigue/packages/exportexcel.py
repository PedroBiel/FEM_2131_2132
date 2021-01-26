# -*- coding: utf-8 -*-
"""
Export pandas DataFrames to Excel

Created on Fri Jan 22 13:23:30 2021

__author__ = Pedro Biel
__version__ = 0.0.0
__email__ = pbiel@taimweser.com
"""

import pandas as pd
#import xlsxwriter


class ExportExcel:
    """Export pandas DataFrame to Excel."""
    
    def __init__(self, df):
        """Asumes df is a pandas DataFrame to export to Excel."""
        
        self.df = df
        
        cols1 = [
            'bar', 'node', 'component_group', 'noth_effect',
            'sigma_x_max_[MPa]', 'sigma_x_min_[MPa]', 'sigma_y_max_[MPa]',
            'sigma_y_min_[MPa]', 'tau_xy_max_[MPa]', 'tau_xy_min_[MPa]'
            ]
        cols2 = [
            'bar', 'node', 'component_group', 'noth_effect',
            'sigma_x_max_[MPa]', 'sigma_y_max_[MPa]', 'tau_xy_max_[MPa]',
            'sigma_xa_[MPa]', 'sigma_ya_[MPa]', 'tau_a_[MPa]'
            ]
        cols3 = [
            'bar', 'node', 'component_group', 'noth_effect',
            'ratio_s_x', 'ratio_s_y', 'ratio_t_xy', 'ratio_1', 'ratio_2',
            'Validate'
            ]
        
        self.df1 = self.df[cols1].copy()
        self.df2 = self.df[cols2].copy()
        self.df3 = self.df[cols3].copy()
        
        self.n_rows_df1 = len(self.df1.index)
        self.n_rows_df2 = len(self.df2.index)
        
    def export_excel(self):
        """Pandas Excel with multiple DataFrames."""
        
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter('fatigue_check.xlsx', engine='xlsxwriter')

        # Position the dataframes in the worksheet.
        self.df1.to_excel(writer, sheet_name='fatigue check')
        self.df2.to_excel(writer, sheet_name='fatigue check',
                     startrow=self.n_rows_df1 + 2)
        self.df3.to_excel(writer, sheet_name='fatigue check',
                     startrow=self.n_rows_df1 + self.n_rows_df2 + 4)
        
        # Get the xlsxwriter workbook and worksheet objects.
        wb = writer.book
        ws = writer.sheets['fatigue check']
        
        # Add some cell formats.
        format1 = wb.add_format()
        format1.set_align('center')
        
        format2 = wb.add_format()
        format2.set_bg_color('#EAFAF1')  # Hell green. https://htmlcolorcodes.com/es/
        
        format3 = wb.add_format()
        format3.set_bg_color('#FEF5E7')  # Hell orange.
        
        # Set the column width.
        ws.set_column('B:C', 7, format1)
        ws.set_column('D:K', 19, format1)
        
        # Hide screen and printed gridlines.
        ws.hide_gridlines(2)
        
        # Write a conditional format over a range.
        ws.conditional_format(
            'I26:I35', {
                'type': 'cell',
                'criteria': '<=',
                'value': 1.0,
                'format': format2
                })
        
        ws.conditional_format(
            'I26:I35', {
                'type': 'cell',
                'criteria': '>',
                'value': 1.0,
                'format': format3
                })
        
        ws.conditional_format(
            'J26:J35', {
                'type': 'cell',
                'criteria': '<=',
                'value': 1.05,
                'format': format2
                })
        
        ws.conditional_format(
            'J26:J35', {
                'type': 'cell',
                'criteria': '>',
                'value': 1.05,
                'format': format3
                })
        
        ws.conditional_format(
            'K26:K35', {
                'type': 'cell',
                'criteria': '==',
                'value': '"yes"',
                'format': format2
                })
        
        ws.conditional_format(
            'K26:K35', {
                'type': 'cell',
                'criteria': '==',
                'value': '"no"',
                'format': format3
                })
        
        # Close the Pandas Excel writer and output the Excel file.
        writer.save()
        