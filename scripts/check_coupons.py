import json
import datetime
import requests

def verify_and_clean():
    with open('coupons.json', 'r', encoding='utf-8') as f:
        coupons = json.load(f)

    active_coupons = []
    now = datetime.datetime.now(datetime.timezone.utc)

    for item in coupons:
        # 1. 检查是否过期
        try:
            exp_date = datetime.datetime.fromisoformat(item['expiresAt'].replace('Z', '+00:00'))
            if exp_date < now:
                print(f"[-] 剔除已过期卡券: {item['brand']} - {item['title']}")
                continue
        except Exception as e:
            print(f"[-] 日期解析异常: {item['brand']}, 错误: {e}")
            continue

        # 2. 检查短链接连通性
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15'
            }
            resp = requests.head(item['universalLink'], headers=headers, allow_redirects=True, timeout=8)
            if resp.status_code >= 400:
                print(f"[-] 链接失效 ({resp.status_code}): {item['brand']}")
                continue
        except Exception as e:
            print(f"[-] 请求异常: {item['brand']}, 错误: {e}")
            continue

        active_coupons.append(item)

    # 导出给 App 使用的最终清单
    with open('active_coupons.json', 'w', encoding='utf-8') as f:
        json.dump(active_coupons, f, ensure_ascii=False, indent=2)
    
    print(f"[+] 巡检完成，可用活券: {len(active_coupons)} 张")

if __name__ == '__main__':
    verify_and_clean()
