# Multi-Format Hash Cracker

Educational Python tool for learning about hash functions and password security.

## ⚠️ IMPORTANT - LEGAL DISCLAIMER

**THIS TOOL IS FOR EDUCATIONAL PURPOSES ONLY**
- Only use on systems you own or have explicit written authorization to test
- Never use on unauthorized systems - doing so is illegal
- Created for cybersecurity students to learn about hash functions and password security
- Unauthorized password cracking is a criminal offense

## Features

✅ **Supports 6+ Hash Formats:**
- MD5 (32 chars)
- SHA1 (40 chars)
- SHA224 (56 chars)
- SHA256 (64 chars)
- SHA384 (96 chars)
- SHA512 (128 chars)
- NTLM (32 chars) - Windows password hashes
- bcrypt (optional - requires installation)

✅ **Auto-Detection:**
- Automatically detects hash type based on length
- Manual override available with `-t` flag

✅ **Performance Features:**
- Real-time progress updates
- Hash/second rate calculation
- Attempt counting
- Time tracking

## Installation

### Basic Installation
```bash
# Make executable
chmod +x hash_cracker.py

# No additional dependencies needed for MD5, SHA-family hashes
```

### Optional: bcrypt Support
```bash
# Install bcrypt for bcrypt hash cracking
pip install bcrypt
```

## Usage

### Generate Sample Hashes
```bash
python3 hash_cracker.py --samples
```

Output:
```
Password: password123

MD5:     482c811da5d5b4bc6d497ffa98491e38
SHA1:    cbfdac6008f9cab4083784cbd1874f76618d2a97
SHA256:  ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f
SHA512:  bed4efa1d4fdbd954bd3705d6a2a78270ec9a52ecfbfb010c61862af5c76af...
```

### Create Sample Wordlist
```bash
python3 hash_cracker.py --create-wordlist
```

### Crack a Hash (Auto-Detect)
```bash
python3 hash_cracker.py -H 482c811da5d5b4bc6d497ffa98491e38 -w wordlist.txt
```

### Crack with Specific Hash Type
```bash
python3 hash_cracker.py -H <hash> -w wordlist.txt -t sha256
```

### Full Command Reference
```
usage: hash_cracker.py [-h] [-H HASH] [-w WORDLIST] [-t TYPE] [--samples] [--create-wordlist]

Options:
  -H, --hash HASH        Hash to crack
  -w, --wordlist WORDLIST Path to wordlist file
  -t, --type TYPE        Hash type (auto-detect if not specified)
  --samples              Generate sample hashes for testing
  --create-wordlist      Create sample wordlist
```

## Examples

### Example 1: Crack MD5 Hash
```bash
# Generate test hash
python3 hash_cracker.py --samples

# Crack it
python3 hash_cracker.py -H 482c811da5d5b4bc6d497ffa98491e38 -w wordlist.txt
```

### Example 2: Crack SHA256 Hash
```bash
python3 hash_cracker.py -H ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f -w wordlist.txt -t sha256
```

### Example 3: Use rockyou.txt (if available)
```bash
# Download rockyou.txt wordlist (common in Kali Linux)
python3 hash_cracker.py -H <hash> -w /usr/share/wordlists/rockyou.txt
```

## How It Works

1. **Hash Detection**: Tool examines hash length to determine type
2. **Wordlist Reading**: Reads passwords from wordlist file
3. **Hashing**: Generates hash for each password using specified algorithm
4. **Comparison**: Compares generated hash with target hash
5. **Match**: If hashes match, password is found!

## Wordlists

### Included Sample Wordlist
The tool can generate a small sample wordlist with common passwords:
```bash
python3 hash_cracker.py --create-wordlist
```

### Popular Wordlists for Learning
- **rockyou.txt** - 14 million passwords (most popular)
- **SecLists** - Collection of security testing lists
- **CrackStation** - Large password dictionaries

### Download rockyou.txt
```bash
# On Kali Linux
sudo gunzip /usr/share/wordlists/rockyou.txt.gz

# Or download
wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt
```

## Performance Tips

1. **Use Smaller Wordlists First**: Test with small lists before large ones
2. **Common Passwords**: Most weak passwords are in top 10,000
3. **Hash Type**: Some algorithms (bcrypt) are intentionally slow
4. **File I/O**: SSD storage improves wordlist reading speed

## Educational Use Cases

