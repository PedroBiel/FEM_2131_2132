# -*- coding: utf-8 -*-
"""
FEM 2131/2132
3-4.5.1 Fatigue check for structural elemensts
3-4.5.1.2 Shear stresses in the material of structural parts
Permissible stresses for shear

Created on 21 Jan 2021 9:09

__author__ = Pedro Biel
__version__ = 0.0.0
__email__ = pbiel@taimweser.com
"""


class DataFrame:
    """
    Pandas DataFrame with the data for the calculation of the stresses for 
    fatigue.
    """
    
    def __init__(self, df):
        """
        Asumes df is the pandas DataFrame with the data for the calculation 
        of the stresses for fatigue, get the values of the columns.
        
        Parameters
        ----------
        df : pandas DataFrame ; data for the calculation of the stresses for 
                                fatigue.
        """
        
        self.df = df
        
    def get_df(self):
        """Getter of the DataFrame."""
        
        return self.df.copy()
        
    def get_df_columns(self):
        """Getter of the list wiht the DataFrame columns."""
        
        return list(self.df.columns)
        
    def get_sigma_W0(self):
        """Basic stress for W0 [MPa]."""
        
        return self.df['sigma_W0_[MPa]'].copy()
    
    def get_k_txy(self):
        """Ratio between the extreme stresses tau_xy."""
        
        return self.df['k_txy'].copy()

class Formulae(DataFrame):
    """
    Formulae for de permissible stresses for fatigue with shear loads 
    according to FEM 2131/2132.
    """
    
    def __init__(self, df, sigma_E, sigma_R):
        """
        Asumes df, sigma_E and sigma_R the data for the calculation of the 
        stresses for fatigue, get the permissible stresses for fatigue in 
        case of ratio k ≤ 0 and k > 0 for shear.

        Parameters
        ----------
        df      : pandas DataFrame ; data for the calculation of the stresses 
                                     for fatigue.
        sigma_E : int              ; [MPa] elastic limit of steel.
        sigma_R : int              ; [MPa] ultimate tensile strength of steel.
        """
        
        DataFrame.__init__(self, df)
        
        self.sigma_W0 = self.get_sigma_W0()
        self.sigma_E = sigma_E
        self.sigma_R = sigma_R
    
    def tension_stress_k_neg(self, k):
        """
        Permissible stress for k ≤ 0 and tension.
        
        Parameters
        ----------
        k : pandas Serie : ratio between the extreme stresses.
        """
        
        sigma_t = self.sigma_W0 * 5 / (3 - 2 * k)
        sigma_t = sigma_t.where(
            sigma_t <= 0.66 * self.sigma_E,  0.66 * self.sigma_E
            )
        
        return sigma_t
    
    def tension_stress_k_pos(self, k):
        """
        Permissible stress for k > 0 and tension.
        
        Parameters
        ----------
        k : pandas Serie : ratio between the extreme stresses.
        """
        
        sigma_0 = self.tensile_stress_k_0()
        sigma_1 = self.tensile_sttress_k_1()
        sigma_t = sigma_0 / (1 - (1 - sigma_0 / sigma_1) * k)
        sigma_t = sigma_t.where(
            sigma_t <= 0.66 * self.sigma_E,  0.66 * self.sigma_E
            )
        
        return sigma_t
    
    def tensile_stress_k_0(self):
        """Tensile stress for k = 0."""
        
        sigma_0 = 1.66 * self.sigma_W0
        
        return sigma_0
    
    def tensile_sttress_k_1(self):
        """Tensile stress for k = +1."""
        
        sigma_1 = 0.75 * self.sigma_R
        
        return sigma_1


class PermissibleTau(Formulae):
    """
    Permissible stresses for fatigue with shear loads according to 
    FEM 2131/2132.
    """
    
    def __init__(self, df, sigma_E, sigma_R):
        """
        Asumes df, sigma_E, sigma_R the data for the calculation of the 
        stresses for fatigue, get the permissible stresses for fatigue in 
        case of ratio k ≤ 0 and k > 0 for shear.

        Parameters
        ----------
        df      : pandas DataFrame ; data for the calculation of the stresses 
                                     for fatigue.
        sigma_W : pandas Serie     ; [MPa] basic stress.
        sigma_E :  int             ; [MPa] elastic limit of steel.
        sigma_R : int              ; [MPa] ultimate tensile strength of steel.
        """
        
        Formulae.__init__(self, df, sigma_E, sigma_R)
        
        self.k_txy = self.get_k_txy()
        
    def shear_stress(self):
        """Permissible stress for shear."""
        
        tension_stress_k_neg = self.tension_stress_k_neg(self.k_txy)
        tension_stress_k_pos = self.tension_stress_k_pos(self.k_txy)
        tension_stress = tension_stress_k_neg.where(
            self.k_txy <= 0, tension_stress_k_pos
            )
        shear_stress = tension_stress / 3**(0.5)
        
        return shear_stress


if __name__ == '__main__':

    import pandas as pd
    import random
    random.seed(0)
    
    sigma_E = 280
    sigma_R = 440
    
    d = {
        'sigma_W0_[MPa]': [random.randint(120, 164) for i in range(5)],
        'k_txy': [random.uniform(-1, 1) for i in range(5)]
        }
    df = pd.DataFrame(d)
    sigma_W0 = df['sigma_W0_[MPa]']
    k = df.k_txy
    print('\nsigma_W0')
    print(sigma_W0)
    print('\nk')
    print(k)
    
    stress = Formulae(df, sigma_E, sigma_R)
    tension_stress_k_neg = stress.tension_stress_k_neg(k)
    tension_stress_k_pos = stress.tension_stress_k_pos(k)
    tensile_stress_k_0 = stress.tensile_stress_k_0()
    tensile_sttress_k_1 = stress.tensile_sttress_k_1()
    
    print('\ntension stress k neg')
    print(tension_stress_k_neg)
    
    print('\ntension stress k pos')
    print(tension_stress_k_pos)
    
    print('\ntensile stress k = 0')
    print(tensile_stress_k_0)
    print('\ntansile stress k = +1')
    print(tensile_sttress_k_1)
    
    permissible_stress = PermissibleTau(df, sigma_E, sigma_R)
    shear_stress = permissible_stress.shear_stress()
    
    print('\nshear stress')
    print(shear_stress)
