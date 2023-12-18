import torch
import torchvision
from torchvision import transforms, datasets
import torch.nn as nn
import torch.optim as optim
from  net import vgg16
import random 
from torchvision import transforms
import datetime
import os
import datetime

from torch.utils.tensorboard import SummaryWriter

tb_writer = SummaryWriter(log_dir="runs/logs_vgg/") 

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 数据预处理和加载
train_transform = transforms.Compose([
        transforms.Resize(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

test_transform = transforms.Compose([
        transforms.Resize(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

batch_size = 32

## 加载数据集

train_dataset = datasets.ImageFolder('/data/hanbo/images/fruits-360_dataset/fruits-360/Training', transform=train_transform)
test_dataset = datasets.ImageFolder('/data/hanbo/images/fruits-360_dataset/fruits-360/Test', transform=test_transform)

# train_class_to_idx = train_dataset.class_to_idx
# test_class_to_idx = test_dataset.class_to_idx

# #class_labels = ['Apple 苹果', 'Banana 香蕉', 'Onion 洋葱', 'Orange 橘子', 'Watermelon 西瓜']


## 构建 batch 数据
train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)
test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=False)

# 创建ResNet50网络实例
net = vgg16().to(device)

# 打印模型结构
#print(net)

## 定义损失函数和优化器
criterion  = nn.CrossEntropyLoss()

#optimizer = optim.Adam(net.parameters(), lr=0.00001)
optimizer = optim.SGD(net.parameters(), lr=0.0001, momentum=0.9)

best_accuracy = 0 
# 开始循环训练
for epoch in  range(49):
    current_time = datetime.datetime.now()
    print("当前时间：", current_time)
    net.train()
    running_loss = 0.0
    correct_pre = 0
    for images, labels in train_loader:
        images = images.to(device)
        labels = labels.to(device)
        outputs = net(images)
        loss = criterion(outputs, labels)
             
        #_,pre_lables_index=(torch.max(outputs,1)) 

        probabilities = torch.softmax(outputs, dim=1)
        _,pre_lables_index = (torch.max(probabilities,1))
        
        correct_pre += (pre_lables_index == labels).sum().item()
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    epoch_loss = running_loss / len(train_loader)
    train_accuracy = correct_pre / len(train_dataset)
    print("epoch:{},epoch_loss:{},train_accuracy:{}".format(epoch,epoch_loss,train_accuracy))

###  进行推理
    infer_correct = 0
    net.eval()
    with torch.no_grad():
         for  images, labels in test_loader:
              images = images.to(device)
              labels = labels.to(device)
              outputs = net(images)
              infer_loss = criterion(outputs,labels) 

             # _, infer_labels = torch.max(outputs,1) 
              probabilities = torch.softmax(outputs, dim=1)
              _,infer_labels_index = (torch.max(probabilities,1))
              infer_correct += (infer_labels_index == labels).sum().item() 
    infer_accuracy = infer_correct / len(test_dataset) 
    print('infer_accuracy: {} \n'.format(infer_accuracy))
    tb_writer.add_scalar('infer_accuracy/epoch', infer_accuracy, epoch)
    tb_writer.add_scalar('infer_loss/epoch', infer_loss, epoch)

     # 保存在测试集上表现最好的模型
    if infer_accuracy > best_accuracy:
        best_accuracy = infer_accuracy
        #best_epoch = epoch
        torch.save(net.state_dict(), f'/data/hanbo/fruit/model/best_vgg{epoch}.pth')
    if infer_accuracy == 1:
        break 
print("Best accuracy achieved at epoch {}, test accuracy: {}".format(epoch, best_accuracy))
tb_writer.close()
