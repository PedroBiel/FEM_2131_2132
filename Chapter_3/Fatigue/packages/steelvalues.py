# -*- coding: utf-8 -*-
"""
FEM 2131/2132
3-4.5.1 Fatigue check for structural elemensts
Steel grade, elastic limit and ultimate tensile strength

Created on Mon Jan 25 08:11:56 2021

__author__ = Pedro Biel
__version__ = 0.0.0
__email__ = pbiel@taimweser.com
"""


class SteelValues:
    """Steel grade, elastic limit and ultimate tensile strength."""
    
    def __init__(self, df, steel_grade):
        """
        Asumes steel_grade is the steel grade of the material, get the elastic
        limit fy and the ultimate tensile strength fu of the material.

        Parameters
        ----------
        df          : pandas DataFrame ; characteristic values for the steel.
        steel_grade : str              ; steel grade of the material
        """
        
        self.df = df
        self.steel_grade = steel_grade
        
        self.d = {
            'Fe 360': 'S 235',
            'Fe 430': 'S 275',
            'Fe 510': 'S 355',
            'S 235': 'S 235',
            'S 275': 'S 275',
            'S 355': 'S 355'
            }  # Data with the values to search in the DataFrame.
        
        self.d1 = {
            'Fe 360': 'Fe360',
            'Fe 430': 'Fe430',
            'Fe 510': 'Fe510',
            'S 235': 'Fe360',
            'S 275': 'Fe430',
            'S 355': 'Fe510'
            }  # Data with the values to search in the database.
        
    def get_steel_grade(self):
        """Getter of the steel grade of the material."""
        
        return self.steel_grade
    
    def get_steel_for_db(self):
        """Getter of the steel for de database of structural steel."""
        
        return self.d1[self.steel_grade]
    
    def elastic_limit(self):
        """Elastic limit fy."""
        
        sigma_E = self.df.loc[(
            self.df['Calidad'] == self.d[self.steel_grade]) & (
            self.df['tmax'] == 40.0)]['fy'].item()
        
        return sigma_E
    
    def ultimate_tensile_strength(self):
        """Ultimate tensile strength fu."""
        
        sigma_R = self.df.loc[(
            self.df['Calidad'] == self.d[self.steel_grade]) & (
            self.df['tmax'] == 40.0)]['fu'].item()
                
        return sigma_R