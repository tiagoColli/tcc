import time

import pandas as pd


class BeamSearch:
    def __init__(
        self,
        score_method_instance,
        min_items_per_subspace,
        max_items_per_subspace,
        dimensions,
        subspaces
    ) -> None:
        self.score_method_instance = score_method_instance
        self.min_items_per_subspace = min_items_per_subspace
        self.max_items_per_subspace = max_items_per_subspace
        self.dimension = dimensions
        self.subspaces = subspaces

    def calculateMetricForEachSubspace(self, queryPoint, storeToSql={}, **kwarg):
        self.results = pd.DataFrame(
            columns=["AttributesCombination", "Score", "NumberAttributes"]
        )

        startExecution = time.process_time()

        self.results = self.calculateMetricUsingBeamSearch(
            queryPoint, self.results, storeToSql)

        self.oamElapsedTime = time.process_time() - startExecution

        return self.results

    def calculateMetricUsingBeamSearch(self, queryPoint, results, storeToSql={}):
        for itNumberAttributes in range(2, self.subspaceGenerationParameters["maxItemsPerSubspace"]):
            subspaces = []

            if itNumberAttributes == 1 or itNumberAttributes == 2:
                subspaces = self.subspacesGeneration.generateSubspacesByBeamSearch(
                    self.originalDataframe.columns.tolist(),
                    itNumberAttributes,
                    self.subspaceGenerationParameters["beamWidth"],
                    None
                )

            else:

                subspaces = self.subspacesGeneration.generateSubspacesByBeamSearch(
                    self.originalDataframe.columns.tolist(),
                    itNumberAttributes,
                    self.subspaceGenerationParameters["beamWidth"],
                    results[results["NumberAttributes"] == itNumberAttributes -
                            1].sort_values(by=['Score'])["AttributesCombination"].tolist()
                )

            for itSubspace in subspaces:
                self.resetMetrics()
                metric = self.runMethod(
                    queryPoint, self.originalDataframe[itSubspace])
                results.loc[len(results)] = [itSubspace,
                                             metric, len(itSubspace)]

        return results

    def calculateMetric(self, args):
        print(f'{str(args["attributes"])}\n')
        metric = self.runMethod(
            args["queryPoint"], self.originalDataframe[args["attributes"]])
        return [str(args["attributes"]), metric, len(args["attributes"])]
