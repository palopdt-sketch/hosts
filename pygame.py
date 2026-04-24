import os
import time
import ctypes
import requests
import subprocess
import re
import psutil # Cần cài đặt: pip install psutil

# --- CẤU HÌNH ---
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
# File hosts chứa nội dung chặn và dòng # Version: X.X.X
GITHUB_HOSTS_URL = "https://raw.githubusercontent.com/palopdt-sketch/hosts/refs/heads/main/hosts"
# File game.txt chứa danh sách tên process (ví dụ: GenshinImpact.exe)
GITHUB_GAMES_URL = "https://raw.githubusercontent.com/palopdt-sketch/hosts/refs/heads/main/game.txt"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_version_from_content(content):
    """Tìm dòng có dạng '# Version: X.X.X'"""
    match = re.search(r"#\s*Version:\s*([^\s\n\r]+)", content)
    return match.group(1) if match else None

def flush_dns():
    try:
        subprocess.run(["ipconfig", "/flushdns"], check=True, capture_output=True)
        print(">>> Đã Flush DNS.")
    except Exception as e:
        print(f"Lỗi Flush DNS: {e}")

def force_kill_games():
    """Tải danh sách game và ép đóng các tiến trình đang chạy"""
    try:
        resp = requests.get(GITHUB_GAMES_URL, timeout=10)
        if resp.status_code != 200:
            return
        
        # Lấy list game, chuyển về chữ thường để so sánh chính xác
        banned_games = [line.strip().lower() for line in resp.text.splitlines() if line.strip()]
        
        if not banned_games:
            return

        # Duyệt qua các tiến trình đang chạy
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                p_name = proc.info['name'].lower()
                # Kiểm tra xem tên process có chứa từ khóa game nào không
                if any(game in p_name for game in banned_games):
                    p_obj = psutil.Process(proc.info['pid'])
                    p_obj.terminate() # Yêu cầu đóng
                    p_obj.wait(timeout=3) # Chờ 3s nếu không đóng thì kill hẳn
                    p_obj.kill() # Ép buộc đóng (Force Kill)
                    print(f"--- ĐÃ CHẶN GAME: {proc.info['name']} (PID: {proc.info['pid']})")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                continue
    except Exception as e:
        print(f"Lỗi khi quét game: {e}")

def update_hosts_logic():
    if not is_admin():
        print("LỖI: Vui lòng chạy bằng quyền Administrator!")
        return

    try:
        # 1. Kiểm tra cập nhật hosts
        print("\nChecking updates...")
        response = requests.get(GITHUB_HOSTS_URL, timeout=15)
        response.raise_for_status()
        remote_content = response.text
        remote_version = get_version_from_content(remote_content)

        # Đọc local
        local_content = ""
        if os.path.exists(HOSTS_PATH):
            with open(HOSTS_PATH, "r", encoding="utf-8") as f:
                local_content = f.read()
        local_version = get_version_from_content(local_content)

        # So sánh và cập nhật
        if local_version != remote_version:
            print(f"Update detected: {local_version} -> {remote_version}")
            with open(HOSTS_PATH, "w", encoding="utf-8") as f:
                f.write(remote_content)
            flush_dns()
        else:
            print(f"Hosts OK (v{local_version})")

        # 2. Quét và diệt game
        force_kill_games()

    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")

if __name__ == "__main__":
    print("Dịch vụ bảo mật đang chạy ngầm (Chu kỳ 1 phút)...")
    while True:
        update_hosts_logic()
        time.sleep(60)
