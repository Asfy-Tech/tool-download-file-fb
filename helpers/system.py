import socket
import platform
import requests
import logging
import multiprocessing
from time import sleep
import os
from threading import Thread
import shutil
import json
from bot import send
from helpers.global_value import get_global_theard_event
global_theard_event = get_global_theard_event()

def get_system_info():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except Exception as e:
        local_ip = f"Không lấy được IP cục bộ ({e})"

    try:
        # Sử dụng dịch vụ bên ngoài để lấy IP công khai
        public_ip = requests.get("https://api64.ipify.org?format=json").json()["ip"]
    except Exception as e:
        public_ip = f"Không lấy được IP công khai ({e})"

    return {
        "Hệ điều hành": f"{platform.system()} {platform.release()}",
        "Phiên bản": platform.version(),
        "Kiến trúc": platform.architecture()[0],
        "Tên máy": platform.node(),
        "CPU": platform.processor(),
        "Số lõi CPU": multiprocessing.cpu_count(),
        "Địa chỉ IP cục bộ": local_ip,
        "Địa chỉ IP công khai": public_ip
    }


def get_system():
    global system
    return system

def clear_temp():
    temp_dir = os.getenv('TEMP')
    if not temp_dir:
        return
    print(f"Thư mục TEMP hiện tại: {temp_dir}")
    logging.info(f"Thư mục TEMP hiện tại: {temp_dir}")
    for item in os.listdir(temp_dir):
        item_path = os.path.join(temp_dir, item)
        try:
            if os.path.isdir(item_path):  # Kiểm tra xem có phải thư mục không
                shutil.rmtree(item_path)  # Xóa thư mục
                print(f"Đã xóa thư mục: {item_path}")
                logging.info(f"Đã xóa thư mục: {item_path}")
            else:
                os.remove(item_path)  # Xóa file
                print(f"Đã xóa file: {item_path}")
                logging.info(f"Đã xóa file: {item_path}")
        except Exception as e:
            pass

def clear_cache():
    while True:
        clear_temp()
        print("[INFO] Đã dọn dẹp thư mục Temp. Chờ 5 phút để tiếp tục.")
        logging.info("[INFO] Đã dọn dẹp thư mục Temp. Chờ 5 phút để tiếp tục.")
        sleep(300)  # Dừng 5 phút

def start_clear_cache_thread():
    # Tạo một thread mới để chạy clear_cache
    thread = Thread(target=clear_cache, daemon=True)
    thread.start()