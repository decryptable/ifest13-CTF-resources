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