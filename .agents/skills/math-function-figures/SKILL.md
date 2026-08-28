---
name: math-function-figures
description: Generate mathematical function visualizations: single-variable functions (y=f(x), parametric curves), multi-variable functions (surface plots, contour maps, vector fields), complex mappings (conformal mapping, transformations), and phase portraits. Use when plotting mathematical functions, curves, surfaces, fields, or mappings.
---

# Math Function Figures (数学函数可视化)

数学函数可视化工具包：一元实函数、多元实函数、参数曲线、复变映射、向量场、相图等。支持单面板、多面板、2D/3D 等多种布局。

本技能覆盖本仓库中所有数学相关的图片绘制模式。

## 何时使用

- **一元实函数**：y = f(x) 的图像、极值点、零点、渐近线
- **参数曲线**：(x(t), y(t))、极坐标曲线 r(θ)、Lissajous 图形
- **多元实函数**：z = f(x,y) 的曲面图、等高线图、梯度向量场
- **复变映射**：共形映射 w = f(z)、线性变换、Möbius 变换
- **向量场**：2D/3D 向量场、流线、散度/旋度可视化
- **相图**：微分方程的相平面、轨线、平衡点
- **隐函数**：F(x,y) = 0 的等高线、隐式曲面

**不要用于**：纯物理模型图（使用 `physics-model-figures`），或纯数据统计图。

## 核心模式

### 1. 一元实函数 y = f(x)

单面板函数图像，标注关键特征：

```python
from _viz.output import Presets
SPEC = Presets.PNG_TEXTBOOK  # 或 PNG_MATH_PANEL（无衬线）

fig = SPEC.figure()
ax = fig.add_subplot(111)

x = np.linspace(-5, 5, 500)
y = f(x)
ax.plot(x, y, color="#1f4e9b", lw=2.0, label=r"$y = f(x)$")

# 坐标轴
ax.axhline(0, color="k", lw=0.8, zorder=0)
ax.axvline(0, color="k", lw=0.8, zorder=0)
ax.grid(True, color="#dddddd", lw=0.6, zorder=0)

# 标注关键点
ax.scatter([x0], [y0], s=40, color="k", zorder=5)
ax.annotate("extrema", xy=(x0, y0), xytext=(10, 10),
            textcoords="offset points", fontsize=10)

# 渐近线（虚线）
ax.axvline(x_asym, color="#888888", ls="--", lw=1.0)

ax.set_xlabel("x", fontsize=11)
ax.set_ylabel("y", fontsize=11)
ax.legend(fontsize=10)
```

### 2. 参数曲线 (x(t), y(t))

极坐标、Lissajous、摆线等：

```python
theta = np.linspace(0, 2*np.pi, 500)

# 极坐标玫瑰线 r = cos(2θ)
r = np.cos(2 * theta)
x = r * np.cos(theta)
y = r * np.sin(theta)

ax.plot(x, y, color="#2e8b57", lw=2.0)
ax.set_aspect("equal")
```

### 3. 多元实函数 z = f(x,y)

#### 3D 曲面图

```python
fig = SPEC.figure()
ax = fig.add_subplot(111, projection="3d")

x = np.linspace(-2, 2, 100)
y = np.linspace(-2, 2, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

ax.plot_surface(X, Y, Z, cmap="viridis", alpha=0.8)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
```

#### 等高线图

```python
fig, ax = plt.subplots()
contour = ax.contourf(X, Y, Z, levels=20, cmap="coolwarm")
fig.colorbar(contour, ax=ax, label="z = f(x,y)")
ax.contour(X, Y, Z, levels=20, colors="k", linewidths=0.5)
```

#### 梯度向量场

```python
# 计算梯度
dZ_dx, dZ_dy = np.gradient(Z, x, y)

# 降采样（避免箭头过密）
step = 5
ax.quiver(X[::step, ::step], Y[::step, ::step],
          dZ_dx[::step, ::step], dZ_dy[::step, ::step],
          color="#c0392b", alpha=0.7)
```

