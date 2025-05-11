# Data dari DAT_00402360
dat_array = [
    0x00004946, 0x0000cff9, 0x0001a4f5, 0x0001685d, 0x000430cb,
    0x0004a8a4, 0x0004d896, 0x0002d339, 0x0006eb41, 0x00082e3b,
    0x0007cf05, 0x000afe89, 0x000a0122, 0x00056661, 0x000ac88d,
    0x000d5d81, 0x000df251, 0x000df8f9, 0x000dcb9f, 0x00075e79,
    0x0008dfa8, 0x000843e7, 0x0010bb9d, 0x00167771, 0x00151730,
    0x000b07ed, 0x0017d8f0, 0x00147eea, 0x00196d5b, 0x000bd6e5,
    0x000c7c4e, 0x000d958d, 0x001d0a1f, 0x000db844, 0x001d3db1
]

# Fungsi untuk merekayasa balik flag
def reverse_engineer(dat_array):
    flag = ""
    for i in range(len(dat_array)):
        multiplier = 2 * i + 1
        value = dat_array[i] // multiplier  # Integer division
        c1 = value // 256
        c2 = value % 256
        if 32 <= c1 <= 126 and 32 <= c2 <= 126:  # Printable ASCII
            flag += chr(c1) + chr(c2)
        else:
            print(f"Invalid characters at index {i}: c1={c1}, c2={c2}")
            return None
    return flag

# Jalankan dan cetak flag
flag = reverse_engineer(dat_array)
if flag:
    print(f"Flag: {flag}")
else:
    print("Gagal merekayasa balik flag.")