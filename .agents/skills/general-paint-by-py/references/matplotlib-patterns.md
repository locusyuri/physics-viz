# Matplotlib 可复用代码模式

面向"教科书风格教学图"的常用 matplotlib 片段。按需取用，并保持与所在仓库既有脚本风格一致。

## 1. 脚本骨架模板（推荐结构）

```python
"""<图题一句话>。
<第二段：规则/内容要点的清单，每条对应 docstring 与代码里的常量>。
Run with: uv run python src/.../<name>.py
"""

from __future__ import annotations
from dataclasses import replace
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # 让 `_viz` 可导入
from _viz.output import Presets

SPEC = replace(Presets.SVG_MATH, figsize=(9.5, 9.5), transparent=False)  # 白底示例
OUT_DIR = Path(__file__).resolve().parent.parent.parent / "output"

# 颜色 / 尺寸 / 内容常量集中在此
RED = "#c0392b"
BLU = "#1f4e9b"
INK = "#333333"


def panel(ax):
    """在一个子图上画完内容（单面板图也这样做，便于日后扩展）。"""
    ...


def build_figure():
    fig = SPEC.figure()
    panel(fig.add_subplot(111))
    return fig


def main():
    fig = build_figure()
    path = SPEC.save(fig, OUT_DIR / "<dashed-name>")
    plt.close(fig)
    print(f"Saved: {path}")


if __name__ == "__main__":
    main()
```

把复杂的数学/规则转成常量数组而不是写在绘制循环里，例如：

```python
PRIMES = {2, 3, 5, 7, 11, ...}
COUNTS = {2: 49, 3: 16, 5: 6, 7: 3}   # 之后 assert 校验
```

## 2. 多面板、等物理尺度

两图并排，确保正方形/等宽几何在屏幕上大小一致（`aspect="equal"` 且坐标跨度相同）：

```python
fig = SPEC.figure()
axL = fig.add_axes([0.05, 0.10, 0.40, 0.80])
axR = fig.add_axes([0.55, 0.10, 0.40, 0.80])
for ax in (axL, axR):
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1)
    ax.set_aspect("equal"); ax.axis("off")
```

面板之间加贯穿性元素（箭头/共用说明）时，叠加一个覆盖全图、关闭坐标轴的透明 axes，用 figure 分数坐标画：

```python
axm = fig.add_axes([0, 0, 1, 1]); axm.set_axis_off()
axm.annotate("", xy=(0.52, 0.5), xytext=(0.48, 0.5),
             xycoords="figure fraction", textcoords="figure fraction",
             arrowprops=dict(arrowstyle="<|-|>", color="#222", lw=1.6,
                             mutation_scale=16, clip_on=False))
fig.text(0.5, 0.52, "conjugation", ha="center", fontsize=13, color="#222")
```

## 3. 隐藏装饰的"结构图"坐标设置

```python
ax.set_xlim(-0.5, 10.5)
ax.set_ylim(10.5, -0.5)      # 需要"第一行在顶部"时反转 y
ax.set_aspect("equal")
ax.axis("off")
```

曲线图去上右脊、保留浅刻度：

```python
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for spine in ax.spines.values():
    spine.set_color("#333"); spine.set_linewidth(0.8)
ax.tick_params(colors="#333", labelsize=9)
```

## 4. 补丁图元（矩形、圆、圆角块）

```python
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch

ax.add_patch(Rectangle((x0, y0), w, h, facecolor="#cfe3f7",
                       edgecolor="#1f4e9b", lw=1.4, zorder=2))
ax.add_patch(Circle((cx, cy), r, facecolor="white", edgecolor="none", zorder=4))
ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.03,rounding_size=0.12",
                            facecolor="#cfe3f7", edgecolor="#1f4e9b", zorder=2))
# 实线边框矩形只描边：
ax.add_patch(Rectangle((0, 0), 24, 9, facecolor="none", edgecolor="#1a1a1a", lw=1.6))
```

## 5. 网格 + 单元格 / 删除线模式

等距网格：先画整根横竖线（不要每条边单独画），再填文字与覆盖层：

```python
for x in range(N + 1):
    ax.plot([x, x], [0, N], color="#d5d5d5", lw=0.8, zorder=1)
for y in range(N + 1):
    ax.plot([0, N], [y, y], color="#d5d5d5", lw=0.8, zorder=1)

# 单元格底色（必须先于网格线，zorder 0.5）
ax.add_patch(Rectangle((c, r), 1, 1, facecolor="#e2e2e2", edgecolor="none", zorder=0.5))
# 居中的数字
ax.text(c + 0.5, r + 0.5, str(n), ha="center", va="center", fontsize=13,
        color="#333", zorder=2)
# 斜删除线要压在数字之上（zorder=3），左下→右上：y 随 x 反向变化（若 y 已反转）
ax.plot([c + 0.09, c + 0.91], [r + 0.91, r + 0.09], color=RED, lw=1.4, zorder=3)
```

