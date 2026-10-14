# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability affecting this website or repository — for example, an exposed credential, a cross-site scripting (XSS) issue, or a misconfigured file — please report it responsibly rather than opening a public GitHub issue.

**Please email:** jopetnah.intl.ltd@gmail.com with the subject line `SECURITY: [brief description]`

Include, where possible:
- A description of the vulnerability and its potential impact
- Steps to reproduce it
- Any relevant URLs, screenshots, or logs

We will acknowledge reports as promptly as possible and work to address confirmed issues.

## Scope

This repository contains a static marketing website (HTML, CSS, and JavaScript) with no backend, no database, and no user authentication system. The realistic scope for security issues here is limited to:
- Client-side vulnerabilities (e.g., XSS via unsanitized content)
- Exposed sensitive information committed to the repository in error
- DNS/domain configuration issues once the custom domain is connected

## Supported Versions

This is a single, continuously deployed website rather than a versioned software release — there is one live version at any given time, served from the `main` branch. Security reports should be made against whatever is currently live.
