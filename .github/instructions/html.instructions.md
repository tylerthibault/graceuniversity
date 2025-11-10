---
applyTo: '**'
---

# HTML/Jinja2 Template Structure Guidelines

## Project Structure
This Flask application uses a page-based structure with Jinja2 templating:

### Directory Structure
- `templates/bases/` - Base templates for inheritance
  - `public.html` - Base template for public pages (before login)
  - `private.html` - Base template for private pages (after login)
- `templates/public/<page_name>/` - Public pages
  - `index.html` - Main page template
  - `components/` - Page-specific components
    - `<component_name>.html` - Individual component files
- `templates/private/<role>/<page_name>/` - Private pages by role
  - `index.html` - Main page template
  - `components/` - Page-specific components
    - `<component_name>.html` - Individual component files

## Template Inheritance Rules

### 1. Main Page Templates (`<page_name>/index.html`)
All main page templates MUST use Jinja2 `{% extends %}` to inherit from a base template:

**For Public Pages (before login):**
```html
{% extends "bases/public.html" %}

{% block title %}Page Title{% endblock %}

{% block content %}
  <!-- Page content here -->
{% endblock %}
```

**For Private Pages (after login):**
```html
{% extends "bases/private.html" %}

{% block title %}Page Title{% endblock %}

{% block content %}
  <!-- Page content here -->
{% endblock %}
```

### 2. Component Files (`<page_name>/components/<component_name>.html`)
Component files contain reusable HTML snippets that are included in main page templates:

**Component Example (`components/hero_section.html`):**
```html
<section class="hero">
  <h1>{{ title }}</h1>
  <p>{{ description }}</p>
</section>
```

**Including Components in Main Templates:**
```html
{% extends "bases/public.html" %}

{% block content %}
  {% include "public/landing/components/hero_section.html" %}
  {% include "public/landing/components/features.html" %}
{% endblock %}
```

## File Naming Conventions
- Main page template: Always named `index.html`
- Components: Descriptive names in snake_case (e.g., `navigation_bar.html`, `user_card.html`)
- Directories: Page names in snake_case or lowercase (e.g., `landing/`, `dashboard/`, `user_profile/`)

## Best Practices
1. **Always extend from a base template** - Never create standalone HTML pages
2. **Use components for reusability** - Break pages into logical components
3. **Pass context variables** - Use Jinja2 variables for dynamic content
4. **Keep components focused** - Each component should have a single responsibility
5. **Consistent block names** - Use standard block names: `title`, `content`, `scripts`, `styles`

## Example Page Structure

### Public Page (Landing)
```
templates/public/landing/
├── index.html                    # Extends bases/public.html
└── components/
    ├── hero_section.html
    ├── features.html
    └── cta_section.html
```

### Private Page (Dashboard)
```
templates/private/admin/dashboard/
├── index.html                    # Extends bases/private.html
└── components/
    ├── stats_cards.html
    ├── recent_activity.html
    └── user_table.html
```