先集中收集"要画的覆盖元素"，再统一绘制，便于控制层级与批量设置。

## 6. 文字 / mathtext / 标注

```python
ax.text(4.6, 3.5, r"$E = kq\,/\,r^2$", fontsize=13, color="#1f4e9b")
ax.text(4.6, 3.5, r"$\frac{\partial u}{\partial t}$", fontsize=12)  # 复杂公式用 \frac 等
# 转义：普通文本里用 \u2192、\u00d7（如 "9 \u2192 6\u00d74"），不要在 r"" 里手敲箭头
ax.annotate("label", xy=(x, y), xytext=(12, 6), textcoords="offset points",
            fontsize=11, color="#333",
            arrowprops=dict(arrowstyle="-|>", color="#333", lw=1.0))
```

公式不要用普通 unicode 拼写（如 `Q_h`），统一 mathtext：`r"$Q_h$ in"`。强调点：

```python
ax.scatter([x], [y], s=24, facecolor="white", edgecolor="#1f4e9b", zorder=5)  # 空心记号
ax.plot(x, y, "ko", ms=6, zorder=5)
```

## 7. 方向箭头（`annotate` / `FancyArrowPatch`）

```python
ax.annotate("", xy=(1.6, 3.0), xytext=(1.2, 3.4),
            arrowprops=dict(arrowstyle="-|>", color=BLU, lw=1.8,
                            mutation_scale=15, zorder=4))
# 双头、精确起点终点：
from matplotlib.patches import FancyArrowPatch
ax.add_patch(FancyArrowPatch((0.1, 0), (0.8, 0), arrowstyle="-|>",
                             mutation_scale=9, color=RED, lw=1.2, zorder=3))
```

## 8. 手动图例

```python
from matplotlib.lines import Line2D
handles = [
    Line2D([0], [0], color=RED, lw=1.6, label="Field Lines"),
    Line2D([0], [0], marker="o", color="none", markerfacecolor=BLU,
           markersize=9, label="Test Point"),
    Line2D([0], [0], color="#999", lw=1.2, ls="--", label="Reference"),
]
ax.legend(handles=handles, loc="lower right", fontsize=9, frameon=True,
          facecolor="white", edgecolor="#cccccc")
```

不需要方框时：`frameon=False`。放图外右下：`bbox_to_anchor=(1.0, 0.0), loc="lower left"`。

## 9. 刻度细节

```python
ax.set_xticks(np.arange(0, 11, 2)); ax.set_yticks(np.arange(0, 6, 1))
ax.tick_params(labelsize=9)
ax.grid(True, which="both", color="#dddddd", lw=0.6)   # 曲线图可选淡网格
```

## 10. 建议调色板

| 用途 | 建议色 |
| --- | --- |
| 墨色文字/主线 | `#1a1a1a` `#333333` |
| 深蓝 | `#1f4e9b` |
| 中蓝 | `#2196F3` / `#2980b9` |
| 红 | `#c0392b` / `#E53935` |
| 橙 | `#e67e22` |
| 绿 | `#27ae60` / `#2e8b57` |
| 紫 | `#CDB5E9`（淡）/ `#8e44ad` |
| 浅灰参考 | `#999999` `#888888` |
| 淡填充 | `#AED3F0` `#A6DFE2` `#BFE2A5` `#F7C98F` `#CDB5E9` |
| 极浅网格 | `#dddddd` `#d5d5d5` |

同图内颜色数量控制在 4~6 个语义色以内，并让图例解释每种颜色的含义。

## 11. 常见坑

- **文字越界**：`annotate` 文本用 `textcoords="offset points"` 或用足够大的 `xlim/ylim`；难以目测时给 `ax.text` 加 `bbox`。
- **`aspect("equal")` + 不匹配的范围**：会强制压缩一个轴，导致圆变成椭圆或网格变扁；结构图务必先定范围再 equal。
- **反转 y 轴后坐标直觉错乱**：画"从左下到右上"等方向线时逐点核对（数据 y 增大 = 视觉向下）。
- **覆盖顺序**：文字默认 zorder 高，覆盖物（如删除线）要显式更高 zorder 才能压在文字上。
- **mathtext 转义**：`%` 必须写作 `\%`，中文与普通文本混用 mathtext 会乱——图内注释保持英文。
- **公式里的空格**：mathtext 用 `\,` 或 `\;` 控制间距。
- **透明背景未关**：需要白底交付时设 `transparent=False`（见 project-conventions）。
