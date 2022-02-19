import os
import numpy as np
from pathlib import Path

import tensorflow as tf
from tensorflow.keras import layers
import matplotlib.pyplot as plt


class DataSet:
    def __init__(self, dataset_path, batch_size):
        self.batch_size = batch_size
        # Path to the data directory
        data_dir = Path(dataset_path)

        # Get list of all the images
        images = sorted(list(map(str, list(data_dir.glob("*.png")))))
        labels = [img.split(os.path.sep)[-1].split(".png")[0] for img in images]
        characters = sorted(set(char for label in labels for char in label))

        print("Number of images found: ", len(images))
        print("Number of labels found: ", len(labels))
        print("Number of unique characters: ", len(characters))
        print("Characters present: ", characters)
        print("Vocabulary Length:", len(characters))
        # total images and labels
        self.len = len(images)
        self.total_labels = len(characters)
        self.max_length = max([len(label) for label in labels])
        self.img_height, self.img_width = 50, 200

        # Splitting data into training and validation sets
        x_train, x_valid, y_train, y_valid = self.split_data(np.array(images), np.array(labels))
        
        # Mapping characters to integers
        self.char_to_num = layers.experimental.preprocessing.StringLookup(
            vocabulary=list(characters), num_oov_indices=1, mask_token=None)

        # Mapping integers back to original characters
        self.num_to_char = layers.experimental.preprocessing.StringLookup(
            vocabulary=self.char_to_num.get_vocabulary(), mask_token=None, invert=True)

        self.train_dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train))
        self.train_dataset = (
            self.train_dataset.map(
                self.encode_single_sample, num_parallel_calls=tf.data.experimental.AUTOTUNE
            )
            .batch(self.batch_size)
            .prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
        )

        # self.validation_dataset = tf.data.Dataset.from_tensor_slices((x_valid, y_valid))
        # self.validation_dataset = (
        #     self.validation_dataset.map(
        #         self.encode_single_sample, num_parallel_calls=tf.data.experimental.AUTOTUNE
        #     )
        #     .batch(self.batch_size)
        #     .prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
        # )

    def split_data(self, images, labels, train_size=1, shuffle=True):
        # 1. Get the total size of the dataset
        size = len(images)
        # 2. Make an indices array and shuffle it, if required
        indices = np.arange(size)
        if shuffle:
            np.random.shuffle(indices)
        # 3. Get the size of training samples
        train_samples = int(size * train_size)
        # 4. Split data into training and validation sets
        x_train, y_train = images[indices[:train_samples]], labels[indices[:train_samples]]
        x_valid, y_valid = images[indices[train_samples:]], labels[indices[train_samples:]]
        return x_train, x_valid, y_train, y_valid

    def encode_single_sample(self, img_path, label):
        # 1. Read image
        img = tf.io.read_file(img_path)
        # 2. Decode and convert to grayscale
        img = tf.io.decode_png(img, channels=1)
        # 3. Convert to float32 in [0, 1] range
        img = tf.image.convert_image_dtype(img, tf.float32)
        # 4. Resize to the desired size
        img = tf.image.resize(img, [self.img_height, self.img_width])
        # 5. Transpose the image because we want the time
        # dimension to correspond to the width of the image.
        img = tf.transpose(img, perm=[1, 0, 2])
        # img = img[:,:,0] # here reshaping it as [200,50,1]->[200,50] for input to RNN
        # 6. Map the characters in label to numbers
        label = self.char_to_num(tf.strings.unicode_split(label, input_encoding="UTF-8"))
        # 7. Return a dict as our model is expecting two inputs
        return {"image": img, "label": label}


if __name__ == '__main__':
    ds = DataSet("./chord_train", 16)
    _, ax = plt.subplots(4, 4, figsize=(10, 5))
    for batch in ds.train_dataset.take(1):
        images = batch["image"]
        labels = batch["label"]
        for i in range(16):
            img = (images[i] * 255).numpy().astype("uint8")
            label = tf.strings.reduce_join(ds.num_to_char(labels[i])).numpy().decode("utf-8")
            ax[i // 4, i % 4].imshow(img[:, :, 0].T, cmap="gray")
            ax[i // 4, i % 4].set_title(label)
            ax[i // 4, i % 4].axis("off")
    plt.show()







