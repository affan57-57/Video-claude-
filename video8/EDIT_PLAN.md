# Video 8: "Stop! 5 kesilapan masa mandi" (kesilapan → Frescura Body → share → komen)

**Status: PREVIEW v1**, `preview/preview_v1.mp4` (1080x1920, draft, tag PREVIEW). Final akan dirender selepas diluluskan.

- Asal: 62.8 s. Selepas edit: **51.0 s** (49.4 s suara + 1.6 s kad penutup).
- Hook: **"Stop!"** + tapak tangan diangkat (rakaman klien) + papan STOP dicop. Muka: **0.62 s sahaja** (bawah 1 saat), mata ke lensa, hflip. Selepas 4.5 saat pertama, klien membaca skrip di bawah kamera, jadi selebihnya B-roll dan motion graphics sepenuhnya.
- Suara: bilik senyap (lantai ~−46 dBFS). 10 segmen disamakan level → RNNoise + FFT denoise, gate, EQ (kehangatan, potong "box", presence, air), de-esser, compressor ringan, exciter, gandaan tetap −14 LUFS, dipercepat 1.12x tanpa ubah pitch (`voice_studio.sh`). Mix −13 LUFS: suara depan, SFX kuat, muzik lembut.

## Gaya baru: "Mineral Mist" (belum pernah digunakan)
- **Font baru:** **Fraunces** (serif "soft & wonky" optical, tajuk/nombor) + **Sora** (caption tebal 70 px, label). **Palet:** kabus mineral, mutiara, dakwat laut dalam, biru laut, buih, pasir + merah bata untuk amaran.
- **Caption baru:** tanpa kotak; teks dengan halo mutiara (halo gelap pada babak gelap); kata kunci disapu marker biru laut (amaran = merah bata) ketika disebut.
- **Infografik pendidikan:** termometer (merkuri naik ke zon PANAS), dail tekanan (jarum ke KUAT), kaunter pam ×1→×5 + cop "TAK BOLEH!", bar bilas tersekat ~70% + kanta pembesar menunjuk sisa sabun, titisan kelembapan yang surut.
- **Teknik baru:** topeng B-roll **titisan air**/kapsul/bulatan; peralihan **riak air** antara kesilapan; **progress 5 titisan** di atas; **cermin berwap dilap** untuk dedah produk; **orbit bahan** keliling produk; **kad wangian berpusing 3D**; cop **MITOS** (lebih kuat ≠ lebih bersih); **senarai semak ringkasan** dipangkah; kapal terbang kertas **share** ke 3 kawan (+1); **gelembung chat** "baru tahu!".

## Apa yang dibuang
| Masa asal | Dibuang | Sebab |
|---|---|---|
| 0.0–0.7 | senyap | permulaan |
| 1.2–1.4, 4.0–5.0, 10.6–11.0, 16.4–16.8, 21.4–21.8, 27.9–28.3, 34.5–35.1, 50.8–51.2, 58.6–58.9 | jeda | awkward pause |
| jeda dalam ayat (> ~0.2 s) | dirapatkan | pace |

Tiada ulangan/cubaan semula dalam rakaman ini.