### Learning Objectives
- Understand how password hashing works
- Learn differences between hash algorithms
- Recognize importance of strong passwords
- Practice dictionary attacks safely
- Understand why salting is important

### Lab Exercises
1. **Hash Different Passwords**: See how same algorithm produces different hashes
2. **Compare Algorithms**: Notice MD5 vs SHA256 vs bcrypt differences
3. **Test Password Strength**: Try cracking your own passwords
4. **Speed Comparison**: Compare cracking speeds of different algorithms
5. **Salting Demo**: Understand why salting prevents rainbow tables

## Security Lessons

### Why Hash Cracking Works
- Weak/common passwords are in wordlists
- Unsalted hashes are vulnerable to rainbow tables
- Fast hashing algorithms (MD5, SHA1) crack quickly

### Defense Strategies
✅ Use **strong, unique passwords** (12+ characters, random)
✅ Use **password managers**
✅ Implement **salting** (random data added to passwords)
✅ Use **slow hash functions** (bcrypt, scrypt, Argon2)
✅ Enable **multi-factor authentication (MFA)**
✅ Implement **rate limiting** on login attempts

### Never Do This
❌ Store passwords in plaintext
❌ Use MD5 or SHA1 for passwords (too fast)
❌ Reuse passwords across sites
❌ Use common passwords (password123, admin, etc.)

## Troubleshooting

### "Wordlist not found"
```bash
# Check file path exists
ls -la your_wordlist.txt

# Use absolute path
python3 hash_cracker.py -H <hash> -w /full/path/to/wordlist.txt
```

### "Could not detect hash type"
```bash
# Manually specify type
python3 hash_cracker.py -H <hash> -w wordlist.txt -t md5
```

### "bcrypt not installed"
```bash
# Install bcrypt support
pip install bcrypt
```

## Hash Format Reference

| Algorithm | Hash Length | Example |
|-----------|-------------|---------|
| MD5 | 32 chars | 5f4dcc3b5aa765d61d8327deb882cf99 |
| SHA1 | 40 chars | cbfdac6008f9cab4083784cbd1874f76618d2a97 |
| SHA256 | 64 chars | ef92b778bafe771e89245b89ecbc08a44a4e166c... |
| SHA512 | 128 chars | bed4efa1d4fdbd954bd3705d6a2a78270ec9a52e... |
| NTLM | 32 chars | 8846f7eaee8fb117ad06bdd830b7586c |
| bcrypt | Variable | $2b$12$KIXxm... |

## Advanced Usage

### Create Custom Wordlists
```bash
# Combine multiple lists
cat list1.txt list2.txt > combined.txt

# Remove duplicates
sort -u wordlist.txt > unique.txt

# Generate variations with John the Ripper
john --wordlist=base.txt --rules --stdout > expanded.txt
```

### Batch Hash Cracking
```python
# Create script to crack multiple hashes
hashes = [
    "hash1...",
    "hash2...",
    "hash3..."
]

for h in hashes:
    os.system(f"python3 hash_cracker.py -H {h} -w wordlist.txt")
```

## Comparison with Other Tools

| Tool | Strengths | Use Case |
|------|-----------|----------|
| **hash_cracker.py** | Educational, simple, multi-format | Learning |
| **John the Ripper** | Professional, rule-based, fast | Pentesting |
| **Hashcat** | GPU acceleration, fastest | Production cracking |
| **Hydra** | Online attacks, many protocols | Network services |

## Resources for Learning

### Practice Environments
- **TryHackMe** - Guided hacking challenges
- **HackTheBox** - CTF-style pentesting
- **OverTheWire** - War games for beginners

### Vulnerable Apps
- **DVWA** - Damn Vulnerable Web Application
- **WebGoat** - OWASP training app
- **Metasploitable** - Intentionally vulnerable VM

### Further Reading
- OWASP Password Storage Cheat Sheet
- "Practical Cryptography" by Ferguson & Schneier
- NIST Password Guidelines

## Contributing

This is an educational tool. Suggestions for improvements:
- Additional hash algorithms
- GUI interface
- Rule-based attack modes
- Hybrid attack modes
- Multi-threading support

## License

MIT License - Free for educational use

## Acknowledgments

Created for cybersecurity education and ethical hacking training.

---

**Remember: With great power comes great responsibility. Use this knowledge to build better security, not to break it.**
