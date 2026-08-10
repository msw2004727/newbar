# -*- coding: utf-8 -*-
"""《熊媽媽的圍巾》一鍵配音生成器 — 微軟 Edge 神經語音（免註冊、免金鑰、免費）"""
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
    "呼呼": {
        "voice": "zh-TW-HsiaoYuNeural",
        "pitch": 24,
        "vol": 0
    },
    "媽媽": {
        "voice": "zh-TW-HsiaoYuNeural",
        "pitch": -6,
        "vol": -4
    }
}

LINES = [
    ("p1-1", "旁白", "小熊呼呼有一條圍巾，是媽媽一針一針織的。", -16, 0, 0),
    ("p1-2", "旁白", "圍巾好長好長，可以繞三圈。", -20, 0, 0),
    ("p2-1", "旁白", "只要圍上它，呼呼就什麼都不怕。", -12, 0, 0),
    ("p2-2", "呼呼", "今天我要去很遠很遠的地方！", -4, 0, 0),
    ("p3-1", "旁白", "每天早上，媽媽都幫他圍好才出門。", -16, 0, 0),
    ("p3-2", "媽媽", "繞緊一點，這樣媽媽的手就一直在你身上。", -22, 0, 0),
    ("p4-1", "旁白", "那天下午，呼呼在森林裡追蝴蝶。", -10, 0, 0),
    ("p4-2", "旁白", "追著追著，圍巾從脖子上滑下來了。", -18, 0, 0),
    ("p5-1", "旁白", "回到家門口，呼呼摸摸脖子，", -18, 0, 0),
    ("p5-2", "呼呼", "圍巾呢？", 0, 0, 0),
    ("p6-1", "旁白", "他找遍了草叢，找遍了樹下。", -8, 0, 0),
    ("p6-2", "旁白", "小河邊也找了，石頭後面也找了。", -12, 0, 0),
    ("p6-3", "旁白", "圍巾不見了。", -34, 0, 0),
    ("p7-1", "旁白", "天慢慢黑了。", -26, 0, 0),
    ("p7-2", "旁白", "呼呼蹲在路邊，一直不敢回家。", -24, 0, 0),
    ("p7-3", "呼呼", "媽媽會不會……生氣？", -30, 0, 0),
    ("p8-1", "旁白", "門口的燈亮著。", -22, 0, 0),
    ("p8-2", "旁白", "媽媽站在那裡，張開了手。", -20, 0, 0),
    ("p9-1", "呼呼", "圍巾……我把圍巾弄丟了。", -32, 0, 0),
    ("p9-2", "旁白", "媽媽沒有生氣。她把呼呼抱得好緊好緊。", -24, 0, 0),
    ("p9-3", "媽媽", "圍巾丟了沒關係，媽媽的手還在呀。", -26, 0, 0),
    ("p10-1", "旁白", "那天晚上，媽媽又拿出了毛線。", -20, 0, 0),
    ("p10-2", "旁白", "呼呼靠在旁邊，看著媽媽一針、一針。", -30, 0, 0),
    ("p11-1", "旁白", "織著織著，呼呼睡著了。", -28, 0, 0),
    ("p11-2", "旁白", "夢裡好像有一條，長長長長的圍巾。", -32, 0, 0),
    ("p12-1", "旁白", "新的圍巾織好了，比以前更長。", -14, 0, 0),
    ("p12-2", "旁白", "長到可以繞四圈，", -20, 0, 0),
    ("p12-3", "呼呼", "這一圈，是給媽媽的。", -12, 0, 0),
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
    print("=" * 58); print(f"  《熊媽媽的圍巾》配音生成中 — 共 {len(LINES)} 句"); print("=" * 58)
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
