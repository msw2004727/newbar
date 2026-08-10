# -*- coding: utf-8 -*-
"""一次生成所有繪本的配音：走訪 books/*/tools/生成配音.py 全部執行一遍"""
import os, sys, subprocess, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
scripts = sorted(set(glob.glob(os.path.join(ROOT, "books", "*", "tools", "生成配音.py"))
                   + glob.glob(os.path.join(ROOT, "books", "*", "生成配音.py"))))

if not scripts:
    print("找不到任何繪本的配音腳本，請確認 books/ 資料夾存在。"); sys.exit(1)

print("=" * 60)
print(f"  找到 {len(scripts)} 本繪本，開始依序生成配音")
print("=" * 60)
fails = []
for i, s in enumerate(scripts, 1):
    book = os.path.basename(os.path.dirname(os.path.dirname(s)))
    print(f"\n【{i}/{len(scripts)}】{book}")
    r = subprocess.run([sys.executable, s] + sys.argv[1:])
    if r.returncode != 0:
        fails.append(book)
print("\n" + "=" * 60)
print("全部完成！" if not fails else "以下繪本有問題，可單獨再跑一次：" + "、".join(fails))
print("=" * 60)
