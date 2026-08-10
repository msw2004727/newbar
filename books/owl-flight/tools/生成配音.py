# -*- coding: utf-8 -*-
"""《飛不起來的咕咕》一鍵配音生成器 — 微軟 Edge 神經語音（免註冊、免金鑰、免費）"""
import asyncio, sys, os, subprocess, shutil
try:
    import edge_tts
except ImportError:
    print("正在安裝語音套件 edge-tts ...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "--upgrade", "edge-tts"])
    import edge_tts

# 角色音色（想換聲音改這裡）
# zh-TW-HsiaoChenNeural 曉臻(女,溫暖) / zh-TW-HsiaoYuNeural 曉雨(女,柔和) / zh-TW-YunJheNeural 雲哲(男,沉穩)
ROLES = {
    "旁白": {
        "voice": "zh-TW-HsiaoChenNeural",
        "pitch": 0,
        "vol": 0
    },
    "咕咕": {
        "voice": "zh-TW-HsiaoYuNeural",
        "pitch": 26,
        "vol": 0
    },
    "老貓頭鷹": {
        "voice": "zh-TW-YunJheNeural",
        "pitch": -14,
        "vol": -6
    }
}

LINES = [
    ("p1-1", "旁白", "咕咕是一隻小貓頭鷹。", -16, 0, 0),
    ("p1-2", "旁白", "他住在森林裡最高的那棵樹上。", -16, 0, 0),
    ("p2-1", "旁白", "天一黑，大家就展開翅膀飛出去。", -10, 0, 0),
    ("p2-2", "旁白", "咻，一下就不見了。", 0, 0, 0),
    ("p2-3", "旁白", "只有咕咕，還站在樹枝上。", -20, 0, 0),
    ("p3-1", "咕咕", "今天一定可以。", -16, 0, 0),
    ("p3-2", "旁白", "他站到樹枝最前面，用力拍拍翅膀。", -12, 0, 0),
    ("p4-1", "旁白", "第一次，", -22, 0, 0),
    ("p4-2", "旁白", "撲通。", -28, 0, 0),
    ("p5-1", "旁白", "第二次，他爬上大石頭。", -14, 0, 0),
    ("p5-2", "旁白", "再一次，撲通。", -26, 0, 0),
    ("p6-1", "旁白", "第三次、第四次、第五次……", -26, 0, 0),
    ("p6-2", "旁白", "咕咕的翅膀好痠，腳也磨破了。", -24, 0, 0),
    ("p6-3", "旁白", "森林好安靜，大家都飛走了。", -28, 0, 0),
    ("p7-1", "咕咕", "我是不是……永遠都飛不起來？", -32, 0, 0),
    ("p8-1", "旁白", "這時候，老貓頭鷹落在旁邊的樹枝上。", -18, 0, 0),
    ("p8-2", "老貓頭鷹", "咕咕，你數過自己跳了幾次嗎？", -30, 0, 0),
    ("p9-1", "咕咕", "……十七次。", -26, 0, 0),
    ("p9-2", "老貓頭鷹", "那就，再跳一次。", -38, 0, 0),
    ("p10-1", "旁白", "咕咕站起來，走回樹枝最前面。", -18, 0, 0),
    ("p10-2", "旁白", "第十八次。", -34, 0, 0),
    ("p11-1", "旁白", "風，剛剛好在那個時候吹過來。", -28, 0, 0),
    ("p11-2", "旁白", "咕咕的腳，沒有碰到地面。", -10, 0, 0),
    ("p12-1", "旁白", "那天晚上，咕咕飛過了整片森林。", -8, 0, 0),
    ("p12-2", "旁白", "原來會飛的秘訣，不是翅膀有多大。", -24, 0, 0),
    ("p12-3", "旁白", "是願意再跳一次。", -30, 0, 0),
]   # (檔名, 角色, 唸稿, 語速%, 額外音高Hz, 額外音量%)

def _book_dir():
    here = os.path.dirname(os.path.abspath(__file__))
    for d in (here, os.path.dirname(here)):
        if os.path.exists(os.path.join(d, "index.html")):
            return d
    return here

OUT = os.path.join(_book_dir(), "audio")
FORCE = "--force" in sys.argv

def fmt(n, u): return f"{'+' if n >= 0 else ''}{n}{u}"

async def one(name, role, text, rate, dp, dv):
    cfg = ROLES[role]
    path = os.path.join(OUT, name + ".mp3")
    if not FORCE and os.path.exists(path) and os.path.getsize(path) > 1200:
        print(f"  - {name}.mp3  已存在，跳過"); return
    c = edge_tts.Communicate(text, cfg["voice"], rate=fmt(rate, "%"),
                             pitch=fmt(cfg["pitch"] + dp, "Hz"), volume=fmt(cfg["vol"] + dv, "%"))
    await c.save(path)
    print(f"  OK {name}.mp3  [{role}] {os.path.getsize(path)/1024:5.1f} KB   {text[:16]}")

async def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 58); print(f"  《飛不起來的咕咕》配音生成中 — 共 {len(LINES)} 句"); print("=" * 58)
    ok, fail = 0, []
    for item in LINES:
        try:
            await one(*item); ok += 1
        except Exception as e:
            fail.append(item[0]); print(f"  X {item[0]}.mp3 失敗：{str(e)[:80]}")
        await asyncio.sleep(0.35)
    print("-" * 58); print(f"完成 {ok} / {len(LINES)} 句 -> {OUT}")
    if fail: print("失敗：" + "、".join(fail) + "（再跑一次會自動補生成）")
    if shutil.which("ffmpeg"):
        print("偵測到 ffmpeg，統一音量中 ...")
        for name, *_ in LINES:
            src = os.path.join(OUT, name + ".mp3")
            if not os.path.exists(src): continue
            tmp = src + ".tmp.mp3"
            r = subprocess.run(["ffmpeg", "-y", "-i", src, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                                "-ar", "44100", "-ac", "1", "-b:a", "96k", tmp], capture_output=True)
            if r.returncode == 0: os.replace(tmp, src)
            elif os.path.exists(tmp): os.remove(tmp)
        print("音量統一完成。")

if __name__ == "__main__":
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
