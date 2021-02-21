from scipy.stats import beta 
import numpy as np

def beta_dist_estimator(data):
        
    if not data.empty:
    
        x = data.Age.value_counts(dropna=False).sort_index()
        z = x/np.sum(x)

        a1, b1, loc1, scale1 = beta.fit(z, floc=0, fscale=1)
        
        return a1, b1, loc1, scale1
