import math
import random
import os
import tkintertools as tkt
import tkintertools.animation as animation
import tkintertools.color as color
import tkintertools.constants as constants
import tkintertools.standard.shapes as shapes
import tkintertools.style as style
import tkintertools.three as three


constants.SYSTEM = "Windows11"  # 强制指定
#constants.FONT = "霞鹜文楷 屏幕阅读版"  # 若字体异常，注释掉它

def _callback(_: float) -> None:
    """callback function of animation"""
    for item in geos[:5]:
        item.rotate(dy=-0.005, dz=0.01)
        item.update()
    for item in text3ds[:5]:
        item.rotate(dy=0.005, dz=0.01)
        item.update()
    for item in geos[5:]:
        item.rotate(dy=0.005, dz=-0.01)
        item.update()
    for item in text3ds[5:]:
        item.rotate(dy=-0.005, dz=0.01)
        item.update()
    space.space_sort()


def colorful(colortup: tuple[str, str]) -> None:
    first = color.str_to_rgb(colortup[0])
    second = color.str_to_rgb(colortup[1])
    for i, fill in enumerate(color.gradient(first, second, 1280, contoller=animation.smooth)):
        space.itemconfigure(colorlines[i], fill=color.rgb_to_str(fill))


def alert(text: str) -> None:
    hint.texts[0].set(text)  # type: ignore
    tkt.animations.MoveWidget(hint, 500, (0, -130*space._ratio[1]),controller=animation.rebound, fps=60).start()
    tkt.animations.MoveWidget(hint, 500, (0, 130*space._ratio[1]), controller=animation.smooth, fps=60).start(delay=2000)


def move_right() -> None:
    for widget in login_widgets:
        animation.MoveWidget(widget, 500, (900, 0),controller=animation.smooth, fps=60).start()
    for widget in signup_widgets:
        animation.MoveWidget(widget, 500, (900, 0),controller=animation.rebound, fps=60).start(delay=100)


def move_left() -> None:
    for widget in login_widgets:
        animation.MoveWidget(widget, 500, (-900, 0),controller=animation.rebound, fps=60).start(delay=100)
    for widget in signup_widgets:
        animation.MoveWidget(widget, 500, (-900, 0),controller=animation.smooth, fps=60).start()

#切换主题函数
def Change_Theme(Button: tkt.Button) -> None:   
    animation.MoveWidget(Button, 700, (0, -50),controller=animation.smooth, fps=60).start()
    animation.MoveWidget(Button, 300, (0, 50),controller=animation.smooth, fps=60).start()
    switch_theme(Button)
    
flag_theme=False
def switch_theme(Button: tkt.Button) -> None:
    global flag_theme
    style.use_theme("dark" if flag_theme else "light")
    if flag_theme:
        flag_theme =False
        Button.shapes[0].styles = {"normal": {"fill": "#CBCDCE", "outline": "#CBCDCE"},"hover": {"fill": "#CBCDCE", "outline": "#CBCDCE"}}
        colorful(colortup=("#322B41","#1C1824"))
    else:
        flag_theme =True
        colorful(colortup=("#EEC1EB", "#B3C1EE"))
        Button.shapes[0].styles = {"normal": {"fill": "#E9CB4E", "outline": "#E9CB4E"},"hover": {"fill": "#E9CB4E", "outline": "#E9CB4E"}}
        
#切换动画函数
def Change_AnButton(Button: tkt.Button) -> None:
    animation.MoveWidget(Button, 700, (0, -50),controller=animation.smooth, fps=60).start()
    animation.MoveWidget(Button, 300, (0, 50),controller=animation.smooth, fps=60).start()
    Animation_Start(Button)
flag_An = False
def Animation_Start(Button: tkt.Button) -> None:
    global flag_An,An
    if flag_An == False:
        flag_An = True
        An.start()
    else:
        flag_An = False
        An.stop()


def get_random_int(min: int, max: int, interval: int) -> int:
    a = random.randint(min, -interval)
    b = random.randint(interval, max)
    return random.choice((a, b))

#登录系统
def Success_Login() -> None:
    Username_value = login_widgets[3].get()
    Password_value = login_widgets[5].get()

    credentials_file = 'credentials.txt'
    
    # 检查文件是否存在
    if not os.path.exists(credentials_file):
        print("账号文件不存在，已创建新的。")
        open("credentials.txt", "x")
    # 读取文件并将用户名和密码存储在字典中
    credentials = {}
    with open(credentials_file, 'r') as file:
        for line in file:
            if ':' in line:
                username, password = line.strip().split(':')
                credentials[username] = password
    
    # 检查用户名是否存在
    if Username_value in credentials:
        if credentials[Username_value] == Password_value:
            print("登录成功！")
            alert("Login Success!")
        else:
            print("密码错误。")
            alert("Account is Error!")
    else:
        print("账号不存在。")
        alert("Account is Error!")
        
