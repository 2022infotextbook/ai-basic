# -*- coding: utf-8 -*-
"""데이터 증강

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17jJA2u3A09RAUyelQOC0MOSOe1qEN096

데이터 증강 실습을 위한 페이지.

이미지는 jpg 또는 jpeg 파일을 사용하세요.
"""

# 이미지 업로드
from google.colab import files
import os

while True:
    uploaded = files.upload()
    uploaded_image_path = list(uploaded.keys())[0]

    # 파일 확장자 확인
    file_extension = os.path.splitext(uploaded_image_path)[1].lower()
    if file_extension not in ['.jpg', '.jpeg']:
        print(f"'{uploaded_image_path}'은/는 jpg 또는 jpeg 형식이 아닙니다. 다시 시도해주세요.")
        continue
    else:
        break

# 이미지 불러오기 및 전처리
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread
from skimage.transform import rotate, rescale, resize, warp, AffineTransform
from skimage.util import random_noise, crop
from skimage.exposure import rescale_intensity
from skimage.filters import gaussian
from skimage.color import rgb2hsv, hsv2rgb
import cv2

def load_and_preprocess_image(image_path):
    img = imread(image_path)
    img = cv2.resize(img, (128, 128))
    return img

image = load_and_preprocess_image(uploaded_image_path)

def augment_image(image, degree=90, scale=1.2, sigma=3, crop_size=20):
    # 회전
    rotated_image = rotate(image, degree, mode='edge')

    # 노이즈 추가
    noisy_image = random_noise(image)

    # 좌우 반전
    flip_lr_image = np.fliplr(image)

    # 수직 반전
    flip_ud_image = np.flipud(image)

    # 밝기 조절
    v_min, v_max = np.percentile(image, (0.2, 99.8))
    better_contrast = rescale_intensity(image, in_range=(v_min, v_max))

    # 크기 변경
    rescaled_image = rescale(image, scale)
    pad_width = [(int((rescaled_image.shape[0]-image.shape[0])/2), int((rescaled_image.shape[0]-image.shape[0])/2)),
                 (int((rescaled_image.shape[1]-image.shape[1])/2), int((rescaled_image.shape[1]-image.shape[1])/2)),
                 (0, 0)]
    resized_image = np.pad(rescaled_image, pad_width, mode='constant')

    # 가장자리 제거
    cropped_image = crop(image, ((crop_size, crop_size), (crop_size, crop_size), (0, 0)))

    # 색상 변경
    hsv_image = rgb2hsv(image)
    hsv_image[...,0] = (hsv_image[...,0] + 0.5) % 1  # hue channel
    color_changed_image = hsv2rgb(hsv_image)

    # 흐릿하게
    blurred_image = gaussian(image, sigma=sigma, channel_axis=True)

    return rotated_image, noisy_image, flip_lr_image, flip_ud_image, better_contrast, resized_image, cropped_image, color_changed_image, blurred_image

# 이미지 증강
rotated_image, noisy_image, flip_lr_image, flip_ud_image, better_contrast, resized_image, cropped_image, color_changed_image, blurred_image = augment_image(image)

# 원본 이미지 및 증강된 이미지 출력
fig, axs = plt.subplots(3, 5, figsize=(15, 8))

# 원본 이미지

axs[0, 2].imshow(image)
axs[0, 2].set_title('Original Image')

# 증강된 이미지
# 원본 이미지 크기에 맞게 잘라내기
rotated_image = cv2.resize(rotated_image, (image.shape[1], image.shape[0]))
axs[1, 0].imshow(rotated_image)
axs[1, 0].set_title('Rotated Image')

axs[1, 1].imshow(noisy_image)
axs[1, 1].set_title('Noisy Image')

axs[1, 3].imshow(flip_lr_image)
axs[1, 3].set_title('Left-Right Flipped Image')

axs[1, 4].imshow(flip_ud_image)
axs[1, 4].set_title('Up-Down Flipped Image')

axs[2, 0].imshow(better_contrast)
axs[2, 0].set_title('Better Contrast Image')

# 원본 이미지 크기에 맞게 잘라내기
cropped_image = cv2.resize(cropped_image, (image.shape[1], image.shape[0]))
axs[2, 1].imshow(cropped_image)
axs[2, 1].set_title('Cropped Image')

axs[2, 3].imshow(color_changed_image)
axs[2, 3].set_title('Color Changed Image')

axs[2, 4].imshow(blurred_image)
axs[2, 4].set_title('Blurred Image')

for ax in axs.ravel():
    ax.axis('off')

plt.show()