import os
import sys
import shutil
import zipfile

source_dir_path = "/Users/kai/Downloads/MySQL原理分析"
file_name_order = []
dir_name = "mysql"
args = sys.argv[1:]
if args:
    source_dir_path, dir_name = args[0] or source_dir_path, args[1] or dir_name

current_dir_path = os.getcwd()
saved_dir_path = os.path.join(current_dir_path, dir_name)
if not os.path.exists(saved_dir_path):
    os.mkdir(saved_dir_path)

# 解压缩zip文件
for zip_fn in os.listdir(source_dir_path):
    if os.path.isdir(os.path.join(source_dir_path, zip_fn)):
        shutil.copytree(os.path.join(source_dir_path, zip_fn), os.path.join(saved_dir_path, zip_fn))
    if not zip_fn.endswith(".zip"):
        continue
    n = len(zip_fn)
    with zipfile.ZipFile(os.path.join(source_dir_path, zip_fn)) as f:
        f.extractall(path=os.path.join(saved_dir_path, zip_fn[0:n - 4]))
    # os.remove(os.path.join(path, zip_fn))

# 调用rename，组织文件名称
for folder_name in os.listdir(saved_dir_path):
    if not os.path.isdir(os.path.join(saved_dir_path, folder_name)):
        continue
    file_name_order.append(folder_name)
    for md_name in os.listdir(os.path.join(saved_dir_path, folder_name)):
        if not md_name.endswith(".md"):
            continue
        os.rename(os.path.join(saved_dir_path, folder_name, md_name),
                  os.path.join(saved_dir_path, folder_name, folder_name + ".md"))

# 构造排序前缀
n = len(file_name_order)
for i in range(len(file_name_order)):
    name = file_name_order[i]
    v = name.split(" ", 1)
    if 2 != len(v):
        continue
    order, s = name.split(" ", 1)
    name = (len(str(n)) - len(order)) * "0" + order + " " + s
    file_name_order[i] = name

# 排序
names = sorted(file_name_order, key=lambda x: x[0:len(str(n))])

rows = [f"* [{dir_name}]\n"]
# 输出所需的markdown文本
for i in range(len(names)):
    # * [第一节 sql](sql/一条SQL语句是怎么执行的.md)
    name = names[i]
    row = f"    * [{name}]({dir_name}/{name}/{name + '.md'})\n"
    print(row)
    rows.append(row)

# 追加写入文件
with open("./SUMMARY.md", "a+", encoding="utf-8") as f:
    f.writelines(rows)

print(f"Success!\nThe output dir: {saved_dir_path}\n")
