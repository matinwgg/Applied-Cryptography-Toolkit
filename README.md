# Applied Cryptography Toolkit

A security-focused Python toolkit for studying and demonstrating modern applied cryptography.

## Scope
- AES-256-GCM authenticated encryption
- Argon2id password-based key derivation
- Ed25519 signatures
- X25519 key agreement
- HKDF key derivation
- Secure random token generation
- Canonical serialization
- Negative tests for tampering, nonce misuse, and invalid inputs

> Educational project. Do not use this package as a drop-in replacement for a reviewed cryptographic library in production.

## Design principles
1. Never implement cryptographic primitives from scratch.
2. Prefer authenticated encryption.
3. Use memory-hard password derivation.
4. Separate key agreement, key derivation, and encryption.
5. Fail closed on malformed input.

## License
MIT
