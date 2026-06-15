---
version: alpha
name: One-Page Beginners Guide Mission Manual System
source: /Users/vikinglu/Downloads/DESIGN-spacex.md adapted for this repository
register: brand
---

# Design

## Design Intent

This project uses a mission-oriented black-and-white exhibition language inspired by aerospace campaign sites, adapted for Traditional Chinese long-form instructional guides. The goal is not to clone a space brand. The goal is to make each guide feel like a precise mission manual: cinematic first viewport, fixed overlay navigation, high-contrast industrial typography, minimal chrome, and scroll motion that clarifies progress.

## Non-Negotiables

- Do not use SpaceX names, logos, rockets, Mars landscapes, launch imagery, or trademarked assets.
- Keep the site static: HTML, CSS, JavaScript, GitHub Pages.
- `PRODUCT.md` and `DESIGN.md` are required reading before future visual or animation changes.
- Content is the product. Motion must never hide, delay, or replace readable article content.
- Prefer black, white, near-black, and gray hairlines. Do not introduce decorative accent colors.

## Colors

```css
--canvas: #000000;
--canvas-soft: #080808;
--surface: #0d0d0f;
--surface-2: #151517;
--ink: #ffffff;
--ink-soft: #f0f0f2;
--muted: #a8a8ad;
--muted-2: #6e6e76;
--hairline: #3a3a3f;
--hairline-soft: rgba(255,255,255,.14);
--light: #ffffff;
--light-ink: #000000;
```

Black and white do the brand work. Generated cinematic imagery may contribute grayscale depth, but UI chrome should not add colored glows, gradients, or decorative accents.

## Typography

- Latin/UI chrome: `D-DIN`, `Arial Narrow`, `Arial`, `Verdana`, sans-serif fallback.
- Traditional Chinese content: `Noto Sans TC`, `PingFang TC`, `Microsoft JhengHei`, system sans-serif.
- Display headings use heavy condensed rhythm, uppercase for Latin fragments, tight line-height, positive tracking.
- Chinese headings should preserve readability: use weight and scale instead of forcing Latin-style uppercase behavior.
- No serif display pairing and no mono-as-decoration. Code blocks may use system mono only because they contain code/prompt text.

## Layout

- Every page opens with a near full-viewport hero over a generated black-and-white mission-control background.
- Top navigation is fixed/overlay style: black transparent surface, white text, minimal borders.
- The main article uses a mission layout: sticky chapter rail on desktop, single readable column on mobile.
- Content modules use small radii, hairline borders, and flat surfaces. Avoid soft shadows, glassmorphism, nested cards, and bento grids.
- Tables, code blocks, details/FAQ, and callouts must remain highly readable on mobile.

## Components

### Mission Hero
Full-bleed dark hero with a short label, one large H1, one lead paragraph, one ghost outlined CTA, and a compact guide telemetry strip. The CTA is a ghost pill. Do not place two competing CTAs in the hero.

### Overlay Nav
Fixed at top with wordmark and five guide links. On mobile the links scroll horizontally instead of becoming a dense menu.

### Chapter Rail
Desktop-only sticky rail generated from page headings. It provides progress orientation, not decoration. The active state is a white hairline/text shift, not a colored badge.

### Article Modules
Use flat panels only when they group real content: code/prompt blocks, tables, callouts, FAQ/details, workflow steps. Default long-form text should remain open and unboxed.

### Motion
Use GSAP core and ScrollTrigger:

- Hero load: timeline for label, H1 lines, lead, CTA, telemetry.
- Content reveal: `ScrollTrigger.batch()` for headings and major modules.
- Progress: top scroll bar and chapter rail fill/scrub.
- Parallax: subtle transform on hero media only.
- Reduced motion: no large transforms, no scrub/parallax, immediate content visibility.

## Do Not

- Do not add purple gradients, beige paper backgrounds, decorative orbs, glow blobs, glass cards, or icon grids.
- Do not use gradient text.
- Do not pair 1px borders with large soft card shadows.
- Do not repeat tiny eyebrow labels above every section.
- Do not convert long article sections into repeated equal cards.
- Do not make animations a gate for content visibility.
