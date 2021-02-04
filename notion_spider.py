import time

import requests

client = requests.session()

# 任务请求，返回taskID
enqueueTaskUrl = "https://www.notion.so/api/v3/enqueueTask"
# 获取下载链接，需要返回success
getTaskUrl = "https://www.notion.so/api/v3/getTasks"

# 文章的链接后缀
blockId = ""
# cookies中的token_v2字段
token_v2 = ""

headers = {
    "content-type": "application/json",
    "accept": "*/*",
    "content-security-policy": "application/json; charset=utf-8",
}

cookies = {
    "token_v2": token_v2,
    "origin": "https://www.notion.so",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36"
}


def get_space():
    url = "https://www.notion.so/api/v3/getSpaces"
    resp = client.post(url, cookies=cookies, headers=headers)
    if resp.status_code == 200:
        resp = resp.json()
        headers.update({"x-notion-active-user-header": list(resp.keys())[0]})


def get_taskId():
    request_params = {"task": {"eventName": "exportBlock", "request": {"blockId": blockId, "recursive": True, "exportOptions": {"exportType": "markdown", "timeZone": "Asia/Shanghai", "locale": "en"}}}}
    resp = client.post(enqueueTaskUrl, json=request_params, headers=headers, cookies=cookies)
    task_id = resp.json()["taskId"]
    return task_id


def query_task(task_id):
    url = "https://www.notion.so/api/v3/getTasks"
    params = {"taskIds": [task_id]}
    resp = client.post(url, cookies=cookies, headers=headers, json=params)
    if resp.status_code == 200:
        content = resp.json()["results"][0]
        state = content["state"]
        if state == "in_progress":
            return False, ""
        if state == "success":
            return True, content["status"]["exportURL"]


def get_download_url():
    task_id = get_taskId()
    while True:
        state, download_url = query_task(task_id)
        if not state:
            time.sleep(0.5)
            continue
        return download_url


def get_file(download_url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36",
        "Sec-Fetch-Dest": "Document",
        "Host": "s3.us-west-2.amazonaws.com",
        "sec-ch-ua": '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"'
    }

    resp = client.get(download_url, headers=headers)
    with open("file.zip", "wb") as f:
        f.write(resp.content)

get_space()
download_url = get_download_url()
get_file(download_url)
