# Single source of truth for the edit: voice EDL, captions, SFX cues, scene times.
MAIN_TEMPO = 1.10   # "laju sikit" — voiceover 10% faster (pitch preserved, rubberband)
FB_TEMPO = 1.05     # customer testimonial, 5% faster

# (src_start, src_end, out_start) on the main voiceover — awkward pauses removed
MAIN_SEGS = [
    (0.00, 5.80, 0.10),     # hook
    (7.32, 10.45, 18.83),   # Kalau korang pun nak cuba, cepat check out
    (10.60, 14.08, 21.735), # Stok ... terhad
    (14.14, 17.08, 24.96),  # Cuba korang tengok berapa yang TikTok bagi dekat korang
    (17.10, 18.75, 27.69),  # Tekan beg kuning ni sekarang dan check out
]
# feedback video/audio cut (repeats + echo "Oh mula-mula tak rasa lembut" + double "Tak tipu" removed)
FB_SEGS = [(2.28, 9.00), (12.80, 14.56), (15.90, 16.90)]
FB_OUT = 5.50

def fb_out_segs():
    o = FB_OUT; res = []
    for a, b in FB_SEGS:
        d = (b - a) / FB_TEMPO; res.append((a, b, o)); o += d
    return res

def m(t):
    for a, b, o in MAIN_SEGS:
        if a - 0.05 <= t <= b + 0.05: return round(o + (t - a) / MAIN_TEMPO, 3)
    raise ValueError(t)

def f(t):
    for a, b, o in fb_out_segs():
        if a - 0.05 <= t <= b + 0.05: return round(o + (t - a) / FB_TEMPO, 3)
    raise ValueError(t)

FB_END = fb_out_segs()[-1][2] + (FB_SEGS[-1][1] - FB_SEGS[-1][0]) / FB_TEMPO   # ~14.53
EDU = (round(FB_END, 2), 18.83)
END = (29.19, 31.80)
TOTAL = 31.80

# Captions: (kind, [(word, src_start, src_end, is_keyword)]) ; kind: "vo" main, "fb" customer, "q" interviewer
K = True
CAPS = [
    ("vo", m, [("selepas", 1.18, 1.70, 0), ("cuba", 1.70, 2.10, 0), ("FRESCURA", 2.10, 2.52, K), ("BODY", 2.52, 2.82, K)]),
    ("vo", m, [("korang", 2.86, 3.54, 0), ("kena", 3.54, 3.74, 0), ("tengok", 3.74, 4.20, 0), ("sendiri", 4.20, 4.44, 0)]),
    ("vo", m, [("feedback", 4.44, 5.12, K), ("mereka", 5.12, 5.44, 0), ("ini.", 5.44, 5.76, 0)]),
    ("q", f, [("Rasa", 2.32, 2.68, 0), ("apa", 2.68, 2.82, 0), ("testing", 2.82, 3.08, 0), ("kita", 3.08, 3.38, 0), ("bagi", 3.38, 3.72, 0), ("tu?", 3.72, 3.84, 0)]),
    ("fb", f, [("Alhamdulillah,", 3.84, 4.58, 0), ("rasa", 4.58, 4.84, 0), ("dia", 4.84, 5.16, 0)]),
    ("fb", f, [("lembut", 5.16, 5.52, K), ("sangat.", 5.52, 5.78, 0)]),
    ("fb", f, [("Mula-mula", 5.78, 6.70, 0), ("pakai", 6.70, 6.84, 0), ("tu", 6.84, 7.10, 0), ("tak", 7.10, 7.24, 0), ("rasa", 7.24, 7.42, 0), ("sangat,", 7.42, 7.66, 0)]),
    ("fb", f, [("lama-lama", 7.66, 8.34, K), ("dia", 8.34, 8.52, 0), ("rasa", 8.52, 8.64, 0), ("lembut.", 8.64, 9.00, K)]),
    ("q", f, [("Wangi", 12.86, 13.34, 0), ("tak,", 13.34, 13.48, 0), ("Kak?", 13.48, 13.66, 0)]),
    ("fb", f, [("Kalau", 13.66, 13.98, 0), ("yang", 13.98, 14.18, 0), ("ni,", 14.18, 14.28, 0), ("wangi!", 14.28, 14.54, K)]),
    ("fb", f, [("Tak", 15.94, 16.34, 0), ("tipu", 16.34, 16.64, K), ("lah", 16.64, 16.68, 0), ("ni!", 16.68, 16.86, 0)]),
    ("vo", m, [("Kalau", 7.40, 7.96, 0), ("korang", 7.96, 8.52, 0), ("pun", 8.52, 8.68, 0), ("nak", 8.68, 8.84, 0), ("cuba,", 8.84, 9.38, K)]),
    ("vo", m, [("cepat", 9.38, 10.06, 0), ("check", 10.06, 10.18, K), ("out!", 10.18, 10.38, K)]),
    ("vo", m, [("Stok", 10.68, 11.24, 0), ("yang", 11.24, 11.34, 0), ("tinggal", 11.34, 11.68, 0), ("di", 11.68, 11.80, 0), ("TikTok", 11.80, 12.08, K), ("Shop", 12.08, 12.36, K)]),
    ("vo", m, [("memang", 12.36, 12.84, 0), ("sangat-sangat", 12.84, 13.76, 0), ("terhad!", 13.76, 14.04, K)]),
    ("vo", m, [("Cuba", 14.18, 14.62, 0), ("korang", 14.62, 14.84, 0), ("tengok", 14.84, 15.18, 0), ("berapa", 15.18, 15.72, K)]),
    ("vo", m, [("yang", 15.72, 15.96, 0), ("TikTok", 15.96, 16.26, K), ("bagi", 16.26, 16.66, 0), ("dekat", 16.66, 16.80, 0), ("korang.", 16.80, 17.06, 0)]),
    ("vo", m, [("Tekan", 17.14, 17.50, 0), ("beg", 17.50, 17.60, K), ("kuning", 17.60, 17.72, K), ("ni", 17.72, 17.80, 0), ("sekarang", 17.80, 17.94, 0)]),
    ("vo", m, [("dan", 17.94, 18.20, 0), ("check", 18.20, 18.46, K), ("out!", 18.46, 18.62, K)]),
]

