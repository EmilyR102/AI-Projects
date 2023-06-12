import tensorflow as tf


def train_model(vocab_size,embedding_dim,max_length,training_padded, training_labels, testing_padded, testing_labels):
  """
  create and train a neural network on some data
  return the model
  """
  model = tf.keras.Sequential([
      tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_length),
      tf.keras.layers.GlobalAveragePooling1D(),
      tf.keras.layers.Dense(24, activation='relu'),
      tf.keras.layers.Dense(1, activation='sigmoid')
  ])
  model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
  # model.summary()

  num_epochs = 30
  model.fit(training_padded, training_labels, epochs=num_epochs, validation_data=(testing_padded, testing_labels), verbose=2)

  return model
