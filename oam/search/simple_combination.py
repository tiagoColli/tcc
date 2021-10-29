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
        subspaces: list = None,
        multiprocessing: bool = None
    ):
        if (
            (min_items_per_subspace or max_items_per_subspace or dimensions)
            and subspaces
        ):
            raise Exception(
                'You can either pass your desired subspaces to search '
                'from or use the parameters to generate new subspaces '
                'combining dimensions. Please pass the parameters correctly.')

        self.score_method_instance = score_method_instance
        self.min_items_per_subspace = min_items_per_subspace
        self.max_items_per_subspace = max_items_per_subspace
        self.dimension = dimensions
        self.subspaces = subspaces
        self.multiprocessing = multiprocessing

    def search(self, dataframe: pd.DataFrame, query_point: int) -> pd.DataFrame:        
        if not self.subspaces:
            self.subspaces = self._generate_subspaces()

        results = pd.DataFrame(
            columns=["subspace", "score", "subspace_size"]
        )

        if not self.multiprocessing:
            for subspace in self.subspaces:
                result_row = self._score_subspace(
                    subspace, query_point, dataframe
                )
                # Appends to the last line of the dataframe
                results.loc[len(results)] = result_row

        else:
            # Defining default arguments to the function
            partial_score_subspace = partial(
                self._score_subspace,
                query_point=query_point,
                dataframe=dataframe)
            # Copying the dataframe to every process - possible memory leak
            with futures.ProcessPoolExecutor(max_workers=2) as executor:
                for result_row in executor.map(partial_score_subspace, self.subspaces):
                    # Appends to the last line of the dataframe
                    results.loc[len(results)] = result_row

        return results.sort_values(by=['score'])

    def _generate_subspaces(self) -> list:
        # Using simple combination - all to all for every legth from min to max range
        subspaces_list = []
        for boundary in range(self.min_items_per_subspace, self.max_items_per_subspace):
            [subspaces_list.append(list(all_combinations))
                for all_combinations in combinations(self.dimension, boundary)]

        return subspaces_list

    def _score_subspace(
            self,
            subspace_dimensions: list,
            query_point: int,
            dataframe: pd.DataFrame) -> list:

        score = self.score_method_instance.score(
            dataframe[subspace_dimensions],
            query_point
        )
        logging.info(
            f"subspace {str(subspace_dimensions)} scored: {str(score)}")
        return [subspace_dimensions, score, len(subspace_dimensions)]
