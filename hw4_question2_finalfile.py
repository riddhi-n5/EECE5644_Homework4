# -*- coding: utf-8 -*-
"""HW4_Question2_FinalFile.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1N0quhMoBpptgDoxB5H3ysap5-I7Kfdz0
"""

import numpy as np
import matplotlib.image as mpimg 
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
from matplotlib.pyplot import figure
from matplotlib import colors
cmap = colors.LinearSegmentedColormap(
    'red_blue_classes',
    {'red': [(0, 1, 1), (1, 0.7, 0.7)],
     'green': [(0, 0.7, 0.7), (1, 0.7, 0.7)],
     'blue': [(0, 0.7, 0.7), (1, 1, 1)]})
plt.cm.register_cmap(cmap=cmap)
from sklearn.model_selection import GridSearchCV
from sklearn import svm
import pandas as pd
from sklearn.model_selection import KFold
import cv2 as cv
from skimage import color

img = cv.imread('/content/surfer.jpeg')

def generate_feature_vector(image):
  # Load image, get its dimensions
  image_np = np.array(image)
  # Return an array of the row and column indices of the image (height and width)
  img_indices = np.indices((image_np.shape[0], image_np.shape[1]))
  
  if image_np.ndim == 3:
    # Create the features matrix of row and col indices, plus pixel values
    features = np.array([img_indices[0].flatten(), img_indices[1].flatten(), 
                             image_np[..., 0].flatten(), image_np[..., 1].flatten(), image_np[..., 2].flatten()])
    min_f = np.min(features, axis=1)
    max_f = np.max(features, axis=1)
    ranges = max_f - min_f
        # Each feature normalized to the unit interval [0,1] using max-min normalization: (x - min) / (max - min) 
        # New axis np.newaxis to allow numpy broadcasting
        # np.diag(1/ranges) to perform the division operation in matrix form
    normalized_data = np.diag(1 / ranges).dot(features - min_f[:, np.newaxis])
  else:
    print("Not a colour image")
        
  # Returns feature vector of normalized pixels as shape (height*width, 3 or 5)
  return image_np, normalized_data.T

kf = KFold(10, shuffle=True)
img_np, feature_vector = generate_feature_vector(img)
grid_cv: GridSearchCV = GridSearchCV(GaussianMixture(), {"n_components": np.arange(1, 11)}, cv=kf).fit(feature_vector)

pd.DataFrame(grid_cv.cv_results_)

fig, ax = plt.subplots(figsize=(11, 7))
#labels = grid_cv.predict(feature_vector) 
#bitmap=(labels.reshape(img_np.shape[0],img_np.shape[1]))

#condensing the above two lines as:
gmm_img = color.label2rgb(grid_cv.predict(feature_vector).reshape(img_np.shape[:2]), img_np, kind="overlay")
ax.imshow(gmm_img)

rows =1
cols = 2

fig = plt.figure(figsize=(20, 15))
fig.add_subplot(rows, cols, 1)
plt.imshow(img)
plt.axis('off')
plt.title("Original Image")

fig.add_subplot(rows, cols, 2)
plt.imshow(gmm_img)
plt.axis('off')
plt.title("GMM-based Segmentation labels image")
plt.show()