import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision 
import matplotlib.pyplot as plt 
import numpy as np

transform = torchvision.transforms.Compose([torchvision.transforms.ToTensor(), torchvision.transforms.Normalize((0.5,), (0.5,))])
train_set = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=transform)
test_set = torchvision.datasets.MNIST(root='./data', train=False, download=True, transform=transform)

train_loader = torch.utils.data.DataLoader(train_set, batch_size=32, shuffle=True)
test_loader = torch.utils.data.DataLoader(test_set, batch_size=32, shuffle=False)

print('Number of images in the training dataset:', len(train_set))
print('Number of images in the testing dataset:', len(test_set))

print(f"Shape of the images in the training dataset: {train_loader.dataset[0][0].shape}")

class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork,self).__init__()
        #128 : activation values
        self.input = nn.Linear(28*28,128)
        self.hidden = nn.Linear(128,64)
        self.output = nn.Linear(64,10)
        
    def forward(self,x):
        x = x.view(-1,28*28)
        x = F.relu(self.input(x))
        x = F.relu(self.hidden(x))
        x = F.log_softmax(self.output(x),dim=1)
        return x

model = NeuralNetwork()

loss_function = nn.NLLLoss()
optimizer = optim.Adam(model.parameters(),lr=0.001)

epochs=5
for epoch in range(epochs):
    for images,labels in train_loader:
        optimizer.zero_grad()
        output = model(images)
        loss = loss_function(output,labels)
        
        loss.backward()
        optimizer.step()
        
    print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')
        


correct = 0
total = 0
with torch.no_grad():
    for images, labels in test_loader:
        output = model(images)
        _, predicted = torch.max(output, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
        
print(f'Accuracy of the neural network on the {total} test images: {100 * correct / total}%')