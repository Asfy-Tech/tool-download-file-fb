import os
import time

class FileDownloadHandler:
    def __init__(self, driver=None):
        self.driver = driver
        self.download_dir = self._get_default_download_dir()
        os.makedirs(self.download_dir, exist_ok=True)


    def _get_default_download_dir(self):
        """Tạo thư mục tải xuống mặc định trong thư mục hiện tại."""
        current_dir = os.path.abspath(os.getcwd())
        download_dir = os.path.join(current_dir, "downloads")
        return download_dir

    def get_latest_file(self):
        """Tìm file mới nhất trong thư mục tải xuống."""
        files = os.listdir(self.download_dir)
        if not files:
            return None  # Không có file nào
        paths = [os.path.join(self.download_dir, f) for f in files]
        latest_file = max(paths, key=os.path.getctime)
        return latest_file

    def wait_for_file_download(self, timeout=180):
        """Đợi file mới xuất hiện trong thư mục tải xuống."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            latest_file = self.get_latest_file()
            if latest_file and not latest_file.endswith(".crdownload"):  # Đợi file tải xong
                return latest_file
            time.sleep(1)  # Kiểm tra mỗi giây
        raise Exception("File download timeout!")

    def send_file_to_server(self, file_path, server_url):
        """Gửi file lên server."""
        import requests
        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = requests.post(server_url, files=files)
            return response

    def remove_file(self, file_path):
        """Xóa file sau khi xử lý."""
        os.remove(file_path)
        print(f"File đã xóa: {file_path}")
