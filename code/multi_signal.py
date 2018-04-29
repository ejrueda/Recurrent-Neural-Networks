def multi_signal(s_A, s_B, new_col):
    """
    dada dos señales s_A y s_B, se obtiene una multiseñal donde la
    señal que predomina para la contrucción es s_A
    new_col, par darle nombre a la nueva columna
    """
    import numpy as np
    import pandas as pd
    #saco los valores que si están en el mismo instante de tiempo
    #se filtra la señal s_B por los indices que tiene s_A
    values = s_B.filter(items=s_A.index, axis=0)
    #inserto una columna llena de ceros para posteriormente colocar ahi los valores a utilizar
    s_A.insert(loc=2, column=new_col, value=np.zeros((s_A.shape[0],1)))
    #llenamos con los datos
    s_A.loc[values.index,new_col] = values.loc[values.index,values.columns[0]]
    #llenamos los ceros
    s_A.loc[s_A.loc[s_A.index,new_col]==0, s_B.new_col] = s_A.loc[s_A.loc[s_A.index,new_col]==0,s_A.columns[0]]
    
    return s_A