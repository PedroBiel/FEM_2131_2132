# -*- coding: utf-8 -*-
"""
FEM 2131/2132
3-4.5.1 Fatigue check for structural elemensts
3-4.5.1.1 Tensile and compressive loads
Permissible stresses for fatigue

Created on 20 Jan 2021 11:30

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
        
    def get_sigma_W(self):
        """Basic stress [MPa]."""
        
        return self.df['sigma_W_[MPa]'].copy()
    
    def get_k_sx(self):
        """Ratio between the extreme stresses sigma_x."""
        
        return self.df['k_sx'].copy()
    
    def get_k_sy(self):
        """Ratio between the extreme stresses sigma_y."""
        
        return self.df['k_sy'].copy()
        
class Formulae(DataFrame):
    """
    Formulae for de permissible stresses for fatigue with tensile and 
    comprensive loads according to FEM 2131/2132.
    """
    
    def __init__(self, df, sigma_E, sigma_R):
        """
        Asumes df, sigma_E and sigma_R the data for the calculation of 
        the stresses for fatigue, get the permissible stresses for fatigue in 
        case of ratio k ≤ 0 and k > 0 for tension and compression.

        Parameters
        ----------
        df      : pandas DataFrame ; data for the calculation of the stresses 
                                     for fatigue.
        sigma_E : int              ; [MPa] elastic limit of steel.
        sigma_R : int              ; [MPa] ultimate tensile strength of steel.
        """
        
        DataFrame.__init__(self, df)
        
        self.sigma_W = self.get_sigma_W()
        self.sigma_E = sigma_E
        self.sigma_R = sigma_R
    
    def tension_stress_k_neg(self, k):
        """
        Permissible stress for k ≤ 0 and tension.
        
        Parameters
        ----------
        k : pandas Serie ; ratio between the extreme stresses.
        """
        
        sigma_t = self.sigma_W * 5 / (3 - 2 * k)
        sigma_t = sigma_t.where(
            sigma_t <= 0.66 * self.sigma_E,  0.66 * self.sigma_E
            )
        
        return sigma_t
    
    def compression_stress_k_neg(self, k):
        """
        Permissible stress for k ≤ 0 and compression.
        
        Parameters
        ----------
        k : pandas Serie ; ratio between the extreme stresses.
        """
        
        sigma_c = self.sigma_W * 2 / (1 - k)
        
        return sigma_c
    
    def tension_stress_k_pos(self, k):
        """
        Permissible stress for k > 0 and tension.
        
        Parameters
        ----------
        k : pandas Serie , ratio between the extreme stresses.
        """
        
        sigma_0 = self.tensile_stress_k_0()
        sigma_1 = self.tensile_stress_k_1()
        sigma_t = sigma_0 / (1 - (1 - sigma_0 / sigma_1) * k)
        sigma_t = sigma_t.where(
            sigma_t <= 0.66 * self.sigma_E,  0.66 * self.sigma_E
            )
        
        return sigma_t
    
    def compression_stress_k_pos(self, k):
        """
        Permissible stress for k > 0 and compression.
        
        Parameters
        ----------
        k : pandas Serie : ratio between the extreme stresses.
        """
        
        sigma_t = self.tension_stress_k_pos(k)
        sigma_c = 1.2 * sigma_t
        
        return sigma_c
    
    def tensile_stress_k_0(self):
        """Tensile stress for k = 0."""
        
        sigma_0 = 1.66 * self.sigma_W
        
        return sigma_0
    
    def tensile_stress_k_1(self):
        """Tensile stress for k = +1."""
        
        sigma_1 = 0.75 * self.sigma_R
        
        return sigma_1


class PermissibleSigma(Formulae):
    """
    Permissible stresses for fatigue with tensile and comprensive loads 
    according to FEM 2131/2132.
    """
    
    def __init__(self, df, sigma_E, sigma_R):
        """
        Asumes df, sigma_E, sigma_R the data for the calculation of the 
        stresses for fatigue, get the permissible stresses for fatigue in 
        case of ratio k ≤ 0 and k > 0 for tension and compression.

        Parameters
        ----------
        df      : pandas DataFrame ; data for the calculation of the stresses 
                                     for fatigue.
        sigma_E : int              ; [MPa] elastic limit of steel.
        sigma_R : int              ; [MPa] ultimate tensile strength of steel.
        """
        
        Formulae.__init__(self, df, sigma_E, sigma_R)
        
        self.k_sx = self.get_k_sx()
        self.k_sy = self.get_k_sy()
        
    def tension_stress_x(self):
        """Permissible stress_x for tension."""
        
        return self.tension_stress(self.k_sx)
    
    def tension_stress_y(self):
        """Permissible stress_y for tension."""
        
        return self.tension_stress(self.k_sy)
    
    def compression_stress_x(self):
        """Permissible stress_x for compression."""
        
        return self.compression_stress(self.k_sx)
    
    def compression_stress_y(self):
        """Permissible stress_y for compression."""
        
        return self.compression_stress(self.k_sy)

    def tension_stress(self, k):
        """Permissible stress for tension."""
        
        tension_stress_k_neg = self.tension_stress_k_neg(k)
        tension_stress_k_pos = self.tension_stress_k_pos(k)
        tension_stress = tension_stress_k_neg.where(
            k <= 0, tension_stress_k_pos
            )
        
        return tension_stress
    
    def compression_stress(self, k):
        """Permissible stress for compression."""
        
        compression_stress_k_neg = self.compression_stress_k_neg(k)
        compression_stress_k_pos = self.compression_stress_k_pos(k)
        compression_stress = compression_stress_k_neg.where(
            k <= 0, compression_stress_k_pos
            )
        
        return compression_stress * (-1)  # Compression: (-)


if __name__ == '__main__':

    import pandas as pd
    import random
    random.seed(0)
    
    sigma_E = 280
    sigma_R = 440
    
    d = {
        'sigma_W_[MPa]': [random.randint(27, 84) for i in range(5)],
        'k_sx': [random.uniform(-1, 1) for i in range(5)],
        'k_sy': [random.uniform(-1, 1) for i in range(5)]
        }
    df = pd.DataFrame(d)
    sigma_W = df['sigma_W_[MPa]']
    k_sx = df.k_sx
    k_sy = df.k_sy
    print('\nsigma_W')
    print(sigma_W)
    print('\nk_sx')
    print(k_sx)
    print('\nk_sy')
    print(k_sy)
    
    stress = Formulae(df, sigma_E, sigma_R)
    tension_stress_k_neg = stress.tension_stress_k_neg(k_sx)
    compression_stress_k_neg = stress.compression_stress_k_neg(k_sx)
    tension_stress_k_pos = stress.tension_stress_k_pos(k_sx)
    compression_stress_k_pos = stress.compression_stress_k_pos(k_sx)
    tensile_stress_k_0 = stress.tensile_stress_k_0()
    tensile_stress_k_1 = stress.tensile_stress_k_1()
    
    print('\ntension stress k neg')
    print(tension_stress_k_neg)
    print('\ncompression stress k neg')
    print(compression_stress_k_neg)
    
    print('\ntension stress k pos')
    print(tension_stress_k_pos)
    print('\ncompression stress k pos')
    print(compression_stress_k_pos)
    
    print('\ntensile stress k = 0')
    print(tensile_stress_k_0)
    print('\ntansile stress k = +1')
    print(tensile_stress_k_1)
    
    permissible_stress = PermissibleSigma(df, sigma_E, sigma_R)
    tensile_stress = permissible_stress.tension_stress_x()
    compression_stress = permissible_stress.compression_stress_x()
    
    print('\ntensile stress')
    print(tensile_stress)
    print('\ncompresion stress')
    print(compression_stress)