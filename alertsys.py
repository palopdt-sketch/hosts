import time
import ctypes
import requests
import hashlib

# --- CẤU HÌNH ---
GITHUB_THONGBAO_URL = "https://raw.githubusercontent.com/palopdt-sketch/hosts/refs/heads/main/thongbao.txt"
CHECK_INTERVAL = 30  # Kiểm tra mỗi 30 giây

# Hằng số cho MessageBox Windows
MB_OK                = 0x0
MB_ICONINFORMATION   = 0x40
MB_ICONWARNING       = 0x30
MB_SYSTEMMODAL       = 0x1000   # Luôn hiện lên trên cùng, ưu tiên cao
HWND_BROADCAST       = 0xFFFF

def show_popup(title: str, message: str):
    """Hiện hộp thoại popup trên Windows, luôn nằm trên cùng."""
    ctypes.windll.user32.MessageBoxW(
        0,
        message,
        title,
        MB_OK | MB_ICONWARNING | MB_SYSTEMMODAL
    )

def get_content_hash(text: str) -> str:
    return hashlib.md5(text.strip().encode("utf-8")).hexdigest()

def check_and_notify(last_hash: str) -> str:
    """
    Tải thongbao.txt từ GitHub.
    Nếu có nội dung mới → hiện popup.
    Trả về hash hiện tại.
    """
    try:
        resp = requests.get(GITHUB_THONGBAO_URL, timeout=10)
        if resp.status_code != 200:
            print(f"[!] Không lấy được file (HTTP {resp.status_code})")
            return last_hash

        content = resp.text.strip()

        # Bỏ qua nếu file trống
        if not content:
            return last_hash

        current_hash = get_content_hash(content)

        # Chỉ hiện popup khi nội dung thay đổi so với lần trước
        if current_hash != last_hash:
            print(f"[+] Phát hiện thông báo mới:\n{content}\n")
            show_popup("📢 Thông báo từ Ba", content)
            return current_hash

    except requests.exceptions.RequestException as e:
        print(f"[!] Lỗi kết nối: {e}")

    return last_hash

if __name__ == "__main__":
    print("=== Dịch vụ thông báo đang chạy ngầm ===")
    print(f"Kiểm tra mỗi {CHECK_INTERVAL} giây...\n")

    last_known_hash = ""

    # Lần đầu: ghi nhận hash hiện tại mà KHÔNG hiện popup
    # (tránh hiện lại thông báo cũ khi khởi động lại script)
    try:
        resp = requests.get(GITHUB_THONGBAO_URL, timeout=10)
        if resp.status_code == 200 and resp.text.strip():
            last_known_hash = get_content_hash(resp.text)
            print("[*] Đã ghi nhận nội dung hiện tại, chờ thông báo mới...")
    except Exception:
        pass

    while True:
        last_known_hash = check_and_notify(last_known_hash)
        time.sleep(CHECK_INTERVAL)
