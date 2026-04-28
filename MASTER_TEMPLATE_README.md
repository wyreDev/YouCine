# YouCine Master Template System

This master template system allows you to create consistent layouts across all pages of your video sharing platform.

## How to Use the Master Template

### 1. Include the Template System
Add this script tag to your HTML page:
```html
<script src="master-template.js"></script>
```

### 2. Use the Master Template
In your page's JavaScript, call `useMasterTemplate()` with your content:

```javascript
document.addEventListener('DOMContentLoaded', async function() {
    await useMasterTemplate({
        PAGE_TITLE: 'Your Page Title',
        PAGE_HEAD_CONTENT: '<meta name="description" content="Page description">',
        PAGE_CONTENT: `
            <!-- Your page content here -->
            <h2>Welcome to my page</h2>
            <p>This content will be inserted into the master template.</p>
        `,
        PAGE_SCRIPTS: '<script>console.log("Page-specific scripts");</script>'
    });
});
```

### 3. Available Placeholders

- `<!-- PAGE_TITLE -->` - Page title in the `<title>` tag
- `<!-- PAGE_HEAD_CONTENT -->` - Additional content for the `<head>` section
- `<!-- PAGE_CONTENT -->` - Main content that goes in the `.container` div
- `<!-- PAGE_SCRIPTS -->` - Additional scripts before closing `</body>`

### 4. Features Included in Master Template

- **Header**: Logo, search functionality, admin button
- **Search System**: Filter videos by title
- **Footer**: Contact information
- **Responsive Design**: Works on all devices
- **Consistent Styling**: Uses weed.css and adminlogin.css

### 5. Example Usage

See `template-example.html` for a complete working example.

### 6. Converting Existing Pages

To convert an existing page to use the master template:

1. Keep only the unique content of your page
2. Wrap it in the `useMasterTemplate()` call
3. Remove duplicate HTML structure (DOCTYPE, head, header, footer)

This ensures all pages have a consistent look and feel while maintaining their unique content.