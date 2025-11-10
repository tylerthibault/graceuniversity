# Flash Message Component - Usage Guide

## Overview
The Grace City flash message component provides auto-dismissing notifications with a visual timer that pauses on hover.

## Features
- ✅ **Auto-dismiss** - Messages disappear after 5 seconds (configurable)
- ✅ **Pause on hover** - Timer pauses when cursor is over the message
- ✅ **Visual timer** - Progress bar shows countdown
- ✅ **Manual close** - Click X button to dismiss immediately
- ✅ **Multiple categories** - Success, error, warning, info
- ✅ **Theme-aware** - Follows Grace City theme system
- ✅ **Smooth animations** - Slide in/out with transitions

## Usage in Controllers

### Basic Flash Messages
```python
from flask import flash

# Success message
flash('Login successful!', 'success')

# Error message
flash('Invalid credentials', 'error')
# or
flash('Invalid credentials', 'danger')

# Warning message
flash('Your session will expire soon', 'warning')

# Info message
flash('Please check your email', 'info')
```

### Multiple Messages
```python
flash('User created successfully', 'success')
flash('Verification email sent', 'info')
```

## Message Categories

### Success (`success`)
- **Color**: Green (#10b981)
- **Icon**: Checkmark circle
- **Use for**: Successful operations, confirmations

### Error/Danger (`error` or `danger`)
- **Color**: Red (#ef4444)
- **Icon**: X circle
- **Use for**: Failed operations, validation errors

### Warning (`warning`)
- **Color**: Orange (#f59e0b)
- **Icon**: Triangle with exclamation
- **Use for**: Cautions, potential issues

### Info (`info`)
- **Color**: Blue (#3b82f6)
- **Icon**: Info circle
- **Use for**: General information, tips

## Configuration

### Default Duration
Messages auto-dismiss after 5000ms (5 seconds). This is set in the template:
```html
<div class="gc-flash gc-flash-{{ category }}" data-gc-flash data-duration="5000">
```

### Custom Duration
To change the duration, edit the `data-duration` attribute in `app_components/flash.html`:
```html
<div class="gc-flash gc-flash-{{ category }}" data-gc-flash data-duration="8000">
```

## Behavior

### Timer Lifecycle
1. Message appears with slide-in animation
2. Progress bar starts counting down
3. **On hover**: Timer pauses, progress bar stops
4. **On leave**: Timer resumes from where it paused
5. After duration completes or close button clicked: Message slides out

### Visual Feedback
- **Progress bar**: Horizontal bar at bottom shows remaining time
- **Hover effect**: Card elevates and shifts slightly left
- **Close button**: X icon in top-right corner

## Template Structure

The component is automatically included in:
- ✅ `bases/public.html` - All public pages
- ✅ `bases/private.html` - All private/authenticated pages

No need to manually include it in child templates.

## Styling

### Theme Integration
The component uses Grace City CSS variables:
- `--gc-bg-secondary` - Message background
- `--gc-border-primary` - Border color
- `--gc-text-primary` - Text color
- `--gc-shadow-card` - Shadow effects

### Responsive
- Desktop: Fixed position, top-right corner
- Mobile (<640px): Expands to full width with margins

## Examples

### Login Success
```python
@auth_bp.route('/login', methods=['POST'])
def login():
    # ... authentication logic ...
    flash('Welcome back!', 'success')
    return redirect(url_for('dashboard.index'))
```

### Form Validation Error
```python
@auth_bp.route('/register', methods=['POST'])
def register():
    if not validate_email(email):
        flash('Invalid email format', 'error')
        return redirect(url_for('auth.register_page'))
```

### Multiple Notifications
```python
@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.get_by_id(user_id)
    user.delete()
    
    flash(f'User {user.name} deleted successfully', 'success')
    flash('All associated data has been removed', 'info')
    
    return redirect(url_for('admin.users'))
```

## Accessibility

- **ARIA labels**: Close button has `aria-label="Close"`
- **Keyboard accessible**: Close button can be focused and activated
- **Color contrast**: All categories meet WCAG AA standards
- **Icons + text**: Messages include both icon and text for clarity

## Technical Details

### JavaScript Class
- `FlashMessage` class handles each message
- Tracks: duration, remaining time, pause state
- Uses `requestAnimationFrame` for smooth progress bar
- Cleans up DOM when message is removed

### Animation
- **Slide in**: `slideInRight` (0.3s ease-out)
- **Slide out**: `slideOutRight` (0.3s ease-out)
- **Progress bar**: Linear transform with `requestAnimationFrame`

### Position
- Fixed positioning: `top: 20px; right: 20px`
- Z-index: 9999 (above all content)
- Stack vertically with 12px gap

## Troubleshooting

### Messages Not Appearing
1. Check if flash is being called in controller
2. Verify base template includes `app_components/flash.html`
3. Check browser console for JavaScript errors

### Timer Not Working
1. Ensure JavaScript is enabled
2. Check if `data-gc-flash` attribute exists
3. Verify `data-duration` is a valid number

### Wrong Colors
1. Check category name matches: `success`, `error`/`danger`, `warning`, `info`
2. Verify theme CSS variables are loaded
3. Check browser DevTools for CSS conflicts

## Best Practices

1. **Keep messages short** - One line is ideal
2. **Use appropriate category** - Match severity to category
3. **Don't spam** - Limit to 2-3 messages at once
4. **Actionable feedback** - Tell users what happened and what to do next
5. **Test both themes** - Verify appearance in dark and light modes
