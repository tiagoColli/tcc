
import time
import math
import datetime

import pandas
import numpy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from OAM import OAM


class IsolationPath(OAM):
    def __init__(self, subsampleRate, numberPaths, **kwargs):
        super(IsolationPath, self).__init__(**kwargs)
        self.subsampleRate = subsampleRate
        self.numberPaths = numberPaths
        self.averagePathLength = 0
        self.allPathsLength = []

    def resetMetrics(self):
        super().resetMetrics()
        self.averagePathLength = 0
        self.allPathsLength = []
        self.averageEvolution = []
        pass

    def calculatePath(self, orignalDataframe, queryPointIndex):
        subspace = orignalDataframe.copy(deep=True)
        subspace *= 10**5
        subspace = subspace[subspace.columns[:len(subspace)]].astype("int32")

        # garante que o index estara certo (quando dataframes sao adicionados, o indice nem sempre eh atualizado)
        subspace = subspace.reset_index(drop=True)

        # contador de divisoes
        isolationPath = 0

        while True:
            # Conseguiu isolar o ponto de interesse?
            if(len(subspace) <= 1):
                break

            # Sorteia um atributo
            randomAttributeIndex = numpy.random.random_integers(
                low=0, high=len(subspace.columns)-1, size=None)
            randomAttributeName = subspace.columns[randomAttributeIndex]
            attributeMax = subspace[randomAttributeName].max()
            attributeMin = subspace[randomAttributeName].min()

            if attributeMin == attributeMax:
                # Remove o atributo
                subspace = subspace.drop(randomAttributeName, axis=1)
                # Se nao for o ultimo atributo, volta para a fase de sorteio. Se for, aplica um fator de correcao e termina
                if len(subspace.columns) == 0:
                    isolationPath = isolationPath+2 * \
                        (math.log(len(subspace))+numpy.euler_gamma)-2
                    break
                continue

            # Ponto de partiÃ§Ã£o da Ã¡rvore
            intersectionPoint = numpy.random.uniform(
                attributeMin, attributeMax, None)

            # Valor do atributo para o objeto de interesse
            objectValue = subspace.loc[queryPointIndex, randomAttributeName]
            if objectValue < intersectionPoint:
                subspace = subspace[subspace[randomAttributeName]
                                    < intersectionPoint]

            else:
                subspace = subspace[subspace[randomAttributeName]
                                    >= intersectionPoint]
            isolationPath = isolationPath+1

        del subspace
        return isolationPath

    def runMethod(self, queryPointIndex, dataframe):
        dataframeWithoutQueryPoint = dataframe.drop(queryPointIndex)
        allPathsLength = []
        startExecution = time.process_time()

        for i in range(self.numberPaths):
            # Faz a subamostragem do conjunto de dados e adiciona o objeto de interesse
            subsampled = dataframeWithoutQueryPoint.sample(
                n=self.subsampleRate-1)
                
            subsampled = subsampled.append(dataframe.iloc[queryPointIndex, :])
            # Calcula o caminho para esse conjunto de dados submostrados.
            # O objeto de interesse Ã© sempre o Ãºltimo da dataframe
            allPathsLength.append(self.calculatePath(
                subsampled, len(subsampled)-1))

        # media dos caminhos
        averagePath = sum(allPathsLength)/len(allPathsLength)

        # media em cada etapa
        # self.averageEvolution=[sum(self.allPathsLength[:it+1])/(it+1) for it in range(len (self.allPathsLength))]
        # print(time.process_time() - startExecution)

        return averagePath

    # def plotResult(self):
    #     plt.plot(self.allPathsLength, color='y',label='Comprimento dos caminhos')
    #     plt.plot(self.averageEvolution, color='r', linestyle=':',label='EvoluÃ§Ã£o da mÃ©dia')
    #     plt.axhline(y=self.averagePath, color='b', linestyle='dashed',label='MÃ©dia')
    #     plt.legend(loc='upper right')
    #     plt.show()
