2020年8月初，tensorflow 2.3版本发布，Tensorflow的安装一直是困扰初学者的一个坎，下面我们来看一下如何用五分钟安装最新版本的Tensorflow 2.3 。

第一步，要检查和搭建环境。

以下 64 位系统支持 TensorFlow：

（1）Ubuntu 16.04 或更高版本

（2）Windows 7 或更高版本

（3）macOS 10.12.6 (Sierra) 或更高版本（不支持 GPU）

（4）Raspbian 9.0 或更高版本

Python版本要求为 3.5 – 3.7 。

第二步，安装 miniconda 和 VC(windows系统需要)

推荐使用 Miniconda 搭建python环境，

Miniconda是最小的conda安装环境，它提供了：

1. conda 包管理工具

2. python

可在官网下载对应 python 3.5 - 3.7 版本的 miniconda ，

也可加日月光华微信 louhh01 从学习交流群下载。

VC安装可从微软的官网下载，也可在Tensorflow学习交流群文件下载 。

安装完 VC 后需重启计算机。

第三步，明确自己安装的Tensorflow版本

Tensorflow分为CPU版本和GPU版本。

GPU 版本的 TensorFlow 可以利用 NVIDIA GPU 强大的计算加速能力，使 TensorFlow 的运行更为高效， 尤其是可以成倍提升模型训练的速度。

安装GPU版本必须有GPU 硬件的支持。 TensorFlow 对 NVIDIA 显卡的支持较为完备。

对于 NVIDIA 显卡，要求其 CUDA Compute Capability 须不低于 3.5。

一、对于没有Nvidia显卡的同学，我们来看一下 CPU 版本的安装：

（一）升级 pip 版本

（可选步骤，如果pip版本大于19.0， 可忽略此步骤，pip版本查看命令： pip -V），

打开anaconda prompt 命令行，执行：

                            python -m pip install --upgrade pip
（二）安装tensorflow2.3的cpu版本

pip install tensorflow-cpu==2.3.0 -i https://pypi.douban.com/simple/
等待安装结束即可完成安装。

二、Tensorflow GPU 版本安装

（一）检查nvidia驱动版本，NVIDIA驱动程序需 418.x 或更高 版本。

可在命令行中执行查看驱动版本： nvidia-smi

（二）安装依赖库

GPU版本有两个依赖库cuda和cudnn，对于 tensorflow2.3来讲，

CUDA的版本需要是 10.1

cudnn版本号需要不小于 7.6

因为GPU版本这两个依赖库比较大，不推荐大家手动配置，

我们使用conda安装，建议大家设置 conda的国内源。可加日月光华微信 louhh01 获取配置好的conda配置文件，然后放到自己的用户文件下即可。

然后打开anaconda prompt 命令行，先后执行下面两行安装命令：

conda install cudatoolkit=10.1 
conda install cudnn=7.6.5
最后执行tensorflow安装：

pip install tensorflow-gpu==2.3.0 -i https://pypi.douban.com/simple
搞定！