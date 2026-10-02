# Applied Cryptography Toolkit

## About

An educational Python toolkit for studying modern applied cryptography through reviewed constructions built on established cryptographic primitives. It is designed to connect cryptographic engineering with the mathematics and security assumptions behind the primitives.

### Why it exists

Implementing cryptography is less about inventing primitives and more about composing well-understood primitives correctly. This project provides small, testable examples for authenticated encryption, password derivation, signatures, key agreement, key derivation, serialization, and failure handling.

## Features

- AES-256-GCM authenticated encryption
- Argon2id password-based key derivation
- Ed25519 digital signatures
- X25519 key agreement
- HKDF key derivation
- Secure random token generation
- Canonical serialization
- Negative tests for tampering and malformed input
- Explicit verification-failure handling

## Tech Stack

- Python
- `cryptography`
- Argon2
- pytest
- `pyproject.toml` packaging

## Architecture

```text
Application input
      ↓
Validation / canonicalization
      ↓
Key derivation or key agreement
      ↓
Established cryptographic primitive
      ↓
Authenticated output
      ↓
Verification / negative-path tests
```

The toolkit deliberately uses established libraries rather than implementing AES, Ed25519, X25519, or other primitives from scratch.

## Project Structure

```text
.
├── src/                 # Toolkit implementation
├── tests/               # Positive and negative security tests
├── pyproject.toml       # Package/dependency configuration
└── README.md
```

## Prerequisites

- Python 3.11+
- pip or an equivalent Python environment manager

## Getting Started

```bash
git clone https://github.com/matinwgg/Applied-Cryptography-Toolkit.git
cd Applied-Cryptography-Toolkit
python -m venv .venv
source .venv/bin/activate
pip install -e .
pytest -q
```

## Usage

Use the public APIs exposed by `src/`. Each primitive should be treated as a small demonstration of a cryptographic construction, with key/nonce lifecycle and serialization requirements preserved by the caller.

## Security Model

The project emphasises authenticated encryption, memory-hard password derivation, separation of key agreement from key derivation, explicit verification, and fail-closed handling. It is **not** a replacement for a reviewed production cryptographic library.

The mathematical foundations include finite fields, modular arithmetic, groups, probability, entropy, computational hardness, collision resistance, authentication, and key derivation.

## Testing

```bash
pytest -q
```

Security tests should include tampering, malformed ciphertexts, nonce misuse assumptions, invalid signatures, wrong keys, and serialization changes.

## Limitations & Future Work

- Formalise security properties for each construction.
- Add property-based tests.
- Add interoperability vectors from authoritative standards.
- Add benchmark comparisons with established libraries.
- Document key lifecycle and threat models more formally.

## Contributing

Add tests with every cryptographic behaviour change. Prefer standards-backed constructions and reviewed libraries. Never submit real secrets or production keys.

## License

MIT

## Author

**A. Matin Odoom**
