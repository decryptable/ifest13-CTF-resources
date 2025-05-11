# Ququerer - FORENSIC

## 1. Penjelasan Singkat terkait dengan Challenge  
Pada challenge ini, peserta diberikan file capture jaringan (`ququerer.pcap`) dan diminta untuk melakukan analisis untuk menemukan flag. Tidak seperti challenge pcap biasa, challenge ini memanfaatkan protokol ICMP sebagai medium penyisipan data yang tidak lazim, yaitu fragmen gambar PNG. Peserta ditantang untuk menyusun kembali data tersebut dan memecahkan informasi tersembunyi di dalamnya.

## 2. Cara Pengerjaan  

### a. Observasi Awal  
Saya tidak menggunakan Wireshark untuk menganalisis file `.pcap`. Sebagai gantinya, saya menggunakan **tshark** (CLI dari Wireshark) untuk menyaring dan mengekstrak semua payload dari protokol ICMP:

```bash
tshark -r ququerer.pcap -Y "icmp" -T fields -e data.data > icmp_payload.txt
````

### b. Analisis Payload ICMP

Setelah ditelaah, ditemukan bahwa sebagian payload ICMP mengandung signature file PNG:

```
89 50 4E 47 0D 0A 1A 0A
```

dan diakhiri dengan:

```
00 00 00 00 49 45 4E 44 AE 42 60 82
```

Menunjukkan bahwa file `.pcap` ini menyisipkan file PNG secara tersembunyi dalam ICMP echo packet.

### c. Rekonstruksi File PNG

Dengan menggunakan Python, saya memproses file `icmp_payload.txt` untuk:

1. Menggabungkan seluruh data payload ICMP menjadi satu stream biner.
2. Menemukan semua file PNG yang valid di dalam stream.
3. Menyimpan setiap file PNG ke folder `png_files`.

```python
import re
import os

payload_file = 'icmp_payload.txt' # tshark -r ququerer.pcap -Y "icmp" -T fields -e data.data > icmp_payload.txt          
output_dir = 'png_files'
png_signature = b'\x89PNG\r\n\x1a\n'

# Buat direktori output
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Baca payload
with open(payload_file, 'r') as f:
    lines = f.readlines()

# Gabungkan semua payload
binary_data = b''
for line in lines:
    if line.strip():
        try:
            data = bytes.fromhex(line.replace(':', ''))
            binary_data += data
        except:
            continue

# Cari file PNG
png_files = []
start = 0
while True:
    start = binary_data.find(png_signature, start)
    if start == -1:
        break
    # Cari akhir file PNG (chunk IEND: 00:00:00:00:49:45:4e:44:ae:42:60:82)
    iend = binary_data.find(b'\x00\x00\x00\x00IEND\xae\x42\x60\x82', start)
    if iend == -1:
        break
    end = iend + 12  # Sertakan panjang chunk IEND
    png_files.append(binary_data[start:end])
    start = end

# Simpan file PNG
for i, png_data in enumerate(png_files):
    output_file = os.path.join(output_dir, f'image_{i+1}.png')
    with open(output_file, 'wb') as f:
        f.write(png_data)
    print(f"File PNG disimpan: {output_file}")

# Cetak jumlah file
print(f"Total file PNG ditemukan: {len(png_files)}")
```

Hasilnya, berhasil diekstrak **100 buah file PNG**:

```
Total file PNG ditemukan: 100
```

### d. Penyusunan Gambar

Setelah diperiksa secara manual, terlihat bahwa masing-masing gambar merupakan bagian kecil dari sebuah QR Code. Untuk menyatukan gambar-gambar tersebut, saya menulis script `merge.py` yang menyusun 100 gambar secara vertikal:

```python
from PIL import Image
import os

input_dir = 'png_files'
output_file = 'qr_code.png'

# Dapatkan daftar file PNG
png_files = [f'image_{i}.png' for i in range(1, 101)]
png_files = [os.path.join(input_dir, f) for f in png_files if os.path.exists(os.path.join(input_dir, f))]

# Buka semua gambar
images = [Image.open(png_file) for png_file in png_files]

# Pastikan semua gambar memiliki lebar yang sama
widths = [img.width for img in images]
if len(set(widths)) != 1:
    print("Error: Gambar memiliki lebar berbeda!")
    exit(1)
width = widths[0]
total_height = sum(img.height for img in images)

# Buat kanvas baru
combined_image = Image.new('RGB', (width, total_height))

# Tempel gambar secara vertikal
y_offset = 0
for img in images:
    combined_image.paste(img, (0, y_offset))
    y_offset += img.height

# Simpan kode QR
combined_image.save(output_file)
print(f"Kode QR disimpan: {output_file}")
```

Script tersebut menghasilkan satu gambar akhir bernama `qr_code.png`.

### e. Ekstraksi Flag

Setelah QR code berhasil disusun, saya melakukan scanning menggunakan aplikasi pemindai QR di ponsel, dan hasilnya:

```
Flag: IFEST13{M4ST3R_R3CONSTRUCT0R_PACK3T}
```

## 3. Kesimpulan

Challenge ini menarik karena mengeksplorasi penggunaan protokol ICMP sebagai jalur komunikasi tersembunyi untuk menyisipkan data biner (steganografi jaringan).