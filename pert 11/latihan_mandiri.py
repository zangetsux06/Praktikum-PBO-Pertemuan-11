from abc import ABC, abstractmethod
from dataclasses import dataclass

# DATA MODEL

@dataclass
class Mahasiswa:
    nama: str
    sks_lulus: int
    mata_kuliah_diambil: list  # List mata kuliah yang sudah diambil

# ==========================================
# 1. KODE BURUK (SEBELUM REFACTOR)
# (Sesuai deskripsi soal: menggunakan if/else dalam satu method)

class BadValidatorManager:
    def validate_registration(self, mhs: Mahasiswa, jenis_validasi: str):
        # Pelanggaran OCP: Harus ubah kode jika ada aturan baru
        # Pelanggaran SRP: Satu method mengurusi banyak logika berbeda
        if jenis_validasi == "sks":
            if mhs.sks_lulus < 100:
                print(f"[Bad] {mhs.nama} Gagal: SKS kurang dari 100.")
                return False
            print(f"[Bad] {mhs.nama} Lolos validasi SKS.")
            return True
        elif jenis_validasi == "prasyarat":
            if "Algoritma" not in mhs.mata_kuliah_diambil:
                print(f"[Bad] {mhs.nama} Gagal: Belum ambil Algoritma.")
                return False
            print(f"[Bad] {mhs.nama} Lolos validasi Prasyarat.")
            return True
        else:
            print("Jenis validasi tidak dikenal.")
            return False


# 2. HASIL REFACTORING (SOLID)


# --- ABSTRAKSI (DIP & OCP) ---
class IValidator(ABC):
    """Kontrak: Semua validator harus punya method validate"""
    @abstractmethod
    def validate(self, mhs: Mahasiswa) -> bool:
        pass

# --- IMPLEMENTASI KONKRIT (SRP) ---
# Tiap class hanya bertanggung jawab untuk satu jenis validasi

class SksValidator(IValidator):
    def validate(self, mhs: Mahasiswa) -> bool:
        MIN_SKS = 100
        if mhs.sks_lulus >= MIN_SKS:
            print(f"[Check SKS] {mhs.nama}: Lolos (SKS {mhs.sks_lulus}).")
            return True
        print(f"[Check SKS] {mhs.nama}: Gagal (Butuh {MIN_SKS}, punya {mhs.sks_lulus}).")
        return False

class PrerequisiteValidator(IValidator):
    def validate(self, mhs: Mahasiswa) -> bool:
        SYARAT = "Algoritma"
        if SYARAT in mhs.mata_kuliah_diambil:
            print(f"[Check Prasyarat] {mhs.nama}: Lolos (Sudah ambil {SYARAT}).")
            return True
        print(f"[Check Prasyarat] {mhs.nama}: Gagal (Belum ambil {SYARAT}).")
        return False

# --- CHALLENGE OCP (Fitur Baru) ---
# Kita menambah validasi Pembayaran tanpa menyentuh kode lama
class TuitionFeeValidator(IValidator):
    def validate(self, mhs: Mahasiswa) -> bool:
        # Simulasi cek tagihan ke database keuangan
        print(f"[Check SPP] {mhs.nama}: Lolos (SPP Lunas).")
        return True

# --- KOORDINATOR (Registration Service) ---
class RegistrationService:
    # Dependency Injection: Menerima list validator apapun
    def __init__(self, validators: list[IValidator]):
        self.validators = validators

    def register(self, mhs: Mahasiswa):
        print(f"\n--- Memproses Registrasi: {mhs.nama} ---")
        is_valid = True
        
        # Iterasi semua aturan validasi (Polymorphism)
        for validator in self.validators:
            if not validator.validate(mhs):
                is_valid = False
                break # Berhenti jika salah satu gagal
        
        if is_valid:
            print(f"HASIL: {mhs.nama} BERHASIL Registrasi.")
        else:
            print(f"HASIL: {mhs.nama} GAGAL Registrasi.")


# PROGRAM UTAMA

if __name__ == "__main__":
    # 1. Setup Data Mahasiswa
    # Mahasiswa A: SKS Cukup, Sudah ambil Algoritma
    mhs_lulus = Mahasiswa("Reza", 110, ["Algoritma", "Basis Data"])
    # Mahasiswa B: SKS Kurang
    mhs_gagal_sks = Mahasiswa("Alan", 80, ["Algoritma"])
    # Mahasiswa C: SKS Cukup, Belum ambil Algoritma
    mhs_gagal_syarat = Mahasiswa("Radit", 105, ["Statistika", "Matematika Diskrit"])

    # 2. Setup Validator (Inject Dependencies)
    # Kita bisa mengatur urutan atau menambah validator baru dengan mudah
    rules = [
        SksValidator(),
        PrerequisiteValidator(),
        TuitionFeeValidator() # Pembuktian OCP (Challenge)
    ]

    # 3. Jalankan Service
    service = RegistrationService(rules)
    
    service.register(mhs_lulus)       # Harusnya Berhasil
    service.register(mhs_gagal_sks)   # Harusnya Gagal di SKS
    service.register(mhs_gagal_syarat)# Harusnya Gagal di Prasyarat

    