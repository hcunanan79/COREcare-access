# Contributing to COREcare Access

Thank you for contributing to COREcare Access! This guide will help you get started.

## Getting Started

1. **Read the [README.md](README.md)** for project overview and setup instructions
2. **Set up your local environment** following the development setup guide
3. **Review the [Architecture](docs/ARCHITECTURE.md)** to understand the system design

## Development Workflow

### Branch Strategy

```
main (production)
  └── feature/your-feature-name
  └── fix/bug-description
  └── docs/documentation-update
```

- `main` - Production branch, auto-deploys to Render
- `feature/*` - New features
- `fix/*` - Bug fixes
- `docs/*` - Documentation updates

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the code style guidelines below

3. **Test locally**
   ```bash
   python manage.py runserver
   # Test your changes at http://localhost:8000
   ```

4. **Run migrations** if you modified models
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Commit with clear messages**
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

6. **Push and create a Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Pull Request Guidelines

- Provide a clear description of what changed and why
- Link any related issues
- Ensure the app runs without errors locally
- Request review from a team member

## Code Style

### Python

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use meaningful variable and function names
- Keep functions focused and small
- Add docstrings for complex functions

### Django Conventions

- Models: Singular names (`Client`, not `Clients`)
- Views: Use class-based views for complex logic, function-based for simple
- Templates: Use template inheritance with `base.html`
- URLs: Use descriptive, lowercase names with hyphens

### Templates & Design System

- Extend from `base.html` for consistent styling
- Use Django template tags properly (`{% %}` for logic, `{{ }}` for output)
- Keep logic minimal in templates
- **Always follow the [COREcare Design System](docs/DESIGN_SYSTEM.md)** for all user-facing pages
  - Use CSS classes from `portal.css` or `admin.css`, never inline `style=""`
  - Use semantic HTML (`<h1>`, `<h2>`, `<label>`, `<button>`)
  - Leverage CSS variables: `var(--primary)`, `var(--navy)`, `var(--text-muted)`
  - Test responsive design at 320px, 768px, and 1024px breakpoints
  - Verify WCAG AA color contrast ratios (4.5:1 for text)

**Design System Reference**: See [docs/DESIGN_SYSTEM.md](docs/DESIGN_SYSTEM.md) for:
- Color palette and CSS variables
- Typography guidelines (Playfair Display + Inter)
- Spacing and layout patterns
- Component examples (buttons, forms, cards, messages)
- Mobile responsiveness requirements
- Accessibility standards

### Mobile Testing Requirements

**Critical**: 70% of caregivers and 80% of family members access the portal via mobile. All UI changes MUST be tested on mobile devices before deployment.

#### Required Mobile Tests

Before submitting any PR that affects UI/templates/CSS:

- [ ] **iPhone Safari** (iOS 15, 16, or 17) - Test in portrait and landscape
- [ ] **Android Chrome** (latest version) - Test on physical device or emulator
- [ ] **Content Alignment**: Verify content is left-aligned on mobile (<961px), centered on desktop (≥961px)
- [ ] **No Horizontal Scroll**: Test at 320px width (iPhone SE) - no horizontal scrollbar
- [ ] **Touch Targets**: All buttons/links are ≥44px × 44px (tap-friendly)
- [ ] **Form Inputs**: Font size ≥16px to prevent auto-zoom on iOS
- [ ] **Safe Area**: Content respects iPhone notch/Dynamic Island (not obscured)
- [ ] **Viewport Meta Tag**: `viewport-fit=cover` is present in `<head>`

#### Mobile Testing Tools

**Real Devices (Preferred)**:
- Borrow team iPhones/Android phones for testing
- Test on your personal phone

**Chrome DevTools Device Emulation**:
1. Open Chrome DevTools (F12)
2. Click "Toggle Device Toolbar" (Ctrl+Shift+M / Cmd+Shift+M)
3. Test these viewports:
   - **320px** (iPhone SE) - Critical minimum width
   - **375px** (iPhone 12/13) - Most common
   - **393px** (iPhone 14 Pro) - Dynamic Island
   - **428px** (iPhone 14 Pro Max) - Large phone
   - **768px** (iPad) - Tablet breakpoint
   - **1024px** (iPad Pro landscape) - Desktop breakpoint

