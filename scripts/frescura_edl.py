# Edit decision list for the FRESCURA BODY awareness ad (all times in seconds).
# Source files: aw = voiceover (3.MOV), fb = customer feedback (F10.MOV), pump = foam b-roll.
VO_TEMPO = 1.10          # voiceover sped up 10% (pitch preserved)

# (out_start, source, src_in, src_out, tempo)
SPEECH = [
    (0.20,  "aw", 0.30, 3.60, VO_TEMPO),    # Kami tak perlu cakap banyak, biar pelanggan sendiri yang cerita.
    (3.35,  "aw", 4.20, 7.72, VO_TEMPO),    # Dengar sampai habis apa yang mereka katakan tentang Frescura Body.
    (6.62,  "fb", 0.10, 2.92, 1.0),         # Tadi kita pergi tester dekat Kak kan, so far Kak rasa macam mana?
    (9.48,  "fb", 4.62, 6.30, 1.0),         # Rasa wangi, lembut.
    (11.20, "fb", 7.66, 9.66, 1.0),         # Memang tak tipulah ni, wangi dan lembut tu?
    (13.24, "fb", 9.90, 11.80, 1.0),        # Allah.. Dah beli, dah beli!
    (22.45, "aw", 9.40, 15.16, VO_TEMPO),   # So korang jangan tunggu lama-lama, stok terhad ... checkout sekarang, tekan beg kuning
    (27.69, "aw", 15.40, 17.46, VO_TEMPO),  # dan tengok ... yang kami bagi dekat korang.
]
# awkward pauses removed: aw 3.60-4.20, aw 7.72-9.40 (1.7 s dead air + noise), aw 15.16-15.40,
# fb 2.92-4.62 (repeated question), fb 6.30-7.66 (echoed "wangi dan lembut")
DURATION = 32.3

SFX = [  # (time, name, gain_db)
    (0.00, "sub_hit", -2), (0.00, "whoosh_fast", -8), (1.25, "whoosh_fast", -10), (1.29, "tick", -10),
    (1.80, "shimmer", -15), (2.95, "swell", -12), (3.28, "whoosh", -7), (3.40, "tick", -11),
    (5.84, "shimmer", -9), (5.84, "sub_hit", -11), (6.45, "swell", -10), (6.60, "whoosh", -6),
    (6.80, "tick", -11), (6.95, "tick", -16), (7.05, "tick", -16), (7.15, "tick", -16), (7.25, "tick", -16), (7.35, "tick", -16),
    (9.46, "whoosh_fast", -10), (9.74, "pop", -6), (10.36, "pop", -6), (10.38, "shimmer", -12),
    (11.18, "whoosh_fast", -11), (12.26, "tick", -11), (13.22, "whoosh_fast", -11), (13.62, "sub_hit", -10), (13.64, "tick", -8),
    (15.12, "whoosh", -5), (15.14, "sub_hit", -7), (15.55, "tick", -9), (16.48, "whoosh_fast", -8), (16.60, "bubbles", -8),
    (18.28, "whoosh_fast", -8), (18.40, "tick", -9), (20.08, "whoosh_fast", -8), (20.20, "shimmer", -9),
    (22.38, "whoosh", -6), (22.45, "tick", -12), (23.81, "alert", -8), (24.72, "tick", -9), (25.30, "tick", -9),
    (26.05, "whoosh_fast", -9), (26.09, "kaching", -6), (26.81, "tap", -4), (27.45, "pop", -5), (27.47, "tap", -6),
    (28.55, "shimmer", -13), (29.10, "riser", -9), (29.72, "sting", -4),
]
