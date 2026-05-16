# Security Policy

## Supported Versions
Security updates apply to the latest development branch and the most recent tagged release. Older versions may not receive patches.

## Reporting a Vulnerability
If you discover a security issue, please report it privately:

**security@linktech.engineering**

Do not open a public GitHub issue for security‑related topics.

We will acknowledge receipt within 48 hours and provide a timeline for resolution.

## Security Expectations
TimerDeck interacts with systemd, cron, and system‑level metadata. To maintain a secure environment:

- No unvalidated input is passed to system commands.
- No external code is executed beyond systemd, journalctl, or other standard Linux utilities.
- No sensitive data (credentials, tokens, passwords) is logged.
- All privilege‑elevated operations must be explicit and user‑approved.
- TimerDeck must fail closed on unexpected errors.
- Editing unit files must include validation and safety checks.
- Future packaging (AppImage, Flatpak, DEB) must not introduce additional attack surface.

## Responsible Disclosure
We request that researchers follow responsible disclosure practices and allow maintainers time to address issues before public release.

Thank you for helping keep TimerDeck and the Linktech Engineering Tools Suite secure.
