import threading
import os
import json
class AccountProcess:
    def __init__(self, json_file_path='db.json'):
        self.json_file_path = json_file_path
        self.progress_data = {} 
        self.load_data()

    def add_process(self, process):
        self.progress_data[process["id"]] = process

    def update_process(self, id, new_text):
        try:
            if id in self.progress_data:
                process = self.progress_data[id]
                status_label = process.get("status_label") 
                process["status"] = new_text
                if status_label:
                    status_label.config(text=new_text) 
        except Exception as e:
            # logging.error(f"Đã xảy ra lỗi khi cập nhật task_label: {e}")
            print(f"Đã xảy ra lỗi khi cập nhật task_label: {e}")
        
    def update_task(self, id, newtask):
        try:
            if id in self.progress_data:
                process = self.progress_data[id]
                process.get('tasks').append(newtask)
                task_label = process.get("task_label") 
                if task_label:
                    task_label.config(text=len(process.get('tasks')))
        except Exception as e:
            # logging.error(f"Đã xảy ra lỗi khi cập nhật task_label: {e}")
            print(f"Đã xảy ra lỗi khi cập nhật task_label: {e}")

    def update_statusVie(self,acc):
        try:
            status_vie = acc.get('status_vie')
            process = self.progress_data[acc.get('id')]
            if status_vie == 1:
                if 'vie_button' in process:
                    process['vie_button'].config(text="Tắt cào vie")
                process['status_vie'] = 2
            else:
                if 'vie_button' in process:
                    process['vie_button'].config(text="Bật cào vie")
                process['status_vie'] = 1
        except Exception as e:
            # logging.error(f"Đã xảy ra lỗi khi cập nhật task_label: {e}")
            print(f"Đã xảy ra lỗi khi cập nhật task_label: {e}")

    def show(self, id):
        process = self.progress_data[id]
        return process


    def stop_process(self, id):
        # Dừng tiến trình theo id
        try:
            if id in self.progress_data:
                process = self.progress_data[id]
                process['status_process'] = 2
                stop_event = process.get('stop_event')
                
                # Đặt stop_event nếu có
                if stop_event:
                    stop_event.set()

                # Cập nhật giao diện ngay lập tức
                close_button = process.get("close_button")
                if close_button:
                    close_button.config(text="Đang đóng...", state="disabled")

                # Định nghĩa task dừng tiến trình trong một thread riêng
                def stop_task(process):
                    tasks = process.get('tasks', [])
                    for thread in tasks:
                        if thread.is_alive():
                            thread.join()  # Đợi các thread kết thúc

                    # Sau khi hoàn thành, xóa tiến trình khỏi danh sách và đóng giao diện
                    self.progress_data[id].get('row').destroy()
                    del self.progress_data[id]  # Xóa khỏi progress_data

                # Chạy stop_task trong một thread riêng biệt
                threading.Thread(target=stop_task, args=(process,), daemon=True).start()
        except Exception as e:
            # logging.error(f"Đã xảy ra lỗi khi cập nhật task_label: {e}")
            print(f"Đã xảy ra lỗi khi cập nhật task_label: {e}")

    
    def load_data(self):
        try:
            # Kiểm tra nếu file tồn tại và có thể mở
            if os.path.exists(self.json_file_path):
                with open(self.json_file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    self.progress_data = {}
                    for item in data.get("accounts", []):
                        self.progress_data[item.get('id')] = item
                    print("Data loaded successfully.")
            else:
                raise FileNotFoundError(f"{self.json_file_path} does not exist.")

        except FileNotFoundError:
            # Nếu file không tồn tại, tạo mới file với định dạng mặc định
            print(f"Error: {self.json_file_path} not found. Creating new file with default format.")
            self.create_default_file()

        except json.JSONDecodeError:
            # Nếu không thể parse được JSON, tạo lại file với định dạng mặc định
            print(f"Error: Failed to decode JSON from {self.json_file_path}. Creating new file with default format.")
            self.create_default_file()

    def create_default_file(self):
        # Tạo file mới với định dạng mặc định
        default_data = {"accounts": []}
        with open(self.json_file_path, 'w', encoding='utf-8') as file:
            json.dump(default_data, file, ensure_ascii=False, indent=4)
        print(f"Created new file with default data: {self.json_file_path}")

    def get_all_processes(self):
        self.load_data()
        return self.progress_data


# Biến toàn cục lưu instance của FanpageProcess
accounts_process_instance = AccountProcess()

def get_accounts_process_instance():
    return accounts_process_instance
