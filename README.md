# Analisis Refactoring SOLID

## 1. Analisis Pelanggaran SOLID (Sebelum Refactoring)
Pada kode awal (`BadValidatorManager`), ditemukan pelanggaran prinsip SOLID:
* **Single Responsibility Principle (SRP):** Satu kelas menangani terlalu banyak tanggung jawab (validasi SKS dan Prasyarat sekaligus).
* **Open/Closed Principle (OCP):** Kode tidak tertutup untuk modifikasi. Menambah aturan baru (misal SPP) memaksa kita mengubah kode asli (menambah `if/else`).
* **Dependency Inversion Principle (DIP):** Modul bergantung pada implementasi detail (logika hardcoded), bukan pada abstraksi.

## 2. Implementasi Solusi
* **SRP:** Validasi dipecah menjadi kelas `SksValidator`, `PrerequisiteValidator`, dan `TuitionFeeValidator`.
* **DIP:** Menggunakan Interface `IValidator` sebagai kontrak.
* **OCP:** Menambah fitur validasi baru cukup dengan membuat kelas baru tanpa menyentuh kode lama.

## 3. Refleksi
Menggunakan **Dependency Injection (DI)** lebih efektif daripada `if/else` karena:
1.  **Fleksibilitas:** Menambah fitur semudah memasang plugin baru.
2.  **Decoupling:** Memisahkan logika validasi dari alur utama program.
3.  **Testing:** Memudahkan pengujian tiap validator secara terpisah.
