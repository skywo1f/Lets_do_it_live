import os

import tensorflow as tf
from tensorflow import keras
from dcGanLib import *
import imageio

print(tf.version.VERSION)

# Create a basic model instance
generator = my_generator_model()
'''
checkpoint_path = '/home/iviti/dcGan/training_checkpoints/ckpt-332'
# Loads the weights
generator.load_weights(checkpoint_path)
noise = tf.random.normal([1, 100])

generated_image = generator(noise, training=False)
'''



generator = my_generator_model()

discriminator = my_discriminator_model()

# from the DCGAN tutorial
cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=True)

generator_optimizer = tf.keras.optimizers.Adam(1e-4)
discriminator_optimizer = tf.keras.optimizers.Adam(1e-4)
checkpoint_dir = './training_checkpoints'
checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
checkpoint = tf.train.Checkpoint(generator_optimizer=generator_optimizer,
                                 discriminator_optimizer=discriminator_optimizer,
                                 generator=generator,
                                 discriminator=discriminator)

latest = tf.train.latest_checkpoint(checkpoint_dir)
checkpoint.restore(latest)

seed = 5

# classify an image
#checkpoint.discriminator(training_images[0:2])
while True:
    seed = seed + 1
    tf.random.set_seed(seed);
    noise = tf.random.normal([1, 100])
# generate an image
    generated_image = checkpoint.generator(noise)

    plt.imshow(generated_image[0, :, :, 0])
    plt.show()
