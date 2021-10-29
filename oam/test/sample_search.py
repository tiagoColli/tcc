# import sys
# sys.path.insert(0, '../../')
# import pandas as pd

# from oam.score.isolation_path import IsolationPath
# from oam.search.simple_combination import SimpleCombination


# df = pd.read_csv('../../datasets/df_outliers.csv')

# ipath = IsolationPath(
#     subsample_size=256,
#     number_of_paths=500
# )

# search = SimpleCombination(
#     ipath,
#     # min_items_per_subspace=2,
#     # max_items_per_subspace=4,
#     # dimensions=['variation_mean', 'variation_std', 'up_count',
#     #             'down_count', 'top_15_variation_mean',
#     #             'top_15_variation_std'],
#     subspaces=[
#         ['variation_std', 'down_count', 'top_15_variation_std'],
#         ['variation_mean', 'up_count', 'top_15_variation_mean']	
#     ]

# )


# search.search(df, 41)


# normalizar + ajuste de pesos