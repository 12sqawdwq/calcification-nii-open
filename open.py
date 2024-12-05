import os
import numpy as np
import nibabel as nib
from ipywidgets import interact, IntSlider
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

sns.set_style('darkgrid')

# 设置数据目录
data_dir = r"C:\Users\ziyu.zhao23\Downloads\dataset\test\use"
output_dir = r"C:\Users\ziyu.zhao23\Downloads\dataset\test\output"

# 创建输出目录
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 获取目录下所有的nii.gz文件
files = [f for f in os.listdir(data_dir) if f.endswith('.nii.gz')]

# 打印发现的文件数量
print(f'Found {len(files)} NIfTI files.')


def save_image_as_png(image_data, output_path, layer):
    plt.imshow(image_data[:, :, layer], cmap='gray')
    plt.axis('off')
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.close()


def load_and_display(image_path):
    # 加载图像
    image_obj = nib.load(image_path)
    image_data = image_obj.get_fdata()
    height, width, depth = image_data.shape
    print(f"Image: {os.path.basename(image_path)}")
    print(f"The image object height: {height}, width:{width}, depth:{depth}")
    print(f'image value range: [{image_data.min()}, {image_data.max()}]')
    pixdim = image_obj.header['pixdim']
    print(f'z轴分辨率： {pixdim[3]}')
    print(f'in plane 分辨率： {pixdim[1]} * {pixdim[2]}')
    z_range = pixdim[3] * depth
    x_range = pixdim[1] * height
    y_range = pixdim[2] * width
    print(x_range, y_range, z_range)

    def explore_3dimage(layer):
        plt.figure(figsize=(10, 5))
        plt.imshow(image_data[:, :, layer], cmap='gray')
        plt.title(f'Explore Layers of {os.path.basename(image_path)}', fontsize=20)
        plt.axis('off')
        plt.show()

    # 创建交互式控件
    interact(explore_3dimage, layer=IntSlider(min=0, max=depth-1, step=1, value=0))

    # 保存所有层为图片
    file_base_name = os.path.splitext(os.path.basename(image_path))[0]
    for i in tqdm(range(depth), desc=f'Saving images for {file_base_name}'):
        output_path = os.path.join(output_dir, f"{file_base_name}_layer_{i}.png")
        save_image_as_png(image_data, output_path, i)


# 遍历所有nii.gz文件并加载显示和保存层
for file in files:
    load_and_display(os.path.join(data_dir, file))