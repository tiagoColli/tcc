from itertools import combinations

import pandas as pd

from IsolationPath import IsolationPath

df = pd.read_csv('../datasets/df_outliers.csv')
df.drop(columns=['Unnamed: 0', 'datetime', 'LOF_score', 'LOF_predictions'], inplace=True)

subspacesList = []
for itBoundary in range(2, 6):
    subspacesList = subspacesList + [list(x) for x in combinations(df.columns, itBoundary)]

isolationPath = IsolationPath(20, 3, debug=True)
isolationPath.setConfigurations(
    "SimpleCombination",
    subspacesList
)

queryPoint = 40

# normalData.loc[appendRowIndex] = faultyData.loc[queryPoint]
isolationPath.setDataframe(df)

df2 = isolationPath.calculateMetricForEachSubspace(
    queryPoint, defaultColumns=None)

df2.sort_values(by=['Score'])