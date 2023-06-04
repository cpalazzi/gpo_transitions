# %%
import os
import glob
import pandas as pd
import re
import seaborn as sns

# %%
files = [i for i in glob.glob(f'*.xlsx')]

# %%
result = {'demand_factor':[] ,'LCOA':[]}
for file in files: 
    # read in the file, you may need to specify some extra parameters
    # check the pandas docs for read_csv
    df = pd.read_excel(file,sheet_name='headline_figures',index_col='Parameter')

    # now select the value you want
    # this will vary depending on what your indexes look like (if any)
    # and also your column names
    value = df.loc['Total']['Cost per ton']

    # append to the list
    s = file
    demand_factor = re.search('factor_(.*?)_', s).group(1)
    result['demand_factor'].append(demand_factor)
    result['LCOA'].append(value)

# you should now have a list in the format:
# [('2021-09-13_13-42-16.csv', 100), ('2021-09-13_13-42-22.csv', 255), ...

# load the list of tuples as a dataframe for further processing or analysis...
result_df = pd.DataFrame(result).set_index('demand_factor').sort_index()
# %%
sns.lineplot(
    data=result_df,
    x='demand_factor',
    y='LCOA'
)
# %%
