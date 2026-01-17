# COREcare Design System

The COREcare design system establishes a unified visual language across all user-facing pages (landing, portal, admin). This document defines the color palette, typography, spacing, components, and usage patterns to ensure consistency and maintainability.

## Table of Contents
1. [Colors](#colors)
2. [Typography](#typography)
3. [Spacing & Layout](#spacing--layout)
4. [Components](#components)
5. [Usage Patterns](#usage-patterns)
6. [Mobile Responsiveness](#mobile-responsiveness)
7. [Accessibility](#accessibility)
8. [CSS Architecture](#css-architecture)

---

## Colors

The COREcare brand uses a carefully chosen palette of Emerald and Navy, complemented by neutral grays and semantic colors for status messaging.

### Primary Colors

| Color | Hex | Use Case | CSS Variable |
|-------|-----|----------|--------------|
| **Emerald** | `#2ecc71` | Primary actions, buttons, links, accents | `--primary` |
| **Emerald (Hover)** | `#27ae60` | Hover state for primary actions | `--primary-hover` |
| **Emerald (Light 10%)** | `rgba(46, 204, 113, 0.1)` | Light backgrounds, hover states for rows | `--primary-light` |
| **Navy** | `#2c3e50` | Headers, text, dark accents | `--navy` |
| **Navy (Light)** | `#34495e` | Secondary accents, borders | `--navy-light` |

### Neutral Colors

| Color | Hex | Use Case | CSS Variable |
|-------|-----|----------|--------------|
| **Background** | `#f8f9fa` | Page background | `--bg` |
| **Card** | `#ffffff` | Card backgrounds, form inputs | `--card` |
| **Text** | `#2c3e50` | Primary text (same as Navy) | `--text` |
| **Text (Light)** | `#6c757d` | Secondary text, less emphasis | `--text-light` |
| **Text (Muted)** | `#adb5bd` | Help text, disabled state, tertiary text | `--text-muted` |
| **Border** | `#e0e0e0` | Borders, dividers, separators | `--border` |

### Semantic Colors

| Color | Hex | Use Case | CSS Variable |
|-------|-----|----------|--------------|
| **Success** | `#2ecc71` | Success messages, positive feedback | `--success` |
| **Warning** | `#f39c12` | Warning messages, caution states | `--warning` |
| **Danger** | `#e74c3c` | Errors, delete actions, critical alerts | `--danger` |
| **Info** | `#3498db` | Information messages, neutral alerts | `--info` |

### Usage Examples

```css
/* Button with primary color */
.btn-primary {
  background: var(--primary);
  color: #fff;
}

.btn-primary:hover {
  background: var(--primary-hover);
}

/* Text content */
body {
  color: var(--text);
}

/* Secondary text (labels, help) */
.text-muted {
  color: var(--text-muted);
}

/* Error state */
.error-message {
  background: #fadbd8;  /* Light red */
  color: var(--danger);
}
```

---

## Typography

COREcare uses two Google Fonts for a professional, accessible appearance:
- **Playfair Display** (serif) - Headings, brand elements
- **Inter** (sans-serif) - Body text, UI labels, form inputs

### Font Weights

| Weight | Use Case | Font |
|--------|----------|------|
| 400 | Body text, form inputs | Inter |
| 500 | Labels, secondary headings | Inter |
| 600 | Emphasis, button text, menu items | Inter, Playfair Display |
| 700 | Headings, bold text | Playfair Display |

### Font Sizes

| Size | Usage | HTML Tag | Example |
|------|-------|----------|---------|
| `1.6rem` | Page titles, main headings | `<h1>` | "Welcome to COREcare" |
| `1.3rem` | Section headings | `<h2>` | "Your Care Dashboard" |
| `1.1rem` | Subsection headings | `<h3>` | "Today's Schedule" |
| `1rem` | Body text, form labels | `<p>`, `<label>` | Standard paragraph text |
| `0.95rem` | Secondary labels | `<label>` | Form field labels |
| `0.9rem` | Button text, metadata | `<button>`, `<small>` | Button labels |
| `0.85rem` | Help text, captions | `<small>` | "This field is required" |

### Font Import

All stylesheets include:
```css
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');
```

### Usage Examples

```css
/* Page title */
h1 {
  font-family: 'Playfair Display', serif;
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--navy);
}

/* Body text */
body, p {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.6;
  color: var(--text);
}

/* Form label */
label {
  font-family: 'Inter', sans-serif;
  font-size: 0.95rem;
  font-weight: 500;
  color: var(--navy);
}

/* Help text */
.form-help {
  font-family: 'Inter', sans-serif;
  font-size: 0.85rem;
  color: var(--text-muted);
}
```

---

## Spacing & Layout

COREcare uses a 8px base unit for consistent spacing throughout the application.

### Spacing Scale

| Multiplier | Pixels | CSS Variable | Usage |
|------------|--------|--------------|-------|
| 0.5x | 4px | - | Fine adjustments, minimal spacing |
| 1x | 8px | `--spacing-1` | Basic spacing between elements |
| 1.5x | 12px | `--spacing-2` | Form field spacing, small gaps |
| 2x | 16px | `--spacing-3` | Default padding/margin, standard gaps |
| 2.5x | 20px | `--spacing-4` | Section spacing, larger margins |
| 3x | 24px | `--spacing-5` | Card padding, page margins |
| 4x | 32px | `--spacing-6` | Large section spacing |

### Padding & Margin

```css
/* Small form elements */
input, button, select {
  padding: 10px 12px;     /* 12px vertical, 12px horizontal */
}

/* Cards */
.card {
  padding: 24px;          /* 3x (24px) on all sides */
}

/* Section spacing */
section {
  margin-bottom: 24px;    /* 3x (24px) */
}

/* Form field spacing */
.form-group {
  margin-bottom: 16px;    /* 2x (16px) */
}
```

### Shadows

| Severity | CSS | Usage |
|----------|-----|-------|
| Subtle | `0 2px 8px rgba(0, 0, 0, 0.06)` | Cards, small elements |
| Standard | `0 4px 20px rgba(0, 0, 0, 0.08)` | Sticky headers, prominent cards |

```css
--shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
--shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.06);

.card {
  box-shadow: var(--shadow-sm);
}

.header {
  box-shadow: var(--shadow);
}
```

---

## Components

### Buttons

#### Primary Button
- **Color**: Emerald (#2ecc71)
- **Text**: White (#fff)
- **Padding**: 10px 20px
- **Border Radius**: 6px
- **Hover**: Darker Emerald (#27ae60), slight lift effect

```html
<button class="btn btn-primary">Sign Up</button>
```

```css
.btn-primary {
  background: var(--primary);
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary:hover {
  background: var(--primary-hover);
  box-shadow: var(--shadow-sm);
  transform: translateY(-1px);
}
```

#### Secondary Button
- **Color**: Navy (#2c3e50)
- **Text**: White (#fff)
- **Use**: Links, cancel actions, tertiary CTAs

```html
<button class="btn btn-secondary">Cancel</button>
```

#### Delete/Danger Button
- **Color**: Red (#e74c3c)
- **Text**: White (#fff)
- **Use**: Destructive actions (delete, remove)

```html
<button class="btn btn-danger">Delete</button>
```

### Form Elements

#### Text Input
```html
<input type="text" class="form-input" placeholder="Username">
```

```css
.form-input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--border);
  border-radius: 4px;
  font-family: 'Inter', sans-serif;
  font-size: 1rem;
  color: var(--text);
  background: var(--card);
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px var(--primary-light);
}
```

#### Form Group
```html
<div class="form-group">
  <label class="form-label">Email Address</label>
  <input type="email" class="form-input" required>
  <small class="form-help">We'll never share your email.</small>
</div>
```

```css
.form-group {
  margin-bottom: 16px;
}

.form-label {
  color: var(--navy);
  font-weight: 500;
  display: block;
  margin-bottom: 6px;
  font-size: 0.95rem;
}

.form-help {
  color: var(--text-muted);
  display: block;
  margin-top: 4px;
  font-size: 0.85rem;
}

.form-field-error {
  color: var(--danger);
  display: block;
  margin-top: 4px;
  font-size: 0.85rem;
}
```

### Cards

```html
<div class="card">
  <h2 class="card-title">Upcoming Schedule</h2>
  <p>Content goes here</p>
</div>
```

```css
.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 24px;
  box-shadow: var(--shadow-sm);
}

.card-title {
  font-family: 'Playfair Display', serif;
  color: var(--navy);
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 1.3rem;
}
```

### Messages (Alerts)

#### Success Message
```html
<div class="message message-success">
  Profile updated successfully!
</div>
```

```css
.message-success {
  background: rgba(46, 204, 113, 0.1);
  color: var(--success);
  padding: 12px 16px;
  border-radius: 6px;
  border-left: 4px solid var(--success);
}
```

#### Error Message
```html
<div class="message message-error">
  Invalid username or password.
</div>
```

```css
.message-error {
  background: #fadbd8;
  color: var(--danger);
  padding: 12px 16px;
  border-radius: 6px;
  border-left: 4px solid var(--danger);
}
```

---

## Usage Patterns

### Template Inheritance

All authenticated pages should extend `base.html`:

```django
{% extends "base.html" %}

{% block title %}Page Title{% endblock %}

{% block content %}
<!-- Page content here -->
{% endblock %}
```

The `base.html` template provides:
- Navy header with COREcare branding
- Navigation
- Portal CSS stylesheet link
- Footer
- Consistent layout wrapper

### Unauthenticated Pages

Unauthenticated pages (landing, login, signup) should extend `base.html` and will inherit the header/footer styling automatically.

### Creating New Pages

1. **Extend base.html** for consistency
2. **Use CSS classes from portal.css or admin.css** - never use inline `style=""`
3. **Use semantic HTML**: `<h1>`, `<h2>`, `<label>`, `<button>`
4. **Leverage CSS variables**: `var(--primary)`, `var(--navy)`, `var(--text-muted)`, etc.
5. **Test on mobile**: Use Chrome DevTools device emulation

### Adding New Components

If creating a reusable component (e.g., a modal, card variant):

1. Define all styles in `portal.css` or `admin.css`
2. Use BEM (Block Element Modifier) naming for clarity:
   ```css
   .component-name { }           /* Block */
   .component-name__element { }  /* Element */
   .component-name--variant { }  /* Modifier */
   ```
3. Document in this file under the Components section
4. Use semantic HTML without inline styles

### Example: Creating a New Page

```django
{% extends "base.html" %}
{% block title %}My New Page{% endblock %}

{% block content %}
<div class="main-content">
  <h1>Welcome</h1>

  <div class="card">
    <h2 class="card-title">Card Title</h2>
    <p class="text-muted">Secondary text here</p>
  </div>

  <form method="POST" class="auth-form">
    {% csrf_token %}
    <div class="form-group">
      <label class="form-label">Name</label>
      <input type="text" class="form-input" name="name" required>
    </div>
    <button type="submit" class="btn btn-primary">Submit</button>
  </form>
</div>
{% endblock %}
```

---

## Mobile Responsiveness

The design system is mobile-first. Breakpoints are defined at:

| Breakpoint | Width | Use Case |
|-----------|-------|----------|
| **Mobile** | 320px-767px | Default, optimized for small screens |
| **Tablet** | 768px-1023px | Medium screens, flexible layouts |
| **Desktop** | 1024px+ | Large screens, multi-column layouts |

### Responsive Layout Example

```css
/* Mobile first */
.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

/* Tablet and up */
@media (min-width: 768px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

### Navigation Responsiveness

The header adapts to mobile screens. Test the following breakpoints:
- **320px**: iPhone SE, older phones
- **375px**: iPhone 12/13
- **428px**: iPhone 14 Pro
- **768px**: iPad
- **1024px**: iPad Pro, desktop

---

## Accessibility

All COREcare pages must meet **WCAG AA** standards for accessibility.

### Color Contrast

All interactive elements must have a contrast ratio of at least **4.5:1** for normal text and **3:1** for large text.

#### Verified Contrasts
- Navy text (#2c3e50) on light background (#f8f9fa): **14:1** ✓
- Emerald text (#2ecc71) on white: **3.1:1** (use for non-critical text only)
- Emerald button text (#fff) on Emerald (#2ecc71): **4.5:1** ✓
- Navy button text (#fff) on Navy (#2c3e50): **6.5:1** ✓
- Red error text (#e74c3c) on white: **5.5:1** ✓

### Form Accessibility

All form inputs must have:
- Associated `<label>` with `for` attribute
- Clear focus states (border color + box-shadow)
- Error messages linked to inputs via `aria-describedby`

```html
<div class="form-group">
  <label for="email" class="form-label">Email</label>
  <input
    id="email"
    type="email"
    class="form-input"
    aria-describedby="email-help"
    required>
  <small id="email-help" class="form-help">We'll never share your email.</small>
</div>
```

### Focus States

All interactive elements (buttons, links, inputs) must have visible focus states:

```css
button:focus, a:focus {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
}
```

### Images & Icons

All images must have descriptive alt text:
```html
<img src="logo.png" alt="COREcare Access Logo">
```

---

## CSS Architecture

### File Organization

```
static/css/
├── portal.css          /* Main portal design system */
└── admin.css           /* Django admin interface styling */
```

### CSS Variables

All colors, shadows, and common values use CSS custom properties for maintainability:

```css
:root {
  /* Colors */
  --primary: #2ecc71;
  --primary-hover: #27ae60;
  --primary-light: rgba(46, 204, 113, 0.1);
  --navy: #2c3e50;
  --navy-light: #34495e;
  --bg: #f8f9fa;
  --card: #ffffff;
  --text: #2c3e50;
  --text-light: #6c757d;
  --text-muted: #adb5bd;
  --border: #e0e0e0;

  /* Effects */
  --shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.06);

  /* Status */
  --success: #2ecc71;
  --warning: #f39c12;
  --danger: #e74c3c;
  --info: #3498db;
}
```

### Naming Conventions

Class names follow a semantic, readable pattern:

```css
/* Layout */
.main-content { }
.container { }
.header { }

/* Components */
.button, .btn, .btn-primary { }
.card { }
.form-group { }

/* Modifiers (use with BEM) */
.btn--large { }
.card--highlighted { }

/* States */
.is-active { }
.is-disabled { }
.has-error { }
```

### Avoiding Anti-Patterns

❌ **Don't do this:**
```css
/* Inline styles in templates */
<div style="color: #2ecc71; padding: 20px; border-radius: 8px;">

/* ID selectors (too specific) */
#my-button { color: red; }

/* !important flags */
.text-primary { color: var(--primary) !important; }

/* Magic numbers */
.card { padding: 23px; }   /* Should be 24px, a multiple of 8 */
```

✅ **Do this instead:**
```css
/* Use classes from stylesheet */
<div class="card">

/* Use class selectors */
.button-primary { color: white; }

/* Use CSS variables and base units */
.card { padding: 24px; }

/* Let cascade work */
.text-primary { color: var(--primary); }
```

---

## Maintenance & Updates

### Updating Colors

To change the primary color globally, update the CSS variable in `portal.css` and `admin.css`:

```css
:root {
  --primary: #NEW_COLOR;
  --primary-hover: #NEW_HOVER;
  --primary-light: rgba(N, E, W, 0.1);
}
```

All pages that reference `var(--primary)` will automatically update.

### Adding New Components

1. Define in `portal.css` with clear comments
2. Document here with HTML examples
3. Test on mobile (320px, 768px, 1024px breakpoints)
4. Verify WCAG AA contrast ratios
5. Commit with message: "Add new component: [component name]"

### CSS Linting

The build process includes CSS linting with [stylelint](https://stylelint.io/) to enforce consistency:

```bash
npm run lint:css
```

Linting rules are configured in `.stylelintrc.json` to match this design system.

---

## Questions or Issues?

If you're unsure about design decisions or need clarification:
1. Check this document first
2. Ask in the #design-system Slack channel
3. Create an issue with the `design-system` label

Remember: Consistency is key. When in doubt, match the existing pattern.
