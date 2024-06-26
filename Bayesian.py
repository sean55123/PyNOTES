import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import os 
import csv

class GaussianProcess:
    def __init__(self, kernel, noise=1e-10):
        self.kernel = kernel
        self.noise = noise

    def fit(self, X_train, y_train):
        self.X_train = np.atleast_2d(X_train)
        self.y_train = y_train.reshape(-1, 1)
        self.K = self.kernel(self.X_train, self.X_train) + self.noise * np.eye(len(self.X_train))
        self.K_inv = np.linalg.inv(self.K)

    def predict(self, X):
        X = np.atleast_2d(X)
        K_trans = self.kernel(X, self.X_train)
        y_mean = K_trans.dot(self.K_inv).dot(self.y_train)
        K_self = self.kernel(X, X) + self.noise * np.eye(len(X))
        y_var = K_self - K_trans.dot(self.K_inv).dot(K_trans.T)
        return y_mean, np.diag(y_var).reshape(-1, 1)

def rbf_kernel(X1, X2, length_scale=1.0, variance=1.0):
    X1 = np.atleast_2d(X1)
    X2 = np.atleast_2d(X2)
    sqdist = np.sum(X1**2, axis=1).reshape(-1, 1) + np.sum(X2**2, axis=1) - 2 * np.dot(X1, X2.T)
    return variance * np.exp(-0.5 / length_scale**2 * sqdist)

def expected_improvement(X, X_sample, model, xi):
    X = np.atleast_2d(X)
    mu, sigma = model.predict(X)
    mu_sample, _ = model.predict(X_sample)
    
    mu_sample_opt = np.min(mu_sample)
    
    with np.errstate(divide='warn'):
        imp = mu_sample_opt - mu - xi
        Z = imp / sigma
        ei = imp * norm.cdf(Z) + sigma * norm.pdf(Z)
        ei[sigma == 0.0] = 0.0
    
    return ei

def propose_location(acquisition, X_sample, Y_sample, model, xMax, xMin, decimal, xi, n_restarts=25):
    best_x = None
    best_acq_value = -np.inf
    
    for _ in range(n_restarts):
        x_random = np.array([np.round(np.random.uniform(xMin[j], xMax[j], size=(1,)), decimal[j]) for j in range(len(xMin))]).reshape(1, -1)
        acq_value = acquisition(x_random, X_sample, model, xi)
        
        if acq_value > best_acq_value:
            best_x = x_random
            best_acq_value = acq_value
            
    return best_x

def Record(n, params, score, name, wbpath, data_label):
    value = [n] + list(params) + [score]
    if os.path.isfile(wbpath):
        with open(name, 'a+', newline = '') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(value)
    else:
        with open(name, 'a+', newline = '') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data_label)
            writer.writerow(value)

def optimize(n_iterations, xMax, xMin, decimal, objective_function, model, csv_filename, wbpath, data_label):
    csv_filename += '.csv'
    wbpath += '.csv'
    xi_initial = 1
    X_init = np.array(list(map(lambda x, y, z: np.round(np.random.uniform(x, y), z), xMax, xMin, decimal)))
    X_init = np.atleast_2d(X_init)
    Y_init = np.float64(objective_function(X_init[0]))

    X_best = np.inf
    Y_best = np.inf
    model.fit(X_init, Y_init)

    for i in range(n_iterations):
        xi = xi_initial * (0.5 ** (i / (n_iterations // 2)))
        X_next = propose_location(expected_improvement, X_init, Y_init, model, xMax, xMin, decimal, xi)
        
        Y_next = np.float64(objective_function(X_next[0])) 

        X_init = np.vstack((X_init, X_next))
        Y_init = np.vstack((Y_init, Y_next))

        model.fit(X_init, Y_init)
       
        if Y_next < Y_best:
            X_best = X_next
            Y_best = Y_next    
        print('-----------------------------------------') 
        print(f"Iteration {i + 1}: Current trial = {X_next[0]}, Current score = {Y_next}")
        Record(i+1, X_best[0], Y_best, csv_filename, wbpath, data_label)
    
    print('-----------------------------------------')
    print('BO ended!')
    print("Final recommendation:", X_best[0])
    print("Final results:", Y_best)
    return Y_best