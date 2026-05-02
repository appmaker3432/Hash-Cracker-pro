#!/usr/bin/env python3
"""
Multi-Format Hash Cracker
Educational tool for learning about hash functions and password security
ONLY USE ON AUTHORIZED SYSTEMS FOR EDUCATIONAL PURPOSES
"""

import hashlib
import sys
import time
import argparse
from pathlib import Path

# Optional: bcrypt support (install with: pip install bcrypt)
try:
    import bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False
    print("[!] bcrypt not installed. Install with: pip install bcrypt")


class HashCracker:
    """Multi-format hash cracking tool"""
    
    SUPPORTED_ALGORITHMS = {
        'md5': 32,
        'sha1': 40,
        'sha224': 56,
        'sha256': 64,
        'sha384': 96,
        'sha512': 128,
        'ntlm': 32,  # Windows NTLM hashes
    }
    
    def __init__(self):
        self.hash_target = None
        self.hash_type = None
        self.wordlist_path = None
        self.start_time = None
        self.attempts = 0
        
    def detect_hash_type(self, hash_string):
        """Auto-detect hash type based on length"""
        hash_len = len(hash_string)
        
        # Check for bcrypt (starts with $2a$, $2b$, $2y$)
        if hash_string.startswith(('$2a$', '$2b$', '$2y$')) and BCRYPT_AVAILABLE:
            return 'bcrypt'
        
        # Detect by length
        possible_types = []
        for algo, length in self.SUPPORTED_ALGORITHMS.items():
            if hash_len == length:
                possible_types.append(algo)
        
        if len(possible_types) == 1:
            return possible_types[0]
        elif len(possible_types) > 1:
            print(f"[?] Multiple possible hash types: {', '.join(possible_types)}")
            return possible_types[0]  # Default to first match
        else:
            return None
    
    def hash_password(self, password, algorithm):
        """Generate hash for given password and algorithm"""
        if algorithm == 'bcrypt':
            if not BCRYPT_AVAILABLE:
                return None
            # For cracking bcrypt, we verify instead of generating
            return None
        elif algorithm == 'ntlm':
            # NTLM is MD4 hash of UTF-16LE encoded password
            try:
                return hashlib.new('md4', password.encode('utf-16le')).hexdigest()
            except ValueError:
                # MD4 not available in newer Python/OpenSSL
                print("[!] MD4/NTLM not supported in this Python version")
                return None
        else:
            # Standard hashlib algorithms
            return hashlib.new(algorithm, password.encode()).hexdigest()
    
    def verify_bcrypt(self, password, hash_string):
        """Verify password against bcrypt hash"""
        if not BCRYPT_AVAILABLE:
            return False
        try:
            return bcrypt.checkpw(password.encode(), hash_string.encode())
        except:
            return False
    
    def crack_hash(self, hash_string, wordlist_path, hash_type=None):
        """Main cracking function"""
        self.hash_target = hash_string.lower().strip()
        self.wordlist_path = wordlist_path
        self.start_time = time.time()
        self.attempts = 0
        
        # Detect or use provided hash type
        if hash_type:
            self.hash_type = hash_type.lower()
        else:
            self.hash_type = self.detect_hash_type(self.hash_target)
        
        if not self.hash_type:
            print(f"[!] Could not detect hash type for: {self.hash_target}")
            return None
        
        print(f"[*] Hash Type: {self.hash_type.upper()}")
        print(f"[*] Target Hash: {self.hash_target}")
        print(f"[*] Wordlist: {wordlist_path}")
        print(f"[*] Starting crack...\n")
        
        # Check if wordlist exists
        if not Path(wordlist_path).exists():
            print(f"[!] Wordlist not found: {wordlist_path}")
            return None
        
        # Start cracking
        try:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as wordlist:
                for line in wordlist:
                    password = line.strip()
                    self.attempts += 1
                    
                    # Progress update every 10000 attempts
                    if self.attempts % 10000 == 0:
                        elapsed = time.time() - self.start_time
                        rate = self.attempts / elapsed if elapsed > 0 else 0
                        print(f"[*] Tried {self.attempts} passwords... ({rate:.0f} hash/sec)")
                    
                    # Check if hash matches
                    if self.hash_type == 'bcrypt':
                        if self.verify_bcrypt(password, self.hash_target):
                            self.print_success(password)
                            return password
                    else:
                        hashed = self.hash_password(password, self.hash_type)
                        if hashed and hashed.lower() == self.hash_target:
                            self.print_success(password)
                            return password
            
            # No match found
            self.print_failure()
            return None
            
        except KeyboardInterrupt:
            print("\n[!] Cracking interrupted by user")
            self.print_stats()
            return None
        except Exception as e:
            print(f"[!] Error: {e}")
            return None
    
    def print_success(self, password):
        """Print success message with stats"""
        elapsed = time.time() - self.start_time
        rate = self.attempts / elapsed if elapsed > 0 else 0
        
        print("\n" + "="*60)
        print("[+] PASSWORD CRACKED!")
        print("="*60)
        print(f"[+] Hash: {self.hash_target}")
        print(f"[+] Password: {password}")
        print(f"[+] Hash Type: {self.hash_type.upper()}")
        print(f"[+] Attempts: {self.attempts:,}")
        print(f"[+] Time: {elapsed:.2f} seconds")
        print(f"[+] Rate: {rate:.0f} hashes/second")
        print("="*60 + "\n")
    
    def print_failure(self):
        """Print failure message with stats"""
        elapsed = time.time() - self.start_time
        rate = self.attempts / elapsed if elapsed > 0 else 0
        
        print("\n" + "="*60)
        print("[-] PASSWORD NOT FOUND")
        print("="*60)
        print(f"[-] Hash: {self.hash_target}")
        print(f"[-] Attempts: {self.attempts:,}")
        print(f"[-] Time: {elapsed:.2f} seconds")
        print(f"[-] Rate: {rate:.0f} hashes/second")
        print("="*60 + "\n")
    
    def print_stats(self):
        """Print current statistics"""
        elapsed = time.time() - self.start_time
        rate = self.attempts / elapsed if elapsed > 0 else 0
        print(f"\n[*] Attempts: {self.attempts:,}")
        print(f"[*] Time: {elapsed:.2f} seconds")
        print(f"[*] Rate: {rate:.0f} hashes/second")