## Storyboard (masa selepas edit)
| Masa | Suara | Visual |
|---|---|---|
| 0.00–0.62 | Stop! | **Muka klien (0.62 s)** + tapak tangan + papan STOP dicop |
| 0.62–2.92 | Jangan buat 5 kesilapan ini masa mandi | Pancuran (kabus) + "5" gergasi + "kesilapan" + chip MASA MANDI + 5 titisan |
| 2.92–7.82 | 01 air terlalu panas → kulit kering | B-roll mandi berwap dalam titisan + termometer naik ke PANAS ✕ + chip KULIT KERING |
| 7.82–12.46 | 02 gosok terlalu kuat → lebih kuat lebih bersih | Tangan menggosok + dail tekanan ke KUAT + kad "lebih kuat ≠ lebih bersih" + cop MITOS |
| 12.46–16.48 | 03 sabun berlebihan. Tak boleh tu. | Buih sabun + dispenser dalam bulatan + kaunter pam ×1→×5 + cop TAK BOLEH! |
| 16.48–21.46 | 04 tidak membilas dengan sempurna → sisa sabun | Air pancuran (gelap) + bar BILAS tersekat + kanta pembesar pada sisa sabun |
| 21.46–26.48 | 05 terlupa pelembab → kulit mudah kering | Krim tangan dalam kapsul + titisan kelembapan surut + chip SELEPAS MANDI / MUDAH KERING |
| 26.48–28.52 | Frescura Body hadir dengan kandungan | Cermin berwap dilap → produk berbuih |
| 28.52–30.14 | sea salt… mineral semula jadi | Ombak dari udara + garam laut dalam bulatan + "Sea Salt" + chip |
| 30.14–33.57 | sebagai sebahagian daripada formulasi penjagaan badan | Orbit: SEA SALT / MINERAL / GENTLE FOAMING / 500 ML keliling produk |
| 33.57–36.48 | Ditambah pula dengan wangian berinspirasikan perfume | Semburan perfume + "wangian" + kilauan |
| 36.48–37.94 | seperti Bombshell dan Midnight Fantasy | Kad Woman Glory by Bombshell & Noche by Midnight Fantasy berpusing 3D |
| 37.94–40.30 | untuk menjadikan rutin mandi lebih istimewa | Duo produk atas kayu + kad kaca + riak |
| 40.30–43.30 | Jangan biarkan kawan-kawan korang buat kesilapan yang sama | Senarai 5 kesilapan dipangkah satu-satu |
| 43.30–46.54 | Share video ini supaya lebih ramai tahu… | Telefon + "Share" + kapal terbang kertas ke 3 kawan (+1) |
| 46.54–49.38 | Kalau korang tahu tips ni, komen baru tahu | Gelembung chat → "baru tahu!" + ❤ |
| 49.38–50.98 | (penutup) | Frescura Body, Woman Glory · Noche |

## Perlu pengesahan
- Ayat CTA kedengaran **"Kalau korang tahu tips ni, komen baru tahu"** (disemak dua kali dengan whisper). Mungkin maksudnya "kalau korang *tak* tahu…"; caption ikut apa yang disebut. Kalau mahu ditukar, beritahu.
- "Kandungan **sea salt**": whisper dengar "sisa"; label botol tertulis "Ocean Salt".
- Muka 0.62 s (bawah 1 saat, ikut permintaan terakhir). Borang tulis "2 saat"; kalau mahu 2 saat, beritahu.
- Klien sebut akan hantar gambar produk tambahan. Preview ini guna gambar produk sedia ada; boleh ditukar bila gambar baru sampai.

## Sumber
- B-roll: [Mixkit](https://mixkit.co) (Mixkit Free License): 21766, 10334, 21764, 5321, 21768, 44812, 34517, 44834, 45118, 31745, 22402, 21694, 4915, 39774. Tangan sahaja / tiada kulit terdedah.
- Fon: Fraunces, Sora (SIL Open Font License, google/fonts).
- SFX & muzik: disintesis sendiri (`make_audio.py`: titis, cop, buzz, semburan, riak + kalimba 92 bpm). Komposisi: HyperFrames v0.9.10.

## Cara build semula
```bash
cd video8
python3 -I ../scripts/edit_audio.py src/main.mp4 sh.rnnn audio cuts.json   # snap_win 0.02, quiet_db -36
./voice_studio.sh                                                          # TEMPO=1.12
python3 -I ../scripts/transcribe.py audio/voice16k.wav audio/words_seg.json && cp audio/words_seg.json project/assets/audio/words.json
python3 -I prep_broll.py mixkit project/assets/broll src/main.mp4
python3 -I build.py project
python3 make_audio.py project/assets/audio/voice.wav project/assets/audio
ffmpeg -i project/assets/audio/mix_raw.wav -af loudnorm=I=-13:TP=-1:LRA=9 -ar 48000 project/assets/audio/mix.wav
cd project && npx hyperframes@0.9.10 render -q draft -o ../preview/preview_v1.mp4
```
