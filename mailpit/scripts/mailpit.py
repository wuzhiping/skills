#!/usr/bin/env python3
import requests, base64, os, json, sys

API_URL = "http://10.17.1.26:8025/api/v1/send"

def main():
    # 从标准输入读取 JSON
    args = json.load(sys.stdin)
    
    # 构建 payload
    payload = {
        "From": {"Email": args["from_email"], "Name": args.get("from_name", "")},
        "To": [{"Email": e} for e in args["to"]],
        "Subject": args["subject"]
    }
    
    if args.get("text"): payload["Text"] = args["text"]
    if args.get("html"): payload["HTML"] = args["html"]
    if args.get("cc"): payload["Cc"] = [{"Email": e} for e in args["cc"]]
    if args.get("bcc"): payload["Bcc"] = [{"Email": e} for e in args["bcc"]]
    
    # 附件
    if args.get("attachments"):
        payload["Attachments"] = []
        for path in args["attachments"]:
            with open(path, "rb") as f:
                payload["Attachments"].append({
                    "Content": base64.b64encode(f.read()).decode(),
                    "Filename": os.path.basename(path)
                })
    
    # 发送
    try:
        r = requests.post(API_URL, json=payload, headers={"Content-Type": "application/json"})
        print(json.dumps({"success": r.status_code == 200, "status_code": r.status_code, "response": r.text}))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))

if __name__ == "__main__":
    main()
