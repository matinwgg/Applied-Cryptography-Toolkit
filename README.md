# Applied Cryptography Toolkit

A security-focused Python toolkit for studying modern applied cryptography through safe, reviewed constructions rather than reimplementing primitives.

## Cryptographic scope

- AES-256-GCM authenticated encryption
- Argon2id password-based key derivation
- Ed25519 digital signatures
- X25519 key agreement
- HKDF key derivation
- Secure random token generation
- Canonical serialization
- Negative tests for tampering, nonce misuse, malformed input, and verification failures

## Mathematical foundations

The project connects implementation to the mathematics of finite fields, modular arithmetic, groups, probability, entropy, computational hardness, collision resistance, authentication, and key derivation.

## Design principles

1. Never implement cryptographic primitives from scratch for production use.
2. Prefer authenticated encryption.
3. Use memory-hard password derivation.
4. Separate key agreement, key derivation, and encryption.
5. Fail closed on malformed or unauthenticated input.
6. Make security assumptions explicit and test negative cases.

## Research value

This repository is useful as a foundation for studying applied cryptography, secure systems, password security, protocol design, adversarial thinking, and cryptographic engineering.

> **Educational project.** Do not use this package as a drop-in replacement for a reviewed production cryptographic library.

## License

MIT