### 4. 复变映射 w = f(z)

双面板展示映射前后：

```python
SPEC = Presets.PNG_MATH_PANEL  # 宽幅双面板
fig = SPEC.figure()

# 左面板：z 平面
ax_z = fig.add_subplot(121)
ax_z.set_title("z-plane", fontsize=14, fontweight="bold")
# ... 绘制域 D 和点

# 右面板：w 平面
ax_w = fig.add_subplot(122)
ax_w.set_title("w-plane", fontsize=14, fontweight="bold")
# ... 绘制映射后的域 f(D) 和点

# 中间箭头（figure fraction 坐标）
ax_z.annotate(
    "",
    xy=(0.66, 0.50), xycoords="figure fraction",
    xytext=(0.36, 0.50), textcoords="figure fraction",
    arrowprops=dict(
        arrowstyle="-|>",
        connectionstyle="arc3,rad=-0.3",
        color="#c0392b",
        lw=2.5,
        mutation_scale=30,
    ),
)
fig.text(0.50, 0.72, r"$w = f(z)$", fontsize=13,
         ha="center", fontweight="bold")
```

参考实现：`src/math_paper/conformal_mapping.py`

### 5. 向量场 F(x,y) = (P, Q)

2D 向量场、流线：

```python
x = np.linspace(-2, 2, 20)
y = np.linspace(-2, 2, 20)
X, Y = np.meshgrid(x, y)

# 向量场分量
P = -Y
Q = X

# 向量场图
ax.quiver(X, Y, P, Q, color="#1f4e9b", alpha=0.7)
ax.set_aspect("equal")

# 或：流线
ax.streamplot(X, Y, P, Q, color="#2e8b57", density=1.5)
```

### 6. 相图（微分方程）

dx/dt = f(x,y), dy/dt = g(x,y)：

```python
# 向量场
ax.quiver(X, Y, f(X,Y), g(X,Y), color="#888888", alpha=0.5)

# 数值求解轨线
from scipy.integrate import solve_ivp

def system(t, z):
    x, y = z
    return [f(x,y), g(x,y)]

for x0, y0 in initial_conditions:
    sol = solve_ivp(system, [0, 10], [x0, y0], dense_output=True)
    t = np.linspace(0, 10, 200)
    z = sol.sol(t)
    ax.plot(z[0], z[1], color="#c0392b", lw=1.5)

# 平衡点
ax.scatter([0], [0], s=60, color="k", zorder=5)
```

### 7. 隐函数 F(x,y) = 0

使用等高线绘制隐式曲线：

```python
x = np.linspace(-2, 2, 400)
y = np.linspace(-2, 2, 400)
X, Y = np.meshgrid(x, y)

# 隐函数：x² + y² - 1 = 0（单位圆）
F = X**2 + Y**2 - 1

ax.contour(X, Y, F, levels=[0], colors="k", linewidths=2.0)
```

## 约定（来自 AGENTS.md）

- 默认输出：**透明背景 PNG**，除非明确要求其他格式
- 复用 `src/_viz/output.py` 中的 `Presets.*`
- 数学图默认使用 **无衬线字体**：`Presets.PNG_MATH_PANEL`
- 所有标注文本使用 **英文**
- 配色约定：
  - 函数曲线：蓝色 `#1f4e9b` 或绿色 `#2e8b57`
  - 向量场/箭头：红色 `#c0392b` 或蓝色 `#1f4e9b`
  - 坐标轴/文字：黑色
  - 网格：浅灰 `#dddddd`
  - 区域填充：浅蓝 `#4a90d9`，alpha=0.3

## 输出预设

| 预设 | 用途 | 尺寸 | 字体 |
|------|------|------|------|
| `PNG_MATH_PANEL` | 双面板映射图 | 14×6.5, 300dpi | 无衬线 |
| `PNG_TEXTBOOK` | 教科书风格（单/多面板） | 14×7, 300dpi | 衬线 |
| `PNG_PRINT` | 高分辨率方形图 | 9.5×9, 300dpi | 默认 |
| `SVG_TEXTBOOK` | 矢量教科书风格 | 12×12 | 衬线 |

