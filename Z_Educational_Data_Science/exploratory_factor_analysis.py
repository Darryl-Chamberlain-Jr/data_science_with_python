# Exploratory Factor Analysis
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import semopy # SEM optimization in python
import graphviz
from PIL import Image
from IPython.display import display

from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity
from factor_analyzer.factor_analyzer import calculate_kmo

def perform_adequecy_test(df):
    chi_square_value,p_value=calculate_bartlett_sphericity(df)
    #p-value 0, so observed correlation matrix is not identity
    if p_value < 0.01:
        print(f"Bartlett's test of sphericity suggests the observed correlation matrix is not an identity matrix (p-value={round(p_value, 4)}).")
        kmo_all,kmo_model=calculate_kmo(df)
        if kmo_model > 0.6:
            print(f'KMO Test suggests factor analysis is appropriate (KMO={round(kmo_model, 2)}).')
            print('\nFactor Analysis is appropriate with this data.\n')
        else:
            print(f'KMO Test suggests factor analysis is not appropriate (KMO={round(kmo_model, 2)}).')
            print('\nFactor Analysis is not appropriate with this data.\n')
    else:
        print(p_value)
        print(f"Bartlett's test of sphericity suggests the observed correlation matrix is potentially an identity matrix and thus no factor analysis should be performed.")

def calculate_suggested_number_of_factors(df):
    # Step 2: Calculate Number of Factors
    fa=FactorAnalyzer()
    fa.fit(df)
    ev,v=fa.get_eigenvalues()
    n_factors=len(np.where(ev > 1)[0])
    print(f'Suggested number of factors: {n_factors}')
    
    # Create scree plot using matplotlib
    plt.scatter(range(1,df.shape[1]+1),ev)
    plt.plot(range(1,df.shape[1]+1),ev)
    plt.title('Scree Plot')
    plt.xlabel('Factors')
    plt.ylabel('Eigenvalue')
    plt.grid()
    plt.show()

    return fa

def create_factor_loading_matrix(df, fa, n_factors, variable_labels, df_name):
    fa.set_params(n_factors=n_factors, rotation='promax')
    fa.fit(df)
    loadings=fa.loadings_
    loading_df=pd.DataFrame(loadings).round(4)
    for col_name in loading_df.columns:    
        loading_df[col_name]=np.where(loading_df[col_name] < 0.4, '', loading_df[col_name])
    loading_df['variables']=variable_labels
    loading_df.set_index('variables', drop=True, inplace=True)
    #loading_df.to_excel(f'loadings_{df_name}.xlsx')
    return loading_df

def total_variance_explained(fa, n_factors):
    fa.get_factor_variance()
    # Sum of second row is total % cumulative variance explained by the N factors
    total_variance_explained = fa.get_factor_variance()[1].sum()
    print(f'\n{int(round(total_variance_explained*100, 0))}% cumulative variance explained by the {n_factors} factors')