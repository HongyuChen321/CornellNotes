main.py  
作用：项目的入口文件，负责初始化应用程序并显示主窗口。
主要功能：创建 QApplication 实例，显示 MainPage 窗口，并启动应用程序的事件循环。
main_page.py  
作用：定义主页面的逻辑和界面。
主要功能：设置主页面的布局和控件，处理用户交互（如打开文件、创建新文件夹等），以及与 NotePage 进行交互。
note_page.py  
作用：定义笔记页面的逻辑和界面。
主要功能：设置笔记页面的布局和控件，处理文本编辑（如加粗、斜体、下划线等），以及文件的打开、保存和另存为操作。
ui_main_page.py  
作用：由 Qt Designer 生成的主页面的 UI 文件，包含主页面的界面布局和控件定义。
主要功能：定义主页面的界面元素及其属性，供 main_page.py 使用。
ui_note_page.py
作用：由 Qt Designer 生成的笔记页面的 UI 文件，包含笔记页面的界面布局和控件定义。
主要功能：定义笔记页面的界面元素及其属性，供 note_page.py 使用。