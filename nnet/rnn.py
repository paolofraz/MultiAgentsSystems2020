
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Masking, Embedding
from keras.callbacks import EarlyStopping, ModelCheckpoint

# Create model
model = Sequential()

# Embedding layer
# input_dim = highest num in vocab + 1 -> 10 + 1 = 11
# output_dim (currently arbitrarily chosen as 64)
model.add(Embedding(11, 64))

# Fully connected layer
# TODO: shape
model.add(Dense(64, activation='relu'))

# Masked average pooling layer (assuming masked values are 0)
model.add(MaskedAveragePool())

# Recurrent layer
model.add(LSTM(128, return_sequences=False, 
               dropout=0.1, recurrent_dropout=0.1))

# Final fully connected layer that should return a movement action as an array with 3 numbers {0-10}
model.add(Dense(3, activation='tanh'))

# Create callbacks
callbacks = [EarlyStopping(monitor='val_loss', patience=5), ModelCheckpoint('../models/model.h5'), save_best_only=True, save_weights_only=False)]


# Train model     
# X_train = lidar input + positions?
# Y_train = action?
#                        
# history = model.fit(X_train,  y_train, 
#                     batch_size=2048, epochs=150,
#                     callbacks=callbacks,
#                     validation_data=(X_valid, y_valid))


# HELPERS

# Masked average pooling (doesn't exist in keras out of the box)

class MaskedAveragePool(Layer):
    def __init__(self, **kwargs):
        self.supports_masking = True
        super(MaskedAveragePool, self).__init__(**kwargs)

    def compute_mask(self, input, input_mask=None):
        # do not pass the mask to the next layers
        return None

    def call(self, x, mask=None):
        if mask is not None:
            # mask (batch, time)
            mask = K.cast(mask, K.floatx())
            # mask (batch, x_dim, time)
            mask = K.repeat(mask, x.shape[-1])
            # mask (batch, time, x_dim)
            mask = tf.transpose(mask, [0,2,1])
            x = x * mask
        return K.sum(x, axis=1) / K.sum(mask, axis=1)

    def get_output_shape_for(self, input_shape):
        # remove temporal dimension
        return input_shape[0], input_shape[2]