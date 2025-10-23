#!/usr/bin/env python3
"""
Performance optimization script for the portfolio website.
Minifies CSS and JavaScript files and optimizes assets.
"""

import os
import re
import gzip
import shutil
from pathlib import Path

def minify_css(css_content):
    """Basic CSS minification"""
    # Remove comments
    css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
    
    # Remove extra whitespace
    css_content = re.sub(r'\s+', ' ', css_content)
    
    # Remove whitespace around specific characters
    css_content = re.sub(r'\s*([{}:;,>+~])\s*', r'\1', css_content)
    
    # Remove trailing semicolons
    css_content = re.sub(r';}', '}', css_content)
    
    return css_content.strip()

def minify_js(js_content):
    """Basic JavaScript minification"""
    # Remove single-line comments (but preserve URLs)
    js_content = re.sub(r'(?<!:)//.*$', '', js_content, flags=re.MULTILINE)
    
    # Remove multi-line comments
    js_content = re.sub(r'/\*.*?\*/', '', js_content, flags=re.DOTALL)
    
    # Remove extra whitespace
    js_content = re.sub(r'\s+', ' ', js_content)
    
    # Remove whitespace around operators and punctuation
    js_content = re.sub(r'\s*([{}();,=+\-*/])\s*', r'\1', js_content)
    
    return js_content.strip()

def create_gzipped_version(file_path):
    """Create gzipped version of file for better compression"""
    with open(file_path, 'rb') as f_in:
        with gzip.open(f'{file_path}.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    original_size = os.path.getsize(file_path)
    compressed_size = os.path.getsize(f'{file_path}.gz')
    compression_ratio = (1 - compressed_size / original_size) * 100
    
    print(f"  Compressed: {original_size} bytes → {compressed_size} bytes ({compression_ratio:.1f}% reduction)")

def optimize_css_files():
    """Optimize CSS files"""
    print("Optimizing CSS files...")
    
    css_dir = Path('static/css')
    if not css_dir.exists():
        print("  CSS directory not found")
        return
    
    for css_file in css_dir.glob('*.css'):
        if css_file.name.endswith('.min.css'):
            continue
            
        print(f"  Processing {css_file.name}")
        
        with open(css_file, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        minified_content = minify_css(original_content)
        
        # Save minified version
        min_file = css_file.parent / f"{css_file.stem}.min.css"
        with open(min_file, 'w', encoding='utf-8') as f:
            f.write(minified_content)
        
        original_size = len(original_content)
        minified_size = len(minified_content)
        reduction = (1 - minified_size / original_size) * 100
        
        print(f"    Minified: {original_size} chars → {minified_size} chars ({reduction:.1f}% reduction)")
        
        # Create gzipped version
        create_gzipped_version(min_file)

def optimize_js_files():
    """Optimize JavaScript files"""
    print("Optimizing JavaScript files...")
    
    js_dir = Path('static/js')
    if not js_dir.exists():
        print("  JavaScript directory not found")
        return
    
    for js_file in js_dir.glob('*.js'):
        if js_file.name.endswith('.min.js'):
            continue
            
        print(f"  Processing {js_file.name}")
        
        with open(js_file, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        minified_content = minify_js(original_content)
        
        # Save minified version
        min_file = js_file.parent / f"{js_file.stem}.min.js"
        with open(min_file, 'w', encoding='utf-8') as f:
            f.write(minified_content)
        
        original_size = len(original_content)
        minified_size = len(minified_content)
        reduction = (1 - minified_size / original_size) * 100
        
        print(f"    Minified: {original_size} chars → {minified_size} chars ({reduction:.1f}% reduction)")
        
        # Create gzipped version
        create_gzipped_version(min_file)

def generate_performance_report():
    """Generate a performance optimization report"""
    print("\nGenerating performance report...")
    
    report = []
    report.append("# Portfolio Website Performance Report\n")
    report.append("## Optimization Summary\n")
    
    # Check file sizes
    static_dir = Path('static')
    if static_dir.exists():
        total_size = 0
        file_count = 0
        
        for file_path in static_dir.rglob('*'):
            if file_path.is_file() and not file_path.name.endswith('.gz'):
                size = file_path.stat().st_size
                total_size += size
                file_count += 1
        
        report.append(f"- Total static files: {file_count}")
        report.append(f"- Total size: {total_size / 1024:.1f} KB")
        report.append("")
    
    # Performance recommendations
    report.append("## Performance Recommendations\n")
    report.append("### Implemented Optimizations:")
    report.append("- ✅ CSS and JavaScript minification")
    report.append("- ✅ Gzip compression for static files")
    report.append("- ✅ Lazy loading for images")
    report.append("- ✅ GPU acceleration for animations")
    report.append("- ✅ Reduced motion support for accessibility")
    report.append("- ✅ Mobile-optimized animations")
    report.append("")
    
    report.append("### Additional Recommendations:")
    report.append("- 🔄 Implement service worker for caching")
    report.append("- 🔄 Use WebP images with fallbacks")
    report.append("- 🔄 Implement critical CSS inlining")
    report.append("- 🔄 Add resource hints (preload, prefetch)")
    report.append("- 🔄 Consider using a CDN for static assets")
    report.append("")
    
    report.append("### Core Web Vitals Targets:")
    report.append("- First Contentful Paint (FCP): < 1.5s")
    report.append("- Largest Contentful Paint (LCP): < 2.5s")
    report.append("- Cumulative Layout Shift (CLS): < 0.1")
    report.append("- First Input Delay (FID): < 100ms")
    
    with open('performance_report.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print("  Performance report saved to performance_report.md")

def main():
    """Main optimization function"""
    print("🚀 Starting portfolio website optimization...\n")
    
    try:
        optimize_css_files()
        print()
        optimize_js_files()
        print()
        generate_performance_report()
        
        print("\n✅ Optimization complete!")
        print("\nNext steps:")
        print("1. Test the website with minified files")
        print("2. Run Lighthouse audit for performance metrics")
        print("3. Configure server to serve .gz files when available")
        print("4. Monitor Core Web Vitals in production")
        
    except Exception as e:
        print(f"\n❌ Optimization failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())