import os
import time
import ctypes
import requests
import subprocess
import re

# Cấu hình đường dẫn
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
# Đường dẫn file hosts trên Github của bạn
GITHUB_HOSTS_URL = "https://raw.githubusercontent.com/palopdt-sketch/hosts/refs/heads/main/hosts"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_version_from_content(content):
    """
    Tìm dòng có dạng '# Version: X.X.X' trong nội dung file
    """
    match = re.search(r"#\s*Version:\s*([^\s\n\r]+)", content)
    if match:
        return match.group(1)
    return None

def flush_dns():
    try:
        subprocess.run(["ipconfig", "/flushdns"], check=True, capture_output=True)
        print("Đã làm mới bộ nhớ đệm DNS (Flush DNS).")
    except Exception as e:
        print(f"Lỗi khi flush DNS: {e}")

def update_hosts_logic():
    if not is_admin():
        print("LỖI: Vui lòng chạy script bằng quyền Administrator!")
        return

    try:
        # 1. Lấy nội dung file hosts từ Github
        print("Đang kiểm tra cập nhật từ Github...")
        response = requests.get(GITHUB_HOSTS_URL, timeout=15)
        response.raise_for_status()
        remote_content = response.text
        remote_version = get_version_from_content(remote_content)

        # 2. Kiểm tra file hosts local
        local_content = ""
        if os.path.exists(HOSTS_PATH):
            with open(HOSTS_PATH, "r", encoding="utf-8") as f:
                local_content = f.read()
        
        local_version = get_version_from_content(local_content)

        # 3. So sánh version hoặc kiểm tra sự tồn tại của dòng version
        # Nếu không tìm thấy version local hoặc version khác nhau thì mới update
        if local_version is None:
            print("Không tìm thấy thông tin version trong file hosts local. Đang tiến hành cài đặt mới...")
            should_update = True
        elif local_version != remote_version:
            print(f"Phát hiện version mới: {remote_version} (Hiện tại: {local_version}). Đang cập nhật...")
            should_update = True
        else:
            print(f"File hosts đã ở version mới nhất ({local_version}).")
            should_update = False

        if should_update:
            # Ghi đè file hosts
            with open(HOSTS_PATH, "w", encoding="utf-8") as f:
                f.write(remote_content)
            
            # Làm mới DNS
            flush_dns()
            print("Cập nhật file hosts thành công!")

    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")

if __name__ == "__main__":
    print("Dịch vụ tự động cập nhật hosts đang chạy ngầm (1 phút/lần)...")
    while True:
        update_hosts_logic()
        time.sleep(60)
