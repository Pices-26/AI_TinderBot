from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D


class CnnModel:

    def __init__(self, X, y, batch,e ):
        self.X = X
        self.y = y
        self.model = Sequential()
        self.batch = batch
        self.e = e

    #layout of a model
    #possbile can add 2 dropout layers
    def model_structure(self):
        self.model.add(Conv2D(256, (3, 3), input_shape=self.X.shape[1:]))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        self.model.add(Conv2D(256, (3, 3)))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        self.model.add(Flatten())  #converts 3D to 1D vector
        self.model.add(Dense(64))

        self.model.add(Dense(1))
        self.model.add(Activation('sigmoid'))

    #compiling model
    def model_comp(self):
        self.model.compile(loss='binary_crossentropy',
                           optimizer='adam',
                           metrics=['accuracy'])

    #training the model
    def model_fit (self):
        #validation can be decreased to 0.2 depending on the size of the data
        self.model.fit(self.X, self.y, batch_size= self.batch, epochs= self.e, validation_split=0.3)

    #predicting current person
    def prediction(self, image):
        p = self.model.predict(image)
        #print(p) #was used for debugging
        return p #returns decision to like or not