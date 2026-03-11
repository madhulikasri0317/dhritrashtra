# TailwindCSS Setup & Customization Guide

## Overview

Dhritrashtra frontend uses TailwindCSS 3.3 for styling. This guide covers setup, configuration, and customization.

## Installation & Setup

### Already Installed Files

**tailwind.config.js** - Main configuration file
```javascript
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3b82f6',
        danger: '#dc2626',
        warning: '#f59e0b',
        success: '#10b981',
      },
      spacing: {
        'safe': 'max(1rem, env(safe-area-inset-bottom))',
      },
    },
  },
  plugins: [],
}
```

**index.css** - Global styles with Tailwind directives
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Verify Installation

1. Check `package.json` includes:
```json
"dependencies": {
  "tailwindcss": "^3.3.0",
  ...
}
```

2. Run development server:
```bash
npm run dev
```

3. Check that styles are applied (look for colored backgrounds, shadows, etc.)

---

## Core Concepts

### Utility-First Approach

Instead of writing CSS:
```css
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  background-color: white;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
```

Use Tailwind classes:
```jsx
<div className="flex items-center justify-between p-6 bg-white shadow-md">
```

### Responsive Design

Tailwind uses mobile-first breakpoints:

```jsx
// Mobile (default)
// Tablet (768px+)
<div className="grid grid-cols-1 md:grid-cols-2">

// Large (1024px+)
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4">

// Extra Large (1280px+)
<div className="hidden xl:block">
```

**Breakpoints:**
| Name | Size | Use Case |
|------|------|----------|
| `sm` | 640px | Small tablets |
| `md` | 768px | Tablets |
| `lg` | 1024px | Small desktops |
| `xl` | 1280px | Large desktops |
| `2xl` | 1536px | Extra large screens |

---

## Color Palette

### Disease Risk Colors (Standard)

**High Risk (Red)**
```jsx
className="text-red-700 bg-red-50 border-red-500"
className="bg-red-100 text-red-800"  // Badge
```

**Medium Risk (Yellow)**
```jsx
className="text-yellow-700 bg-yellow-50 border-yellow-500"
className="bg-yellow-100 text-yellow-800"  // Badge
```

**Low Risk (Green)**
```jsx
className="text-green-700 bg-green-50 border-green-500"
className="bg-green-100 text-green-800"  // Badge
```

### UI Colors

**Primary (Blue)**
- `bg-blue-500` - Buttons, primary actions
- `text-blue-700` - Links, highlighted text
- `border-blue-600` - Borders for important elements

**Secondary (Gray)**
- `text-gray-900` - Headings, dark text
- `text-gray-600` - Body text
- `bg-gray-50` - Light backgrounds
- `bg-gray-100` - Slightly darker backgrounds
- `border-gray-200` - Subtle borders

**Status (Green)**
- `bg-green-100` - Success messages
- `text-green-700` - Success text

### Custom Colors (in tailwind.config.js)

```javascript
colors: {
  primary: '#3b82f6',    // Blue-500
  danger: '#dc2626',     // Red-600
  warning: '#f59e0b',    // Amber-500
  success: '#10b981',    // Emerald-600
}
```

Usage:
```jsx
className="bg-primary text-white"  // Custom color
className="bg-danger px-4 py-2"    // Custom color
```

---

## Common Patterns

### Card Layout

```jsx
<div className="bg-white rounded-lg shadow-md p-6 border-t-4 border-blue-500">
  <h3 className="text-lg font-bold text-gray-900">Card Title</h3>
  <p className="text-gray-600 mt-2">Card content goes here</p>
</div>
```

**Classes Breakdown:**
- `bg-white` - White background
- `rounded-lg` - Rounded corners (8px)
- `shadow-md` - Medium drop shadow
- `p-6` - Padding all sides (1.5rem)
- `border-t-4` - Top border 4px
- `border-blue-500` - Blue color border

### Badge/Pill

```jsx
<span className="inline-block px-3 py-1 rounded-full text-xs font-bold bg-red-100 text-red-800">
  HIGH RISK
</span>
```

### Button

```jsx
<button className="px-4 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors duration-200">
  Click Me
</button>
```

### Grid Layout

Two columns on desktop, one on mobile:
```jsx
<div className="grid grid-cols-1 md:grid-cols-2 gap-6">
  <div>Column 1</div>
  <div>Column 2</div>
</div>
```

Four columns on large screens:
```jsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
```

