# Preparing the script as a string
script = """
import pandas as pd
import statsmodels.formula.api as smf

# Load the dataset
file_path = 'path_to_your_file.csv'
data = pd.read_csv(file_path)

# Transform the data to long format
df_long = pd.melt(data, id_vars=['Reactions'], var_name='Treatment', value_name='Value')

# Determine sulfate and oxygen presence
df_long['Sulfate'] = df_long['Treatment'].apply(lambda x: 'S+' in x)
df_long['Oxygen'] = df_long['Treatment'].apply(lambda x: 'O+' in x)

# Function to run mixed-effects model for each reaction
def run_mixed_model_for_reaction(reaction_data):
    model = smf.mixedlm("Value ~ Sulfate * Oxygen", reaction_data, groups=reaction_data["Reactions"])
    model_fit = model.fit()
    results = model_fit.params
    pvalues = model_fit.pvalues
    return results, pvalues

# Get unique reactions
reaction_names = data['Reactions'].unique()

# Run model for each reaction
mixed_effects_results = {}
for reaction in reaction_names:
    reaction_data = df_long[df_long['Reactions'] == reaction]
    mixed_effects_results[reaction] = run_mixed_model_for_reaction(reaction_data)

# Process the results
mixed_effects_summary = {}
for reaction, (coef, pval) in mixed_effects_results.items():
    mixed_effects_summary[reaction] = {
        'Effect of Sulfate': {'Effect Size': coef['Sulfate[T.True]'], 'P-value': pval['Sulfate[T.True]']},
        'Effect of Oxygen': {'Effect Size': coef['Oxygen[T.True]'], 'P-value': pval['Oxygen[T.True]']},
        'Combined Effect': {'Effect Size': coef['Sulfate[T.True]:Oxygen[T.True]'], 'P-value': pval['Sulfate[T.True]:Oxygen[T.True]'}
    }

# Convert to DataFrame
mixed_effects_df = pd.DataFrame(mixed_effects_summary).stack().apply(pd.Series)

# Save to CSV
output_csv_path = 'your_output_path.csv'
mixed_effects_df.to_csv(output_csv_path)
"""

# Writing the script to a text file
script_file_path = '/mnt/data/mixed_effects_model_analysis_script.py'
with open(script_file_path, "w") as file:
    file.write(script)

script_file_path
