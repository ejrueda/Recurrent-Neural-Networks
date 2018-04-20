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