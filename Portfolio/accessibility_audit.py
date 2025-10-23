#!/usr/bin/env python3
"""
Accessibility and SEO audit script for the portfolio website.
Checks for common accessibility issues and SEO best practices.
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup

class AccessibilityAuditor:
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.passed = []
    
    def audit_html_file(self, file_path):
        """Audit an HTML file for accessibility issues"""
        print(f"Auditing {file_path.name}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Check basic HTML structure
        self.check_html_structure(soup)
        
        # Check headings hierarchy
        self.check_heading_hierarchy(soup)
        
        # Check images
        self.check_images(soup)
        
        # Check forms
        self.check_forms(soup)
        
        # Check links
        self.check_links(soup)
        
        # Check ARIA attributes
        self.check_aria_attributes(soup)
        
        # Check color contrast (basic check)
        self.check_color_contrast(soup)
        
        # Check keyboard navigation
        self.check_keyboard_navigation(soup)
    
    def check_html_structure(self, soup):
        """Check basic HTML structure"""
        # Check for lang attribute
        html_tag = soup.find('html')
        if html_tag and html_tag.get('lang'):
            self.passed.append("✅ HTML lang attribute present")
        else:
            self.issues.append("❌ Missing lang attribute on <html> tag")
        
        # Check for title
        title = soup.find('title')
        if title and title.text.strip():
            self.passed.append("✅ Page title present")
        else:
            self.issues.append("❌ Missing or empty page title")
        
        # Check for meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            self.passed.append("✅ Meta description present")
        else:
            self.warnings.append("⚠️ Missing meta description")
        
        # Check for viewport meta tag
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        if viewport:
            self.passed.append("✅ Viewport meta tag present")
        else:
            self.issues.append("❌ Missing viewport meta tag")
    
    def check_heading_hierarchy(self, soup):
        """Check heading hierarchy"""
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        if not headings:
            self.warnings.append("⚠️ No headings found")
            return
        
        # Check for h1
        h1_count = len(soup.find_all('h1'))
        if h1_count == 1:
            self.passed.append("✅ Exactly one H1 tag found")
        elif h1_count == 0:
            self.issues.append("❌ No H1 tag found")
        else:
            self.issues.append(f"❌ Multiple H1 tags found ({h1_count})")
        
        # Check heading order
        heading_levels = [int(h.name[1]) for h in headings]
        for i in range(1, len(heading_levels)):
            if heading_levels[i] > heading_levels[i-1] + 1:
                self.warnings.append(f"⚠️ Heading hierarchy skip detected: h{heading_levels[i-1]} to h{heading_levels[i]}")
    
    def check_images(self, soup):
        """Check images for accessibility"""
        images = soup.find_all('img')
        
        for img in images:
            alt_text = img.get('alt')
            if alt_text is None:
                self.issues.append("❌ Image missing alt attribute")
            elif alt_text == '':
                self.passed.append("✅ Decorative image with empty alt text")
            else:
                self.passed.append("✅ Image has descriptive alt text")
        
        # Check for lazy loading
        lazy_images = soup.find_all('img', attrs={'loading': 'lazy'})
        if lazy_images:
            self.passed.append(f"✅ {len(lazy_images)} images use lazy loading")
    
    def check_forms(self, soup):
        """Check forms for accessibility"""
        forms = soup.find_all('form')
        
        for form in forms:
            # Check for labels
            inputs = form.find_all(['input', 'textarea', 'select'])
            for input_elem in inputs:
                input_id = input_elem.get('id')
                input_type = input_elem.get('type', '')
                
                if input_type in ['hidden', 'submit', 'button']:
                    continue
                
                # Check for associated label
                if input_id:
                    label = soup.find('label', attrs={'for': input_id})
                    if label:
                        self.passed.append("✅ Form input has associated label")
                    else:
                        self.issues.append("❌ Form input missing associated label")
                else:
                    self.issues.append("❌ Form input missing id attribute")
            
            # Check for fieldsets in complex forms
            fieldsets = form.find_all('fieldset')
            if len(inputs) > 5 and not fieldsets:
                self.warnings.append("⚠️ Complex form might benefit from fieldsets")
    
    def check_links(self, soup):
        """Check links for accessibility"""
        links = soup.find_all('a')
        
        for link in links:
            href = link.get('href')
            text = link.get_text(strip=True)
            
            # Check for meaningful link text
            if not text or text.lower() in ['click here', 'read more', 'more']:
                self.warnings.append("⚠️ Link has non-descriptive text")
            
            # Check external links
            if href and (href.startswith('http') and 'jaiyanth' not in href):
                target = link.get('target')
                if target == '_blank':
                    rel = link.get('rel', [])
                    if 'noopener' in rel or 'noreferrer' in rel:
                        self.passed.append("✅ External link has security attributes")
                    else:
                        self.warnings.append("⚠️ External link missing security attributes")
    
    def check_aria_attributes(self, soup):
        """Check ARIA attributes"""
        # Check for ARIA labels
        aria_labeled = soup.find_all(attrs={'aria-label': True})
        if aria_labeled:
            self.passed.append(f"✅ {len(aria_labeled)} elements have ARIA labels")
        
        # Check for ARIA roles
        role_elements = soup.find_all(attrs={'role': True})
        if role_elements:
            self.passed.append(f"✅ {len(role_elements)} elements have ARIA roles")
        
        # Check for ARIA hidden on decorative elements
        aria_hidden = soup.find_all(attrs={'aria-hidden': 'true'})
        if aria_hidden:
            self.passed.append(f"✅ {len(aria_hidden)} decorative elements are hidden from screen readers")
    
    def check_color_contrast(self, soup):
        """Basic color contrast check"""
        # This is a simplified check - in practice, you'd use tools like axe-core
        style_tags = soup.find_all('style')
        css_content = ' '.join([style.get_text() for style in style_tags])
        
        # Check for color definitions
        if 'color:' in css_content and 'background' in css_content:
            self.passed.append("✅ Color and background properties found (manual contrast check needed)")
        
        # Check for dark mode support
        if 'dark:' in css_content or '@media (prefers-color-scheme: dark)' in css_content:
            self.passed.append("✅ Dark mode support detected")
    
    def check_keyboard_navigation(self, soup):
        """Check keyboard navigation support"""
        # Check for focus styles
        focusable_elements = soup.find_all(['a', 'button', 'input', 'textarea', 'select'])
        
        # Check for tabindex usage
        tabindex_elements = soup.find_all(attrs={'tabindex': True})
        for elem in tabindex_elements:
            tabindex = elem.get('tabindex')
            try:
                if int(tabindex) > 0:
                    self.warnings.append("⚠️ Positive tabindex found - may disrupt tab order")
            except ValueError:
                pass
        
        # Check for skip links
        skip_links = soup.find_all('a', href=re.compile(r'^#'))
        if skip_links:
            self.passed.append("✅ Skip links found for keyboard navigation")
    
    def generate_report(self):
        """Generate accessibility audit report"""
        report = []
        report.append("# Accessibility Audit Report\n")
        
        total_checks = len(self.passed) + len(self.warnings) + len(self.issues)
        report.append(f"**Total checks performed:** {total_checks}")
        report.append(f"**Passed:** {len(self.passed)}")
        report.append(f"**Warnings:** {len(self.warnings)}")
        report.append(f"**Issues:** {len(self.issues)}\n")
        
        if self.passed:
            report.append("## ✅ Passed Checks\n")
            for item in self.passed:
                report.append(f"- {item}")
            report.append("")
        
        if self.warnings:
            report.append("## ⚠️ Warnings\n")
            for item in self.warnings:
                report.append(f"- {item}")
            report.append("")
        
        if self.issues:
            report.append("## ❌ Issues to Fix\n")
            for item in self.issues:
                report.append(f"- {item}")
            report.append("")
        
        # Add recommendations
        report.append("## 🔧 Recommendations\n")
        report.append("### Immediate Actions:")
        if self.issues:
            report.append("1. Fix all critical accessibility issues listed above")
        report.append("2. Test with screen readers (NVDA, JAWS, VoiceOver)")
        report.append("3. Test keyboard navigation (Tab, Enter, Space, Arrow keys)")
        report.append("4. Verify color contrast ratios meet WCAG AA standards (4.5:1)")
        report.append("")
        
        report.append("### SEO Improvements:")
        report.append("- Add structured data (JSON-LD) for better search visibility")
        report.append("- Optimize images with descriptive filenames")
        report.append("- Add Open Graph and Twitter Card meta tags")
        report.append("- Create XML sitemap")
        report.append("- Add robots.txt file")
        report.append("")
        
        report.append("### Performance & Accessibility:")
        report.append("- Implement prefers-reduced-motion media query")
        report.append("- Add focus indicators for all interactive elements")
        report.append("- Ensure minimum touch target size (44x44px)")
        report.append("- Test with various assistive technologies")
        
        return '\n'.join(report)

def main():
    """Main audit function"""
    print("🔍 Starting accessibility and SEO audit...\n")
    
    auditor = AccessibilityAuditor()
    
    # Find HTML templates
    template_dir = Path('templates')
    if template_dir.exists():
        html_files = list(template_dir.glob('*.html'))
        
        for html_file in html_files:
            auditor.audit_html_file(html_file)
            print()
    else:
        print("Templates directory not found")
        return 1
    
    # Generate report
    report = auditor.generate_report()
    
    with open('accessibility_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("📋 Accessibility audit complete!")
    print("📄 Report saved to accessibility_report.md")
    
    # Print summary
    print(f"\n📊 Summary:")
    print(f"   ✅ Passed: {len(auditor.passed)}")
    print(f"   ⚠️  Warnings: {len(auditor.warnings)}")
    print(f"   ❌ Issues: {len(auditor.issues)}")
    
    if auditor.issues:
        print(f"\n🚨 {len(auditor.issues)} critical issues found - please review and fix")
        return 1
    else:
        print("\n🎉 No critical accessibility issues found!")
        return 0

if __name__ == "__main__":
    exit(main())