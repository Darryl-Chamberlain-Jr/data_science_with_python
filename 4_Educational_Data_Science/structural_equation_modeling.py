# Structrual Equation Modeling

def run_SEM(data, description, name):
    model_SEM=semopy.Model(description)
    optimize_results = model_SEM.fit(data)
    #print(optimize_results)

    inspect_estimates = model_SEM.inspect(mode='list', what='names', std_est=True)
    inspect_df=pd.DataFrame(inspect_estimates)
    inspect_df.to_excel(f'./SEM_Results/Estimates/inspect_estimates_{name}.xlsx')

    fit_stats=semopy.calc_stats(model_SEM)
    fit_stats_df=pd.DataFrame(fit_stats)
    fit_stats_df.to_excel(f'./SEM_Results/Fit_Stats/fit_stats_{name}.xlsx')

    g=semopy.semplot(model_SEM, f'./SEM_Results/Graphs/model_{name}.jpg', plot_covs=True)
    # In the future, remove p-values for less clutered graphs
    img=Image.open(f'./SEM_Results/Graphs/model_{name}.jpg')
    display(img)

    fit_ideal_dict = {
    #    'chi2': '0',
    #    'chi2 p-value': '>0.05',
        'RMSEA': '<0.1',
        'CFI': '>0.9',
        'GFI': '>0.9',
        'TLI': '>0.95'
    }

    fit_actual_dict = {
    #    'chi2': fit_stats_df.at['Value', 'chi2'],
    #    'chi2 p-value': fit_stats_df.at['Value', 'chi2 p-value'],  
        'RMSEA': fit_stats_df.at['Value', 'RMSEA'],  
        'CFI': fit_stats_df.at['Value', 'CFI'],
        'GFI': fit_stats_df.at['Value', 'GFI'],
        'TLI': fit_stats_df.at['Value', 'TLI']
    }

    print(f'Model Name: {name}')
    for key in fit_ideal_dict.keys():
        print(f'Ideal {key} is {fit_ideal_dict[key]}, actual is {round(fit_actual_dict[key], 2)}')

    semopy.report(model_SEM, f'./SEM_Results/Reports/model_{name}')

def string_together_labels(list_of_labels):
    if len(list_of_labels)>0:
        first_label=list_of_labels.pop(0)
        final_str=first_label
        while len(list_of_labels)>0:
            temp_label=list_of_labels.pop(0)
            final_str+=f'+{temp_label}'
    else:
        final_str=''
    return final_str

def factor_description(sum_of_labels, factor_name):
    return f'{factor_name} =~ {sum_of_labels}'

def combine_description(list_of_factor_dicts):
    final_description=''
    for temp_dict in list_of_factor_dicts:
        temp_sum_of_labels=string_together_labels(temp_dict['question_labels'])
        temp_factor_description=factor_description(temp_sum_of_labels, temp_dict['factor_name'])
        if final_description!='':
            final_description+=f'\n{temp_factor_description}'
        else:
            final_description=temp_factor_description
    return final_description