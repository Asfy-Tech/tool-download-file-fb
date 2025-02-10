import tkinter as tk
from main.root import get_root

def setup_menu():
    from helpers.base import render 
    root = get_root()

    """Tạo menu chính."""
    menubar = tk.Menu(root)

    # Trang chủ
    menubar.add_command(label="Trang chủ", command=lambda: render('home'))

    # Lấy bài viết Fanpage
    menubar.add_command(label="Danh sách tài khoản", command=lambda: render('accounts'))

    # menubar.add_command(label="Đăng nhập", command=lambda: render('login'))
    
    menubar.add_command(label="Cài đặt môi trường", command=lambda: render('settings'))

    menubar.add_command(label="Xem log", command=lambda: render('logs'))

    # Áp dụng menu vào cửa sổ chính
    root.config(menu=menubar)

