import pandas as pd
import numpy as np
class PNLEstimatorWrapper:
    
    def __init__(self, estimator, PNL_column, exclude_PNL_column_from_training=True):
        self.estimator = estimator
        self.PNL_column = PNL_column
        self.exclude_PNL_column_from_training = exclude_PNL_column_from_training
        
    def fit(self, X, y):
        assert 'PNL_1' and 'PNL_0' in X.columns, "column "+self.PNL_column+" not in X dataframe"
        if self.exclude_PNL_column_from_training:
            X = X[[col for col in X.columns if col!=self.PNL_column[0] and col!=self.PNL_column[1]]]
        self.estimator.fit(X,y)
        
    def predict(self, X):
        assert 'PNL_1' and 'PNL_0' in X.columns, "column "+self.PNL_column+" not in X dataframe"
        if self.exclude_PNL_column_from_training:
            X = X[[col for col in X.columns if col!=self.PNL_column[0] and col!=self.PNL_column[1]]]
        return self.estimator.predict(X)
    
    def score(self, X, y):
        pnl_1 = X.PNL_1
        pnl_0 = X.PNL_0
        pre = self.predict(X)
        r = sum((pre==1)*pnl_1 + (pre==0)*pnl_0)
        sell = sum(pre==0) + sum(pre==2)
        buy = sum(pre==1) + sum(pre==3)
        #percent_0 = np.mean(y==pre)*100
        percent_1 = np.mean((pre==1)*(y==1)) # si sube y gano
        percent_0 = np.mean((pre==0)*(y==0)) # si baja y gano
        percent_3 = np.mean((pre==3)*(y==3)) # si sube y pierdo
        percent_2 = np.mean((pre==2)*(y==2)) # si baja y pierdo
        
        count_ones, count_zeros = 0,0
        l_one, l_zero = [],[]
        for i in pre:
            if i==1:
                l_zero.append(count_zeros)
                count_zeros = 0
                count_ones += 1
            else:
                l_one.append(count_ones)
                count_zeros += 1
                count_ones = 0
        l_zero.append(count_zeros)
        l_one.append(count_ones)
        
        #return np.array([r,buy,sell,max(l_one),max(l_zero)])
        return np.array([r,buy,sell,max(l_one),max(l_zero),percent_1,percent_0,percent_3,percent_2]), pre
        
    def get_params(self, deep=False):
        return {"PNL_column": self.PNL_column,
                "exclude_PNL_column_from_training": self.exclude_PNL_column_from_training,
                "estimator": self.estimator}