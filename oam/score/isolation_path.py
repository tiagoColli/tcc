import numpy
import types
import math


class IsolationPath:
    def __init__(self, subsample_size, number_of_paths):
        self.subsample_size = subsample_size
        self.number_of_paths = number_of_paths

    def score(self, dataframe, query_point_index):
        dataframe_without_query = dataframe.drop(query_point_index)
        done_paths_length = []

        for i in range(self.number_of_paths):
            subsample = self._subsample_dataframe_with_query(
                dataframe_without_query, query_point_index
            )

            done_paths_length.append(
                self._calc_path_length(subsample, len(subsample)-1)
            )

        # returns the average path
        return sum(done_paths_length)/len(done_paths_length)

    def _subsample_dataframe_with_query(self, dataframe, query_point_index):
        subsample = dataframe.sample(n=self.subsample_size-1)
        return subsample.append(dataframe.iloc[query_point_index, :])

    def _calc_path_length(self, subspace, query_point_index):
        subspace_sample = subspace.copy(deep=True)
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
                continue

            # if the subspace has no more cuts to be done, adjust the path lenth and end the loop
            if len(subspace_sample.columns) == 0:
                sample_size = len(subspace_sample)
                path_length = self._path_length_adjustment(
                    path_length, sample_size
                )
                break
            # else cut the tree
            else:
                # get a random split point in the tree
                split_point = numpy.random.uniform(
                    random_attribute.min, random_attribute.max, None
                )

                # get the query point in the `random_attribute` dimension
                query_point = subspace.loc[query_point_index,
                                           random_attribute.name]

                subspace_sample = self._cut_tree(
                    subspace_sample, split_point, query_point, random_attribute.name
                )

                path_length = path_length + 1

        del subspace_sample
        return path_length

    # draw an random attribute from the subspace
    def _get_random_attribute(self, subspace_sample):
        random_index = numpy.random.random_integers(
            low=0, high=len(subspace_sample.columns)-1, size=None)
        random_attribute = types.SimpleNamespace()
        random_attribute.name = subspace_sample.columns[random_index]
        random_attribute.max = subspace_sample[random_attribute.name].max()
        random_attribute.min = subspace_sample[random_attribute.name].min()

        return random_attribute

    # adjust the path lenth when the subspace has no more cuts to be done
    def _path_length_adjustment(self, path_length, sample_size):
        return path_length+2 * ((math.log(sample_size)+numpy.euler_gamma)-2)

    # split the subspace in the given `split_point`
    def _cut_tree(self, subspace_sample, split_point, query_point, random_attribute_name):
        if query_point < split_point:
            return subspace_sample[subspace_sample[random_attribute_name] < split_point]
        else:
            return subspace_sample[subspace_sample[random_attribute_name] >= split_point]
