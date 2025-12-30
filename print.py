import pyautogui
import time

# ===============================
# 配置
# ===============================
CHAR_DELAY = 0.02   # 每个字符间隔 (秒)
LINE_DELAY = 0.1    # 每行间隔 (秒)
WAIT_BEFORE_START = 2  # 启动前等待 (秒)

# ===============================
# 长文本（替换为你的 Markdown/中文/公式）
# ===============================
long_text = """nanobanana pro,
### 大图标题：仑卡奈单抗 (Lecanemab) 疾病修饰疗法全景机制图

第一部分：左侧——病理起源（分子的“黑化”过程）
背景：神经元细胞膜。
起始点（APP剪切）：
绘制APP（淀粉样前体蛋白）横跨细胞膜。
标注病理途径：β-分泌酶和γ-分泌酶像两把剪刀，先后剪开APP。
结果：释放出 Aβ 单体 (Monomers)（标注毒性最强的 Aβ42）。
核心加速器（北极突变）：
在一个分支标注“Arctic Mutation (E22G)”，显示该突变让单体像磁铁一样极速聚集。

第二部分：中间核心区——聚集级联与药物靶点（战争爆发地）
聚集阶梯（从左往右的进化）：
1. 单体 (Monomers) →
2. 寡聚体 (Oligomers) →
3. 核心靶点：可溶性原纤维 (Protofibrils) →
4. 纤维与斑块 (Fibrils & Plaques)
药物干预（仑卡奈单抗/BAN2401）：
绘制大量 Y字型抗体。
精准锁定：箭头指向可溶性原纤维，高亲和力结合，防止其进一步演变为斑块并抑制神经毒性。

第三部分：右侧——药理效应与清除机制（清理战场）
清除路径 1：原位清除
绘制小胶质细胞 (Microglia) 包围被抗体标记的原纤维进行吞噬。
清除路径 2：外周沉降 (Sink Effect)
画出血脑屏障 (BBB)。
显示抗体带着 Aβ 从脑实质穿过屏障进入血管。
指标变化：标注脑内 Aβ 浓度↓，血浆 Aβ 浓度↑。
"""

# ===============================
# 主函数：逐字符输入文本
# ===============================
def type_long_text(text, char_delay=CHAR_DELAY, line_delay=LINE_DELAY):
    for line in text.splitlines():
        # 使用 write() 方法支持中文和其他 Unicode 字符
        pyautogui.write(line, interval=char_delay)
        pyautogui.press('enter')
        time.sleep(line_delay)

# ===============================
# 执行流程
# ===============================
if __name__ == "__main__":
    print(f"请在 {WAIT_BEFORE_START} 秒内切换到目标应用...")
    time.sleep(WAIT_BEFORE_START)
    print("开始输入长文本...")
    type_long_text(long_text)
    print("输入完成！")
