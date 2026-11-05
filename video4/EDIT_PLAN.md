# Video 4: "Perempuan ada dua jenis" (Bombshell vs Midnight Fantasy)

**Status: PREVIEW**, `preview/preview_v1.mp4` (1080x1920, draft, tag PREVIEW). Final akan dirender selepas diluluskan.

- Asal: 58.9 s. Selepas edit: **49.0 s** (47.6 s suara + 1.4 s kad penutup).
- Gaya: **modern motion graphics, minimalist luxury** (ikut Video 3). Latar ivory, Montserrat nipis, garis halus, B-roll dalam bingkai bulat/bucu bulat, caption pil, nombor seksyen 01–05 dan progress bar.
- Muka: **0.86 s sahaja** (2.11–2.97 s, "Hang pun geng mana?"). Tunjuk jari ke penonton, kemudian pandang tepat ke lensa. Rakaman selfie di-hflip supaya logo baju terbaca betul.
- Audio: setiap segmen disamakan ke −20 dBFS sebelum denoise, kemudian RNNoise + FFT denoise, EQ, de-esser, compressor dan loudness −14 LUFS. 24 jeda dirapatkan (5.4 s). Muzik latar minimalis 96 bpm dengan ducking, dan 79 sound FX.

## Apa yang dibuang
| Masa asal | Dibuang | Sebab |
|---|---|---|
| 3.74–5.14 | jeda 1.4 s | awkward pause |
| 15.06–16.96 | "Ok, yang kedua," + jeda | false start (diulang terus: "tim yang kedua") |
| 29.92–30.36 | "Ok," | filler |
| 39.56–40.40 | "Ok," + jeda | filler |
| 24 jeda > 0.2 s | dirapatkan ke 0.12 s | pace |

## Hook
0:00 terus tunjuk kinetic type **"PEREMPUAN, ada 2 jenis"** dengan gambar dua botol dan label MIDNIGHT FANTASY / BOMBSHELL. Kemudian satu-satunya shot muka: **"Hang pun GENG mana?"**.

## Storyboard (masa selepas edit)
| Masa | Suara | Visual | SFX |
|---|---|---|---|
| 0.00–2.11 | Perempuan ada dua jenis | Kinetic type + foto duo botol (latar putih) + label | boom, swoosh, pop |
| 2.11–2.97 | Hang pun geng mana? | **Muka** + "GENG mana?" | swoosh, tick, pop |
| 2.97–4.70 | Pertama, geng Bombshell | No. 01, kad botol Woman Glory, "BOMBSHELL" | boom |
| 4.70–8.30 | fresh, floral, feminine, elegant | B-roll mawar merah + bulatan mawar pink + 4 chip ikut suara | pop ×4, chime |
| 8.30–11.45 | classy, penuh keyakinan | B-roll wanita bertudung tersenyum + "CLASSY & penuh keyakinan" | boom, chime |
| 11.45–13.70 | Tim kedua: geng Midnight Fantasy | Latar ungu malam, No. 02, kad botol Noche | boom, shimmer |
| 13.70–17.55 | manis, fruity | Bulatan strawberi + chip MANIS / FRUITY | pop ×2 |
| 17.55–18.95 | agak misteri | B-roll bulan berkabus, "MISTERI" blur-in | boom, shimmer |
| 18.95–21.50 | paling penting, menggoda | Bulatan hati terapung, "Menggoda" | riser, boom |
| 21.50–23.40 | tapi goda suami je lah | Ikon cincin kahwin + "SUAMI JE tau!" | pop, chime |
| 23.40–25.25 | aura tersendiri | B-roll lavender + cincin aura bercahaya | shimmer, boom |
| 25.25–27.30 | tapi aku nak tahu, betulkah | **Klip pam botol Woman Glory, latar ditukar ke ivory studio** | foam |
| 27.30–31.60 | wangian = personaliti? | Kad edukasi: WANGIAN = PERSONALITI? + jadual Bombshell → classy·yakin / Midnight Fantasy → misteri·aura | boom, click |
| 31.60–35.55 | jangan malu-malu, komen Bombshell | B-roll wanita bertudung dengan telefon + bubble komen "Bombshell!" (taip) | pop, click |
| 35.55–39.90 | komen Midnight Fantasy | Latar bintang + bulatan tangan menaip + bubble "Midnight Fantasy!" | pop, click |
| 39.90–41.10 | tolong share video ni | Latar buih pink + butang SHARE ditekan | pop, click |
| 41.10–47.40 | tanya kawan-kawan, geng mana? | Foto duo botol (kayu) + UI pilihan: pilih Bombshell → Midnight Fantasy | click, pop |
| 47.40–49.00 | (penutup) | FRESCURA BODY: komen BOMBSHELL atau MIDNIGHT FANTASY | chime |

## Perlu perhatian
- Klip pantai asal (`5_6253415165421685938.MP4`) ada teks **"mengawal tekanan darah"** dan **"membuang toksin"** di hujungnya. Dakwaan kesihatan ni tak dapat dibuktikan, jadi bahagian tu **tidak digunakan**.
- Gambar produk tambahan: satu gambar (marmar, 720x1280) labelnya tertulis **"FRESCUAA BODY"**, dan satu lagi tulisan "MIDNIGHT FANTASY" pada labelnya herot. Kedua-duanya tidak digunakan.
- Klip Noche (`5_6059646302818405093.mp4`) dah ada bingkai telefon dan teks, jadi tidak digunakan. Botol Noche ditunjuk melalui gambar produk.

## Sumber
- B-roll: [Mixkit](https://mixkit.co) (Mixkit Free License). Klip: 38386, 40294, 49306, 49311, 16025, 4433, 18802, 1244, 21694, 4915, 4124, 13787. Klip yang dedah kulit dan klip arak dielak.
- SFX & muzik: disintesis sendiri (`video3/make_audio_min.py`).
- Komposisi: HyperFrames v0.9.10 (`video4/project/`).

## Cara build semula
```bash
cd video4
python3 -I ../scripts/edit_audio.py src/main.mov sh.rnnn audio cuts.json
python3 -I ../scripts/transcribe.py audio/voice16k.wav audio/words.json
python3 -I prep_broll.py mixkit project/assets/broll src/main.mov
MATTE_MODEL=isnet-general-use python3 work/matte_fast.py src/pump2.mp4 4.3 6.0 work/matte_pump
LIGHT=1 python3 ../video2/compose_pump.py work/matte_pump project/assets/broll/pump_ivory.mp4 0.5 0.5
python3 -I build.py project            # also writes assets/audio/sfx_cues.json
python3 ../video3/make_audio_min.py project/assets/audio/voice.wav project/assets/audio
ffmpeg -i project/assets/audio/mix_raw.wav -af loudnorm=I=-14:TP=-1:LRA=9 -ar 48000 project/assets/audio/mix.wav
cd project && npx hyperframes@0.9.10 render -q draft -o ../preview/preview_v1.mp4      # final: python3 -I ../build.py . --final; render -q delivery
```
