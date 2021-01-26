# -*- coding: utf-8 -*-
"""
FEM 2131/2132
3-4.5.1 Fatigue check for structural elemensts
3-4.5.1.3 Combined loads in tension (or compression) and shear
Permissible combined stresses for fatigue

Created on 21 Jan 2021 13:19

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
    
    def get_sigma_x_max(self):
        """Getter of sigma_x_max."""
        
        return self.df['sigma_x_max_[MPa]'].copy()
    
    def get_sigma_y_max(self):
        """Getter of sigma_y_max."""
        
        return self.df['sigma_y_max_[MPa]'].copy()
    
    def get_tau_xy_max(self):
        """Getter of tau_xy_max."""
        
        return self.df['tau_xy_max_[MPa]'].copy()
    
    def get_sigma_tx(self):
        """Getter of sigma_tx."""
        
        return self.df['sigma_tx_[MPa]'].copy()
    
    def get_sigma_cx(self):
        """Getter of sigma_cx."""
        
        return self.df['sigma_cx_[MPa]'].copy()
    
    def get_sigma_ty(self):
        """Getter of sigma_ty."""
        
        return self.df['sigma_ty_[MPa]'].copy()
    
    def get_sigma_cy(self):
        """Getter of sigma_cy."""
        
        return self.df['sigma_cy_[MPa]'].copy()
    
    def get_tau_a(self):
        """Getter of tau_a."""
        
        return self.df['tau_a_[MPa]'].copy()


class Formulae(DataFrame):
    """
    Formulae for de permissible combined stresses for fatigue with tensile,
    comprensive and shear loads according to FEM 2131/2132.
    """
    
    def __init__(self, df):
        """
        Asumes df has the data for the calculation of the stresses for 
        fatigue, get the permissible combined stresses for fatigue.

        Parameters
        ----------
        df : pandas DataFrame : data for the calculation.
        """
        
        DataFrame.__init__(self, df)
        
        self.sigma_x_max = self.get_sigma_x_max()
        self.sigma_y_max = self.get_sigma_y_max()
        self.tau_xy_max = self.get_tau_xy_max()
        self.sigma_tx = self.get_sigma_tx()
        self.sigma_cx = self.get_sigma_cx()
        self.sigma_ty = self.get_sigma_ty()
        self.sigma_cy = self.get_sigma_cy()
        self.tau_a = self.get_tau_a()
        
    def get_df_columns(self):
        """List with the names of the columns of the DataFrame."""
        
        return list(self.df.columns)[:]
    
    def permissible_stress(self, sigma_max, sigma_t, sigma_c):
        """
        Permissible stress.
        For sigma_max in tension -> permissible stress = sigma_t
        For sigma_max in compression -> permissible stress = sigma_c
        Sigma_max in tension ≥ 0 (positive value)
        Sigma_max in compression < 0 (negative value)
        """
        
        sigma = sigma_t.where(sigma_max >=0, sigma_c)
        
        return sigma
    
    def ratio(self, sigma_max, sigma_t, sigma_c):
        """Stress ratio."""
        
        sigma_a = self.permissible_stress(sigma_max, sigma_t, sigma_c)
        
        return sigma_max / sigma_a
    
    def ratio_sigma_x(self):
        """Stress ratio for sigma_x."""
        
        ratio = self.ratio(self.sigma_x_max, self.sigma_tx, self.sigma_cx)
        
        return ratio
    
    def ratio_sigma_y(self):
        """Stress ratio for sigma_y."""
        
        ratio = self.ratio(self.sigma_y_max, self.sigma_ty, self.sigma_cy)
        
        return ratio
    
    def ratio_tau_xy(self):
        """Stress ratio for tau_xy."""
        
        ratio = self.tau_xy_max.abs() / self.tau_a
        
        return ratio
    
    def ratio_1(self):
        """
        Combined stress ratio.
        First option (formula (5) in FEM 2131/2132, 3-4.5.1.3).
        """
        
        ratio_s_x = self.ratio_sigma_x()
        ratio_s_y = self.ratio_sigma_y()
        ratio_t_xy = self.ratio_tau_xy()
        
        permissible_stress_xa = self.permissible_stress(
            self.sigma_x_max, self.sigma_tx, self.sigma_cx
            )
        permissible_stress_ya = self.permissible_stress(
            self.sigma_y_max, self.sigma_ty, self.sigma_cy
            )
        ratio_s_xy = \
            self.sigma_x_max * self.sigma_y_max / \
                (permissible_stress_xa * permissible_stress_ya).abs()
    
        r1 = ratio_s_x**2 + ratio_s_y**2 - ratio_s_xy + ratio_t_xy**2
        
        return r1
    
    def ratio_2(self):
        """
        Combined stress ratio.
        Second option (formula in footnote *(1) in FEM 2131/2132, 3-4.5.1.3).
        """
        
        r1 = self.ratio_1()
        r2 = r1**(0.5)
        
        return r2
        

class PermissibleStress(Formulae):
    """
    Permissible stresses for fatigue with tensile, comprensive and shear loads 
    according to FEM 2131/2132.
    """
    
    def __init__(self, df):
        """
        Asumes df has the data for the calculation of the stresses for 
        fatigue, get the permissible stresses for fatigue.

        Parameters
        ----------
        df : pandas DataFrame : data for the calculation.
        """
        
        Formulae.__init__(self, df)
        
    def get_permissible_stress_sx(self):
        """Permissible stress for sigma_x."""
        
        s = self.permissible_stress(
            self.sigma_x_max, self.sigma_tx, self.sigma_cx
            )
        
        return s
    
    def get_permissible_stress_sy(self):
        """Permissible stress for sigma_y."""
        
        s = self.permissible_stress(
            self.sigma_y_max, self.sigma_ty, self.sigma_cy
            )
        
        return s
    
    def get_permissible_stress_txy(self):
        """Permissible stress for tau_xy."""
        
        s = self.tau_a
        
        return s
        
    def get_ratio_sigma_x(self):
        """Stress ratio for sigma_x."""
        
        r = self.ratio_sigma_x()
        
        return r
    
    def get_ratio_sigma_y(self):
        """Stress ratio for sigma_y."""
        
        r = self.ratio_sigma_y()
        
        return r
    
    def get_ratio_tau_xy(self):
        """Stress ratio for tau_xy."""
        
        r = self.ratio_tau_xy()
        
        return r
        
    def get_ratio_1(self):
        """"
        Combined stress ratio.
        First option (formula (5) in FEM 2131/2132, 3-4.5.1.3).
        """
        
        r1 = self.ratio_1()
        
        return r1
    
    def get_ratio_2(self):
        """
        Combined stress ratio.
        Second option (formula in footnote *(1) in FEM 2131/2132, 3-4.5.1.3).
        """
        
        r2 = self.ratio_2()
        
        return r2
    

if __name__ == '__main__':

    import pandas as pd
    import random
    random.seed(0)
    
    d = {
        'sigma_x_max_[MPa]': [random.randint(-120, 120) for i in range(5)],
        'sigma_y_max_[MPa]': [random.randint(-40, 40) for i in range(5)],
        'tau_xy_max_[MPa]': [random.randint(-4, 4) for i in range(5)],
        'sigma_tx_[MPa]': [random.randint(0, 150) for i in range(5)],
        'sigma_cx_[MPa]': [random.randint(-150, 0) for i in range(5)],
        'sigma_ty_[MPa]': [random.randint(0, 50) for i in range(5)],
        'sigma_cy_[MPa]': [random.randint(-50, 0) for i in range(5)],
        'tau_a_[MPa]': [random.randint(0, 5) for i in range(5)]
        }
    df = pd.DataFrame(d)
    print(df[['sigma_x_max_[MPa]', 'sigma_y_max_[MPa]', 'tau_xy_max_[MPa]']])
    print(df[['sigma_tx_[MPa]', 'sigma_cx_[MPa]']])
    print(df[['sigma_ty_[MPa]', 'sigma_cy_[MPa]']])
    print(df[['tau_a_[MPa]']])
    
    stress = PermissibleStress(df)
    
    print('\nratio for sigma_x_max_[MPa]')
    print(stress.ratio(
        df['sigma_x_max_[MPa]'], df['sigma_tx_[MPa]'], df['sigma_cx_[MPa]']
        ))
    print('\nratio for sigma_y_max_[MPa]')
    print(stress.ratio(
        df['sigma_y_max_[MPa]'], df['sigma_ty_[MPa]'], df['sigma_cy_[MPa]']
        ))
    
    print('\n####')
    print('\nratio_sigma_x')
    print(stress.ratio_sigma_x())
    print('\nratio_sigma_y')
    print(stress.ratio_sigma_y())
    print('\nratio_tau_xy')
    print(stress.ratio_tau_xy())
    
    print('\n####')
    print('\nratio_1')
    print(stress.ratio_1())
    print('\nget_ratio_1')
    print(stress.get_ratio_1())
    print('\nratio_2')
    print(stress.ratio_2())
    print('\nget_ratio_2')
    print(stress.get_ratio_2())
    
    


    