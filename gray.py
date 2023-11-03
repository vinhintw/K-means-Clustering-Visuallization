from skimage import io
import numpy as np
f = input("file: ")
# Đọc ảnh gray
image = io.imread(f, as_gray=True)

# Lấy kích thước ảnh
height, width = image.shape

# In ra giá trị mức độ sáng tối của từng điểm ảnh
for i in range(height):
    for j in range(width):
        pixel_value = image[i, j]
        print(f"Pixel ({i}, {j}): {pixel_value}")

