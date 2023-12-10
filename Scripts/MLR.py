import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Load and prepare the data
file_path = '/mnt/data/Modeling.csv'  # Replace with your file path
data = pd.read_csv(file_path)
melted_data = data.melt(id_vars=['Reactions'], var_name='Treatment', value_name='Value')
melted_data['Sulfate'] = melted_data['Treatment'].apply(lambda x: 'Present' if 'S+' in x else 'Absent')
melted_data['Oxygen'] = melted_data['Treatment'].apply(lambda x: 'Present' if 'O+' in x else 'Absent')
melted_data['Sulfate_Oxygen_Present'] = (melted_data['Sulfate'] == 'Present') & (melted_data['Oxygen'] == 'Present')
melted_data['Sulfate_Oxygen_Present'] = melted_data['Sulfate_Oxygen_Present'].map({True: 'Present', False: 'Absent'})

# Initialize a DataFrame to store all results
all_results_df = pd.DataFrame()

# Iterate over each reaction type and perform the analyses
unique_reactions = melted_data['Reactions'].unique()
for reaction in unique_reactions:
    # Filter data for the current reaction
    reaction_data = melted_data[melted_data['Reactions'] == reaction]

    # Fit the models
    mlr_model = ols('Value ~ Sulfate + Oxygen + Sulfate:Oxygen', data=reaction_data).fit()
    combined_effect_model = ols('Value ~ Sulfate_Oxygen_Present', data=reaction_data).fit()

    # Extract and append results
    results = {
        'Reaction': reaction,
        'Sulfate_Effect': mlr_model.params['Sulfate[T.Present]'],
        'Sulfate_p': mlr_model.pvalues['Sulfate[T.Present]'],
        'Oxygen_Effect': mlr_model.params['Oxygen[T.Present]'],
        'Oxygen_p': mlr_model.pvalues['Oxygen[T.Present]'],
        'Interaction_Effect': mlr_model.params['Sulfate[T.Present]:Oxygen[T.Present]'],
        'Interaction_p': mlr_model.pvalues['Sulfate[T.Present]:Oxygen[T.Present]'],
        'Combined_Effect': combined_effect_model.params.get('Sulfate_Oxygen_Present[T.Present]', float('nan')),
        'Combined_Effect_p': combined_effect_model.pvalues.get('Sulfate_Oxygen_Present[T.Present]', float('nan'))
    }
    all_results_df = all_results_df.append(results, ignore_index=True)

# Save the results
results_csv_path = '/mnt/data/all_inclusive_reaction_flux_analysis_results.csv'
all_results_df.to_csv(results_csv_path, index=False)
