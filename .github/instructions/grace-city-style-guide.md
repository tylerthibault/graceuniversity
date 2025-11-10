# Grace City Design System Style Guide

## Design Philosophy
Grace City embodies a **masculine industrial-rustic aesthetic** combining steel and timber elements. The design language reflects strength, authenticity, and permanence through raw materials and honest construction.

## Color Palettes

### Dark Mode (Primary)
```css
/* Backgrounds */
--gc-dark-bg-primary: #0d0d0d;
--gc-dark-bg-secondary: #1a1a1a;
--gc-dark-bg-tertiary: #252525;

/* Steel Tones */
--gc-dark-steel-light: #6d6d6d;
--gc-dark-steel-mid: #4d4d4d;
--gc-dark-steel-dark: #3d3d3d;

/* Wood Tones */
--gc-dark-wood-light: #5a3d2a;
--gc-dark-wood-mid: #4a3320;
--gc-dark-wood-dark: #3d2817;

/* Text */
--gc-dark-text-primary: #d9d9d9;
--gc-dark-text-secondary: #a8a8a8;
--gc-dark-text-tertiary: #8a8a8a;
```

### Light Mode
```css
/* Backgrounds */
--gc-light-bg-primary: #f5f5f5;
--gc-light-bg-secondary: #fefefe;
--gc-light-bg-tertiary: #fafafa;

/* Steel Tones */
--gc-light-steel-light: #c0c0c0;
--gc-light-steel-mid: #a0a0a0;
--gc-light-steel-dark: #8a8a8a;

/* Wood Tones */
--gc-light-wood-light: #d4b896;
--gc-light-wood-mid: #c9a875;
--gc-light-wood-dark: #cca97f;

/* Text */
--gc-light-text-primary: #2d2d2d;
--gc-light-text-secondary: #4a4a4a;
--gc-light-text-tertiary: #5a5a5a;
```

## Typography
- **Primary Font**: 'Trebuchet MS', sans-serif
- **Headings**: Uppercase, wide letter-spacing (8-14px for h1, 3-5px for h2)
- **Weight**: Heavy (700-900) for headings, normal for body

## Core Visual Elements

### Steel Elements
- **I-Beams**: Vertical accents with gradients and inset shadows
- **Rivets**: Small circular elements (8-20px) with radial gradients
- **Corner Brackets**: Angular L-shapes on containers/cards
- **Dividers**: Horizontal beams with riveted ends

### Wood Elements
- **Grain Textures**: Horizontal linear gradients with warm browns
- **Accent Borders**: Top borders on cards/tables (5-6px)
- **Header Bars**: Wood-textured horizontal sections
- **Underlines**: Gradient wood strips (2-4px height)

### Grid & Spacing
- **Grid Background**: Subtle 2px repeating lines
- **Padding**: Generous (35-50px on containers)
- **Gaps**: 15-30px between elements
- **Border Radius**: Minimal (sharp corners preferred)

## Component Patterns

### Buttons
- **Shape**: Clipped polygon corners (10px cuts)
- **Decoration**: Steel rivets in corners
- **Hover**: Translate up 3px, enhance shadow
- **Primary**: Wood gradient background
- **Secondary**: Steel gradient background

### Cards
- **Border**: 2px steel, 5px wood top accent
- **Decoration**: Corner bracket (top-right), rivet
- **Hover**: Lift 8px, increase shadow
- **Title**: Wood underline gradient

### Tables
- **Top Border**: 6px wood gradient
- **Header**: Wood gradient background with steel bottom border
- **Rows**: Hover reveals wood left border (3px)
- **Decoration**: Rivet in header area

### Dividers
- **Height**: 8px steel beam
- **Rivets**: Both ends (20px from edge)
- **Shadow**: Inset top, drop bottom

## Shadow Guidelines
**Dark Mode**: Use rgba(0, 0, 0, 0.5-0.9)
**Light Mode**: Use rgba(0, 0, 0, 0.1-0.2)

## Component Classes
Use these component CSS files:
- `buttons.css` - All button variants
- `cards.css` - Card components
- `tables.css` - Table styling
- `dividers.css` - Section dividers
- `typography.css` - Headings and text

## Usage Rules
1. **Always** include steel + wood combination
2. **Prefer** sharp corners over rounded
3. **Use** heavy letter-spacing on uppercase text
4. **Add** rivets/industrial details to major elements
5. **Maintain** strong visual hierarchy through size/weight
6. **Keep** shadows subtle but present
7. **Ensure** accessibility contrast ratios (4.5:1 minimum)

## Examples
- Dark mode reference: `index7.html`
- Light mode reference: `index8.html`
