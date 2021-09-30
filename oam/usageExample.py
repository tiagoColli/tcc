from IsolationPath import IsolationPath

isolationPath = IsolationPath(NUMBER_ITEMS_TREE, NUMBER_TREES)
isolationPath.setConfigurations("SimpleCombination", [relevantAttributes])

for queryPoint in pLUBPositiveSelectedIndex:
    normalData.loc[appendRowIndex] = faultyData.loc[queryPoint]
    isolationPath.setDataframe(normalData)

    sqlParameters = {
        "tableName": tableNameIPath,
        "engine": engineName
    }

    defaultColumns = {
        "queryPoint": queryPoint,
        "Alarm": True,
    }

    isolationPath.calculateMetricForEachSubspace(
        queryPoint, sqlParameters, defaultColumns=defaultColumns)
