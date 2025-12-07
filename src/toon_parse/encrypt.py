import base64
import itertools
from cryptography.fernet import Fernet


class Encryptor:
    """
    Handles encryption and decryption of data using specified algorithms.
    
    Supported Algorithms:
    - 'fernet': Symmetric encryption (Requires `cryptography` library). High security.
    - 'xor': Simple XOR cipher. Low security, good for obfuscation.
    - 'base64': Base64 encoding. No security, just encoding.
    """
    
    def __init__(self, key=None, algorithm='fernet'):
        self.key = key
        self.algorithm = algorithm.lower()
        self._fernet_suite = None
        
        if self.algorithm == 'fernet':
            if not self.key:
                raise ValueError("Key is required for Fernet encryption.")
            try:
                # Initialize Fernet suite once to validate key immediately
                self._fernet_suite = Fernet(self.key)
            except Exception as e:
                raise ValueError(f"Invalid Fernet key: {e}")

    def encrypt(self, data):
        """
        Encrypts the provided string data.
        """
        if not isinstance(data, str):
            raise ValueError("Data to encrypt must be a string.")

        if self.algorithm == 'fernet':
            return self._fernet_suite.encrypt(data.encode('utf-8')).decode('utf-8')
        elif self.algorithm == 'xor':
            return self._xor_encrypt(data)
        elif self.algorithm == 'base64':
            return base64.b64encode(data.encode('utf-8')).decode('utf-8')
        else:
            raise ValueError(f"Unsupported algorithm: {self.algorithm}")

    def decrypt(self, encrypted_data):
        """
        Decrypts the provided encrypted string data.
        """
        if not isinstance(encrypted_data, str):
            raise ValueError("Data to decrypt must be a string.")

        if self.algorithm == 'fernet':
            return self._fernet_suite.decrypt(encrypted_data.encode('utf-8')).decode('utf-8')
        elif self.algorithm == 'xor':
            return self._xor_decrypt(encrypted_data)
        elif self.algorithm == 'base64':
            try:
                return base64.b64decode(encrypted_data).decode('utf-8')
            except Exception as e:
                raise ValueError(f"Invalid Base64 data: {e}")
        else:
            raise ValueError(f"Unsupported algorithm: {self.algorithm}")

    def _get_key_bytes(self):
        if not self.key:
            raise ValueError("Key is required for XOR cipher.")
        if isinstance(self.key, bytes):
            return self.key
        return str(self.key).encode('utf-8')

    def _xor_encrypt(self, text):
        key_bytes = self._get_key_bytes()
        text_bytes = text.encode('utf-8')
        xor_result = bytes([b ^ k for b, k in zip(text_bytes, itertools.cycle(key_bytes))])
        # Return as hex string for safe transport/storage
        return xor_result.hex()

    def _xor_decrypt(self, hex_text):
        key_bytes = self._get_key_bytes()
        try:
            xor_bytes = bytes.fromhex(hex_text)
            decrypted = bytes([b ^ k for b, k in zip(xor_bytes, itertools.cycle(key_bytes))])
            return decrypted.decode('utf-8')
        except ValueError:
            raise ValueError("Invalid format for XOR decryption (expected hex string).")