**选择指南**：
- 单面板函数图 → `PNG_TEXTBOOK` 或 `PNG_PRINT`
- 双面板映射图 → `PNG_MATH_PANEL`
- 3D 曲面图 → `PNG_PRINT`（方形）
- 需要矢量格式 → `SVG_TEXTBOOK`

## 常见数学图片类型速查

| 类型 | 关键元素 | 参考 |
|------|---------|------|
| 一元函数 | 曲线、极值点、零点、渐近线 | — |
| 参数曲线 | (x(t), y(t))、极坐标 | — |
| 3D 曲面 | plot_surface、colormap | — |
| 等高线 | contourf + contour | — |
| 向量场 | quiver 或 streamplot | — |
| 复变映射 | 双面板 + 箭头 | `conformal_mapping.py` |
| 相图 | 向量场 + 轨线 + 平衡点 | — |
| 隐函数 | contour levels=[0] | — |

## 跨面板元素绘制

### 映射箭头（figure fraction 坐标）

```python
ax.annotate(
    "",
    xy=(0.66, 0.50), xycoords="figure fraction",  # 终点
    xytext=(0.36, 0.50), textcoords="figure fraction",  # 起点
    arrowprops=dict(
        arrowstyle="-|>",
        connectionstyle="arc3,rad=-0.3",  # 负值向上弯
        color="#c0392b",
        lw=2.5,
        mutation_scale=30,
    ),
)
```

**注意**：
- 必须使用 `figure fraction`（0-1 范围），不能用数据坐标
- `rad` 控制弯曲：正=向下，负=向上
- 用 `fig.text()` 在箭头上方添加标签

## 脚本结构模板

```python
"""数学函数可视化。

运行方式：uv run python src/math_paper/my_figure.py
"""

from __future__ import annotations
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _viz.output import Presets

# --------------------------------------------------------------------------- #
# 配置
# --------------------------------------------------------------------------- #
SPEC = Presets.PNG_TEXTBOOK  # 或 PNG_MATH_PANEL
OUT_DIR = Path(__file__).resolve().parent.parent.parent / "output"

# 数学定义
def f(x):
    """函数定义"""
    return np.sin(x) * np.exp(-0.1 * x)

# --------------------------------------------------------------------------- #
# 构建图形
# --------------------------------------------------------------------------- #
def build_figure():
    fig = SPEC.figure()
    ax = fig.add_subplot(111)
    
    # 生成数据
    x = np.linspace(-5, 5, 500)
    y = f(x)
    
    # 绘图
    ax.plot(x, y, color="#1f4e9b", lw=2.0)
    ax.axhline(0, color="k", lw=0.8)
    ax.axvline(0, color="k", lw=0.8)
    ax.grid(True, color="#dddddd", lw=0.6)
    
    # 标注
    ax.set_xlabel("x", fontsize=11)
    ax.set_ylabel("y", fontsize=11)
    
    return fig

def main():
    fig = build_figure()
    path = SPEC.save(fig, OUT_DIR / "my_figure")
    plt.close(fig)
    print(f"Saved: {path}")

if __name__ == "__main__":
    main()
```

## 常见陷阱

- **跨面板箭头坐标错误**：必须用 `figure fraction`，不能用数据坐标
- **3D 图字体问题**：3D 投影下某些文字渲染可能异常，调整 `zorder`
- **向量场过密**：使用 `[::step, ::step]` 降采样
- **等高线不 smooth**：增加网格密度（如 400×400）
- **透明背景丢失**：使用 `Presets.*.save()` 而非直接 `fig.savefig()`
- **字体不匹配**：数学图用无衬线，物理图用衬线

## 扩展建议

新增数学图片类型时：

1. 在 `src/math_paper/` 下创建脚本
2. 选择合适的预设
3. 遵循坐标系、标注、配色约定
4. 更新本技能的"常见数学图片类型速查"表

本技能会随着新图片类型的添加而更新。
