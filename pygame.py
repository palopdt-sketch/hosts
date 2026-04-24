import os
import time
import ctypes
import requests
import subprocess
import psutil

# --- CẤU HÌNH ĐƯỜNG DẪN GITHUB ---
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
URL_VERSION = "https://raw.githubusercontent.com/Lazy/project/main/version.txt"
URL_HOSTS = "https://raw.githubusercontent.com/Lazy/project/main/hosts"
URL_GAMES = "https://raw.githubusercontent.com/Lazy/project/main/game.txt"
LOCAL_VERSION_FILE = "current_version.txt"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def flush_dns():
    try:
        subprocess.run(["ipconfig", "/flushdns"], check=True, capture_output=True)
    except:
        pass

def get_remote_data(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.text.strip()
    except:
        return None
    return None

def kill_game_processes(game_list_raw):
    """Quét và đóng các game có trong danh sách"""
    if not game_list_raw:
        return
    
    # Chuyển nội dung file thành danh sách, loại bỏ dòng trống
    game_list = [line.strip().lower() for line in game_list_raw.split('\n') if line.strip()]
    
    for proc in psutil.process_iter(['name']):
        try:
            p_name = proc.info['name'].lower()
            # Kiểm tra nếu tên process khớp với bất kỳ dòng nào trong game.txt
            if any(game in p_name for game in game_list):
                proc.kill()
                print(f"Banned game detected and closed: {p_name}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

def run_sync():
    if not is_admin():
        print("Vui lòng chạy với quyền Administrator!")
        return

    # 1. Lấy thông tin từ GitHub
    remote_version = get_remote_data(URL_VERSION)
    game_list_content = get_remote_data(URL_GAMES)
    
    if remote_version is None:
        print("Không thể kết nối GitHub để check version.")
    else:
        # 2. Kiểm tra và cập nhật file Hosts
        current_version = ""
        if os.path.exists(LOCAL_VERSION_FILE):
            with open(LOCAL_VERSION_FILE, "r") as f:
                current_version = f.read().strip()

        if remote_version != current_version:
            print(f"Cập nhật version mới: {remote_version}")
            new_hosts = get_remote_data(URL_HOSTS)
            if new_hosts:
                with open(HOSTS_PATH, "w", encoding="utf-8") as f:
                    f.write(new_hosts)
                with open(LOCAL_VERSION_FILE, "w") as f:
                    f.write(remote_version)
                flush_dns()
                print("Đã cập nhật file hosts và Flush DNS.")

    # 3. Quét và chặn Process Game (Luôn chạy mỗi phút)
    if game_list_content:
        kill_game_processes(game_list_content)

if __name__ == "__main__":
    print("Hệ thống quản lý Game & Hosts đang chạy ngầm...")
    while True:
        run_sync()
        time.sleep(60) # Nghỉ 1 phút
