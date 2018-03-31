def redim(signal):
    '''
    recibe un array plano el cual convierte en dos salidas,
    en una de estas se encuentran los resultados pertinentes
    a medir con el PNL y en el otro las predicciones.
    '''
    import numpy as np
    result = signal[:,0][0]
    predict = np.array(signal[:,1][0],dtype=np.float16)
    for i in range(1,len(signal)):
        result = np.concatenate((result,signal[:,0][i]))
        predict = np.concatenate((predict,signal[:,1][i]))
    result = result.reshape((len(signal),signal[:,0][0].shape[0]))
    return result, predict