**Safari Responsive Design Mode** (macOS):
1. Open Safari Developer Tools (Cmd+Option+I)
2. Click "Responsive Design Mode" icon
3. Test iPhone 14 Pro, iPhone SE, iPad

#### Mobile-First CSS Pattern

**Always use mobile-first responsive design**:

```css
/* ❌ WRONG: Desktop-first */
.container {
  margin: 0 auto;  /* Centers on all screens */
}

@media (max-width: 600px) {
  .container {
    margin: 0;  /* Tries to fix mobile */
  }
}

/* ✅ CORRECT: Mobile-first */
.container {
  margin: 0;  /* Left-align by default (mobile) */
}

@media (min-width: 961px) {
  .container {
    margin: 0 auto;  /* Center only on desktop */
  }
}
```

**Reference**: See [Mobile Responsiveness](docs/DESIGN_SYSTEM.md#mobile-responsiveness) in the design system for full guidelines.

#### Common Mobile Issues to Avoid

❌ **Don't**:
- Use `margin: 0 auto` without a desktop media query
- Set font sizes <16px on form inputs (triggers iOS zoom)
- Forget `touch-action: manipulation` on buttons
- Use `:hover` without `:active` states
- Forget `viewport-fit=cover` meta tag

✅ **Do**:
- Test on real iPhones and Android devices
- Start with mobile styles, progressively enhance for desktop
- Use `touch-action: manipulation` on all interactive elements
- Verify safe-area-inset padding on notched devices
- Check WCAG reflow at 320px width

## Project Structure

```
COREcare-access/
├── elitecare/          # Django project settings
├── portal/             # Main portal & authentication
├── caregiver_portal/   # Caregiver features
├── clients/            # Client management
├── shifts/             # Shift scheduling
├── timeclock/          # Time tracking
├── employees/          # Employee profiles
├── credentials/        # Credential tracking
├── assessments/        # Client assessments
├── scheduling/         # Scheduling logic
├── notifications/      # Notification system
├── static/             # CSS, images, JavaScript
├── templates/          # Shared HTML templates
├── scripts/            # Development scripts
└── docs/               # Documentation
```

## Common Tasks

### Adding a New Feature

1. Create or update models in `app/models.py`
2. Run migrations
3. Add views in `app/views.py`
4. Create templates in `templates/app/` or `app/templates/`
5. Register URLs in `app/urls.py`
6. Update admin if needed in `app/admin.py`

### Adding a New Django App

```bash
python manage.py startapp appname
```

Then add to `INSTALLED_APPS` in `elitecare/settings.py`.

### Database Operations

```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Sync from production (for realistic test data)
./scripts/sync_from_prod.sh

# Access Django shell
python manage.py shell
```

### Running the Development Server

```bash
# Standard development server
python manage.py runserver

# With specific port
python manage.py runserver 8080

# Accessible from network
python manage.py runserver 0.0.0.0:8000
```

## Environment Variables

Key environment variables (see `.env.example`):

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `SECRET_KEY` | Django secret key | Yes (production) |
| `DEBUG` | Enable debug mode | No (default: True) |
| `EMPLOYEE_INVITE_CODE` | Registration invite code | No (default: CORECARE) |

## Deployment

- Pushing to `main` triggers auto-deploy on Render
- Migrations must be run manually via SSH after deployment
- Static files are served via WhiteNoise

## Getting Help

- Check existing documentation in `/docs`
- Review similar code in the codebase
- Ask team members for guidance

## Code Review Checklist

Before submitting a PR, verify:

- [ ] Code runs without errors locally
- [ ] No hardcoded secrets or credentials
- [ ] Migrations are included if models changed
- [ ] Templates render correctly
- [ ] URLs are properly configured
- [ ] Admin interface works if models are registered