### Flexbox Layout

```jsx
<div className="flex items-center justify-between p-4">
  <span>Left</span>
  <span>Right</span>
</div>
```

**Flex Classes:**
- `flex` - Enable flexbox
- `items-center` - Vertical center (align-items)
- `justify-between` - Space between (justify-content)
- `space-x-4` - Horizontal spacing between children
- `space-y-4` - Vertical spacing between children

### Table Styling

```jsx
<table className="w-full">
  <thead className="bg-gray-50 border-b border-gray-200">
    <tr>
      <th className="px-4 py-3 text-left text-sm font-semibold">Header</th>
    </tr>
  </thead>
  <tbody className="divide-y divide-gray-200">
    <tr className="hover:bg-gray-50">
      <td className="px-4 py-3">Cell</td>
    </tr>
  </tbody>
</table>
```

### Progress Bar

```jsx
<div className="w-24 h-2 bg-gray-200 rounded-full overflow-hidden">
  <div
    className="h-full bg-blue-500 transition-all duration-300"
    style={{ width: `${percentage}%` }}
  ></div>
</div>
```

### Responsive Hidden

```jsx
// Hide on mobile, show on desktop
<div className="hidden md:block">Desktop only</div>

// Show on mobile, hide on desktop
<div className="md:hidden">Mobile only</div>

// Show only on large screens
<div className="lg:flex">Large screens</div>
```

---

## Typography

### Headings

```jsx
<h1 className="text-4xl font-bold text-gray-900">Page Title</h1>
<h2 className="text-2xl font-bold text-gray-900">Section Title</h2>
<h3 className="text-lg font-semibold text-gray-900">Subsection</h3>
```

**Font Sizes:**
- `text-xs` - 12px
- `text-sm` - 14px
- `text-base` - 16px (default)
- `text-lg` - 18px
- `text-xl` - 20px
- `text-2xl` - 24px
- `text-3xl` - 30px
- `text-4xl` - 36px

### Font Weights

```jsx
className="font-light"     // 300
className="font-normal"    // 400
className="font-medium"    // 500
className="font-semibold"  // 600
className="font-bold"      // 700
```

### Text Colors

```jsx
className="text-gray-900"  // Dark text
className="text-gray-600"  // Medium text
className="text-gray-500"  // Light text
className="text-blue-700"  // Colored text
```

---

## Spacing

### Padding & Margin

```jsx
<div className="p-4">          // Padding all sides
<div className="px-4 py-6">    // Padding horizontal + vertical
<div className="pt-4 pb-8">    // Padding top + bottom
<div className="pl-4 pr-2">    // Padding left + right

<div className="m-4">          // Margin all sides
<div className="mx-auto">      // Margin horizontal (centers)
<div className="mb-4">         // Margin bottom
```

**Spacing Scale (in 0.25rem = 4px units):**
- `0` - 0px
- `1` - 4px
- `2` - 8px
- `4` - 16px
- `6` - 24px
- `8` - 32px

### Gaps (in Grid/Flex)

```jsx
<div className="grid gap-4">     // 16px gap
<div className="space-y-2">      // 8px vertical space between children
<div className="space-x-4">      // 16px horizontal space between children
```

---

## Transitions & Effects

### Hover Effects

```jsx
className="hover:bg-blue-600"           // Change background on hover
className="hover:shadow-lg"             // Increase shadow on hover
className="hover:text-blue-700"         // Change text color on hover
className="hover:scale-105"             // Slightly larger on hover
```

### Transitions

```jsx
className="transition-colors duration-200"    // Smooth color change
className="transition-all duration-300"       // All properties
className="transition-shadow duration-200"    // Shadow transition
```

**Duration:**
- `duration-100` - 100ms
- `duration-200` - 200ms
- `duration-300` - 300ms (default)

### Opacity

```jsx
className="opacity-50"  // 50% opacity
className="hover:opacity-75"  // 75% on hover
```

---

## Borders & Shadows

### Borders

```jsx
className="border"              // 1px solid
className="border-2"            // 2px solid
className="border-t-4"          // Top border 4px
className="border-l-4"          // Left border 4px
className="border-gray-200"     // Gray color
className="border-blue-500"     // Blue color
className="rounded-lg"          // Rounded corners 8px
className="rounded-full"        // Fully rounded (pill shape)
```

### Shadows

```jsx
className="shadow"       // Small shadow
className="shadow-md"    // Medium shadow
className="shadow-lg"    // Large shadow
className="hover:shadow-lg"  // Larger shadow on hover
```

