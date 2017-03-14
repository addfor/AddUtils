# The MIT License (MIT)
# 
# Copyright (c) 2015 addfor s.r.l.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import numpy as np
import multiprocessing
from sklearn.metrics import mean_squared_error, accuracy_score

def reg_score(y_true, y_pred):
    return -mean_squared_error(y_true, y_pred)

def cls_score(y_true, y_pred):
    return accuracy_score(y_true, y_pred)
    
def importance(ensemble, X_train, y_train, score_func):
    n_trees = ensemble.n_estimators
    n_features = X_train.shape[1]

    ret = np.zeros((n_trees, n_features))

    for t in range(n_trees):
        dtree = ensemble.estimators_[t]
        oob_mask = np.invert(dtree.indices_)
        X_oob = X_train[oob_mask, :]
        y_oob = y_train[oob_mask]
        n_oob_samples = y_oob.shape[0]
        
        feat_indices = np.unique(dtree.tree_.feature)
        
        y_noshuffle = dtree.predict(X_oob)
        err_base = score_func(y_oob, y_noshuffle)

        X_cur = np.copy(X_oob)
        for j in feat_indices:
            if j == -2: continue
            np.random.shuffle(X_cur[:,j])
            y_shuffled = dtree.predict(X_cur)
            ret[t,j] = err_base - score_func(y_oob, y_shuffled)
            X_cur[:,j] = X_oob[:,j]
            
    return ret

   

