import time
import ctypes
import requests
import hashlib

# --- CẤU HÌNH ---
GITHUB_THONGBAO_URL = "https://raw.githubusercontent.com/palopdt-sketch/hosts/refs/heads/main/thongbao.txt"
CHECK_INTERVAL = 10  # Kiểm tra mỗi 30 giây

MB_OK            = 0x0
MB_ICONWARNING   = 0x30
MB_SYSTEMMODAL   = 0x1000  # Luôn hiện trên cùng

def show_popup(title: str, message: str):
    ctypes.windll.user32.MessageBoxW(
        0, message, title,
        MB_OK | MB_ICONWARNING | MB_SYSTEMMODAL
    )

def get_content_hash(text: str) -> str:
    return hashlib.md5(text.strip().encode("utf-8")).hexdigest()

def fetch_content() -> str | None:
    try:
        # Thêm timestamp vào URL để bypass cache của GitHub CDN
        url = f"{GITHUB_THONGBAO_URL}?t={int(time.time())}"
        resp = requests.get(url, timeout=10, headers={"Cache-Control": "no-cache"})
        if resp.status_code == 200:
            return resp.text
        else:
            print(f"[!] HTTP {resp.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"[!] Lỗi kết nối: {e}")
        return None

def check_and_notify(last_hash: str) -> str:
    content_raw = fetch_content()
    if content_raw is None:
        return last_hash

    content = content_raw.strip()
    print(f"[~] Nội dung hiện tại: '{content[:60]}'" if content else "[~] File đang trống")

    if not content:
        return last_hash

    current_hash = get_content_hash(content)

    if current_hash != last_hash:
        print(f"[+] Thông báo mới! Đang hiện popup...")
        show_popup("📢 Thông báo từ Ba", content)
        return current_hash
    else:
        print("[=] Nội dung chưa thay đổi, chờ tiếp...")

    return last_hash

if __name__ == "__main__":
    print("=== Dịch vụ thông báo đang chạy ngầm ===")
    print(f"Kiểm tra mỗi {CHECK_INTERVAL} giây...\n")

    last_known_hash = ""

    # Lần đầu: ghi nhận hash hiện tại KHÔNG hiện popup
    content_raw = fetch_content()
    if content_raw and content_raw.strip():
        last_known_hash = get_content_hash(content_raw)
        print(f"[*] Ghi nhận nội dung cũ, chờ nội dung MỚI...\n")
    else:
        print("[*] File đang trống, chờ bạn gõ thông báo trên GitHub...\n")

    while True:
        last_known_hash = check_and_notify(last_known_hash)
        print()
        time.sleep(CHECK_INTERVAL)
