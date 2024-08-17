import numpy as np

class CarFuelEfficiencyPredictor:
    def __init__(self):
        self.slope = 0
        self.intercept = 0
    
    def train(self, X, y):
        """Train the model using simple linear regression."""
        X_mean = np.mean(X)
        y_mean = np.mean(y)
        
        numerator = np.sum((X - X_mean) * (y - y_mean))
        denominator = np.sum((X - X_mean)**2)
        
        self.slope = numerator / denominator
        self.intercept = y_mean - self.slope * X_mean
    
    def predict(self, X):
        """Predict L/100km for given car weights."""
        return self.slope * X + self.intercept
    
    def mean_squared_error(self, X, y):
        """Calculate the mean squared error of the model."""
        predictions = self.predict(X)
        return np.mean((y - predictions)**2)
    
    def r_squared(self, X, y):
        """Calculate the R-squared score of the model."""
        predictions = self.predict(X)
        ss_total = np.sum((y - np.mean(y))**2)
        ss_residual = np.sum((y - predictions)**2)
        return 1 - (ss_residual / ss_total)
    