def create_sample_wordlist():
    """Create a small sample wordlist for testing"""
    sample_passwords = [
        'password', '123456', 'password123', 'admin', 'letmein',
        'welcome', 'monkey', 'dragon', 'master', 'sunshine',
        'princess', 'qwerty', 'starwars', 'shadow', 'superman'
    ]
    
    wordlist_path = '/home/claude/sample_wordlist.txt'
    with open(wordlist_path, 'w') as f:
        for pwd in sample_passwords:
            f.write(pwd + '\n')
    
    print(f"[+] Sample wordlist created: {wordlist_path}")
    return wordlist_path


def generate_sample_hashes():
    """Generate sample hashes for testing"""
    test_password = "password123"
    
    print("\n" + "="*60)
    print("SAMPLE HASHES FOR TESTING")
    print("="*60)
    print(f"Password: {test_password}\n")
    
    # MD5
    md5_hash = hashlib.md5(test_password.encode()).hexdigest()
    print(f"MD5:     {md5_hash}")
    
    # SHA1
    sha1_hash = hashlib.sha1(test_password.encode()).hexdigest()
    print(f"SHA1:    {sha1_hash}")
    
    # SHA256
    sha256_hash = hashlib.sha256(test_password.encode()).hexdigest()
    print(f"SHA256:  {sha256_hash}")
    
    # SHA512
    sha512_hash = hashlib.sha512(test_password.encode()).hexdigest()
    print(f"SHA512:  {sha512_hash}")
    
    # NTLM
    try:
        ntlm_hash = hashlib.new('md4', test_password.encode('utf-16le')).hexdigest()
        print(f"NTLM:    {ntlm_hash}")
    except ValueError:
        print(f"NTLM:    [Not supported - MD4 unavailable]")
    
    # bcrypt (if available)
    if BCRYPT_AVAILABLE:
        bcrypt_hash = bcrypt.hashpw(test_password.encode(), bcrypt.gensalt()).decode()
        print(f"bcrypt:  {bcrypt_hash}")
    
    print("="*60 + "\n")


def main():
    """Main function with CLI argument parsing"""
    parser = argparse.ArgumentParser(
        description='Multi-Format Hash Cracker - Educational Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Crack with auto-detection
  python3 hash_cracker.py -H 5f4dcc3b5aa765d61d8327deb882cf99 -w wordlist.txt
  
  # Crack with specific type
  python3 hash_cracker.py -H <hash> -w wordlist.txt -t sha256
  
  # Generate sample hashes
  python3 hash_cracker.py --samples
  
  # Create sample wordlist
  python3 hash_cracker.py --create-wordlist

Supported Hash Types:
  MD5, SHA1, SHA224, SHA256, SHA384, SHA512, NTLM, bcrypt
        '''
    )
    
    parser.add_argument('-H', '--hash', help='Hash to crack')
    parser.add_argument('-w', '--wordlist', help='Path to wordlist file')
    parser.add_argument('-t', '--type', help='Hash type (auto-detect if not specified)')
    parser.add_argument('--samples', action='store_true', help='Generate sample hashes')
    parser.add_argument('--create-wordlist', action='store_true', help='Create sample wordlist')
    
    args = parser.parse_args()
    
    # Show banner
    print("\n" + "="*60)
    print("  Multi-Format Hash Cracker v1.0")
    print("  Educational Tool - Use Responsibly")
    print("="*60 + "\n")
    
    # Handle special commands
    if args.samples:
        generate_sample_hashes()
        return
    
    if args.create_wordlist:
        create_sample_wordlist()
        return
    
    # Validate required arguments for cracking
    if not args.hash or not args.wordlist:
        parser.print_help()
        print("\n[!] Error: Both --hash and --wordlist are required for cracking")
        print("[*] Use --samples to generate test hashes")
        print("[*] Use --create-wordlist to create a sample wordlist")
        return
    
    # Create cracker and run
    cracker = HashCracker()
    result = cracker.crack_hash(args.hash, args.wordlist, args.type)
    
    if result:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure


if __name__ == "__main__":
    main()
