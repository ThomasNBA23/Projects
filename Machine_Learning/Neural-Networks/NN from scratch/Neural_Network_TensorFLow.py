import tensorflow as tf 
from tensorflow.keras import layers,models
import matplotlib.pyplot as plt 
import numpy as np

(train_images,train_labels),(test_images,test_labels) = tf.keras.datasets.mnist.load_data()
train_images = train_images.astype('float32')/255
test_images = test_images.astype('float32')/255

print('Number of images in the training dataset:', train_images.shape[0])
print('Number of images in the testing dataset:', test_images.shape[0])

print(f"Shape of the images in the training dataset: {train_images[0].shape}")


model = models.Sequential([
    layers.Flatten(input_shape=(28,28,1)),
    layers.Dense(128,activation="relu"),
    layers.Dense(64,activation="relu"),
    layers.Dense(10,activation="softmax")
])


model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])

history = model.fit(
    train_images,
    train_labels,
    epochs=5
)

image,label = test_images[0],test_labels[0]
probabilities = model.predict(image.reshape(1,28,28,1))

test_loss,test_accuracy = model.evaluate(test_images,test_labels)
print(f'Accuracy of the neural network on the {test_images.shape[0]} test images: {test_accuracy * 100:.2f}%')
