#!/usr/bin/env python3
"""
Performance testing script for the portfolio website.
Tests various performance metrics and validates optimizations.
"""

import time
import requests
from pathlib import Path
import gzip
import os

def test_file_sizes():
    """Test that minified files are smaller than originals"""
    print("🔍 Testing file size optimizations...")
    
    static_dir = Path('static')
    results = []
    
    # Test CSS files
    css_dir = static_dir / 'css'
    if css_dir.exists():
        for css_file in css_dir.glob('*.css'):
            if not css_file.name.endswith('.min.css'):
                min_file = css_file.parent / f"{css_file.stem}.min.css"
                if min_file.exists():
                    original_size = css_file.stat().st_size
                    minified_size = min_file.stat().st_size
                    reduction = (1 - minified_size / original_size) * 100
                    results.append(f"  ✅ {css_file.name}: {reduction:.1f}% size reduction")
                else:
                    results.append(f"  ❌ {css_file.name}: No minified version found")
    
    # Test JS files
    js_dir = static_dir / 'js'
    if js_dir.exists():
        for js_file in js_dir.glob('*.js'):
            if not js_file.name.endswith('.min.js'):
                min_file = js_file.parent / f"{js_file.stem}.min.js"
                if min_file.exists():
                    original_size = js_file.stat().st_size
                    minified_size = min_file.stat().st_size
                    reduction = (1 - minified_size / original_size) * 100
                    results.append(f"  ✅ {js_file.name}: {reduction:.1f}% size reduction")
                else:
                    results.append(f"  ❌ {js_file.name}: No minified version found")
    
    return results

def test_gzip_compression():
    """Test gzip compression effectiveness"""
    print("🗜️  Testing gzip compression...")
    
    results = []
    static_dir = Path('static')
    
    for file_path in static_dir.rglob('*.min.*'):
        if file_path.is_file():
            gz_file = Path(f"{file_path}.gz")
            if gz_file.exists():
                original_size = file_path.stat().st_size
                compressed_size = gz_file.stat().st_size
                compression_ratio = (1 - compressed_size / original_size) * 100
                results.append(f"  ✅ {file_path.name}: {compression_ratio:.1f}% compression")
            else:
                results.append(f"  ❌ {file_path.name}: No gzipped version found")
    
    return results

def test_accessibility_features():
    """Test accessibility features in HTML"""
    print("♿ Testing accessibility features...")
    
    results = []
    
    # Check base.html for accessibility features
    base_html = Path('templates/base.html')
    if base_html.exists():
        content = base_html.read_text(encoding='utf-8')
        
        # Check for skip link
        if 'skip-link' in content:
            results.append("  ✅ Skip link implemented")
        else:
            results.append("  ❌ Skip link missing")
        
        # Check for ARIA attributes
        if 'aria-label' in content:
            results.append("  ✅ ARIA labels present")
        else:
            results.append("  ❌ ARIA labels missing")
        
        # Check for focus indicators
        css_file = Path('static/css/styles.css')
        if css_file.exists():
            css_content = css_file.read_text(encoding='utf-8')
            if ':focus' in css_content:
                results.append("  ✅ Focus indicators implemented")
            else:
                results.append("  ❌ Focus indicators missing")
        
        # Check for reduced motion support
        if 'prefers-reduced-motion' in content or 'prefers-reduced-motion' in css_content:
            results.append("  ✅ Reduced motion support")
        else:
            results.append("  ❌ Reduced motion support missing")
    
    return results

def test_seo_features():
    """Test SEO optimization features"""
    print("🔍 Testing SEO features...")
    
    results = []
    
    # Check base.html for SEO features
    base_html = Path('templates/base.html')
    if base_html.exists():
        content = base_html.read_text(encoding='utf-8')
        
        # Check for meta description
        if 'meta name="description"' in content:
            results.append("  ✅ Meta description present")
        else:
            results.append("  ❌ Meta description missing")
        
        # Check for Open Graph tags
        if 'property="og:' in content:
            results.append("  ✅ Open Graph tags present")
        else:
            results.append("  ❌ Open Graph tags missing")
        
        # Check for Twitter Card tags
        if 'name="twitter:' in content:
            results.append("  ✅ Twitter Card tags present")
        else:
            results.append("  ❌ Twitter Card tags missing")
        
        # Check for structured data
        if 'application/ld+json' in content:
            results.append("  ✅ Structured data (JSON-LD) present")
        else:
            results.append("  ❌ Structured data missing")
        
        # Check for canonical URL
        if 'rel="canonical"' in content:
            results.append("  ✅ Canonical URL present")
        else:
            results.append("  ❌ Canonical URL missing")
    
    # Check for robots.txt
    robots_file = Path('static/robots.txt')
    if robots_file.exists():
        results.append("  ✅ robots.txt file present")
    else:
        results.append("  ❌ robots.txt file missing")
    
    return results

