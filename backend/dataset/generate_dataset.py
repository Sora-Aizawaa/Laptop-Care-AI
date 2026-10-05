"""
Generate laptop_complaints.csv
Template-based synthetic dataset generator for LaptopCare AI.
10 categories x ~60-70 samples = ~650 samples.
"""
import csv
import random

random.seed(42)

TEMPLATES = {
    "overheating": [
        "Laptop saya {panas} dan {mati} setelah dipakai {durasi}",
        "Laptop terasa sangat panas terutama di bagian bawah dan kipas {bising}",
        "Fan laptop {bising} lalu laptop {mati} sendiri",
        "Laptop {mati} tiba tiba ketika sedang main game karena {panas}",
        "Suhu laptop terasa {panas} sekali, sampai bagian keyboard ikut panas",
        "Setelah {durasi} laptop langsung restart karena kepanasan",
        "Laptop saya overheat terus, kipas berputar kencang tapi tetap panas",
        "Kalau dipakai lama laptop jadi {panas} dan performa turun drastis",
        "Laptop mati sendiri pas lagi render video, badannya {panas} sekali",
        "Bagian belakang laptop panas berlebihan dan tiba tiba blank lalu mati",
    ],
    "wifi_problem": [
        "Wifi laptop saya tidak muncul sama sekali di daftar jaringan",
        "Laptop tidak bisa konek ke wifi padahal sinyal full",
        "Wifi adapter tidak terdeteksi setelah update windows",
        "Koneksi wifi sering putus nyambung sendiri",
        "Laptop tidak menemukan jaringan wifi apapun",
        "Icon wifi hilang dari taskbar, tidak bisa connect internet",
        "Wifi terhubung tapi internet tidak bisa dipakai sama sekali",
        "Setiap connect wifi selalu muncul limited access",
        "Driver wifi tidak terbaca di device manager",
        "Laptop cuma bisa internet pakai kabel LAN, wifi tidak berfungsi",
    ],
    "bluetooth_problem": [
        "Bluetooth laptop tidak bisa dinyalakan dari settings",
        "Laptop tidak bisa pairing dengan mouse bluetooth",
        "Bluetooth hilang dari device manager setelah update",
        "Headset bluetooth tidak terdeteksi oleh laptop",
        "Bluetooth sering putus sambung sendiri saat dipakai",
        "Tidak ada opsi bluetooth di pengaturan laptop",
        "Laptop gagal terus saat pairing dengan speaker bluetooth",
        "Bluetooth aktif tapi tidak mendeteksi perangkat lain",
        "Driver bluetooth error terus setiap kali dinyalakan",
        "Bluetooth mouse terputus setiap beberapa menit",
    ],
    "black_screen": [
        "Layar laptop hitam total padahal lampu power menyala",
        "Laptop hidup tapi layar tidak menampilkan apa apa",
        "Layar tiba tiba blank hitam saat sedang dipakai",
        "Laptop menyala, kipas jalan, tapi layar gelap total",
        "Setelah update windows layar jadi hitam terus",
        "Layar laptop mati sendiri padahal laptop masih menyala",
        "Booting normal tapi begitu masuk windows layar langsung hitam",
        "Layar eksternal normal tapi layar laptop tetap hitam",
        "Laptop nyala tapi tidak ada tampilan sama sekali di layar",
        "Layar blank hitam disertai bunyi beep saat dinyalakan",
    ],
    "display_flickering": [
        "Layar laptop berkedip kedip terus menerus",
        "Tampilan layar bergaris garis dan flicker saat dipakai",
        "Layar berkedip terutama saat baterai dipakai tanpa charger",
        "Warna layar berubah ubah dan berkedip secara acak",
        "Layar flicker parah ketika membuka aplikasi berat",
        "Muncul garis horizontal yang berkedip di layar laptop",
        "Layar kadang gelap kadang terang sendiri secara tiba tiba",
        "Tampilan layar bergetar dan tidak stabil terus menerus",
        "Layar berkedip saat brightness dinaikkan atau diturunkan",
        "Muncul flicker warna pelangi di sudut layar laptop",
    ],
    "slow_performance": [
        "Laptop saya sangat lambat ketika membuka aplikasi",
        "Laptop lemot parah padahal cuma buka browser",
        "Performa laptop menurun drastis dari biasanya",
        "Laptop lag terus saat multitasking beberapa aplikasi",
        "Booting laptop lama sekali sampai lima menit lebih",
        "Laptop sering hang dan tidak merespon saat digunakan",
        "Membuka file besar membuat laptop jadi sangat lambat",
        "Laptop lemot terus walaupun sudah restart berkali kali",
        "Task manager menunjukkan CPU selalu penuh seratus persen",
        "Laptop nge lag parah saat streaming atau menonton video",
    ],
    "boot_problem": [
        "Laptop tidak bisa booting masuk windows sama sekali",
        "Windows stuck di logo saat booting terus menerus",
        "Laptop hanya menampilkan blue screen setiap kali dinyalakan",
        "Laptop restart terus menerus tidak bisa masuk ke desktop",
        "Muncul pesan operating system not found saat booting",
        "Laptop mentok di halaman BIOS tidak bisa lanjut boot",
        "Booting laptop selalu gagal dan otomatis restart sendiri",
        "Windows tidak bisa boot setelah mati listrik tiba tiba",
        "Laptop stuck di layar loading windows berjam jam",
        "Setiap dinyalakan laptop langsung masuk automatic repair terus",
    ],
    "battery_not_charging": [
        "Baterai laptop tidak mau mengisi walaupun sudah dicolok charger",
        "Laptop menunjukkan not charging padahal charger terpasang",
        "Baterai laptop cepat habis padahal baru saja di cas",
        "Charger terpasang tapi indikator baterai tidak bertambah",
        "Laptop hanya bisa menyala kalau charger terus tercolok",
        "Persentase baterai turun terus meskipun sedang di charge",
        "Baterai laptop drop drastis dari seratus persen ke nol",
        "Lampu indikator charging menyala tapi baterai tidak terisi",
        "Baterai laptop bocor cepat habis dalam waktu singkat",
        "Charger laptop panas dan baterai tidak kunjung penuh",
    ],
    "storage_problem": [
        "Penyimpanan laptop penuh padahal file tidak terlalu banyak",
        "Laptop menampilkan pesan disk space hampir habis terus",
        "Hardisk laptop berbunyi klik klik lalu sangat lambat",
        "SSD laptop tidak terdeteksi di file explorer",
        "Laptop sering muncul pesan disk error saat startup",
        "Kapasitas penyimpanan laptop cepat penuh tanpa sebab jelas",
        "Laptop lemot karena disk usage selalu seratus persen",
        "File di laptop sering corrupt atau tidak bisa dibuka",
        "Partisi penyimpanan hilang setelah laptop mati mendadak",
        "Hardisk laptop mengeluarkan bunyi aneh dan akses file lambat",
    ],
    "keyboard_problem": [
        "Beberapa tombol keyboard laptop tidak berfungsi sama sekali",
        "Keyboard laptop mengetik huruf yang salah terus menerus",
        "Tombol keyboard terasa macet dan susah ditekan",
        "Keyboard laptop tidak merespon sama sekali saat diketik",
        "Lampu keyboard menyala tapi tombol tidak berfungsi",
        "Tombol spasi pada keyboard laptop tidak bisa ditekan",
        "Keyboard sering double input padahal hanya ditekan sekali",
        "Beberapa huruf di keyboard hilang atau kotor sehingga tidak terbaca",
        "Keyboard laptop error setelah tidak sengaja terkena air",
        "Tombol angka di keyboard laptop tidak berfungsi seluruhnya",
    ],
}

FILLERS = {
    "panas": ["panas sekali", "sangat panas", "panas berlebihan", "sangat hangat sekali"],
    "mati": ["mati sendiri", "tiba tiba mati", "shutdown sendiri", "mati mendadak"],
    "durasi": ["sekitar 30 menit", "1 jam", "beberapa menit", "setengah jam", "dua jam"],
    "bising": ["sangat berisik", "berputar sangat kencang", "bunyi kencang sekali"],
}

def fill(template: str) -> str:
    out = template
    for key, options in FILLERS.items():
        token = "{" + key + "}"
        if token in out:
            out = out.replace(token, random.choice(options))
    return out

def main():
    rows = []
    for label, templates in TEMPLATES.items():
        # base templates
        for t in templates:
            rows.append((fill(t), label))
        # generate extra variations by re-filling templates with fillers multiple times
        for _ in range(50):
            t = random.choice(templates)
            filled = fill(t)
            rows.append((filled, label))

    random.shuffle(rows)
    with open("laptop_complaints.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "label"])
        writer.writerows(rows)
    print(f"Generated {len(rows)} rows across {len(TEMPLATES)} categories")

if __name__ == "__main__":
    main()
