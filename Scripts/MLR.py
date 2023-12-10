import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Load the data
file_path = 'your_data_file.csv'  # Replace with your actual file path
data = pd.read_csv(file_path)

# Reshape the data into a long format (if necessary)
melted_data = data.melt(id_vars=['Reactions'], var_name='Treatment', value_name='Value')
melted_data['Sulfate'] = melted_data['Treatment'].apply(lambda x: 'Present' if 'S+' in x else 'Absent')
melted_data['Oxygen'] = melted_data['Treatment'].apply(lambda x: 'Present' if 'O+' in x else 'Absent')

# Prepare for Multiple Linear Regression
mlr_formula = 'Value ~ Sulfate + Oxygen + Sulfate:Oxygen'
unique_reactions = melted_data['Reactions'].unique()

# Initialize a DataFrame to store the results
results_df = pd.DataFrame(columns=['Reaction', 'Sulfate_Effect', 'Sulfate_p', 'Oxygen_Effect', 'Oxygen_p', 'Interaction_Effect', 'Interaction_p'])

# Iterate over each reaction type and fit a model
for reaction in unique_reactions:
    # Filter data for the current reaction
    reaction_data = melted_data[melted_data['Reactions'] == reaction]

    # Fit the MLR model for the current reaction
    mlr_model_reaction = ols(mlr_formula, data=reaction_data).fit()

    # Extract the coefficients and p-values
    coef = mlr_model_reaction.params
    pvalues = mlr_model_reaction.pvalues

    # Append the results to the DataFrame
    results_df = results_df.append({
        'Reaction': reaction,
        'Sulfate_Effect': coef['Sulfate[T.Present]'],
        'Sulfate_p': pvalues['Sulfate[T.Present]'],
        'Oxygen_Effect': coef['Oxygen[T.Present]'],
        'Oxygen_p': pvalues['Oxygen[T.Present]'],
        'Interaction_Effect': coef['Sulfate[T.Present]:Oxygen[T.Present]'],
        'Interaction_p': pvalues['Sulfate[T.Present]:Oxygen[T.Present]']
    }, ignore_index=True)

# Save the results to a CSV file
results_csv_path = 'reaction_flux_analysis_results.csv'  # Replace with your desired path
results_df.to_csv(results_csv_path, index=False)
