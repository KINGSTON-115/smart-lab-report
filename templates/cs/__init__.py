# 📚 计算机实验模板库
# Computer Science Experiment Templates

cs_sorting_algorithm = """
# {{title}}

**作者**: {{author}}
**组别**: {{group}}
**日期**: {{date}}

---

## 一、问题描述

{{problem_description|请描述需要解决的排序问题：}}

给定一个整数数组，要求实现排序算法并分析其性能。

## 二、算法设计

### 2.1 算法选择

本实验选择以下排序算法进行比较：

| 算法 | 时间复杂度 | 空间复杂度 | 稳定性 |
|------|-----------|-----------|--------|
| 冒泡排序 | O(n²) | O(1) | 稳定 |
| 快速排序 | O(nlogn) | O(logn) | 不稳定 |
| 归并排序 | O(nlogn) | O(n) | 稳定 |

### 2.2 算法伪代码

```
// 快速排序
QUICKSORT(A, low, high)
    if low < high
        pivot = PARTITION(A, low, high)
        QUICKSORT(A, low, pivot - 1)
        QUICKSORT(A, pivot + 1, high)

PARTITION(A, low, high)
    pivot = A[high]
    i = low - 1
    for j = low to high - 1
        if A[j] <= pivot
            i = i + 1
            SWAP(A[i], A[j])
    SWAP(A[i + 1], A[high])
    return i + 1
```

## 三、时间复杂度分析

{{complexity_analysis|分析各算法的时间复杂度：}}

- 最好情况：O(nlogn)
- 最坏情况：O(n²)
- 平均情况：O(nlogn)

## 四、实现代码

```python
{{code|粘贴你的代码}}

# 测试代码
if __name__ == "__main__":
    import random
    import time
    
    # 生成测试数据
    n = 10000
    data = [random.randint(1, 100000) for _ in range(n)]
    
    # 测试快速排序
    data_copy = data.copy()
    start = time.time()
    quick_sort(data_copy, 0, len(data_copy) - 1)
    elapsed = time.time() - start
    
    print(f"快速排序 {n} 个元素耗时: {elapsed:.4f}s")
```

## 五、测试用例

| 测试用例 | 输入 | 期望输出 |
|---------|------|---------|
{{test_cases|
| 普通数组 | [64, 34, 25, 12, 22, 11, 90] | [11, 12, 22, 25, 34, 64, 90] |
| 空数组 | [] | [] |
| 单元素 | [5] | [5] |
| 逆序数组 | [9, 8, 7, 6, 5, 4, 3, 2, 1] | [1, 2, 3, 4, 5, 6, 7, 8, 9] |
}}

## 六、实验结果

### 6.1 正确性验证

[插入测试结果截图]

### 6.2 性能对比

| 算法 | n=1000 | n=10000 | n=100000 |
|------|--------|---------|----------|
{{performance|
| 冒泡排序 | 0.15s | 15.2s | - |
| 快速排序 | 0.01s | 0.12s | 1.5s |
| 归并排序 | 0.02s | 0.25s | 3.0s |
}}

[插入性能对比图]

## 七、讨论与优化

{{discussion|讨论实验结果和优化方案：}}

1. 快速排序的 pivot 选择策略优化
2. 对于小数组使用插入排序
3. 尾递归优化

## 八、实验结论

{{conclusion}}

---

*报告生成时间: {{timestamp}}*
"""

cs_machine_learning = """
# {{title}}

**作者**: {{author}}
**组别**: {{group}}
**日期**: {{date}}

---

## 一、问题描述

{{problem_description|描述你要解决的机器学习问题：}}

本实验旨在解决{{task_type|分类/回归/聚类}}问题，通过机器学习方法实现对数据的建模和预测。

## 二、数据集介绍

| 属性 | 描述 |
|------|------|
{{dataset_info|
| 样本数量 | {{samples|}} |
| 特征数量 | {{features|}} |
| 类别数量 | {{classes|}} |
| 缺失值 | {{missing_values|}} |
}}

### 数据集前5行

{{data_preview}}

### 数据集统计信息

{{data_statistics}}

## 三、数据预处理

### 3.1 缺失值处理

{{missing_value_strategy|描述如何处理缺失值：}}

### 3.2 特征工程

{{feature_engineering|描述特征处理：}}

### 3.3 数据划分

| 数据集 | 样本数 | 比例 |
|--------|--------|------|
| 训练集 | {{train_samples|}} | 80% |
| 验证集 | {{val_samples|}} | 10% |
| 测试集 | {{test_samples|}} | 10% |

## 四、模型选择

| 模型 | 优点 | 缺点 |
|------|------|------|
{{models|
| 逻辑回归 | 简单、可解释 | 只能线性分类 |
| 决策树 | 直观、易解释 | 易过拟合 |
| 随机森林 | 泛化好、抗过拟合 | 可解释性差 |
| SVM | 高维有效 | 计算复杂度高 |
}}

## 五、模型训练与评估

### 5.1 训练过程

[插入训练曲线图]

### 5.2 评估指标

| 指标 | 数值 |
|------|------|
{{metrics|
| 准确率 (Accuracy) | {{accuracy|.XX}} |
| 精确率 (Precision) | {{precision|.XX}} |
| 召回率 (Recall) | {{recall|.XX}} |
| F1分数 | {{f1_score|.XX}} |
| AUC-ROC | {{auc|.XX}} |
}}

### 5.3 混淆矩阵

[插入混淆矩阵热力图]

## 六、结果可视化

### 6.1 预测分布

[插入预测结果分布图]

### 6.2 特征重要性

[插入特征重要性图]

## 七、模型解释

{{model_interpretation|解释模型学习到的规律：}}

## 八、讨论与改进

{{discussion}}

1. 模型的局限性
2. 数据增强方案
3. 模型集成策略

## 九、实验结论

{{conclusion}}

---

*报告生成时间: {{timestamp}}*
"""

cs_database = """
# {{title}}

**作者**: {{author}}
**组别**: {{group}}
**日期**: {{date}}

---

## 一、实验目的

{{purpose}}

## 二、数据库设计

### 2.1 需求分析

{{requirements}}

### 2.2 E-R 图

[插入 E-R 图]

### 2.3 数据库模式

```sql
{{schema}}
```

## 三、SQL 实现

### 3.1 创建表

```sql
{{create_tables}}
```

### 3.2 插入数据

```sql
{{insert_data}}
```

### 3.3 查询语句

```sql
{{queries}}
```

## 四、实验结果

[截图展示查询结果]

## 五、实验总结

{{conclusion}}

---

*报告生成时间: {{timestamp}}*
"""

if __name__ == "__main__":
    import os
    os.makedirs("templates/cs", exist_ok=True)
    
    templates = {
        "cs_sorting.md": cs_sorting_algorithm,
        "cs_ml.md": cs_machine_learning,
        "cs_database.md": cs_database,
    }
    
    for name, content in templates.items():
        with open(f"templates/cs/{name}", 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 保存模板: {name}")
    
    print(f"\n📚 已保存 {len(templates)} 个计算机实验模板")
