import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def call_coder_run(func: str, pkg: str, token: str, args: dict):
    """调用 coder_run API - args 需要序列化为字符串"""
    url = "https://abc.feg.com.tw/BDD/API/AI/chatBot/ntfy/coder_run"
    
    # 关键：args 要序列化为 JSON 字符串
    payload = {
        "func": func,
        "pkg": pkg,
        "token": token,
        "args": json.dumps(args)  # 转为字符串 "{\"a\":1,\"b\":2}"
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        resp = requests.post(url, json=payload, headers=headers, verify=False, timeout=60)
        
        # 不直接打印 resp.text，而是解析 JSON
        try:
            data = resp.json()
            return {
                "success": True,
                "status_code": resp.status_code,
                "data": data
            }
        except:
            # 如果返回的不是 JSON，安全打印
            text = resp.text.encode('utf-8', errors='ignore').decode('utf-8')
            return {
                "success": True,
                "status_code": resp.status_code,
                "raw_response": text 
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# 调用
result = call_coder_run(
    func="",
    pkg="",
    token="",
    args={}
)