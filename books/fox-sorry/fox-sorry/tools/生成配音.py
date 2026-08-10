# -*- coding: utf-8 -*-
"""《打破的那個杯子》一鍵配音生成器 — 微軟 Edge 神經語音（免註冊、免金鑰、免費）"""
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
    "阿吉": {
        "voice": "zh-TW-HsiaoYuNeural",
        "pitch": 22,
        "vol": 0
    },
    "奶奶": {
        "voice": "zh-TW-HsiaoYuNeural",
        "pitch": -16,
        "vol": -6
    }
}

LINES = [
    ("p1-1", "旁白", "小狐狸阿吉，最喜歡奶奶的藍色杯子。", -14, 0, 0),
    ("p1-2", "旁白", "那個杯子放在櫃子上，奶奶用了好久好久。", -16, 0, 0),
    ("p2-1", "奶奶", "這個杯子啊，比你還老喔。", -26, 0, 0),
    ("p2-2", "旁白", "奶奶每天早上都用它喝茶。", -16, 0, 0),
    ("p3-1", "旁白", "那天下午，餅乾放在櫃子上。", -16, 0, 0),
    ("p3-2", "旁白", "阿吉踮起腳，伸長了手。", -26, 0, 0),
    ("p4-1", "旁白", "叩，", 0, 0, 0),
    ("p4-2", "旁白", "杯子掉下去了。", -36, 0, 0),
    ("p5-1", "旁白", "碎成了三片。", -38, 0, 0),
    ("p5-2", "旁白", "屋子裡好安靜，安靜到聽得見自己的心跳。", -22, 0, 0),
    ("p6-1", "旁白", "阿吉東看看、西看看。", -12, 0, 0),
    ("p6-2", "旁白", "然後把碎片，藏進了櫃子最裡面。", -26, 0, 0),
    ("p7-1", "旁白", "晚餐的時候，奶奶問：", -14, 0, 0),
    ("p7-2", "奶奶", "咦，我的杯子呢？", -22, 0, 0),
    ("p8-1", "阿吉", "……我不知道。", -30, 0, 0),
    ("p8-2", "旁白", "四個字說出口，阿吉的耳朵，燙燙的。", -24, 0, 0),
    ("p9-1", "旁白", "那天晚上，阿吉一直睡不著。", -24, 0, 0),
    ("p9-2", "旁白", "翻過來，翻過去。", -18, 0, 0),
    ("p9-3", "旁白", "櫃子裡的碎片，好像一直在看著他。", -30, 0, 0),
    ("p10-1", "旁白", "天亮了。", -22, 0, 0),
    ("p10-2", "旁白", "阿吉把三片碎片，捧到奶奶面前。", -26, 0, 0),
    ("p11-1", "阿吉", "奶奶……對不起，是我打破的。", -32, 0, 0),
    ("p11-2", "旁白", "奶奶蹲下來，摸摸他的頭。", -24, 0, 0),
    ("p12-1", "旁白", "奶奶把三片碎片，一片一片黏了起來。", -22, 0, 0),
    ("p12-2", "奶奶", "杯子破了可以黏。", -32, 0, 0),
    ("p12-3", "奶奶", "藏起來的話，才會一直破著。", -38, 0, 0),
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
    print("=" * 58); print(f"  《打破的那個杯子》配音生成中 — 共 {len(LINES)} 句"); print("=" * 58)
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
