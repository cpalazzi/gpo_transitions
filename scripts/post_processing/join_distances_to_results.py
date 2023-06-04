import pandas as pd
from openpyxl import load_workbook

results_filepath = '/Users/carlopalazzi/Programming/shipping_sprint/gpo_transitions/results/aviation/2050_4.5_f1_aviation_4000sup.xlsx'
distances_filepath = '/Users/carlopalazzi/Programming/shipping_sprint/gpo_transitions/Global_Port_Optimisation/Ammonia Cost Data/c_port_port_distance.csv'
results = pd.read_excel(results_filepath, sheet_name='offshore_transport_t')
distances = pd.read_csv(distances_filepath)

# Perform the merge
merged_df = results.merge(distances, left_on=['Supplier', 'Recipient'], right_on=['from_name', 'to_name'], how='left')

# Select the desired columns
desired_columns = results.columns.tolist() + ['distance']
merged_df = merged_df[desired_columns]

with pd.ExcelWriter(
    results_filepath,
    mode='a',
    engine='openpyxl',
    if_sheet_exists='replace',
) as writer:
    merged_df.to_excel(writer, sheet_name='offshore_transport_t', index=False) 