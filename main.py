from tkinter import Tk
from PIL import ImageTk, Image
import sys
import os
import random
import tkinter as tk


class ShakingImage:
    def __init__(self, root, image_path):
        self.root = root
        self.root.title("+1")

        # 创建Canvas替代Label
        self.canvas = tk.Canvas(root, bg='black', highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)

        # 在Canvas上加载图片
        self.image_obj = ImageTk.PhotoImage(Image.open(image_path))

        # 绑定点击事件到Canvas
        self.canvas.bind("<Button-1>", self.shake)

        # 记录初始位置
        self.original_x = root.winfo_x()
        self.original_y = root.winfo_y()

        # 保存原始PIL图像对象
        self.raw_image = Image.open(image_path)
        self.image_id = None  # 新增图片对象ID
        # 初始显示图片
        self.resize_image()

        # 绑定窗口大小改变事件
        # self.root.bind("<Configure>", lambda e: self.resize_image())

        # self.label.lift()  # 保持图片在Canvas上层

    def resize_image(self, event=None):
        # 获取有效窗口尺寸（当窗口未渲染时使用初始尺寸）
        win_width = max(self.root.winfo_width(), 200)  # 400是初始宽度
        win_height = max(self.root.winfo_height(), 200) # 300是初始高度

        # 当窗口最小化时直接返回
        if win_width < 10 or win_height < 10:
            return

        # 计算缩放比例（保留原始宽高比）
        img_width, img_height = self.raw_image.size
        ratio = min(win_width/img_width, win_height/img_height)

        # 缩放图片
        resized = self.raw_image.resize(
            (int(img_width*ratio), int(img_height*ratio)),
            Image.Resampling.LANCZOS
        )

        # 更新标签图片
        self.image_obj = ImageTk.PhotoImage(resized)
        if not self.image_id:
            self.image_id = self.canvas.create_image(
                win_width // 2, win_height // 2,
                image=self.image_obj, anchor='center'
            )
        else:
            self.canvas.itemconfig(self.image_id, image=self.image_obj)
            self.canvas.coords(self.image_id, win_width // 2, win_height // 2)

    def show_text(self, x, y):
        # 直接在Canvas上显示文字（始终在最上层）
        text = self.canvas.create_text(x, y, text="+1",
                                      fill="white", font=("Arial", 24),
                                      anchor="center")
        # 文字上升动画
        def animate(step=0):
            if step < 20:
                self.canvas.move(text, 0, -2)
                # 修改为合法的RGB颜色格式
                gray = 255 - (step * 12)  # 从白到黑渐变 (255 -> 15)
                self.canvas.itemconfig(text, fill=f"#{gray:02x}{gray:02x}{gray:02x}")
                self.root.after(30, lambda: animate(step + 1))
            else:
                self.canvas.delete(text)

        animate()

    def shake(self, event):
        # 在震动前触发文字动画
        self.show_text(event.x, event.y)
        # 木鱼震动参数
        initial_drop = 3  # 初始下坠距离
        bounce_height = 3   # 回弹高度
        shake_steps = [
            (0, initial_drop),   # 快速下坠
            (0, -bounce_height), # 回弹
            (0, bounce_height//2), # 二次回弹
            (0, 0)              # 恢复原位
        ]
        delay = 80  # 每步间隔时间

        # 获取基准坐标
        base_x = self.root.winfo_x()
        base_y = self.root.winfo_y()

        # 添加轻微水平震动
        horizontal_shake = [random.randint(-2, 2) for _ in shake_steps]

        for i, ((dx, dy), h_offset) in enumerate(zip(shake_steps, horizontal_shake)):
            # 计算复合偏移量
            offset_x = dx + h_offset
            offset_y = dy

            # 应用带缓动的位移
            self.root.after(delay * i,
                lambda x=offset_x, y=offset_y: self.root.geometry(
                    f"+{base_x + x}+{base_y + y}"))

        # 最终确保回到精确位置
        self.root.after(delay * len(shake_steps),
            lambda: self.root.geometry(f"+{base_x}+{base_y}"))


def __dir():
    if getattr(sys, 'frozen', False):
        # 打包后环境：返回临时解压目录
        return sys._MEIPASS
    else:
        # 开发环境：返回脚本所在目录
        return os.path.dirname(os.path.abspath(__file__))


if __name__ == "__main__":
    root = Tk()

    # 强制先设置窗口基础尺寸
    root.minsize(200, 150)  # 设置最小尺寸防止归零
    root.geometry("200x200")  # 显式设置初始尺寸
    root.resizable(False, False)

    # 自动居中窗口
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_size = (200, 200)  # 根据图片尺寸调整
    x = (screen_width - window_size[0]) // 2
    y = (screen_height - window_size[1]) // 2
    root.geometry(f"{window_size[0]}x{window_size[1]}+{x}+{y}")

    # 替换为你的图片路径
    app = ShakingImage(root, os.path.join(__dir(), "muyu.png"))
    root.mainloop()


