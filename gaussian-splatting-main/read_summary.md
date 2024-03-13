# Question
1. 为什么NeRF中的合成数据集的bounding box范围是-1.3 ~ 1.3： `gaussian-splatting-main/scene/dataset_readers.py`中的：
```python
240: xyz = np.random.random((num_pts, 3)) * 2.6 - 1.3
```

## scene
### \_\_init\_\_.py
- scene:包括3D高斯场景模型还有一些配置信息，比如说数据集路径等
- sceneLoadTypeCallbacks:获得scene_info一些信息，3D高斯一些初始化的点云都会在这里获得。如果是NeRF生成数据集的话，点云是随机初始化的，在[readNerfSyntheticInfo](#jump_1)
### gaussian_model.py
- GaussianModel: 整个3D高斯场模型
  - \_\_init\_\_: 初始化3D高斯场，其中的torch_empty(0)是占位符的意思
  - setup_function: 构建所有的激活函数和变换函数
  - densify_and_split: 根据得到的梯度值进行点的剪枝，有调用densification_postfix与prune_points.
  - densification_postfix: 有调用cat_tensors_to_optimizer
  - prune_points: 有调用_prune_optimizer
  - optimizer:作为优化器，存储3D高斯场中需要更新的参数
### general_utils.py
- get_expon_lr_func: 调度器，进行学习率的调整
- build_scaling_rotation： 构建椭球的旋转与尺度矩阵
### dataset_readers.py
- <span id="jump_1">readNerfSyntheticInfo</span>: 用于获取NeRF合成数据集

## arguments
### __init__.py
存储超参数信息

## gaussian_render
### __init__.py
- render: 整个渲染流程，有调用diff-gaussian_rasterization中GaussianRasterizationSettings与GaussianRasterizer

## diff-gaussian-rasterization
### cuda_rasterizer
#### rasterizer_impl.cu:实现了自定的forward、backward操作，具体的实现过程调用的同文件夹下的forward.cu以及backward.cu来实现
### \_\_init\_\_.py：对3D中的变量需要的forward与backward通过使用torch.autograd.Function函数进行重载来实现
### ext.cpp：对函数名进行了重新定义
### resterize_points.cu:实现了自定的forward、backward操作,具体操作跑到rasterizer_impl中了。



