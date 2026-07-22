# Cygnus Wave Observatory Tools

**Free, open-source geometry calculators for astrophotographers building dome and roll-off-roof observatories.**

Built by [Cygnus Wave](https://cygnuswave.io) · Licensed under the [Mozilla Public License 2.0](LICENSE)

---

## Tools

### Dome & Mount Geometry Calculator
`dome-calculator.html`

Converts physical measurements — or values you already have — into the exact signed fields NINA's dome-sync tab expects. Shows live whether the shutter actually clears the OTA at every pointing, not just whether the dome rotates to the right azimuth.

**Features**
- Physical measurement worksheet or direct NINA value entry
- Live dome-azimuth calculation ported from NINA's own `DomeSynchronization.cs`
- Interactive 3D observatory model (drag to orbit, scroll to zoom)
- Dual-saddle / dual-OTA support with independent shutter clearance per scope
- GEM and Alt/Az / Fork mount support
- Meridian auto-flip with pier-side tracking
- Local horizon modeling — flat minimum or full custom profile (`.hrz` / CSV import)
- Full-sky coverage sweep by pier side
- Celestial equator and elevated pole reference lines, genuinely latitude-aware
- One-click NINA settings clipboard export
- Save / Load setup as JSON · Reset to Defaults · Dark / Light mode

---

### Roll-Off-Roof Observatory Calculator
`ror-calculator.html`  ·  **v2.00.000**

A real wall-obstruction model for roll-off-roof observatories — checks the walls, parked roof, floor, and ceiling for every possible pointing, not just the current one. Supports up to 4 independent telescopes on separate mounts, with a full pier-layout floor plan and swing-clearance geometry.

**Features**
- Rectangular or fully custom 6-wall building footprint
- Flat, peaked (gable), or wedge (mono-slope) roof profiles
- Parked roof modeled as a real obstruction — not an open gap
- Local terrain horizon layered on top of wall / roof obstruction
- **Interactive pier-layout floor plan** — click and drag piers onto a scaled floor plan; NS/EW position fields stay in sync
- Up to 4 telescopes on independent mounts, each with its own position, mount height, mount type (GEM / Alt-Az), and optics
- Per-telescope swing-radius clearance against walls, floor, and ceiling
- Telescope-to-telescope swing-circle collision check with configurable minimum walkway gap
- Telescope selector dropdown — any of the 4 mounts can drive the live pointing preview and sky coverage sweep
- Full-sky coverage sweep stretched to building aspect ratio
- Exportable horizon profile (`.hrz`) combining walls, roof, and terrain
- 3D building preview with per-scope wireframe swing spheres and OTA tube indicators
- GEM and Alt/Az mount types per telescope
- Save / Load setup as JSON · Reset to Defaults · Dark / Light mode

---

## Quick Start

Both tools are **single self-contained HTML files** — no build step, no server, no dependencies to install.

```bash
git clone https://github.com/SbiviAstro/observatory-tools.git
cd observatory-tools
open dome-calculator.html     # macOS
# or
start dome-calculator.html    # Windows
# or just drag the file into any browser
```

Everything runs locally in your browser. Nothing you enter is sent anywhere.

---

## Repository Structure

```
observatory-tools/
├── dome-calculator.html        # Dome & Mount Geometry Calculator
├── ror-calculator.html         # Roll-Off-Roof Calculator (v2.00.000)
├── index.html                  # Cygnus Wave site homepage
├── about.html
├── help.html
├── dome-manual.html            # Dome calculator user manual
├── ror-manual.html             # ROR calculator user manual
├── changelog.html
├── license.html                # MPL 2.0 full text
├── disclaimer.html
├── privacy.html
├── faq.html
├── contact.html
├── 404.html
├── favicon.svg                 # Cygnus Wave logo favicon
├── cygnuswave-logo.svg         # Full Cygnus Wave logo
├── LICENSE                     # Mozilla Public License 2.0
└── README.md                   # This file
```

---

## How It Works

### Dome Calculator — Core Math
The dome-azimuth calculation is ported verbatim from NINA's `DomeSynchronization.cs`, using the same Accord.Math `Matrix4x4` column-vector conventions. What you see in this calculator is what NINA's dome-sync actually computes — not a simplified approximation.

The mount-to-dome-center offset is decomposed into three signed values (N/S, E/W, Up/Down) plus GEM axis length and lateral axis length for dual-saddle setups. The shutter-clearance check traces a ray from the aperture footprint through the dome surface and verifies the full aperture circle lands within the shutter opening.

### ROR Calculator — Core Math
Wall obstruction is computed as a ray-to-wall distance from the mount's interior point, generalised to an N-wall convex polygon via half-plane intersection (`polygonRayDist()`). The roll-off wall boundary is extended by the roof travel distance before intersection so the parked roof is correctly modelled as an obstruction in that direction.

Roof height at any azimuth:
- **Flat** — constant height
- **Peaked (gable)** — linear taper from ridge to eave, ridge parallel to roll direction
- **Wedge (mono-slope)** — linear taper from low side to high side across the width

Swing clearance per telescope: `swingRadius = axisOffset + tubeLength + aperture/2`. This is the worst-case distance from the mount pivot to the farthest point of the OTA — the radius of the sphere the assembly sweeps through at any pointing. Checked against the minimum of (nearest wall clearance, floor clearance, ceiling clearance) at the mount's own position.

Telescope-to-telescope clearance: `gap = distanceBetweenPivots − (swingRadius₁ + swingRadius₂)`. If `gap < minRequiredGap`, the swing circles overlap and the telescopes will physically collide at some pointing.

---

## Relationship to NINA

The dome calculator's azimuth math is ported from [NINA (Nighttime Imaging 'N' Astronomy)](https://nighttime-imaging.eu), an open-source astrophotography application. Both this project and NINA are licensed under the Mozilla Public License 2.0 in recognition of that shared foundation.

These tools are not affiliated with, endorsed by, or supported by the NINA project or its developers.

---

## License

Both calculators are released under the **Mozilla Public License 2.0 (MPL-2.0)**.

The MPL is a file-level copyleft license. In plain terms:
- ✓ Use freely for any purpose
- ✓ Modify and redistribute
- ✓ Combine with code under other licenses
- ✗ Release modified versions of these specific files under a different license
- ✗ Remove or alter the license notice

See [`LICENSE`](LICENSE) or [`license.html`](license.html) for the full text.

**Third-party dependency:** Both calculators load [Three.js r128](https://threejs.org) from the Cloudflare CDN (MIT License). The script tag includes a Subresource Integrity hash to verify the file's integrity at load time.

---

## Contributing

Contributions welcome under the MPL 2.0. The source is the HTML file itself — view source in your browser to read it, or clone and open in an editor.

If you find a bug, have a feature request, or want to contribute a fix:
1. Open an issue describing the problem or proposal
2. Fork the repo, make your changes, and open a pull request
3. All contributions must be under the MPL 2.0

For bug reports, please include which calculator and version, the values you entered, what you expected, and what you saw.

---

## Special Thanks

**David Funk** and **Andrew Bares** — for their inspiration, feedback, and generosity with their time. These tools are sharper, more useful, and more honest about what they're actually solving because of their input.

---

## Hosted Version

Live at **[cygnuswave.io](https://cygnuswave.io)** · No account required · No data collected

See [`privacy.html`](privacy.html) for the full privacy policy (short version: nothing you enter leaves your device).
