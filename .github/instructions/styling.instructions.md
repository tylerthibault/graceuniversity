---
applyTo: '**'
---

# CSS/Styling Guidelines for Flask Application

## Core Styling Philosophy

This project uses **Bootstrap as the foundation** with **custom CSS for enhancements**.

**Key Principles:**
- **Bootstrap First** - Use Bootstrap classes for layout, grid, and common components
- **Custom CSS Second** - Build on Bootstrap with custom classes for branding and unique designs
- **NO Inline Styles** - Never use `style=""` attributes in HTML
- **CSS Classes Only** - All styling must come from CSS files
- **Exception:** One-off styles can use `<style>` tags within the template file

## CSS Architecture

### File Structure
```
src/static/css/
├── main.css                 # Global styles and variables
├── components/              # Reusable component styles
└── pages/                   # Page-specific styles
```

### Loading Order
```html
<!-- 1. Bootstrap CDN -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- 2. Global custom CSS -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">

<!-- 3. Page-specific CSS (in child templates) -->
{% block styles %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/pages/landing.css') }}">
{% endblock %}
```

## Styling Rules

### 1. NO Inline Styles ❌

**NEVER do this:**
```html
<!-- BAD - Inline styles -->
<div style="color: red; margin-top: 20px;">
    <p style="font-size: 16px;">Text</p>
</div>
```

**ALWAYS do this:**
```html
<!-- GOOD - CSS classes -->
<div class="error-message">
    <p class="body-text">Text</p>
</div>
```

```css
/* In CSS file */
.error-message {
    color: red;
    margin-top: 20px;
}

.body-text {
    font-size: 16px;
}
```

### 2. Bootstrap First, Custom Second

**Use Bootstrap classes for common patterns:**
```html
<!-- Good: Bootstrap for layout and spacing -->
<div class="container">
    <div class="row g-4">
        <div class="col-md-6">
            <button class="btn btn-primary">Submit</button>
        </div>
    </div>
</div>
```

**Add custom classes for branding/customization:**
```html
<!-- Good: Bootstrap + Custom classes -->
<div class="container">
    <div class="row g-4">
        <div class="col-md-6">
            <button class="btn btn-primary btn-grace">Submit</button>
        </div>
    </div>
</div>
```

```css
/* Custom enhancement */
.btn-grace {
    border-radius: 8px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
```

### 3. CSS Class Naming Conventions

**Use BEM (Block Element Modifier) or semantic naming:**

```css
/* BEM Example */
.card-user { }
.card-user__header { }
.card-user__title { }
.card-user--featured { }

/* Semantic Example */
.dashboard-stats { }
.dashboard-stats-item { }
.dashboard-stats-item-value { }
```

**Usage:**
```html
<div class="card card-user card-user--featured">
    <div class="card-user__header">
        <h3 class="card-user__title">John Doe</h3>
    </div>
</div>
```

### 4. One-Off Styles: Use `<style>` Tags

**For truly unique, page-specific styles:**

```html
{% extends "bases/public.html" %}

{% block content %}
<!-- One-off style in template -->
<style>
    .landing-hero-gradient {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 600px;
    }
    
    .landing-cta-pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
</style>

<section class="landing-hero-gradient">
    <button class="btn btn-primary landing-cta-pulse">Get Started</button>
</section>
{% endblock %}
```

**When to use `<style>` tags:**
- ✅ Truly unique styles used only once on a single page
- ✅ Experimental/temporary styles
- ✅ Dynamic styles based on template variables
- ❌ NOT for reusable components
- ❌ NOT for common patterns

## CSS Organization

### Global Variables (main.css)

```css
/* CSS Variables for consistency */
:root {
    /* Colors */
    --color-primary: #667eea;
    --color-secondary: #764ba2;
    --color-success: #10b981;
    --color-danger: #ef4444;
    
    /* Spacing */
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 1.5rem;
    --spacing-xl: 2rem;
    
    /* Border Radius */
    --radius-sm: 4px;
    --radius-md: 8px;
    --radius-lg: 12px;
    
    /* Shadows */
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

/* Global styles */
body {
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    color: #1f2937;
    line-height: 1.6;
}
```

### Component Styles Example

```css
/* Custom button extending Bootstrap */
.btn-grace-primary {
    background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
    border: none;
    border-radius: var(--radius-md);
    font-weight: 600;
    transition: all 0.3s ease;
}

.btn-grace-primary:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}
```

## Responsive Design

**Use Bootstrap breakpoints or media queries:**

```css
/* Bootstrap breakpoints: xs(<576px), sm(≥576px), md(≥768px), lg(≥992px), xl(≥1200px), xxl(≥1400px) */

.hero-section {
    padding: var(--spacing-xl) 0;
}

@media (min-width: 768px) {
    .hero-section {
        padding: 4rem 0;
    }
}
```

## Common Patterns

### Cards
```html
<!-- Bootstrap card with custom enhancements -->
<div class="card card-custom">
    <div class="card-body">
        <h5 class="card-title card-title-custom">Title</h5>
        <p class="card-text">Content</p>
        <a href="#" class="btn btn-primary btn-grace-primary">Action</a>
    </div>
</div>
```

```css
.card-custom {
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card-custom:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-xl);
}

.card-title-custom {
    color: var(--color-primary);
    font-weight: 600;
}
```

### Forms
```html
<!-- Bootstrap form with custom styling -->
<form class="form-grace">
    <div class="mb-3">
        <label for="email" class="form-label form-label-grace">Email</label>
        <input type="email" class="form-control form-control-grace" id="email">
    </div>
    <button type="submit" class="btn btn-primary btn-grace-primary">Submit</button>
</form>
```

```css
.form-grace {
    max-width: 500px;
}

.form-label-grace {
    font-weight: 600;
    color: #374151;
    margin-bottom: var(--spacing-sm);
}

.form-control-grace {
    border-radius: var(--radius-md);
    border: 2px solid #e5e7eb;
    padding: 0.75rem;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.form-control-grace:focus {
    border-color: var(--color-primary);
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}
```