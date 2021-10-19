from itertools import combinations

import pandas as pd

from oam.score.isolation_path import IsolationPath
from search.simple_combination import SimpleCombination


df = pd.read_csv('../datasets/df_outliers.csv')
df.drop( # drop indexes and OD columns
    columns=['Unnamed: 0', 'datetime', 'LOF_score', 'LOF_predictions'],
    inplace=True
)

# Creating subspaces
subspacesList = [] 
for itBoundary in range(2, 6):
    subspacesList = subspacesList + [list(x) for x in combinations(df.columns, itBoundary)]

isolationPath = IsolationPath(20, 3, debug=True) # random metaparameters
isolationPath.setConfigurations(
    "SimpleCombination",
    subspacesList
)

queryPoint = 40 # index of the row to be OAM

isolationPath.setDataframe(df)
output_df = isolationPath.calculateMetricForEachSubspace(
    queryPoint, defaultColumns=None
)

output_df.sort_values(by=['Score'])