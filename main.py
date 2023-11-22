import re
import requests
import os
import json
from tqdm import tqdm
from urllib.parse import quote

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

loop = True

def download(url, save_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(block_size):
                progress_bar.update(len(chunk))
                file.write(chunk)
        progress_bar.close()
        return True
    else:
        return False

while(loop):
  os.system('cls' if os.name == 'nt' else 'clear')
  print(YELLOW + '【抖音无水印解析下载助手】' + RESET)
  src = input(GREEN + '请输入抖音作品链接/分享口令(右键粘贴)：' + RESET)
  match1 = re.search(r"https:\/\/v\.douyin\.com\/([a-zA-Z0-9]+)\/", src)
  match2 = re.search(r"\d{5,}", src)
  if match1:
      url = match1.group(0)
  elif match2:
      # url = match2.group(0)
      url = quote(src)
      
  else:
      print(RED + '抖音链接错误，请重新输入' + RESET)
      exit()

  print(GREEN + '正在解析……' + RESET)
  res = requests.get(f'https://api.mu-jie.cc/douyin?url={url}').json()
  print(GREEN + '\n解析成功！' + RESET)
  print(GREEN + '标题：' + RESET + res['data']['title'])
  print(GREEN + '作者：' + RESET + res['data']['author'])
  print(GREEN + 'UID：' + RESET + res['data']['uid'])
  print(GREEN + '日期：' + RESET + str(res['data']['time']))
  print(GREEN + '点赞：' + RESET + str(res['data']['like']))
  print(GREEN + '类型：' + RESET + res['data']['type'] + '\n')

  if res['data']['type'] == '视频':
    type = '视频'
  else:
      type = '图集'
  if res['data']['title'] == '':
      title = f"无标题 - @{res['data']['author']}"
  else:
      title = re.sub(r'[\\/:*?"<>|]', '', res['data']['title']).replace('\n', '')
  cmd = input(GREEN + f'1: 下载{type}\n2: 返回解析\n其他: 退出\n请输入指令：' + RESET)
  if cmd == '1':
      if type == '视频':
          file_path = f'./video/log/{title}.json'
          os.makedirs(os.path.dirname(file_path), exist_ok=True)
          with open(file_path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(res, ensure_ascii=False, indent=2))
          print(GREEN + '\n正在下载视频……' + RESET)
          save_location = "./video/" + title + ".mp4"
          if download(res['data']['url'], save_location):
            print(GREEN + '下载完成！' + RESET)
          else:
              print(RED + '下载失败！' + RESET)
      else:
          file_path = f'./img/{title}/log.json'
          os.makedirs(os.path.dirname(file_path), exist_ok=True)
          with open(file_path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(res, ensure_ascii=False, indent=2))
          print(GREEN + '\n正在下载图集……' + RESET)
          i = 0
          for img in res['data']['images']:
            i += 1
            save_location = f'./img/{title}/{i}.jpg'
            download(img, save_location)
          if i == len(res['data']['images']):
              print(GREEN + '下载完成！' + RESET)
          else:
              print(RED + '下载失败！' + RESET)
      if input(GREEN + f'\n1: 返回解析\n其他: 退出\n请输入指令：' + RESET) == '1':
          loop = True
      else:
          loop = False
  elif cmd == '2':
      loop = True
  else:
      loop = False