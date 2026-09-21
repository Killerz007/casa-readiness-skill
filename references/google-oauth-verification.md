# Google OAuth Verification Review

This component helps determine what should be prepared for Google OAuth verification. It must not invent Google's decision.

## Review steps

1. Locate all OAuth client IDs/configuration and callback handlers.
2. Enumerate requested scopes from source/configuration and, where accessible, Google Cloud configuration.
3. Map each scope to current authoritative Google documentation when internet access is available.
4. Identify the Google APIs and operations actually called.
5. Identify whether Google user data passes through or is stored by backend/server components.
6. Review token storage, refresh-token lifecycle, revocation, logout and account disconnect.
7. Review data retention/deletion and least-privilege scope use.
8. Compare actual behavior with the privacy policy, consent screen and user-facing disclosures where available.
9. Record any ambiguity as requiring Google confirmation rather than guessing the verification tier/path.

## Important distinction

Google OAuth scope verification and CASA conformance are related but not identical. Do not state that all sensitive scopes automatically require an AL2 assessment. Use current Google documentation for the verification pathway and the ADA CASA specification for technical CASA controls.
