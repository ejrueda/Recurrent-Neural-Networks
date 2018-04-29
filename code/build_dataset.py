# %load ../code/build_dataset.py
def build_dataset(df, window, binary_target=False, delete_constant_values=True, PNL=False):
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
                    if signal[i+window] < signal[i+window-1]: 
                        if (signal[i+window-1] - ask[i+window]) > 0: binary.append(0) # 0 si baja y gano
                        else: binary.append(2) # 2 si baja pero pierdo
                            
                    if signal[i+window] > signal[i+window-1]: # 1 si sube
                        if (signal[i+window] - ask[i+window-1]) > 0: binary.append(1) # 1 si sube y gano
                        else: binary.append(3) # 3 si sube pero pierdo
                        
            else: indx = indx.delete(len(result))
                
        else:

            result.append(signal[i: i + window+1])
            if PNL == True:
                pnl_sell.append(signal[i+window-1] - ask[i+window]) #calcular pnl en caso de venta-compra
                pnl_buy.append(signal[i+window] - ask[i+window-1]) #calcular pnl en caso de compra-venta
            
        if binary_target == True and delete_constant_values == False:
            if signal[i+window] == signal[i+window-1]: binary.append(4) # 2 si se mantiene
                
            if signal[i+window] < signal[i+window-1]:
                if (signal[i+window-1] - ask[i+window]) > 0: binary.append(0) # 0 si baja y gano
                else: binary.append(2) # 2 si baja pero pierdo
                    
            if signal[i+window] > signal[i+window-1]:
                if (signal[i+window] - ask[i+window-1]) > 0: binary.append(1) # 1 si sube y gano
                else: binary.append(3) # 3 si sube pero pierdo
    
    data = pd.DataFrame(np.array(result), index=indx)
    y = np.array(data.iloc[:,window])
    data = data.drop(window,axis=1)
    if PNL == True:
        data['PNL_0'] = pnl_sell
        data['PNL_1'] = pnl_buy 
    if binary_target == True: return data, y, np.array(binary)
    else: return data, y