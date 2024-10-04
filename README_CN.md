# EasyCNC 

[![pyqt6](https://img.shields.io/badge/pyqt6-6.7.0-blue?style=flat-square&logo=qt)](https://pypi.org/project/PyQt6/)
[![sqlalchemy](https://img.shields.io/badge/sqlalchemy-2.0.30-blue?style=flat-square&logo=sqlalchemy)](https://pypi.org/project/sqlalchemy/)
[![opencv-python](https://img.shields.io/badge/opencv--python-4.9.0.80-blue?style=flat-square&logo=opencv)](https://pypi.org/project/opencv-python/)
[![numpy](https://img.shields.io/badge/numpy-1.26.4-blue?style=flat-square&logo=numpy)](https://pypi.org/project/numpy/)
[![matplotlib](https://img.shields.io/badge/matplotlib-3.9.0-blue?style=flat-square&logo=matplotlib)](https://pypi.org/project/matplotlib/)
[![pytest](https://img.shields.io/badge/pytest-8.2.1-blue?style=flat-square&logo=pytest)](https://pypi.org/project/pytest/)

<img src="src/app/resources/images/app%20logo.png" alt="App Logo" width="1200"/>

EasyCNC是一个免费的、跨平台的解决方案，用于有效管理CNC库存和路由器。它可以轻松集成到现有工作流程中，并利用计算机视觉技术对使用过的库存进行数字化，同时能够自动生成高效的零件加工布局。EasyCNC旨在用于3轴CNC路由器的2D零件加工。

支持的语言：
- 英语（英国，美国） 🇬🇧 🇺🇸
- 中文（简体，繁体） 🇨🇳 🇹🇼
- 俄语 🇷🇺
- 日语 🇯🇵

旧版原型应用可以在此找到：https://github.com/nagan319/NEXACut-Pro

# 目录

- 安装
- 使用方法
- 应用结构和功能
- 截图和演示
- 常见问题

# 安装

1. 确保已安装Python和Git。

2. 运行以下命令以执行程序：


您现在应该会看到以下标题屏幕：  

<img src="github images/title screen.PNG" alt="Title Screen" width="800"/>

## 本地运行

该应用可以开箱即用地在本地运行。默认情况下，它配置为在src\data目录中创建一个名为app_data.db的SQLite3数据库。

# 使用方法

使用该应用相当简单。

## 设置配置

<img src="github images/settings.PNG" alt="Settings" width="300"/>

打开应用后，导航到“设置”菜单，确保选择了正确的单位和语言。请注意，必须重启应用以应用新的设置。

## 路由器管理

<img src="github images/manage routers.PNG" alt="Manage Routers" width="800"/>

通过导航到“管理CNC路由器”选项卡，添加新的路由器并配置其参数来添加CNC路由器。在配置完所有参数后，点击“保存”，您将看到路由器预览更改以反映您的CNC路由器。

请注意，所有数字输入字段都支持分数输入以及其他单位的输入（“英寸”、“英尺”、“ft”、“mm”和“cm”）。

## 库存管理

<img src="github images/managing stock.PNG" alt="Manage Stock" width="800"/>

通过导航到“管理库存”选项卡并编辑库存参数来添加CNC库存。在完成编辑尺寸后点击保存。

可以通过导入库存图像并使用应用内置功能进行数字化来数字化预使用的库存。建议将库存平放在对比鲜明的表面上，并从正上方拍摄图像，确保反射和阴影尽可能最小。以下是一个很好的示例：

<img src="github images/stock image.jpg" alt="Stock Image" width="400"/>

如果您想查看更多可接受图像的示例，请查看src\tests\test data\images目录。请不要删除或修改此目录，因为它被各种单元测试引用。请注意，透明的库存可能更难以数字化 - 发射紫外线光或类似方法可能是个好主意。

在拍摄完库存图像后，请确保您要编辑的板材具有所需的尺寸（预览应准确），然后点击“导入图像”。

<img src="github images/image thresholding.PNG" alt="Image Thresholding" width="500"/>

导入您想要的图像（请注意，OpenCV不支持HEIC格式），并调整二值化阈值滑块，直到板材可以清晰地区分于背景。

阈值化图像后，点击“保存结果”。应用的图像处理算法将自动识别任何轮廓或板角。请注意，检测并不是100%准确的，您可能需要手动编辑图像特征。

<img src="github images/feature editing.PNG" alt="Image Thresholding" width="500"/>

应用将要求您添加缺失的角点，直到达到正确的数量（4）。然后，您可以选择错误的角点或不必要的轮廓，并使用“删除”按钮将其删除。完成特征编辑后，图像将被扁平化，并且您将看到最终的轮廓。如果您满意，请点击“保存”，库存将被更新。

## 零件导入和布局生成

在配置了CNC库存和路由器以匹配您的库存后，您可以导入任何您想要加工的CAD零件。

<img src="github images/part file import.PNG" alt="Importing Part Files" width="800"/>

零件可以以STL格式导入，该格式在SolidWorks和Fusion等CAD软件中易于获取。确保下载以毫米为单位的ASCII STL文件。

请注意，为了正确处理CAD文件，它们必须仅由以一定均匀厚度挤压的2D形状组成，并且必须沿X、Y或Z轴正确对齐。此外，请注意，您应仅一次导入具有相同材料和厚度的均匀零件，因为布局优化逻辑需要选择具有相同参数的板材。

在导入所有所需的零件后，选择所有您希望考虑用于加工的库存，以及您希望使用的路由器。您可以手动选择/取消选择单个板材，也可以选择具有特定材料和厚度的所有板材。

# 应用结构和功能

## 应用架构

<img src="github images/mvc.png" alt="MVC" width="500"/>  

<i>图片来源: https://medium.com/@sadikarahmantanisha/the-mvc-architecture-97d47e071eb2</i>

该应用遵循传统的MVC结构。src/app目录分为以下目录和文件：

模块：
- controllers - 处理与数据库交互的主要逻辑。UI与ORM模型之间的中间层。
- models - 用于路由器、板材和导入零件的SQLAlchemy ORM模型，以及相关的实用函数。
- resources - 应用字体、样式表、图像等。
- utils - 各种实用类，处理图像处理、布局优化、STL解析、绘图等。
- views - 各个应用屏幕的高层次小部件。
- widgets - 自定义显示等的低层次小部件。

脚本：
- database - 小脚本用于处理数据库初始化。
- load_settings - 在应用初始化时检索用户设置值。
- logging - 初始化日志配置。
- mainwindow - 修改过的Qt MainWindow类。
- styling - 应用全局字体和样式表。
- translations - 包含所有应用文本及其翻译成支持的语言。

还有其他目录用于存储应用数据和日志，以及一个包含后端逻辑单元测试的单独目录。

## CAD文件转换

<img src="github images/cad conversion.PNG" alt="CAD Conversion" width="500"/>  

CAD文件的转换过程遵循简单的流程。最初，它接收一个由各个面的顶点列表组成的STL文件。该过程识别具有最少唯一坐标的轴，假设CAD文件是平坦的并且与坐标轴平行。然后，它通过过滤掉直接位于目标平面上的面，"压平"文件，丢弃不必要的几何数据。根据定义，外边缘仅属于一个面，因此会过滤掉它们。

我选择STL作为所需的输入格式，因为它比.sldprt等格式更容易处理，几乎没有不必要的特性，可以使用现有库解析，并且可以通过使用Fusion360和SolidWorks等软件中的内置转换工具轻松获得。

## 板材图像转换

<img src="github images/plate conversion.PNG" alt="Plate Conversion" width="500"/>  

图像转换过程包括四个关键阶段，使用Python中的OpenCV图像处理库实现。最初，原始图像通过阈值处理进行调整大小和二值转换。然后，应用额外的过滤，以减少噪声并优化二进制表示。

接下来，使用特征检测算法确定图像的关键特征，包括角点和边缘。尽管我尝试使用OpenCV的默认角点检测方法，但对于该任务来说，它显得笨拙，因此我创建了一种自定义方法，利用点积计算来评估点之间角度的变化。

一旦检测到特征，图像被“压平”并调整为适当的尺寸。板材轮廓列表被序列化并存储在数据库中，作为base64字符串。

## 放置优化

软件中使用的放置优化算法是一个矩形打包算法，它有效地将可用区域（箱子）划分为自由矩形和占用矩形。对于每个零件，根据边界框的面积以降序选择，放置优先级根据左上角的y和x坐标进行排序。

<img src="github images/packing efficiency.png" alt="Packing Efficiency" width="500"/>  

<i>打包效率使用128组均匀随机尺寸的矩形样本进行测试，样本的总面积相加等于箱子的总面积</i>

<img src="github images/max 82.72.png" alt="Plate Conversion" width="500"/>  

<i>在随机样本中实现的最大打包效率（82.72%）</i>

## 布局生成

一旦生成了最佳放置，布局以及所有新放置件的最佳放置将显示出来。除了放置的零件，任何剩余的自由矩形也将显示，考虑到铣刀/钻头直径所需的公差以及可能无法使用的板边缘。生成的布局下方的表格显示了所有放置的零件、它们被放置的箱子以及它们的坐标，从左上角开始。

<img src="github images/plate contours.PNG" alt="Contours and Free Rects" width="300"/>

<img src="github images/newly placed pieces.PNG" alt="Newly Placed Pieces" width="300"/>

<img src="github images/layout table.PNG" alt="Part Layout Table" width="600"/>

# 常见问题

- 为什么整个应用是从头开始制作的/没有使用Django等？  
    我想从头开始创建一个完整的应用，而不依赖于任何外部框架，并且不想处理云托管的麻烦。

- 为什么零件必须以STL格式导入，而不是更传统的CAD格式？  
    STL文件比.sldprt等格式更容易解析和压平，几乎所有CAD软件都可以通用，并且可以使用现有的Python库进行处理。

- 为什么不支持HEIC格式的图像导入？  
    在写这篇文章时，HEIC格式不受OpenCV库支持。

- 如果我对应用有建议/投诉，可以联系谁？  
    我的邮箱：sashanaganov@gmail.com  
    如果您想为应用添加一些自定义功能或改进它，请随意分叉它并进行任何操作，我很乐意看到它。
