import torch
import torchvision.transforms as transforms
from PIL import Image
import matplotlib.pyplot as plt
#from net import AlexNet
import torchvision.transforms as transforms
from PIL import Image, ImageFont, ImageDraw
import os
from  VGGNet import vgg16

# 有 GPU 就用 GPU，没有就用 CPU
device = torch.device("cuda:1" if torch.cuda.is_available() else "cpu")
#font = ImageFont.truetype('SimHei.ttf', 32)   ## 

net = vgg16().to(device)
state_dict = torch.load('/data/fruit/model/best_model_vgg112.pth',map_location=torch.device(device))
net.eval()
net.load_state_dict(state_dict)
# 数据预处理和加载
test_transform = transforms.Compose([
        transforms.Resize(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

##  需要根据自己的分类标签更改
class_labels = ['Apple 苹果', 'Banana 香蕉', 'Onion 洋葱', 'Orange 橘子', 'Watermelon 西瓜']

# image_paths = ['/data/hanbo/fruit/orange.jpeg',
#               '/data/hanbo/fruit/orange_crop.jpg',
#               '/data/hanbo/fruit/orange1_crop.jpg',
#               '/data/hanbo/fruit/apple.jpg',
#                '/data/hanbo/fruit/banana.jpeg'
#               ]

image_paths = ['/data/hanbo/images/fruits-360_dataset/fruits-360/Test/Apple Braeburn/55_100.jpg']

for image_path  in image_paths:
    image_base = Image.open(image_path) 
    image = image_base.convert("RGB")
    image = test_transform(image).unsqueeze(0)
    image = image.to(device)  
   

    with torch.no_grad():
         output = net(image)
    
    probabilities = torch.softmax(output, dim=1)
    _,predicted_label_index=(torch.max(probabilities,1))
    predicted_label_index_item = predicted_label_index.item()
    predicted_label = class_labels[predicted_label_index_item]
    confidence = probabilities[0][predicted_label_index_item].item()
    confidence_formatted = "{:.8f}".format(confidence)
    print('predicted_label: {}  predicted_confidence: {}'.format(predicted_label,confidence_formatted))


# ## 保存图像
#     #plt.imshow(image().permute(1,2,0).cpu())   这是在进行数据转换后的图像上展示
#     plt.imshow(image_base)   ## 这是原始基础图片
#     plt.axis('off')
#     plt.title(f"model predicted is  : {predicted_label}, confidence: {confidence_formatted}")

#     # 获取原始路径的目录和文件名
#     dirname = os.path.dirname(image_path)
#     filename = os.path.basename(image_path)

#     ## 保存猜测的照片名称为原来的名字+guess 比如: orange_guess.jpeg
#     new_filename = os.path.splitext(filename)[0] + '_guess' + os.path.splitext(filename)[1]  
#     new_path = os.path.join(dirname, new_filename)
#     output_path = new_path
#     plt.savefig(output_path)
