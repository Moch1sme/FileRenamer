# 📁 File & Folder Renamer

Aplikasi desktop untuk rename file dan folder secara batch — terinspirasi dari Better File Rename, tapi dengan tambahan dukungan rename **folder** dan antarmuka yang lebih sederhana.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?logo=windows)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Fitur

- **Rename file dan folder** sekaligus (tidak seperti Better File Rename yang hanya file)
- **3 mode rename:**
  - 🔢 Urutan angka — tambah prefix/suffix dengan nomor otomatis, atur padding & step
  - 🔄 Ganti teks — cari dan ganti teks tertentu dalam nama
  - ✏️ Custom template — gunakan variabel `{n}`, `{name}`, `{ext}` bebas
- **Drag & drop** untuk menambah file/folder
- **Urutkan ulang** item dengan drag antar baris
- **Preview** nama baru sebelum diterapkan
- Pilih terapkan ke: file saja, folder saja, atau keduanya

---

## 🚀 Cara Pakai

### Opsi 1 — Langsung jalankan (butuh Python)

```bash
python file_renamer.py
```

### Opsi 2 — Build jadi `.exe` (Windows, sekali saja)

1. Pastikan [Python](https://www.python.org/downloads/) sudah terinstall  
   ⚠️ Centang **"Add Python to PATH"** saat install

2. Download `file_renamer.py` dan `build.bat`, taruh dalam **satu folder**

3. Klik 2x `build.bat` — tunggu 1–2 menit

4. `FileRenamer.exe` siap! Klik 2x untuk buka — tidak perlu Python lagi

---

## 📦 Persyaratan

| Kebutuhan | Versi |
|-----------|-------|
| Python | 3.8 atau lebih baru |
| tkinter | sudah termasuk di Python |
| PyInstaller | diinstall otomatis oleh `build.bat` |

> **Opsional:** Install `tkinterdnd2` untuk drag & drop file dari luar jendela app:
> ```bash
> pip install tkinterdnd2
> ```

---

## 📂 Struktur File

```
📦 file-renamer/
├── file_renamer.py   # Source code utama
├── build.bat         # Script build EXE otomatis (Windows)
└── README.md
```

---

## 🛠️ Mode Rename

### 1. Urutan Angka
Rename file menjadi urutan bernomor dengan format yang bisa dikustomisasi.

| Pengaturan | Keterangan |
|------------|------------|
| Prefix | Teks di awal nama, contoh: `foto_` |
| Suffix | Teks di akhir nama (sebelum ekstensi), contoh: `_2024` |
| Mulai dari | Angka awal urutan |
| Step | Selisih antar nomor |
| Padding | Minimum digit angka, contoh: `2` → `01`, `02` |

**Contoh:** prefix `liburan_`, padding `2`, start `1`
```
IMG_001.jpg  →  liburan_01.jpg
IMG_002.jpg  →  liburan_02.jpg
IMG_003.jpg  →  liburan_03.jpg
```

### 2. Ganti Teks
Cari dan ganti teks tertentu dalam nama file/folder.

**Contoh:** cari `foto`, ganti `gambar`
```
foto_pantai.jpg  →  gambar_pantai.jpg
foto_gunung.jpg  →  gambar_gunung.jpg
```

### 3. Custom Template
Gunakan variabel untuk format nama yang bebas.

| Variabel | Keterangan |
|----------|------------|
| `{n}` | Nomor urut (2 digit) |
| `{name}` | Nama asli file (tanpa ekstensi) |
| `{ext}` | Ekstensi file (tanpa titik) |

**Contoh:** template `{n}_{name}`
```
liburan.jpg  →  01_liburan.jpg
pantai.jpg   →  02_pantai.jpg
```

---


## 📄 Lisensi

[MIT License](LICENSE) — bebas digunakan dan dimodifikasi.

---

## 🤝 Kontribusi

Pull request sangat disambut! Untuk perubahan besar, buka issue terlebih dahulu.

1. Fork repository ini
2. Buat branch baru: `git checkout -b fitur-baru`
3. Commit perubahan: `git commit -m 'Tambah fitur baru'`
4. Push ke branch: `git push origin fitur-baru`
5. Buat Pull Request
# FileRenamer