def captions():
    out = []
    for kind, fn, words in CAPS:
        ws = [(w, fn(a), fn(b), bool(k)) for w, a, b, k in words]
        out.append({"kind": kind, "words": ws})
    for i, g in enumerate(out):
        g["start"] = g["words"][0][1] - 0.04
        nxt = out[i + 1]["words"][0][1] - 0.04 if i + 1 < len(out) else g["words"][-1][2] + 0.4
        g["end"] = min(g["words"][-1][2] + 0.45, nxt)
    # hook: captions start once kinetic hook headline clears
    out[0]["start"] = 1.55
    return out

# SFX cues: (name, time, gain_dB)
def sfx_cues():
    w = lambda t: t
    return [
        ("impact", 0.00, -3), ("glitch", 0.02, -12), ("riser", -0.0, -99),
        ("whoosh", 1.50, -7), ("shimmer", 1.62, -10), ("sparkle", 2.05, -11),
        ("swish", 2.62, -6), ("drop", 2.66, -6), ("pop", 2.80, -9), ("pop", 3.93, -10),
        ("riser", 3.95, -9), ("whoosh", 5.32, -5), ("impact", 5.48, -8),
        ("tap", 5.60, -10),
        ("sparkle", f(5.16), -8), ("ding", f(5.16), -8),
        ("swish", 8.80, -6), ("bubble", 9.0, -12), ("tick", 9.6, -14), ("tick", 10.2, -14), ("tick", 10.8, -14),
        ("ding", 11.55, -9), ("swish", 11.88, -6),
        ("pop", 12.78, -9), ("shimmer", f(14.28), -9), ("sparkle", f(14.28), -10),
        ("stamp", f(15.96), -3), ("whoosh", EDU[0] - 0.22, -6),
        ("impact", EDU[0], -10), ("pop", EDU[0] + 0.15, -10),
        ("tick", EDU[0] + 0.75, -8), ("pop", EDU[0] + 0.78, -8),
        ("tick", EDU[0] + 1.45, -8), ("pop", EDU[0] + 1.48, -8),
        ("tick", EDU[0] + 2.15, -8), ("pop", EDU[0] + 2.18, -8),
        ("bubble", EDU[0] + 2.8, -9), ("sparkle", EDU[0] + 3.0, -12),
        ("whoosh", EDU[1] - 0.25, -5), ("impact", EDU[1], -6),
        ("pop", m(8.84), -8), ("tap", m(10.06), -6), ("ding", m(10.10), -9),
        ("swish", 21.70, -6), ("drop", 21.73, -7),
        *[("tick", 22.0 + i * 0.25, -13) for i in range(10)],
        ("glitch", m(13.76), -5), ("impact", m(13.76), -9),
        ("whoosh", 24.90, -6), ("pop", 25.05, -8), ("kaching", m(15.18), -6), ("sparkle", m(15.96), -10),
        ("swish", 27.63, -6), ("pop", 27.75, -6), ("tap", m(17.50), -3), ("bubble", m(17.52), -13),
        ("ding", m(18.20), -8),
        ("riser", END[0] - 1.2, -14), ("impact", END[0], -4), ("shimmer", END[0] + 0.1, -7), ("sparkle", END[0] + 0.5, -10),
    ]

if __name__ == "__main__":
    import json
    print("FB_END", FB_END, "EDU", EDU)
    for g in captions(): print(round(g["start"], 2), round(g["end"], 2), g["kind"], " ".join(w[0] for w in g["words"]))
    print({k: m(v) for k, v in dict(cuba=8.84, check=10.06, tiktok=11.80, terhad=13.76, berapa=15.18, tiktok2=15.96, beg=17.50, check2=18.20, end=18.62).items()})
    print({k: f(v) for k, v in dict(lembut=5.16, lama=7.66, lembut2=8.64, wangiQ=12.86, wangi=14.28, tipu=15.96).items()})
