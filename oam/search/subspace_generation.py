from itertools import combinations

class SubspacesGeneration:
    def __init__(self):
        pass

    def generateSubspaces(self, generationMethod, **kwargs):
        if generationMethod == "SimpleCombination":
            return self.generateSubspacesBySimpleCombination(kwargs["attributesList"], kwargs["minItemsPerSubspace"], kwargs["maxItemsPerSubspace"])
        else:
            raise Exception('Metodo nao encontrado')

    def generateSubspacesBySimpleCombination(self, attributesList, minItemsPerSubspace, maxItemsPerSubspace):
        subspacesList = []
        for itBoundary in range(minItemsPerSubspace, maxItemsPerSubspace):
            subspacesList = subspacesList + \
                [list(x) for x in combinations(attributesList, itBoundary)]
        return subspacesList