#注册系统
def Success_Singup() -> None:
    Username_value = signup_widgets[3].get()
    Password_value = signup_widgets[5].get()

    credentials_file = 'credentials.txt'
    if not os.path.exists(credentials_file):
        print("账号文件不存在，已创建新的。")
        open("credentials.txt", "x")   
    if(Username_value=="" or Password_value==""):
        alert("Account is Null!")
        return       
    # 检查文件是否存在
    if not os.path.exists(credentials_file):
        with open(credentials_file, 'w') as file:
            file.write(f'{Username_value}:{Password_value}\n')
            print("账号文件不存在，已创建新文件并添加了账号。")
    else:
        # 读取文件并检查用户名是否已存在
        with open(credentials_file, 'r') as file:
            existing_usernames = [line.strip().split(':')[0] for line in file if ':' in line]
        
        if Username_value in existing_usernames:
            print("用户名已存在。")
            alert("Sign Up Error!")

        else:
            with open(credentials_file, 'a') as file:
                file.write(f'{Username_value}:{Password_value}\n')
                print("注册成功！")
                alert("Sign Up Success!")


class DummyFrame(tkt.Widget):

    def __init__(
            self, master: tkt.Canvas, position: tuple[int, int], size: tuple[int, int], *, name: str | None = None, state: str = "normal", through: bool = False, animation: bool = True) -> None:
        super().__init__(master, position, size, name=name,state=state, through=through, animation=animation)
        shapes.RoundedRectangle(self, radius=16)


class Space(three.Canvas3D):

    def space_sort(self) -> None:
        self._items_3d.sort(key=lambda item: item._camera_distance())
        for item in self._items_3d:
            self.lower(item.item, colorlines[-1])


root = tkt.Tk(title="小泪出品")
root.alpha(0.97)
space = Space(root, zoom_item=True, free_anchor=True, keep_ratio="full")
space.place(width=1280, height=720, x=640, y=360, anchor="center")

colorlines = [space.create_line(i, 0, i, 720, width=2, fill="")
              for i in range(1280)]

#切换主题按钮
Line = space.create_line(1205, 0, 1205, 95, width=2, fill="#A5AAA3")
Change_Button =tkt.Button(space, (1180, 65),(50,50), command=lambda: Change_Theme(Change_Button)) #切换深色按钮
switch_theme(Change_Button)

#切换动画按钮
An = animation.Animation(2000, animation.flat, callback=_callback,repeat=-1, derivation=True)
Line_An = space.create_line(1125, 0, 1125, 95, width=2, fill="#A5AAA3")
Animation_Button = tkt.Button(space, (1100, 65),(50,50),command=lambda: Change_AnButton(Animation_Button))

text3ds = []
geos = []

for i in range(10):
    outline = f"#{random.randint(0, (1 << 24)-1):06X}"
    geos.append(
        three.Cuboid(space, get_random_int(-300, 300, 0), get_random_int(-500, 500, 200), get_random_int(-300, 300, 100), 100, 100, 100,
                     color_outline_back=outline,
                     color_outline_down=outline,
                     color_outline_front=outline,
                     color_outline_left=outline,
                     color_outline_right=outline,
                     color_outline_up=outline),
    )
    outline = f"#{random.randint(0, (1 << 24)-1):06X}"
    text3ds.append(three.Text3D(space, (get_random_int(-300, 300, 0),get_random_int(-500, 500, 200), get_random_int(-300, 300, 100)), text="TKT", fill=outline),)


login_widgets = [
    DummyFrame(space, (450, 70), (400, 560), name="Label"),
    tkt.Information(space, (200+450, 80+70), text="Login",fontsize=40, weight="bold"),
    tkt.Information(space, (80+450, 170+70), text="Account "),
    tkt.Entry(space, (25+450, 190+70), (350, 50)),
    tkt.Information(space, (80+450, 280+70), text="Password"),
    tkt.Entry(space, (25+450, 300+70), (350, 50)),
    tkt.Button(space, (25+450, 380+70), (350, 55),text="Login", name="", command=Success_Login),
    tkt.Information(space, (135+450, 470+70),text="Do not have an account?", fontsize=18),
    tkt.UnderlineButton(space, (340+450, 470+70),text="Sign up", fontsize=18, command=move_right)
]
login_widgets[-3].shapes[0].styles = {"normal": {"fill": "#B3C1EE", "outline": "#EEC1EB"},"hover": {"fill": "#EEC1EB", "outline": "#B3C1EE"}}
login_widgets[-3].update()

signup_widgets = [
    DummyFrame(space, (450-900, 70), (400, 560), name="Label"),
    tkt.Information(space, (200+450-900, 80+70),text="Sign up", fontsize=40, weight="bold"),
    tkt.Information(space, (80+450-900, 170+70), text="Account "),
    tkt.Entry(space, (25+450-900, 190+70), (350, 50)),
    tkt.Information(space, (80+450-900, 280+70), text="Password"),
    tkt.Entry(space, (25+450-900, 300+70), (350, 50)),
    tkt.Button(space, (25+450-900, 380+70), (350, 55),text="Sign Up", name="", command=Success_Singup),
    tkt.Information(space, (135+450-900, 470+70),text="Already have an account?", fontsize=18),
    tkt.UnderlineButton(space, (350+450-900, 470+70),text="Login", fontsize=18, command=move_left)
]
signup_widgets[-3].shapes[0].styles = {"normal": {"fill": "#EEC1EB", "outline": "#B3C1EE"},"hover": {"fill": "#B3C1EE", "outline": "#E8BCE5"}}
signup_widgets[-3].update()

hint = tkt.Label(space, (960, 730), (300, 100))

if __name__ == "__main__":   

    root.mainloop()
