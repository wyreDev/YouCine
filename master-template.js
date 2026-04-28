// Master Template System for YouCine
// This script helps load the master template and replace placeholders

class MasterTemplate {
    constructor() {
        this.template = null;
    }

    // Load the master template
    async loadTemplate() {
        try {
            const response = await fetch('master.html');
            this.template = await response.text();
            return this.template;
        } catch (error) {
            console.error('Error loading master template:', error);
            return null;
        }
    }

    // Replace placeholders in the template
    replacePlaceholders(replacements) {
        let result = this.template;
        for (const [placeholder, content] of Object.entries(replacements)) {
            const regex = new RegExp(`<!-- ${placeholder} -->`, 'g');
            result = result.replace(regex, content);
        }
        return result;
    }

    // Apply template to current page
    async applyToPage(replacements) {
        if (!this.template) {
            await this.loadTemplate();
        }

        if (this.template) {
            const newContent = this.replacePlaceholders(replacements);
            document.documentElement.innerHTML = newContent;
        }
    }
}

// Global instance
window.masterTemplate = new MasterTemplate();

// Helper function for pages to use the master template
window.useMasterTemplate = async function(replacements) {
    await window.masterTemplate.applyToPage(replacements);
};