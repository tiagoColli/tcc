import logging
from functools import partial
from concurrent import futures
from itertools import combinations

import pandas as pd


class SimpleCombination:
    def __init__(
        self,
        score_method_instance: int,
        min_items_per_subspace: int = None,
        max_items_per_subspace: int = None,
        dimensions: list = None,
        subspaces: list = None
    ):
        self.score_method_instance = score_method_instance
        self.min_items_per_subspace = min_items_per_subspace
        self.max_items_per_subspace = max_items_per_subspace
        self.dimension = dimensions
        self.subspaces = subspaces
        self.multiprocessing = None

    def search(self, query_point: int, dataframe: pd.DataFrame) -> pd.DataFrame:
        if not self.subspaces:
            self.subspaces = self.generate_subspaces()

        results = pd.DataFrame(
            columns=["subspace", "score", "subspace_size"]
        )

        if not self.multiprocessing:
            for subspace in self.subspaces:
                result_row = self.score_subspace(
                    query_point, dataframe, subspace
                )
                # Appends to the last line of the dataframe
                results.loc[len(results)] = result_row

        else:
            # Copying the dataframe to every process - possible memory leak
            with futures.ProcessPoolExecutor() as executor:
                # Defining default arguments to the function
                partial_score_subspace = partial(
                    self.score_subspace, query_point=query_point, dataframe=dataframe)

                for result_row in executor.map(partial_score_subspace, self.subspaces):
                    # Appends to the last line of the dataframe
                    results.loc[len(results)] = result_row

        return results.sort_values(by=['Score'])

    def generate_subspaces(self) -> list:
        # Using simple combination - all to all for every legth from min to max range
        subspaces_list = []
        for boundary in range(self.min_items_per_subspace, self.max_items_per_subspace):
            [subspaces_list.append(list(all_combinations))
                for all_combinations in combinations(self.dimension, boundary)]

        return subspaces_list

    def score_subspace(self, query_point: int, dataframe: pd.DataFrame, subspace_dimensions: list) -> list:
        score = self.score_method_instance.run(
            query_point,
            dataframe[subspace_dimensions]
        )
        logging.info(
            f"subspace {str(subspace_dimensions)} scored: {str(score)}")
        return [subspace_dimensions, score, len(subspace_dimensions)]
