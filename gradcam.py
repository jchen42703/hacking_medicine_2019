import numpy as np
import os
import matplotlib.pyplot as plt
from pathlib import Path
from skimage.transform import resize

import tensorflow.keras.backend as K
import tensorflow as tf
from tensorflow.python.framework import ops
from tensorflow.keras.preprocessing import image

H, W = (400, 400)
preprocessing_fn = tf.keras.applications.mobilenet_v2.preprocess_input

def load_image(path, preprocess=True):
    """Load and preprocess image."""
    x = image.load_img(path, target_size=(H, W))
    if preprocess:
        x = image.img_to_array(x)
        x = np.expand_dims(x, axis=0)
        x = preprocessing_fn(x)
    return x

def create_save_gradcam(img_path, model):
    stem = Path(img_path).stem
    image_1 = load_image(img_path)
    predict = model.predict(image_1)
    print(f"Probabilty: {predict}")
    target_class = (predict>0.5)*1
    print("Target Class = %d"%target_class)
    last_conv = model.get_layer('Conv_1')
    grads = K.gradients(model.output, last_conv.output)[0]
    pooled_grads = K.mean(grads, axis=(0,1,2))
    iterate = K.function([model.input], [pooled_grads, last_conv.output[0]])
    pooled_grads_value, conv_layer_output = iterate([image_1])
    for i in range(512):
        conv_layer_output[:,:,i] *= pooled_grads_value[i]
    heatmap = np.mean(conv_layer_output,axis=-1)
    for x in range(heatmap.shape[0]):
        for y in range(heatmap.shape[1]):
            heatmap[x,y] = np.max(heatmap[x,y],0)
    heatmap = np.maximum(heatmap,0)
    heatmap /= np.max(heatmap)
    # plt.imshow(heatmap)
    upsample = resize(heatmap, (400, 400), preserve_range=True)
    plt.imshow(image_1.squeeze())
    plt.imshow(1-upsample, alpha=0.5)
    plt.savefig(os.path.join("uploads", f"{stem}_gradcam.jpg"))