def test_performance_features():
    """Test performance optimization features"""
    print("⚡ Testing performance features...")
    
    results = []
    
    # Check base.html for performance features
    base_html = Path('templates/base.html')
    if base_html.exists():
        content = base_html.read_text(encoding='utf-8')
        
        # Check for resource hints
        if 'rel="preconnect"' in content:
            results.append("  ✅ Preconnect hints present")
        else:
            results.append("  ❌ Preconnect hints missing")
        
        if 'rel="dns-prefetch"' in content:
            results.append("  ✅ DNS prefetch hints present")
        else:
            results.append("  ❌ DNS prefetch hints missing")
        
        if 'rel="preload"' in content:
            results.append("  ✅ Resource preloading present")
        else:
            results.append("  ❌ Resource preloading missing")
        
        # Check for font display optimization
        if 'display=swap' in content:
            results.append("  ✅ Font display optimization present")
        else:
            results.append("  ❌ Font display optimization missing")
    
    # Check CSS for performance optimizations
    css_file = Path('static/css/styles.css')
    if css_file.exists():
        css_content = css_file.read_text(encoding='utf-8')
        
        if 'will-change' in css_content:
            results.append("  ✅ GPU acceleration hints present")
        else:
            results.append("  ❌ GPU acceleration hints missing")
        
        if 'contain:' in css_content:
            results.append("  ✅ CSS containment present")
        else:
            results.append("  ❌ CSS containment missing")
    
    return results

def calculate_total_size():
    """Calculate total size of static assets"""
    static_dir = Path('static')
    total_size = 0
    file_count = 0
    
    if static_dir.exists():
        for file_path in static_dir.rglob('*'):
            if file_path.is_file() and not file_path.name.endswith('.gz'):
                total_size += file_path.stat().st_size
                file_count += 1
    
    return total_size, file_count

def generate_performance_summary():
    """Generate comprehensive performance summary"""
    print("\n📊 Generating Performance Summary...")
    
    # Run all tests
    file_size_results = test_file_sizes()
    gzip_results = test_gzip_compression()
    accessibility_results = test_accessibility_features()
    seo_results = test_seo_features()
    performance_results = test_performance_features()
    
    total_size, file_count = calculate_total_size()
    
    # Count results
    total_checks = (len(file_size_results) + len(gzip_results) + 
                   len(accessibility_results) + len(seo_results) + 
                   len(performance_results))
    
    passed_checks = sum(1 for result in (file_size_results + gzip_results + 
                                       accessibility_results + seo_results + 
                                       performance_results) if '✅' in result)
    
    failed_checks = total_checks - passed_checks
    
    # Generate report
    report = []
    report.append("# Portfolio Website Performance Test Report\n")
    report.append(f"**Test Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"**Total Checks:** {total_checks}")
    report.append(f"**Passed:** {passed_checks}")
    report.append(f"**Failed:** {failed_checks}")
    report.append(f"**Success Rate:** {(passed_checks/total_checks)*100:.1f}%\n")
    
    report.append(f"**Static Assets:** {file_count} files, {total_size/1024:.1f} KB total\n")
    
    # Add detailed results
    if file_size_results:
        report.append("## File Size Optimization Results\n")
        report.extend(file_size_results)
        report.append("")
    
    if gzip_results:
        report.append("## Gzip Compression Results\n")
        report.extend(gzip_results)
        report.append("")
    
    if accessibility_results:
        report.append("## Accessibility Features\n")
        report.extend(accessibility_results)
        report.append("")
    
    if seo_results:
        report.append("## SEO Optimization Features\n")
        report.extend(seo_results)
        report.append("")
    
    if performance_results:
        report.append("## Performance Optimization Features\n")
        report.extend(performance_results)
        report.append("")
    
    # Add recommendations
    report.append("## Recommendations\n")
    if failed_checks > 0:
        report.append("### Priority Actions:")
        report.append("1. Address failed checks listed above")
        report.append("2. Re-run optimization scripts if needed")
        report.append("3. Test with real performance monitoring tools")
    else:
        report.append("### Excellent! All checks passed. Consider:")
        report.append("1. Running Lighthouse audits for additional insights")
        report.append("2. Testing with real users and devices")
        report.append("3. Monitoring Core Web Vitals in production")
    
    report.append("\n### Next Steps:")
    report.append("- Deploy to production environment")
    report.append("- Set up performance monitoring")
    report.append("- Configure CDN for static assets")
    report.append("- Implement service worker for caching")
    
    return '\n'.join(report)

def main():
    """Main performance testing function"""
    print("🚀 Starting comprehensive performance testing...\n")
    
    try:
        # Generate comprehensive report
        report = generate_performance_summary()
        
        # Save report
        with open('performance_test_report.md', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("\n✅ Performance testing complete!")
        print("📄 Detailed report saved to performance_test_report.md")
        
        # Print summary to console
        lines = report.split('\n')
        for line in lines[:10]:  # Print first 10 lines as summary
            print(line)
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Performance testing failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main())