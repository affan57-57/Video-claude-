# Video 9: "3 sebab wajib tukar ke Frescura Body" (buih → sea salt → wangian → tekan beg kuning)

**Status: FINAL** (diluluskan klien), `final/video9_3sebab_frescura_1080p.mp4` (1080x1920, `-q delivery`, tanpa tag PREVIEW). Preview: `preview/preview_v1.mp4`.

- Asal: 45.0 s. Selepas edit: **32.5 s** (30.9 s suara + 1.6 s kad penutup).
- Hook: **"Tiga…"** sambil angkat **3 jari**, mata ke lensa. Muka: **0.68 s sahaja** (bawah 1 saat), hflip. Selebihnya B-roll dan motion graphics.
- Suara: bilik senyap (lantai ~−48 dBFS). 10 segmen disamakan level → RNNoise + FFT denoise, gate, EQ, de-esser, compressor ringan, exciter, gandaan tetap −14 LUFS, dipercepat 1.12x tanpa ubah pitch. Mix −13 LUFS: suara depan, SFX kuat, muzik lembut.

## Gaya baru: "Blush & Plum" (belum pernah digunakan)
- **Font baru:** **Gloock** (serif fesyen berkontras tinggi) + **Plus Jakarta Sans** (caption tebal 72 px). **Palet:** blush, krim, plum, mawar (Woman Glory), violet (Noche), champagne; kuning hanya untuk beg kedai.
- **Caption baru:** perkataan muncul satu-satu ikut suara; kata kunci bertukar ke Gloock warna mawar (fon campur).
- **Teknik baru:** tab **SEBAB 01 / 02 / 03**; peralihan **blob organik**; demo **tekan pam** (jari + gelang tap + letupan buih); **perbandingan dua panel** (gosok lama + jam randik dipangkah vs 1× tekan ✓); **kekisi kristal** sea salt; kad kaca **"Sea Salt = Garam Laut"**; **sinar sunburst** "paling best!"; **meter profil wangian** (FRESH / FEMININE, MANIS / FRUITY) atas latar warna wangian; **mockup telefon** dengan butang beg kuning ditekan + bar stok surut; butang **CHECK OUT** → ✓ + konfeti.

## Apa yang dibuang
| Masa asal | Dibuang | Sebab |
|---|---|---|
| 0.0–1.1 | senyap | permulaan |
| 4.1–5.4, 13.0–13.6, 15.7–16.2, 22.6–23.6, 35.7–36.4, 37.6–38.0, 42.1–42.4 | jeda | awkward pause |
| 16.2–16.6 "Yang mana," | dibuang | filler |
| 19.3–20.9 "yang ianya" | dibuang | filler → "…garam laut, kaya mineral semula jadi." |
| jeda dalam ayat | dirapatkan | pace |

"Tekan beg kuning" disebut dua kali (CTA + "dan check out"), jadi kedua-duanya dikekalkan sebagai penegasan, bukan ulangan tersasul.

## Storyboard (masa selepas edit)
| Masa | Suara | Visual |
|---|---|---|
| 0.00–0.68 | Tiga sebab | **Muka klien (0.68 s)** dengan 3 jari + 3 titik pop |
| 0.68–2.70 | …yang wajib korang tukar ke Frescura Body | "3" gergasi mawar + "Frescura Body" + duo produk |
| 2.70–4.83 | 01 tekan je terus berbuih | Produk berbuih; jari tekan pam, gelang tap, letupan buih |
| 4.83–6.62 | Foaming pump, tak payah gosok lama | Gosok lama (jam randik, dipangkah) vs produk 1× TEKAN ✓ |
| 6.62–8.57 | buih lembut terus keluar dari botol | Buih makro + "Buih lembut" + gelembung terapung |
| 8.57–10.27 | 02 ada sea salt | Garam laut + "Sea Salt" + kekisi kristal dilukis |
| 10.27–14.07 | formulasi dengan sea salt ataupun garam laut, kaya mineral semula jadi | Laut jernih + kad "Sea Salt = Garam Laut" + KAYA MINERAL / SEMULA JADI + produk |
| 14.07–15.71 | 03 yang ni yang paling best | Plum + sinar sunburst + "paling best!" + bintang |
| 15.71–18.76 | Wangi dia adalah wangi perfume… | Semburan perfume + "wangi perfume" |
| 18.76–21.32 | Bombshell untuk bau yang fresh dan feminine | Mawar merah + kad Woman Glory by Bombshell + meter FRESH / FEMININE |
| 21.32–24.14 | Midnight Fantasy pula untuk yang suka manis dan fruity | Langit violet + kad Noche by Midnight Fantasy + beri + meter MANIS / FRUITY |
| 24.14–25.30 | Korang nak rasa sendiri tak? | "?" gergasi + buka bungkusan |
| 25.30–28.74 | Tekan beg kuning sekarang sebab stok kita sangat-sangat terhad | Mockup telefon Frescura Body, butang beg kuning ditekan, bar STOK surut + TERHAD! |
| 28.74–30.88 | Tekan beg kuning dan check out | Ikon beg kuning ditekan + butang CHECK OUT → ✓ + konfeti |
| 30.88–32.48 | (penutup) | Frescura Body, Woman Glory · Noche, TEKAN BEG KUNING |

## Nota
- Rakaman telefon (Mixkit 42136) menunjukkan UI kedai/produk lain, jadi ia dikaburkan sepenuhnya sebagai latar sahaja; skrin kedai yang kelihatan ialah mockup Frescura Body sendiri.
- Caption: "Fresh Kura Bodi" → *Frescura Body*, "Forming" → *Foaming*, "minat fantasi" → *Midnight Fantasy*.
- Klien sebut akan hantar gambar produk tambahan; preview ini guna gambar sedia ada.

## Sumber
- B-roll: [Mixkit](https://mixkit.co) (Mixkit Free License): 5321, 44812, 22402, 50236, 21694, 38386, 46203, 10423, 31274, 42136 (dikaburkan).
- Fon: Gloock, Plus Jakarta Sans (SIL Open Font License, google/fonts).
- SFX & muzik: disintesis sendiri (`make_audio.py`, + "ding" beg/checkout; kalimba 98 bpm Fmaj9–Em7–Dm9–G9sus). Komposisi: HyperFrames v0.9.10.

## Cara build semula
```bash
cd video9
python3 -I ../scripts/edit_audio.py src/main.mp4 sh.rnnn audio cuts.json
./voice_studio.sh
python3 -I ../scripts/transcribe.py audio/voice16k.wav audio/words_seg.json && cp audio/words_seg.json project/assets/audio/words.json
python3 -I prep_broll.py mixkit project/assets/broll src/main.mp4
python3 -I build.py project
python3 make_audio.py project/assets/audio/voice.wav project/assets/audio
ffmpeg -i project/assets/audio/mix_raw.wav -af loudnorm=I=-13:TP=-1:LRA=9 -ar 48000 project/assets/audio/mix.wav
cd project && npx hyperframes@0.9.10 render -q draft -o ../preview/preview_v1.mp4
```
