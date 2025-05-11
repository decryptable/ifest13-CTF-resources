# Freeflag - Reverse Engineering

## 1. Penjelasan Singkat terkait dengan Challenge  
Reverse engineering pada sebuah file binary Linux (format ELF) yang diproteksi menggunakan UPX. Binary ini meminta user untuk memasukkan flag dan kemudian memvalidasi input dengan melakukan operasi matematis terhadap tiap 2 byte karakter flag. Hasil operasi kemudian dibandingkan dengan data tetap yang terdapat di section `.data`.

## 2. Cara Pengerjaan  

### a. Unpacking Binary  
Pertama, file binary `freeflag` di-unpack dari UPX menggunakan perintah:

```bash
upx -d freeflag
````

Output: `freeflag-output` yang siap untuk dianalisis.

### b. Decompile dengan Ghidra

Binary dianalisis menggunakan Ghidra. Pada fungsi validasi utama (`FUN_00401080`) ditemukan bahwa:

* Program membaca input flag.
* Input dibagi per 2 karakter.
* Tiap pasangan karakter dikonversi ke integer (big endian), lalu dikalikan dengan `(index * 2 + 1)`.
* Hasilnya dibandingkan dengan data dari `DAT_00402360`.

### c. Dump Data `.data`

Untuk mengambil isi dari `DAT_00402360`, digunakan perintah `gdb`:

```bash
gdb freeflag-unpacked -ex "x/35xw 0x402360" -ex "quit"

GNU gdb (Debian 16.2-1) 16.2
Copyright (C) 2024 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from freeflag-unpacked...
(No debugging symbols found in freeflag-unpacked)
0x402360:       0x00004946      0x0000cff9      0x0001a4f5      0x0001685d
0x402370:       0x000430cb      0x0004a8a4      0x0004d896      0x0002d339
0x402380:       0x0006eb41      0x00082e3b      0x0007cf05      0x000afe89
0x402390:       0x000a0122      0x00056661      0x000ac88d      0x000d5d81
0x4023a0:       0x000df251      0x000df8f9      0x000dcb9f      0x00075e79
0x4023b0:       0x0008dfa8      0x000843e7      0x0010bb9d      0x00167771
0x4023c0:       0x00151730      0x000b07ed      0x0017d8f0      0x00147eea
0x4023d0:       0x00196d5b      0x000bd6e5      0x000c7c4e      0x000d958d
0x4023e0:       0x001d0a1f      0x000db844      0x001d3db1
```

Didapat array data sebagai berikut:

```python
dat_array = [
    0x00004946, 0x0000cff9, 0x0001a4f5, 0x0001685d, 0x000430cb,
    0x0004a8a4, 0x0004d896, 0x0002d339, 0x0006eb41, 0x00082e3b,
    0x0007cf05, 0x000afe89, 0x000a0122, 0x00056661, 0x000ac88d,
    0x000d5d81, 0x000df251, 0x000df8f9, 0x000dcb9f, 0x00075e79,
    0x0008dfa8, 0x000843e7, 0x0010bb9d, 0x00167771, 0x00151730,
    0x000b07ed, 0x0017d8f0, 0x00147eea, 0x00196d5b, 0x000bd6e5,
    0x000c7c4e, 0x000d958d, 0x001d0a1f, 0x000db844, 0x001d3db1
]
```

### d. Reverse Engineering dengan Python

Script Python untuk membalik proses validasi:

```python
def reverse_engineer(dat_array):
    flag = ""
    for i in range(len(dat_array)):
        multiplier = 2 * i + 1
        value = dat_array[i] // multiplier
        c1 = value // 256
        c2 = value % 256
        if 32 <= c1 <= 126 and 32 <= c2 <= 126:
            flag += chr(c1) + chr(c2)
        else:
            print(f"Invalid characters at index {i}: c1={c1}, c2={c2}")
            return None
    return flag

flag = reverse_engineer(dat_array)
print(f"Flag: {flag}")
```

Output:

```
Flag: IFEST13{w3ll_n07h1n9_1z_fr33_1n_l1f3_s0_7h15_1z_n07_s0_fr33_4f73r_4ll}
```

## 3. Kesimpulan

Dengan memahami mekanisme validasi flag dalam binary dan membaca data dari memory, kita dapat membalik proses enkripsi sederhana tersebut.