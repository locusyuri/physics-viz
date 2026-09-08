# physics-viz 仓库绘图约定

在 `physics-viz` 中编写绘图脚本时必须遵守本文约定。

## 目录与产出

- 绘图脚本按领域分布在 `src/math_paper/`（数学/教学图）、`src/electric_field/`、`src/magnetic_field/`、`src/oscillation/` 等子目录。
- 共享输出预设位于 `src/_viz/output.py`（`Presets.*`）。**不要在每个脚本里手写 `figsize`/`dpi`/`facecolor`**，一律从 Preset 出发，需要微调时用 `dataclasses.replace`。

## Preset 选择（关键）

| 场景 | 预设 |
| --- | --- |
| `src/math_paper/` 下的图（**强制 SVG**） | `SVG_MATH`（方形单面板，sans）、`SVG_MATH_PANEL`（宽幅多面板，sans）、`SVG_TEXTBOOK`（衬线、教科书排版） |
| 默认其他图形（PNG，透明背景） | `PNG_TEXTBOOK`（衬线）、`PNG_WEB`、`PNG_PRINT` |

背景默认 `transparent=True`（SVG/PNG 均无底色）。若规格要求**白色背景**，必须显式：

```python
SPEC = replace(Presets.SVG_MATH, transparent=False)              # facecolor 默认 white
SPEC = replace(Presets.SVG_TEXTBOOK, figsize=(9.6, 12.0),
               transparent=False, facecolor="white")
```

`src/math_paper/` 脚本的公共样板（与同目录既有脚本保持一致）：

```python
import sys
from pathlib import Path
from dataclasses import replace
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # 导入 _viz
from _viz.output import Presets

SPEC = replace(Presets.SVG_MATH, ...)                            # 或 SVG_TEXTBOOK / SVG_MATH_PANEL
OUT_DIR = Path(__file__).resolve().parent.parent.parent / "output"
```

执行：从仓库根 `uv run python src/math_paper/<name>.py`，输出落在仓库根的 `output/` 下（如 `output/<dashed-name>.svg`）。其它子目录脚本的 `OUT_DIR`/`sys.path` 写法可能不同——直接照抄该子目录中同类脚本，不要凭空推断。

## 运行与验收

- 运行命令：`uv run python <相对仓库根的路径>`（本项目由 uv 管理，见 `pyproject.toml`/`uv.lock`）。
- 脚本无错误生成文件即完成：**不要调用视觉/看图工具复查图片**，不要自说自话"看起来如何"；只报告保存路径。
- 写完后跑 `read_lints` 清理新引入的 lint 错误。
- 用户没有要求时不要 `git commit`；只有绘图脚本 + 输出文件，不创建 README 等多余文件。

## 内容与排版约定

- 图内**所有文字为英文**；变量/公式用 mathtext（`r"$E = kq/r^2$"`），字母斜体遵循 LaTeX 习惯（变量 italic、函数名/单位正体）。
- 教学图默认**衬线字体**（`SVG_TEXTBOOK`/`PNG_TEXTBOOK` 已配置）；`SVG_MATH` 系为无衬线。选择依据：教科书排版风格选 serif，幻灯片/网页风格可选 sans。
- 图内注释、标注、图例文字保持最小化；一般不给大标题，除非规格要求。
- 几何/结构示意（网格、矩形、圆盘）通常 `axis("off")` + `set_aspect("equal")`；函数曲线图保留浅灰刻度与去除 top/right 脊。
- 每张图一个"单元"的规则可以做成常量 + `assert` 计数自检（例如筛法图里对每类删除线数量断言），保证规格被完整覆盖。
