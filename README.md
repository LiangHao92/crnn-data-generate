# crnn-data-generate，用于生成crnn训练所需的字符图像
本项目在实现对字符图像数据生成的同时，丰富了一些相关功能，如验证字体对字典的支持，进行数据均衡等，并且在生成时对图像做了诸多变换，以更加贴切的模拟真实场景

main.py函数为调用接口，所有的参数设置都可以在config.py中进行修改



draw.py中集成了画图相关的函数，实现如在背景上画字符，选择字体，确定字符颜色等
text.py中集成了语料选择相关的函数，可以在语料文件中选择要生成的字符，也可以直接从字典中随机选取
transform.py中主要是变换函数，对图像进行各种变换，模拟视角问题造成的图像畸变
gengerate.py为主要的生成函数