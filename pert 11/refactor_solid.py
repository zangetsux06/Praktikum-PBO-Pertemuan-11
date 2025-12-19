import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass

# --- KONFIGURASI LOGGING (TUGAS 12) ---
# Ini supaya outputnya ada jam dan tanggalnya, menggantikan print biasa
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s - %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
LOGGER = logging.getLogger('CheckoutSystem')

# --- DATA MODEL ---
@dataclass
class Order:
    """
    Merepresentasikan data pesanan pelanggan.
    
    Args:
        customer_name (str): Nama pelanggan.
        total_price (float): Total harga pesanan.
        status (str): Status pembayaran (default: 'open').
    """
    customer_name: str
    total_price: float
    status: str = "open"

# --- ABSTRAKSI ---
class IPaymentProcessor(ABC):
    """Interface (Kontrak) untuk memproses pembayaran."""
    
    @abstractmethod
    def process(self, order: Order) -> bool:
        """Memproses pembayaran untuk pesanan tertentu."""
        pass

class INotificationService(ABC):
    """Interface (Kontrak) untuk layanan notifikasi."""

    @abstractmethod
    def send(self, order: Order):
        """Mengirim notifikasi terkait status pesanan."""
        pass

# --- IMPLEMENTASI KONKRIT ---
class CreditCardProcessor(IPaymentProcessor):
    """Implementasi pembayaran menggunakan Kartu Kredit."""

    def process(self, order: Order) -> bool:
        # Menggunakan LOGGER.info bukan print
        LOGGER.info(f"Processing Credit Card payment for {order.customer_name} amount {order.total_price}")
        return True

class EmailNotifier(INotificationService):
    """Implementasi notifikasi via Email."""

    def send(self, order: Order):
        # Menggunakan LOGGER.info bukan print
        LOGGER.info(f"Sending email confirmation to {order.customer_name}")

# --- KELAS KOORDINATOR (SERVICE) ---
class CheckoutService:
    """
    Kelas utama untuk mengkoordinasi proses transaksi checkout.
    """

    def __init__(self, payment_processor: IPaymentProcessor, notifier: INotificationService):
        """
        Inisialisasi CheckoutService dengan strategi pembayaran dan notifikasi.
        """
        self.payment_processor = payment_processor
        self.notifier = notifier

    def run_checkout(self, order: Order) -> bool:
        """
        Menjalankan alur checkout: Bayar -> Ubah Status -> Notifikasi.
        Returns: True jika sukses, False jika gagal.
        """
        LOGGER.info(f"--- Memulai Checkout untuk {order.customer_name} ---")
        
        # Delegasi proses bayar
        payment_success = self.payment_processor.process(order)
        
        if payment_success:
            order.status = "paid"
            LOGGER.info(f"Payment Success. Status changed to: {order.status}")
            
            # Delegasi notifikasi
            self.notifier.send(order)
            LOGGER.info("Checkout Process Completed Successfully.\n")
            return True
        else:
            LOGGER.error("Payment Failed. Transaction cancelled.\n")
            return False

class QrisProcessor(IPaymentProcessor):
    """Implementasi pembayaran via QRIS (Fitur tambahan OCP)."""

    def process(self, order: Order) -> bool:
        LOGGER.info(f"Generating QRIS Code for {order.customer_name} amount {order.total_price}")
        return True

# --- PROGRAM UTAMA ---
if __name__ == "__main__":
    # Skenario 1: Kartu Kredit
    andi_order = Order("Andi", 500000)
    email_service = EmailNotifier()
    cc_processor = CreditCardProcessor()
    
    checkout_cc = CheckoutService(cc_processor, email_service)
    checkout_cc.run_checkout(andi_order)

    # Skenario 2: QRIS
    budi_order = Order("Budi", 100000)
    qris_processor = QrisProcessor()
    
    checkout_qris = CheckoutService(qris_processor, email_service)
    checkout_qris.run_checkout(budi_order)


    