---

## Customization

### Adding Custom Colors

Edit `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      primary: '#3b82f6',
      danger: '#dc2626',
      warning: '#f59e0b',
      success: '#10b981',
      // Add new colors
      'custom-blue': '#1e40af',
      'custom-purple': '#7c3aed',
    },
  },
},
```

Usage:
```jsx
className="bg-custom-blue text-white"
```

### Adding Custom Spacing

```javascript
spacing: {
  'safe': 'max(1rem, env(safe-area-inset-bottom))',
  'custom-spacing': '3.5rem',  // 56px
},
```

### Adding Custom Utilities

```javascript
plugins: [
  function({ addUtilities }) {
    addUtilities({
      '.no-scrollbar': {
        '-ms-overflow-style': 'none',
        'scrollbar-width': 'none',
        '&::-webkit-scrollbar': {
          display: 'none',
        },
      },
    })
  }
],
```

---

## Performance Tips

### 1. Purge Unused Styles

The `content` config in `tailwind.config.js` tells Tailwind which files to scan:
```javascript
content: [
  "./index.html",
  "./src/**/*.{js,jsx,ts,tsx}",
],
```

**Don't include:**
- `node_modules/` (scanned automatically)
- Binary files

### 2. Use @apply for Repeated Classes

Instead of repeating classes:
```jsx
className="flex items-center justify-center p-4 bg-white rounded-lg shadow-md"
```

Create a utility in CSS:
```css
@layer components {
  .card {
    @apply flex items-center justify-center p-4 bg-white rounded-lg shadow-md;
  }
}
```

Usage:
```jsx
className="card"
```

### 3. Optimize Build Size

In `tailwind.config.js`, add:
```javascript
safelist: [
  // List rarely-used classes here
  'text-red-700',
  'bg-yellow-50',
],
```

---

## Browser DevTools Inspection

### Finding Tailwind Classes

1. Inspect element (F12)
2. Look at `class` attribute
3. Each space-separated word is a utility class
4. Example: `flex items-center justify-between p-6`
   - `flex` - Flexbox display
   - `items-center` - Vertical center
   - `justify-between` - Space between
   - `p-6` - 1.5rem padding

### Debugging Style Issues

1. **Styles not applying?**
   - Check syntax in `tailwind.config.js`
   - Rebuild: `npm run dev`
   - Clear cache: `rm -rf node_modules && npm install`

2. **Responsive design not working?**
   - Ensure viewport meta tag in HTML:
   ```html
   <meta name="viewport" content="width=device-width, initial-scale=1">
   ```

3. **Custom colors not showing?**
   - Verify in `tailwind.config.js`
   - Restart dev server
   - Check exact class name matches

---

## Common Issues & Solutions

### Issue: Styles appear broken after npm install

**Solution:**
```bash
npm run dev  # Rebuilds Tailwind CSS
```

### Issue: Custom colors not recognized

**Solution:** Make sure `tailwind.config.js` is in project root and properly formatted:
```javascript
export default {
  content: [...],
  theme: {
    extend: {
      colors: { ... }  // Note: inside `extend`
    }
  }
}
```

### Issue: Dark mode not working

**Enable dark mode in config:**
```javascript
darkMode: 'class',  // or 'media'
```

Then use:
```jsx
className="dark:bg-gray-900 dark:text-white"
```

### Issue: Some classes show as unused

This is normal. Tailwind scans for class strings, so dynamic classes won't be detected:
```jsx
// Won't be scanned:
className={`bg-${color}-500`}

// Use safelist instead:
className="bg-red-500 bg-blue-500 bg-green-500"
```

---

## Resources

- **Official Docs:** https://tailwindcss.com
- **Component Examples:** https://tailwindui.com
- **Play Online:** https://play.tailwindcss.com
- **Cheat Sheet:** https://unipop.github.io/taildwind

---

## Configuration Checklist

- [x] TailwindCSS installed in package.json
- [x] `tailwind.config.js` at project root
- [x] `index.css` contains `@tailwind` directives
- [x] `index.js` imports `index.css`
- [x] Content path includes all component files
- [x] Custom colors defined (if needed)
- [x] Custom fonts configured (if needed)
- [x] Dark mode setup (if needed)

---

**Last Updated:** March 10, 2026
**Version:** 1.0.0
**TailwindCSS Version:** 3.3.0
