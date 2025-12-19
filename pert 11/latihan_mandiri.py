import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass

# --- SETUP LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s - %(name)s: %(message)s',
    datefmt='%H:%M:%S'
)
# Logger dengan nama khusus 'Registration'
LOG = logging.getLogger('Registration')

# --- DATA MODEL ---
@dataclass
class Mahasiswa:
    """
    Menyimpan data akademis mahasiswa.
    
    Args:
        nama (str): Nama mahasiswa.
        sks_lulus (int): Jumlah SKS lulus.
        mata_kuliah_diambil (list): List matkul yang sudah diambil.
    """
    nama: str
    sks_lulus: int
    mata_kuliah_diambil: list

# --- ABSTRAKSI ---
class IValidator(ABC):
    """Interface dasar untuk aturan validasi."""
    
    @abstractmethod
    def validate(self, mhs: Mahasiswa) -> bool:
        """Memvalidasi data mahasiswa. Return True jika lolos."""
        pass

# --- IMPLEMENTASI VALIDATOR ---
class SksValidator(IValidator):
    """Cek apakah SKS cukup (Minimal 100)."""
    
    def validate(self, mhs: Mahasiswa) -> bool:
        MIN_SKS = 100
        if mhs.sks_lulus >= MIN_SKS:
            # Info jika berhasil
            LOG.info(f"[SKS] {mhs.nama} Lolos. (Punya: {mhs.sks_lulus})")
            return True
        # Warning jika gagal
        LOG.warning(f"[SKS] {mhs.nama} Gagal. SKS kurang (Cuma {mhs.sks_lulus})")
        return False

class PrerequisiteValidator(IValidator):
    """Cek apakah sudah ambil mata kuliah Algoritma."""
    
    def validate(self, mhs: Mahasiswa) -> bool:
        SYARAT = "Algoritma"
        if SYARAT in mhs.mata_kuliah_diambil:
            LOG.info(f"[Prasyarat] {mhs.nama} Lolos. Sudah ambil {SYARAT}.")
            return True
        LOG.warning(f"[Prasyarat] {mhs.nama} Gagal. Belum ambil {SYARAT}.")
        return False

class TuitionFeeValidator(IValidator):
    """Cek pembayaran SPP (Fitur tambahan)."""
    
    def validate(self, mhs: Mahasiswa) -> bool:
        LOG.info(f"[SPP] {mhs.nama} Status: Lunas.")
        return True

# --- SERVICE KOORDINATOR ---
class RegistrationService:
    """Service utama untuk menangani registrasi."""

    def __init__(self, validators: list[IValidator]):
        self.validators = validators

    def register(self, mhs: Mahasiswa):
        """Jalankan semua validasi untuk satu mahasiswa."""
        LOG.info(f"--- Memulai Validasi: {mhs.nama} ---")
        is_valid = True
        
        for validator in self.validators:
            if not validator.validate(mhs):
                is_valid = False
                # Tidak di-break agar semua error terlihat di log
        
        if is_valid:
            LOG.info(f"HASIL: {mhs.nama} -> BERHASIL REGISTRASI.\n")
        else:
            LOG.error(f"HASIL: {mhs.nama} -> GAGAL REGISTRASI.\n")

# --- MAIN PROGRAM ---
if __name__ == "__main__":
    # Data Mahasiswa
    mhs_lulus = Mahasiswa("Reza", 110, ["Algoritma", "Basis Data"])
    mhs_gagal_sks = Mahasiswa("Alan", 80, ["Algoritma"])
    mhs_gagal_syarat = Mahasiswa("Radit", 105, ["Statistika"])

    # Setup Aturan
    rules = [SksValidator(), PrerequisiteValidator(), TuitionFeeValidator()]
    
    # Jalankan
    service = RegistrationService(rules)
    
    service.register(mhs_lulus)
    service.register(mhs_gagal_sks)
    service.register(mhs_gagal_syarat)