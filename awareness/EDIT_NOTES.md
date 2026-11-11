# Video Awareness — Frescura Body (foaming body shower garam laut)

Projek HyperFrames: `film/` (1080×1920, 30 fps, **35 s**). Status: **PREVIEW** — belum render final.

Versi 35 s: tiada muka langsung (suara sahaja), jeda dirapatkan lagi (25 jeda → 0.06 s) dan suara 1.11× lebih laju (pitch & formant kekal, rubberband). Suara 34.2 s + CTA. Masa dalam jadual di bawah ialah versi 42 s asal; semua babak, kapsyen dan SFX telah dipetakan semula ke garis masa 35 s (`tools/retime.py`).

## Transkrip (selepas buang jeda janggal)

| Masa | Ayat |
| --- | --- |
| 0.00 | Lepas mandi, kulit rasa kering dan bau sabun cepat hilang. *(HOOK)* |
| 3.28 | Jom cuba cara lain. |
| 4.78 | Frescura Body ialah foaming body shower yang mengandungi garam laut. |
| 8.54 | Garam laut kaya mineral semula jadi dan sejak dulu digunakan dalam penjagaan kulit. |
| 14.14 | Ia bantu kulit terasa lebih lembut selepas mandi. |
| 17.38 | Frescura Body digabungkan dengan perfume. |
| 19.76 | Jadi setiap kali mandi, badan berbau wangi. |
| 22.54 | Ada dua pilihan: Woman Glory Bombshell dan Midnight Fantasy. |
| 26.20 | Bombshell manis dan menyerlah. |
| 28.06 | Adapun Noche Midnight Fantasy, baunya lebih lembut dan misteri. |
| 32.82 | Stok batch ini sangat-sangat terhad. |
| 34.66 | Kalau dah lama nak cuba, jangan tunggu sampai habis. |
| 37.92 | Klik link di bawah dan order sekarang. *(CTA)* |

Jeda dibuang: 11 jeda janggal (paling panjang 1.0 s sebelum "Adapun Noche", 0.8 s dalam "dan… Midnight Fantasy"), kemudian 25 jeda kecil dirapatkan. 42.6 s → 37.9 s → 34.2 s (tempo 1.11×).

## Babak

| Babak | Masa | Visual | Motion graphics | SFX |
| --- | --- | --- | --- | --- |
| s01 hook | 0–3.28 | air shower gelap → kulit kering → wajah di sebalik kaca basah | "KULIT KERING?" (frame 0), retak kulit, meter wangian 100%→8% | impact, whoosh ×2 |
| s02 | 3.28–4.75 | buih naik (gelap) | cincin emas, zoom-through | whoosh, sparkle, riser impact |
| s03 produk | 4.75–8.50 | **cutout pump + buih** atas pentas burgundy-emas (latar pantai dibuang) | nama produk, chip FOAMING BODY SHOWER, + GARAM LAUT, kilauan | impact, pop ×2 |
| s04 edukasi | 8.50–14.12 | ombak dari udara → dataran garam → penjagaan kulit | jubin mineral Mg/Ca/K, "Semula Jadi", garis masa DULU→KINI | whoosh, pop/click ×3 |
| s05 | 14.12–17.36 | kulit dekat → **cutout buih di tapak tangan** atas latar champagne | huruf "lembut" satu-satu, zarah cahaya | whoosh, sparkle |
| s06 | 17.36–22.50 | botol perfume (gelap) → shower berkabus | "Garam Laut + PERFUME", kabus, gelombang wangian | whoosh, ping |
| s07 | 22.50–26.20 | pentas gelap | "2 PILIHAN", kad Bombshell & Noche | impact, whoosh ×2 |
| s08 | 26.20–28.06 | mawar → dakwat merah | BOMBSHELL, tag MANIS / MENYERLAH | pop, click |
| s09 | 28.06–32.75 | bandar malam → cecair ungu | kad klip Noche, tag LEMBUT / MISTERI | whoosh, sparkle |
| s10 | 32.75–37.90 | buih (gelap) | STOK terhad, cop SANGAT-SANGAT, bar baki stok 100%→5% | impact, ping |
| s11 CTA | 37.90–42.00 | pentas emas | 2 produk, butang ORDER SEKARANG ditekan, anak panah "klik link di bawah" | whoosh, click, sparkle |

## Audio

- Suara: DeepFilterNet3 (bunyi bising −14 dB), EQ studio (buang muddy 250 Hz, presence 3 kHz, air 10 kHz), de-esser, compressor, tempo 1.11×, −17.5 LUFS. Campuran akhir −13.6 LUFS, puncak −1.0 dBTP.
- Muzik: "Hazy After Hours" — Alejandro Magaña, Mixkit Stock Music Free License, masuk pada groove penuh (15 s).
- SFX: perpustakaan HyperFrames terbina dalam; puncak setiap bunyi diselaraskan dengan gambar.

## Sumber visual

- B-roll: Mixkit (lesen percuma Mixkit), dipotong menegak 9:16. ID klip: 34517, 46044, 42916, 178, 2091, 20980, 51185, 16428, 20766, 42914, 171, 41999, 44821, 49878, 51885.
- Produk: video pump Bombshell (latar dibuang dengan BiRefNet), klip Noche (dipotong dari video promo).

## Perlu pengesahan

1. Jenama: FRESCURA BODY (disahkan).
2. Tiada muka langsung — suara sahaja (seperti diminta).
3. Gambar produk: botol Bombshell & Noche dipotong dari foto studio pelanggan; logo FRESCURA BODY dalam CTA.

## Bina semula

```bash
# alat audio/cutout: tools/ (tx.py transkrip, run_df.py denoise, cutpauses.py buang jeda, rb.py cutout, mkwebm.sh alpha WebM)
cd film && npx hyperframes check && npx hyperframes render -o renders/final.mp4 --quality delivery
```
