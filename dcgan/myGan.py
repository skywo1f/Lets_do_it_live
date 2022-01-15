# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 17:14:12 2021
#imgplot = plt.imshow(imgs[9])
#plt.show()
@author: ivan_
"""
from dcGanLib import  *

from PIL import Image
import os, os.path

imgs = []
path = "/home/iviti/Desktop/eugeniaviti"
valid_images = [".jpg",".gif",".png",".tga"]
for f in os.listdir(path):
    ext = os.path.splitext(f)[1]
    if ext.lower() not in valid_images:
        continue
    thisImg = np.asarray(Image.open(os.path.join(path,f)))
    if thisImg.shape == (1080, 1080, 3):
        temp = np.asarray(Image.open(os.path.join(path,f)))[::4,::4]
        imgs.append(temp[:216,:216])
    #limit this for testing
#    if len(imgs) > 10:
#        break
#print(len(imgs))
tensor = np.array(imgs)
tensor = (tensor - 127.5) / 127.5  # Normalize the images to [-1, 1]

print("size of this tensor is ")
print(len(tensor))

#imgplot = plt.imshow(tensor[6])
#plt.show()

BUFFER_SIZE = 60000
BATCH_SIZE = 256




train_dataset = tf.data.Dataset.from_tensor_slices(tensor).shuffle(BUFFER_SIZE).batch(BATCH_SIZE)
generator = my_generator_model()
noise = tf.random.normal([1, 100])
generated_image = generator(noise, training=False)
#plt.imshow(generated_image[0, :, :, 0])

discriminator = my_discriminator_model()
decision = discriminator(generated_image)
print (decision)

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

EPOCHS = 5000
noise_dim = 100
num_examples_to_generate = 16

# You will reuse this seed overtime (so it's easier)
# to visualize progress in the animated GIF)
seed = tf.random.normal([num_examples_to_generate, noise_dim])

#train(train_dataset, EPOCHS)
#train here
for epoch in range(EPOCHS):
  start = time.time()

  for image_batch in train_dataset:
    train_step(image_batch,generator,discriminator,cross_entropy,generator_optimizer,discriminator_optimizer)

  # Produce images for the GIF as you go
#  display.clear_output(wait=False)
  generate_and_save_images(generator,                          epoch + 1,                           seed)

  # Save the model every 15 epochs
  if (epoch + 1) % 15 == 0:
    checkpoint.save(file_prefix = checkpoint_prefix)

  print ('Time for epoch {} is {} sec'.format(epoch + 1, time.time()-start))

# Generate after the final epoch
display.clear_output(wait=False)
generate_and_save_images(generator,
                         EPOCHS,
                         seed)

checkpoint.restore(tf.train.latest_checkpoint(checkpoint_dir))
display_image(EPOCHS)
