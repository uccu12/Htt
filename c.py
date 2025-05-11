import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Các API proxy miễn phí (bạn có thể thêm nữa)
PROXY_SOURCES = [
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=1000&country=all",
    "https://www.proxy-list.download/api/v1/get?type=http",
]

def fetch_proxies():
    proxies = set()
    for url in PROXY_SOURCES:
        try:
            print(f"🔗 Lấy proxy từ: {url}")
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                for line in res.text.splitlines():
                    line = line.strip()
                    if line and ":" in line:
                        proxies.add(line)
        except Exception as e:
            print(f"⚠️ Lỗi lấy proxy từ {url}: {e}")
    return list(proxies)

def check_proxy(proxy):
    try:
        start = time.time()
        proxy_url = f"http://{proxy}"
        r = requests.get("http://httpbin.org/ip", proxies={"http": proxy_url, "https": proxy_url}, timeout=1)
        duration = (time.time() - start) * 1000
        if r.status_code == 200 and duration < 1000:
            print(f"✔ {proxy} - {int(duration)}ms")
            return proxy
    except:
        pass
    print(f"✖ {proxy}")
    return None

def scan_proxies(proxy_list, max_workers=50):
    good = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(check_proxy, proxy): proxy for proxy in proxy_list}
        for future in as_completed(futures):
            result = future.result()
            if result:
                good.append(result)
    return good

def save_to_file(filename, proxy_list):
    with open(filename, "w") as f:
        for proxy in proxy_list:
            f.write(proxy + "\n")

if __name__ == "__main__":
    print("🚀 Đang tải danh sách proxy...")
    all_proxies = fetch_proxies()
    print(f"🔎 Tổng số proxy lấy được: {len(all_proxies)}")

    print("⚙️ Đang kiểm tra proxy...")
    good_proxies = scan_proxies(all_proxies)

    print(f"\n✅ Proxy hợp lệ: {len(good_proxies)}")
    save_to_file("http.txt", good_proxies)
    print("💾 Đã lưu vào http.txt")
