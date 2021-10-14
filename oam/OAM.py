import os
import time
import logging
import threading

import numpy
import pandas
from sqlalchemy import create_engine

from concurrent import futures
from SubspacesGeneration import SubspacesGeneration


class OAM:

    def __init__(self, **kwarg):
        self.subspaceGenerationParameters = {
            "minItemsPerSubspace": 2,
            "maxItemsPerSubspace": 6,
            "beamWidth": 10
        }

        if("subspaceGenerationParameters" in kwarg):
            self.subspaceGenerationParameters.update(
                kwarg["subspaceGenerationParameters"])

        if "debug" not in kwarg:
            self.debug = False

        else:
            self.debug = kwarg["debug"]

        if "maxRowsResultDataframe" not in kwarg:
            self.maxRowsResultDataframe = 1000

        else:
            self.maxRowsResultDataframe = kwarg["maxRowsResultDataframe"]

        self.lock = threading.Lock()
        logging.basicConfig(level=logging.DEBUG)
        pass

    def setDataframe(self, newDataframe):
        # garante que o index estara certo (quando dataframes sao adicionados, o indice nem sempre eh atualizado)
        self.originalDataframe = newDataframe.reset_index(drop=True)

    def runMethod(self, queryPointIndex, dataframe):
        return numpy.NaN

    def resetMetrics(self):
        self.oamElapsedTime = None
        pass

    def setConfigurations(self, calculationStrategy, subspaces=None):
        if subspaces is None:
            self.subspacesGeneration = SubspacesGeneration()
            self.subspaces = self.subspacesGeneration.generateSubspaces(
                calculationStrategy,
                attributesList=self.originalDataframe.columns,
                minItemsPerSubspace=self.subspaceGenerationParameters["minItemsPerSubspace"],
                maxItemsPerSubspace=self.subspaceGenerationParameters["maxItemsPerSubspace"]
            )

        else:
            self.subspaces = subspaces
        self.calculationStrategy = calculationStrategy

    def calculateMetricForEachSubspace(self, queryPoint, storeToSql={}, **kwarg):
        if kwarg["defaultColumns"] is None:
            self.results = pandas.DataFrame(
                columns=["AttributesCombination", "Score", "NumberAttributes"])
            self.defaultColumns = None

        else:
            self.results = pandas.DataFrame(columns=[
                                            "AttributesCombination", "Score", "NumberAttributes"] + list(kwarg["defaultColumns"].keys()))
            self.defaultColumns = kwarg["defaultColumns"]

        if len(storeToSql) != 0:
            storeToSql["sqlEngine"] = create_engine(
                'sqlite:///' + storeToSql["engine"], echo=False)

        startExecution = time.process_time()

        if self.calculationStrategy == "SimpleCombination":
            self.results = self.calculateMetricUsingSimpleCombination(
                queryPoint, self.results, storeToSql)

        elif self.calculationStrategy == "BeamSearch":
            self.results = self.calculateMetricUsingBeamSearch(
                queryPoint, self.results, storeToSql)

        self.oamElapsedTime = time.process_time() - startExecution

        return self.results

    def calculateMetricUsingSimpleCombination(self, queryPoint, results, storeToSql={}):
        # self.executionTime=[0,0]
        # Em debug nao usa multiprocessos

        if self.debug == True:

            # Se nao tem parametros para SQL, retorna dados em memoria
            if len(storeToSql) == 0:
                for result in map(self.calculateMetric, [{"queryPoint": queryPoint, "attributes": itSubspace} for itSubspace in self.subspaces]):
                    results.loc[len(results)] = result
                    print("Salvou o subspaco " + str(result[0]))

            # Salva em SQL
            else:
                for result in map(self.calculateMetric, [{"queryPoint": queryPoint, "attributes": itSubspace} for itSubspace in self.subspaces]):
                    results.loc[len(results)] = result
                    print("Salvou o subspaco " + str(result[0]))

                    # a cada maxRowsResultDataframe, salva no banco e apaga linhas do dataframe
                    if len(results) > self.maxRowsResultDataframe:
                        results.to_sql(
                            storeToSql["tableName"], con=storeToSql["sqlEngine"], if_exists='append')
                        results.drop(results.index, inplace=True)
                        print("Limpou tabela de resultados")

                # se sobrou alguma coisa, salva tambem
                if len(results) > 0:
                    results.to_sql(
                        storeToSql["tableName"], con=storeToSql["sqlEngine"], if_exists='append')

                    results.drop(results.index, inplace=True)

        # Com multiprocessos
        else:
            if len(storeToSql) == 0:
                with futures.ThreadPoolExecutor(max_workers=8) as executor:
                    for result in executor.map(self.calculateMetric, [{"queryPoint": queryPoint, "attributes": itSubspace} for itSubspace in self.subspaces]):
                        logging.info("Salvou o subspaco " + str(result[0]))
                        results.loc[len(results)] = result

            else:
                with futures.ThreadPoolExecutor(max_workers=8) as executor:
                    for result in executor.map(self.calculateMetric, [{"queryPoint": queryPoint, "attributes": itSubspace} for itSubspace in self.subspaces]):
                        results.loc[len(results)] = result
                        logging.info("Salvou o subspaco " + str(result[0]))

                        # a cada maxRowsResultDataframe, salva no banco e apaga linhas do dataframe
                        if len(results) > self.maxRowsResultDataframe:
                            results.to_sql(
                                storeToSql["tableName"], con=storeToSql["sqlEngine"], if_exists='append')

                            results.drop(results.index, inplace=True)
                            logging.info("Limpou tabela de resultados")

                    # se sobrou alguma coisa, salva tambem
                    if len(results) > 0:
                        results.to_sql(
                            storeToSql["tableName"], con=storeToSql["sqlEngine"], if_exists='append')
                        results.drop(results.index, inplace=True)

        # print(self.executionTime[0])
        # print(self.executionTime[1])
        # print(self.executionTime[0]/self.executionTime[1])
        return results

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

        # startExecution = time.process_time()
        # metric = self.runMethod(args["queryPoint"],self.originalDataframe[args["attributes"]])
        # self.executionTime[0] += (time.process_time() - startExecution)
        # self.executionTime[1] += 1
        # return [str(args["attributes"]), metric, len(args["attributes"])]+list(self.defaultColumns.values())
