class EUtilities:
        
    def build_dataset(self,df, window, binary_target=False, delete_constant_values=True, PNL=False):
        """
        función para construir un data set
        window: tamaño de la ventana a utilizar para construir el dataset
        df: dataframe, con columna bid y ask.
        binary_target: si desea clasificar, este arroja 2 si el valor se mantiene,
        1 si el valor sube y 0 si este baja.
        delete_constant_values: default: True, elimina los valores que se mantienen

        retorna:
        X: dataset, con columna de PNL si así se especifica(default: False)
        y: target
        bt: binary target, default: False
        """

        import pandas as pd
        import numpy as np
        result = []
        binary = [] #para la columna objetivo binaria
        pnl_buy = [] #almacenar el pnl en caso de compra
        pnl_sell = [] #almacenar el pnl en caso de venta
        signal = df.bid
        ask = df.ask
        indx = signal.index[window-1:-1] #se toman los indicen que quedarán al final
        for i in range(len(signal)-window):

            if delete_constant_values == True:
                if signal[i+window] != signal[i+window-1]:

                    result.append(signal[i: i + window+1])
                    if PNL == True: 
                        pnl_sell.append(signal[i+window-1] - ask[i+window]) #calcular pnl en caso de venta-compra
                        pnl_buy.append(signal[i+window] - ask[i+window-1]) #calcular pnl en caso de compra-venta

                    if binary_target == True:
                        if signal[i+window] < signal[i+window-1]: binary.append(0) # 0 si baja
                        if signal[i+window] > signal[i+window-1]: binary.append(1) # 1 si sube

                else: indx = indx.delete(len(result))

            else:

                result.append(signal[i: i + window+1])
                if PNL == True:
                    pnl_sell.append(signal[i+window-1] - ask[i+window]) #calcular pnl en caso de venta-compra
                    pnl_buy.append(signal[i+window] - ask[i+window-1]) #calcular pnl en caso de compra-venta

            if binary_target == True and delete_constant_values == False:
                if signal[i+window] == signal[i+window-1]: binary.append(2) # 2 si se mantiene
                if signal[i+window] < signal[i+window-1]: binary.append(0) # 1 si baja
                if signal[i+window] > signal[i+window-1]: binary.append(1) # 0 si sube

        data = pd.DataFrame(np.array(result), index=indx)
        y = np.array(data.iloc[:,window])
        data = data.drop(window,axis=1)
        if PNL == True:
            data['PNL_0'] = pnl_sell
            data['PNL_1'] = pnl_buy 
        if binary_target == True: return data, y, np.array(binary)
        else: return data, y
    
    #para crear señales multiples
    
    def multi_signal(self,s_A, s_B):
        """
        dada dos señales s_A y s_B, se obtiene una multiseñal donde la
        señal que predomina para la contrucción es s_A
        """
        import pandas as pd
        import numpy as np
        #saco los valores que si están en el mismo instante de tiempo
        #se filtra la señal s_B por los indices que tiene s_A
        values = s_B.filter(items=s_A.index, axis=0)
        #inserto una columa llena de ceros para posteriormente colocar ahi los valores a utilizar
        s_A.insert(loc=2, column=s_B.columns[0]+'new', value=np.zeros((s_A.shape[0],1)))
        #llenamos con los datos
        s_A.loc[values.index,s_B.columns[0]+'new'] = values.loc[values.index,values.columns[0]]
        #llenamos los ceros
        s_A.loc[s_A.loc[s_A.index,s_B.columns[0]+'new']==0, s_B.columns[0]+'new'] = s_A.loc[s_A.loc[s_A.index,s_B.columns[0]+'new']==0,s_A.columns[0]]

        return s_A

    #redimensionar la salida del score
    
    def redim(self,signal):
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

   #para hacer una validación por pasos
    
    def step_validation(self,estimator, X, y, cv):
        '''
        Recibe el estimador,X,y, y un generador cv con el cual hace la validación
        dependiendo que la configuración que este tenga
        '''
        import numpy as np
        result = []
        for index in cv:
            estimator.fit(X.iloc[index[0]], y[index[0]])
            result.append(estimator.score(X.iloc[index[1]], y[index[1]]))
        return np.array(result)

    #particiona el dataset para sacar los indices para la validación por pasos
    
    def v_split(self,X, n_bdtrain, n_bdtest, mday):

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
