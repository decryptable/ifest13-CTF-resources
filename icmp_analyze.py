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