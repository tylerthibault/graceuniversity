# Grace City Theme System

## Overview
The Grace City theme system provides automatic dark/light mode switching with localStorage persistence and zero-flash loading.

## Features
- ✅ **No Flash of Wrong Theme** - Theme loads before page render
- ✅ **Persistent Preference** - Remembers user choice in localStorage
- ✅ **Automatic Switching** - Single toggle changes entire site
- ✅ **CSS Variables** - Easy theming with custom properties
- ✅ **Event System** - Listen for theme changes in your code

## File Structure
```
src/static/
├── js/components/
│   └── theme.js              # Theme manager (loads first)
└── css/components/
    ├── theme-vars.css        # CSS variables for both themes
    ├── buttons.css           # Component styles
    ├── cards.css
    ├── tables.css
    ├── dividers.css
    └── typography.css
```

## Quick Start

### 1. Theme Toggle Button
Already included in `bases/public.html`:

```html
<button class="gc-theme-toggle" 
        data-gc-theme-toggle 
        data-light-text="☀️ Light" 
        data-dark-text="🌙 Dark">
    🌙 Dark
</button>
```

### 2. Using CSS Variables
In your custom styles:

```css
.my-element {
    background: var(--gc-bg-secondary);
    color: var(--gc-text-primary);
    border: 2px solid var(--gc-border-primary);
    box-shadow: var(--gc-shadow-md);
}
```

### 3. Using Component Classes
Load component CSS in your template:

```html
{% block styles %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/components/buttons.css') }}">
<link rel="stylesheet" href="{{ url_for('static', filename='css/components/cards.css') }}">
{% endblock %}
```

Then use classes:
```html
<button class="gc-btn gc-btn-dark-primary">Click Me</button>
<div class="gc-card gc-card-light">Card content</div>
```

## Available CSS Variables

### Backgrounds
- `--gc-bg-primary` - Main page background
- `--gc-bg-secondary` - Container backgrounds  
- `--gc-bg-tertiary` - Nested elements
- `--gc-bg-container` - Card/modal backgrounds

### Steel Tones
- `--gc-steel-light` - Light steel accents
- `--gc-steel-mid` - Medium steel elements
- `--gc-steel-dark` - Dark steel borders

### Wood Tones
- `--gc-wood-light` - Light wood accents
- `--gc-wood-mid` - Medium wood elements
- `--gc-wood-dark` - Dark wood borders
- `--gc-wood-accent` - Wood text color

### Text Colors
- `--gc-text-primary` - Main text
- `--gc-text-secondary` - Secondary text
- `--gc-text-tertiary` - Muted text

### Borders
- `--gc-border-primary` - Main borders
- `--gc-border-secondary` - Subtle borders

### Shadows
- `--gc-shadow-sm` - Small shadows
- `--gc-shadow-md` - Medium shadows
- `--gc-shadow-lg` - Large shadows
- `--gc-shadow-inset` - Inset shadows

## JavaScript API

### Toggle Theme
```javascript
GCTheme.toggle(); // Switches between dark and light
```

### Set Specific Theme
```javascript
GCTheme.set('dark');  // Force dark mode
GCTheme.set('light'); // Force light mode
```

### Get Current Theme
```javascript
const currentTheme = GCTheme.get(); // Returns 'dark' or 'light'
```

### Check if Dark Mode
```javascript
if (GCTheme.isDark()) {
    console.log('Dark mode is active');
}
```

### Listen for Theme Changes
```javascript
window.addEventListener('gc-theme-changed', (event) => {
    console.log('Theme changed to:', event.detail.theme);
    // Update your custom UI elements here
});
```

## Auto-Switching Components

Components automatically adapt when theme changes:

### Buttons
```html
<!-- Dark mode -->
<button class="gc-btn gc-btn-dark-primary"><span>Action</span></button>

<!-- Light mode -->
<button class="gc-btn gc-btn-light-primary"><span>Action</span></button>
```

### Cards
```html
<!-- Dark mode -->
<div class="gc-card gc-card-dark">
    <h3>Title</h3>
    <p>Content</p>
</div>

<!-- Light mode -->
<div class="gc-card gc-card-light">
    <h3>Title</h3>
    <p>Content</p>
</div>
```

### Tables
```html
<div class="gc-table-container gc-table-dark">
    <table>...</table>
</div>
```

## Manual Theme Selection

For pages that need to explicitly use one theme (like index7.html for dark, index8.html for light), you can skip the component classes and use inline styles based on the design, or use data attributes:

```html
<body data-gc-theme="dark">
    <!-- This page will always be dark -->
</body>
```

## Best Practices

1. **Use CSS Variables** - Prefer variables over hardcoded colors
2. **Component Classes** - Use `.gc-*` classes for consistent styling
3. **Avoid Inline Styles** - Use CSS classes for theme-aware styling
4. **Test Both Themes** - Always verify appearance in both modes
5. **Smooth Transitions** - Theme changes are animated automatically

## Troubleshooting

### Flash of Wrong Theme
Make sure `theme.js` loads BEFORE any CSS:
```html
<head>
    <script src="{{ url_for('static', filename='js/components/theme.js') }}"></script>
    <!-- CSS comes after -->
</head>
```

### Theme Not Persisting
Check if localStorage is enabled in the browser. The system falls back to dark mode if localStorage is unavailable.

### Components Not Changing
Verify you're using the correct class names:
- Dark: `.gc-btn-dark`, `.gc-card-dark`, `.gc-table-dark`
- Light: `.gc-btn-light`, `.gc-card-light`, `.gc-table-light`

## Examples

See these files for reference:
- **Dark Mode**: `templates/public/landing/index7.html`
- **Light Mode**: `templates/public/landing/index8.html`
- **Style Guide**: `.github/instructions/grace-city-style-guide.md`
