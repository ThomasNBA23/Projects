import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

data_test = pd.read_csv("data/test.csv")
data = pd.read_csv("data/train.csv")

data = np.array(data)


# m : number of rows, n : number of columns
m,n = data.shape

np.random.shuffle(data)

#Dev data, 1000 data over 42000
data_dev = data[0:1000].T
Y_dev = data_dev[0]
X_dev = data_dev[1:n]

data_train = data[1000:m].T
X_train = data_train[1:n]/255
Y_train = data_train[0]


def init_parameters():
    W1 = np.random.rand(10,784) -0.5
    b1 = np.random.rand(10,1) - 0.5
    W2 = np.random.rand(10,10) - 0.5
    b2 = np.random.rand(10,1) - 0.5
    return W1,b1,W2,b2

def Relu(Z):
    #Go through each element of Z and make the operation
    return np.maximum(Z,0)

def softmax(Z):
    return np.exp(Z)/sum(np.exp(Z))

def forward_prop(W1,b1,W2,b2,X):
    Z1 = W1.dot(X) + b1
    A1 = Relu(Z1)    
    Z2 = W2.dot(A1) + b2
    A2 = softmax(Z2)
    return Z1,A1,Z2,A2


def one_hot(Y):
    #Y.size = m
    #Y_max +1 = 9+1 = 10
    one_hot_Y = np.zeros((Y.size,10))
    #np.arange(Y.size) : creates an array giving the rows where putting a 1, and Y the columns
    one_hot_Y[np.arange(Y.size),Y] = 1
    #Flip it because each row is an example and we want the columns
    return one_hot_Y.T

def deriv_Relu(Z):
    return Z>0

def back_prop(Z1,A1,Z2,A2,W1,W2,X,Y):
    one_hot_Y = one_hot(Y)
    dZ2 = A2 - one_hot_Y
    m=Y.size
    dW2 = (1/m)* dZ2.dot(A1.T)
    dB2 = (1/m)*np.sum(dZ2)
    dZ1 = W2.T.dot(dZ2) * deriv_Relu(Z1)
    dW1 = 1/m * dZ1.dot(X.T)
    dB1 = 1/m * np.sum(dZ1)
    return dW1,dB1,dW2,dB2


def update_params(W1,B1,W2,B2,dW1,dB1,dW2,dB2,alpha):
    W1 = W1 - alpha*dW1
    B1 = B1 - alpha*dB1
    W2 = W2 - alpha*dW2
    B2 = B2 - alpha*dB2    
    return W1,B1,W2,B2

def get_predictions(A2):
    return np.argmax(A2,0)
    
def get_accuracy(predictions,Y):
    return np.sum(predictions==Y)/Y.size

def gradient_descent(X,Y,iterations,alpha):
    W1,B1,W2,B2 = init_parameters()
    for i in range(iterations):
        Z1,A1,Z2,A2 = forward_prop(W1,B1,W2,B2,X)
        dW1,dB1,dW2,dB2 = back_prop(Z1,A1,Z2,A2,W1,W2,X,Y)
        W1,B1,W2,B2 =  update_params(W1,B1,W2,B2,dW1,dB1,dW2,dB2,alpha)
        if i%50 == 0:
            print("Iteration: ",i)
            print("Accuracy: ",get_accuracy(get_predictions(A2),Y))
    return W1,B1,W2,B2


W1,B1,W2,B2 = gradient_descent(X_train,Y_train,500,0.1)

