def multi_signal(s_A, s_B):
    """
    dada dos señales s_A y s_B, se obtiene una multiseñal donde la
    señal que predomina para la contrucción es s_A
    """
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