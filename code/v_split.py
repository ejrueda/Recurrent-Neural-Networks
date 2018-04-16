# Se crea un generador "v_split" para utilizar como método de validación cruzada
def v_split(X, n_bdtrain, n_bdtest, mday):

    """"
    Hace un particionado del dataset, para tomar n_bdtrain días para entrenar
    y n_bdtest para probar, además, mday representa el paso de día a correr.
    X, dataframe, se necesita el indice de este para separar por días.
    n_bdtrain, número de bussines day utilizados para train.
    n_bdtest, número de bussines day utilizados para test.
    mday, días a correr para cada validación.
    
    """
    import pandas as pd
    import numpy as np
    from datetime import date
    start_day = 0
    
    #Divide el data set según días de train, test y cuanto se va moviendo
    bussines_day = []
    dates = pd.unique(X.index.date) #saco las fechas para luego tomar solo año-mes-día

    for i in dates: bussines_day.append(date.__format__(i,'%Y-%m-%d')) #lista de los bussines day
    
    intervals = []
    count = 0
    for i in bussines_day:
        f = len(X[i])-1 +count
        intervals.append([count,f])
        count = f+1
    
    for i in range(len(intervals)-n_bdtrain):
        yield(np.arange(intervals[start_day:start_day+n_bdtrain][0][0],
                        intervals[start_day:start_day+n_bdtrain][n_bdtrain-1][1]+1),
              np.arange(intervals[n_bdtrain+start_day:n_bdtrain+start_day+n_bdtest][0][0],
                        intervals[n_bdtrain+start_day:n_bdtrain+start_day+n_bdtest][n_bdtest-1][1]+1))
    
        start_day += mday
        if start_day+n_bdtest > len(intervals)-n_bdtrain:
            break