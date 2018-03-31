def step_validation(estimator, X, y, cv):
    '''
    Recibe el estimador,X,y, y un generador cv con el cual hace la validación
    dependiendo que la configuración que este tenga
    '''
    import pandas as pd
    import numpy as np
    result = []
    for index in cv:
        estimator.fit(X.iloc[index[0]], y[index[0]])
        result.append(estimator.score(X.iloc[index[1]], y[index[1]]))
    return np.array(result)