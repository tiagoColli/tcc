import math
import types
import pandas as pd
import numpy


class IsolationPath:
    def __init__(self, subsample_size: int, number_of_paths: int):
        self.subsample_size = subsample_size
        self.number_of_paths = number_of_paths

    def score(self, dataframe: pd.DataFrame, query_point_index: int) -> float:
        ''' A function to score a query in a given subspace.

            It performs a binary search in the subspace represented in `dataframe` 
            in search of the object of the informed `query_point_index` position. When it 
            manages to isolate the object, it returns a score that represents the 
            length of the path to isolate the query.

            Args:
                *dataframe* (pd.DataFrame): Dataframe used to build the path tree.

                *query_point_index* (int): Index of the query which you want to calculate the path length.

            Returns:
                *float*: Returns the subspace score. '''
        done_paths_length = []

        for _ in range(self.number_of_paths):
            subsample = self._subsample_dataframe_with_query(
                dataframe, query_point_index
            )

            done_paths_length.append(
                self._calc_path_length(subsample, len(subsample)-1)
            )

        # returns the average path length
        return sum(done_paths_length)/len(done_paths_length)

    def _subsample_dataframe_with_query(
            self,
            dataframe: pd.DataFrame,
            query_point_index: int) -> pd.DataFrame:
        # sample the dataframe without the query
        dataframe_without_query = dataframe.drop(query_point_index)
        subsample = dataframe_without_query.sample(n=self.subsample_size-1)
        # adds it again to ensure its existance
        return subsample.append(dataframe.loc[query_point_index])

    def _calc_path_length(self, subspace: pd.DataFrame, query_point_index: int) -> int:
        subspace_sample = subspace.copy(deep=True)
        subspace_sample.reset_index(drop=True, inplace=True)
        path_length = 0

        # while query points is not isolated yet
        while len(subspace_sample) > 1:
            random_attribute = self._get_random_attribute(
                subspace_sample
            )

            # if the attribute can't be cut anymore, remove it
            if random_attribute.max == random_attribute.min:
                subspace_sample = subspace_sample.drop(
                    random_attribute.name, axis=1
                )

                # if no attributes are left, adjust the path length and end the loop
                if len(subspace_sample.columns) == 0:
                    sample_size = len(subspace_sample)
                    path_length = self._path_length_adjustment(
                        path_length, sample_size
                    )
                    break
                continue

            subspace_sample = self._cut_tree(
                subspace_sample, random_attribute, query_point_index
            )

            path_length = path_length + 1

        del subspace_sample
        return path_length

    def _get_random_attribute(self, subspace_sample: pd.DataFrame) -> types.SimpleNamespace:
        ''' get an random attribute from the subspace and return
        its metadata'''

        random_index = numpy.random.random_integers(
            low=0,
            high=len(subspace_sample.columns)-1,
            size=None
        )

        random_attribute = types.SimpleNamespace()
        random_attribute.name = subspace_sample.columns[random_index]
        random_attribute.max = subspace_sample[random_attribute.name].max()
        random_attribute.min = subspace_sample[random_attribute.name].min()
        return random_attribute

    def _path_length_adjustment(self, path_length: int, sample_size: int) -> float:
        '''apply euler correction to the path lenth when there's no
        subspace left'''

        return path_length+2 * ((math.log(sample_size)+numpy.euler_gamma)-2)

    def _cut_tree(
            self,
            subspace_sample: pd.DataFrame,
            random_attribute: types.SimpleNamespace,
            query_point_index: int) -> pd.DataFrame:
        '''make a random cut in the rows - get a random value in the
        dataframe and keeps all the lower or greater values, depending on
        the query_point sits'''

        # get a random split point in the tree
        split_point = numpy.random.uniform(
            random_attribute.min, random_attribute.max, None
        )

        # get the query point in the `random_attribute` dimension
        query_point = subspace_sample.loc[query_point_index,
                                          random_attribute.name]

        if query_point < split_point:
            return subspace_sample[subspace_sample[random_attribute.name] < split_point]
        else:
            return subspace_sample[subspace_sample[random_attribute.name] >= split_point]
