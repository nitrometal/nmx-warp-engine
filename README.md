# NMX WARP Engine

> High-performance Cloudflare WARP registration gateway and automated AmneziaWG configuration generator.  
> Project by NMX Industries • Lead Developer: NitroMetal-X

## Overview
NMX WARP Engine is an automated serverless gateway engineered to dynamically provision and register Cloudflare WARP cryptographic keypairs (Curve25519) and output production-ready configurations compatible with the AmneziaWG obfuscation protocol.

## Features
- Serverless API: Fast, stateless endpoint hosted on Vercel (/api/generate).
- AmneziaWG Obfuscation Ready: Pre-configured for DPI resistance (I1 handshake prefixes, Jc junk packets, H1-H4 header masks).
- Automated Pool Maintenance: Scheduled GitHub Action workflows regenerating active profiles continuously.
- Enterprise Grade Security: Zero logging, direct Cloudflare upstream routing.

## License
MIT License © 2026 NMX Industries
