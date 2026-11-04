# Video Awareness: Foaming Body Wash (PREVIEW v1)

**Status: PREVIEW (bukan final).** Video penuh ada di `preview/preview_draft.mp4` (draft, ada tag "PREVIEW").

- Asal: 72.2 s → Edit: **62.4 s** (9:16, 1080x1920)
- Muka anda: **2 saat sahaja** (0:00–0:02, hook). Selebihnya B-roll, animasi dan motion graphics.
- Audio: voice dibersihkan (RNNoise + FFT denoise), EQ studio, de-esser, compressor, dan loudness -14 LUFS (standard TikTok/IG/Reels). Ada muzik latar yang mengecil bila anda bercakap (ducking) dan **~70 sound FX**.

## Apa yang dibuang (ulangan / jeda janggal)
| Masa asal | Dibuang | Sebab |
|---|---|---|
| 6.90–8.04 | "Keluar foaming" | ulangan |
| 8.04–11.10 | "So foaming ni, kalau nak kenalkan kat korang" | filler, lambatkan pace |
| 15.64–16.29 | "Tapi" | ayat dipindah jadi hook |
| 29.68–30.90 | "Tak payah berbuih" | ulangan |
| 34.30–35.58 | "Dan" + jeda 1 saat | awkward pause |
| 66.10–67.46 | "Tekan beg kuning sekarang" (kali ke-2) | ulangan CTA |
| 70.66–72.23 | hujung video | bunyi bising / senyap |

## Hook
Ayat paling kuat ("**Bau dia tu pun macam perfume mewah**") dipindah ke 0:00 dengan teks besar
**"SABUN MANDI BAU MACAM PERFUME MEWAH?!"** + impact SFX. Inilah satu-satunya 2 saat muka anda.

## Storyboard
| Masa | Apa anda cakap | Visual | SFX |
|---|---|---|---|
| 0:00–0:02 | Bau dia macam perfume mewah | Muka (punch-in zoom) + headline hook | impact, sparkle |
| 0:02–0:02.6 | (sambungan) | Reveal produk, "FOAMING BODY WASH" | whoosh, pop |
| 0:02.6–0:04.9 | Biasanya sabun gel... | B-roll sabun gel + chip "SABUN GEL" + ✕ | pop, error |
| 0:04.9–0:06.4 | ...ataupun sabun buku | Animasi sabun buku jatuh + ✕ | pop, error |
| 0:06.4–0:09.3 | Tapi yang ni... foaming | B-roll buih + produk naik + "FOAMING!" | impact, bubbles |
| 0:09.3–0:11.2 | Berbuih yang lembut | Buih pink, "BUIH LEMBUT" | pop |
| 0:11.2–0:14.0 | Kalau pegang, gebu-gebu | B-roll tangan berbuih + awan "GEBU-GEBU" | boing |
| 0:14.0–0:19.4 | Keistimewaan kami... wangian ala perfume | **Kad edukasi** 01/02/03 atas B-roll buih → perfume | click, pop, ding |
| 0:19.4–0:22.2 | Tekan je pump, terus keluar buih | **Infografik pam** (tekan → buih keluar) | click, bubbles |
| 0:22.2–0:25.1 | Tak perlu berbuihkan sendiri | B-roll air shower + ✕ "TAK PERLU" | error |
| 0:25.1–0:30.4 | 2 pilihan wangian | Kad Woman Glory **VS** Noce | impact, ding |
| 0:30.4–0:34.9 | Woman Glory: fresh, floral, feminine | B-roll bunga + chip nota wangian | pop x3 |
| 0:34.9–0:37.8 | Noce: sweet, fruity | B-roll strawberi + chip | pop x2 |
| 0:37.8–0:44.0 | Tanpa paraben, tanpa bahan berbahaya | **Checklist edukasi** atas B-roll makmal (+ nota "paraben = bahan pengawet") | stamp x2 |
| 0:44.0–0:47.4 | Telah menjalani ujian makmal | B-roll saintis + cop "UJIAN MAKMAL ✓ DIUJI" | stamp |
| 0:47.4–0:51.0 | Pengalaman mandian lebih istimewa | B-roll shower + "LEBIH ISTIMEWA" | sparkle, ding |
| 0:51.0–0:53.0 | Korang kena try | Hero produk + sinar berputar, "WAJIB TRY!" | riser, impact |
| 0:53.0–0:59.0 | Tekan beg kuning, stok terhad | B-roll telefon (blur) + butang bakul kuning + bar "STOK SANGAT TERHAD" | click, cash, tick |
| 0:59.0–1:02.4 | Pilih wangian favourite, cepat check out | CTA akhir: 2 wangian + butang "CHECK OUT SEKARANG" | pop, cash, ding |

Caption gaya karaoke (perkataan muncul ikut suara, kata kunci warna kuning) sepanjang video.

## Perlu pengesahan anda sebelum FINAL
1. **Nama jenama**: Whisper dengar "try *fresh kurwa body*". Apa ejaan tepat nama produk? (sekarang tak dipaparkan dalam caption)
2. **Wangian kedua**: ejaan "**Noce**" betul?
3. **Ayat ujian**: "telah menjalani ujian *makmal ... bayu*?" Apa sebenarnya ayat penuh? (sekarang caption tunjuk "UJIAN MAKMAL" sahaja)
4. **Gambar produk**: sila upload. Sekarang guna crop botol dari video anda sebagai placeholder (kad produk di 0:02, 0:07, 0:51).

## Sumber
- B-roll: [Mixkit](https://mixkit.co) (Mixkit Free License, boleh guna untuk komersial). Klip yang dedah kulit/bahu sengaja dielak.
- SFX & muzik latar: disintesis sendiri (`scripts/make_audio.py`), tiada isu hak cipta.
- Komposisi: [HyperFrames](https://hyperframes.heygen.com) v0.9.10 (`hf/project/`).

## Cara build semula
```bash
python3 -I scripts/transcribe.py audio16k.wav words.json         # faster-whisper large-v3-turbo
python3 -I scripts/edit_audio.py source.mp4 sh.rnnn OUT/          # potong + studio voice
python3 -I scripts/prep_broll.py source.mp4 mixkit/ hf/project/assets/broll
python3 -I scripts/make_audio.py voice.wav hf/project/assets/audio   # SFX + muzik + mix (needs sfx_cues.json)
ffmpeg -i hf/project/assets/audio/mix_raw.wav -af loudnorm=I=-14:TP=-1:LRA=9 -ar 48000 hf/project/assets/audio/mix.wav
python3 -I scripts/build_composition.py hf/project [--final]
cd hf/project && npx hyperframes render -q draft -o ../../preview/preview_draft.mp4
```
