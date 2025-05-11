# Web V1 - Web Exploit

## 1. Penjelasan Singkat terkait dengan Challenge
Challenge ini merupakan web exploitation berbasis framework Flask (Python). User diberikan source code project web serta akses ke sebuah URL publik. Aplikasi web menyediakan fitur login, register, dan halaman admin untuk melakukan fetch URL eksternal, namun hanya jika user adalah admin. Tujuan utama dari challenge ini adalah mengakses flag yang terdapat di route `/internal`, yang hanya dapat diakses dari localhost (`127.0.0.1`).

## 2. Cara Pengerjaan

### a. Analisis Source Code
Dari hasil ekstrak file `web-v1.zip`, ditemukan file `main.py` yang berisi aplikasi Flask. Berikut poin penting dari source code:

- **Register Form Injection**
Tidak ada validasi field saat register. Semua field dari `request.form` akan dimasukkan ke dalam object `User`. Dengan ini, attacker bisa menambahkan field `is_admin=1`.

- **Restriksi pada /admin/fetch**
Hanya user dengan `is_admin == '1'` yang dapat mengakses endpoint ini. Endpoint ini bisa melakukan HTTP request ke URL yang disediakan user, dengan catatan URL tersebut **harus** mengandung string `"daffainfo.com"`.

- **Route `/internal`**
Hanya dapat diakses jika `request.remote_addr == '127.0.0.1'`, alias hanya dari localhost.

### b. Eksploitasi

1. **Register Akun Admin**
 Lakukan register dengan form data berikut:

```

username=adminuser
password=adminpass
is_admin=1

```

Karena tidak ada validasi pada field input, nilai `is_admin=1` akan diterima dan disimpan di database.

2. **Login**
Login dengan akun admin yang telah dibuat.

3. **Akses `/admin/fetch`**
Setelah login, navigasi ke halaman `/admin/fetch`.

4. **Bypass Hostname Filter**
Di form `url`, input:

```

[http://localhost:1337/internal?host=daffainfo.com](http://localhost:1337/internal?host=daffainfo.com)

```

Karena validasi hanya memeriksa apakah `"daffainfo.com"` terdapat dalam URL (tanpa melakukan validasi hostname sebenarnya), string ini dapat ditambahkan sebagai query parameter untuk melewati filter.

5. **Flag Diperoleh**
Server akan melakukan HTTP request ke `localhost:1337/internal` dari sisi server (server-side request). Karena request ini berasal dari `127.0.0.1`, maka endpoint `/internal` akan merespons dengan flag.

### c. Output
Setelah submit URL pada form `/admin/fetch`, hasil fetch akan menampilkan:

```
Flag: IFEST13{4b0a3c7d05927b28970fdfffe803e7fb}
```

## 3. Kesimpulan
Challenge ini menggabungkan beberapa kelemahan umum di aplikasi web:

- Tidak adanya validasi input di endpoint register (mass assignment vulnerability).
- Filter URL yang rentan terhadap string injection.
- Server-side request forgery (SSRF) yang memungkinkan attacker mengakses endpoint internal.

Dengan mengeksploitasi celah-celah ini, attacker dapat mem-bypass pembatasan dan mengambil flag dari endpoint internal.
