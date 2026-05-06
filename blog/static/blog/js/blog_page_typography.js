(function () {
    const BLOG_TITLE_SELECTORS = [
        '.soho-blog-title',
        '.magazin-blog-title',
        '.rv-title',
        '.pe-title',
        '.sa-title',
        '.spv-title',
        '.nk-title',
        '.mj-title',
        '.jus-title',
        '.vz-title',
        '.vj-title',
        '.blog-header-title',
        '.blog-page-title'
    ];

    const POST_TITLE_SELECTORS = [
        'article h4.mb-0',
        '.blog-post-title'
    ];

    const BOX_TITLE_SELECTORS = [
        '.sidebar-box-title',
        '.blog-box-title',
        '.soho-section-title',
        '.magazin-section-title',
        '.nk-box-title',
        '.spv-box-title',
        '.mj-box-title',
        '.jus-box-title',
        '.vz-box-title',
        '.vj-box-title',
        '.rv-box-title',
        '.pe-box-title',
        '.sa-box-title',
        '.nk-side-title'
    ];

    function uniqueElements(selectors) {
        const seen = new Set();
        const elements = [];

        selectors.forEach(function (selector) {
            document.querySelectorAll(selector).forEach(function (element) {
                if (seen.has(element)) {
                    return;
                }
                seen.add(element);
                elements.push(element);
            });
        });

        return elements;
    }

    function readCssVariable(name, fallback) {
        const styles = window.getComputedStyle(document.body);
        const value = styles.getPropertyValue(name).trim();
        return value || fallback;
    }

    function applyGroup(selectors, role, styles) {
        uniqueElements(selectors).forEach(function (element) {
            element.dataset.editorRole = role;
            if (styles.fontFamily) {
                element.style.fontFamily = styles.fontFamily;
            }
            if (styles.color) {
                element.style.color = styles.color;
            }
            if (styles.fontSize) {
                element.style.fontSize = styles.fontSize;
            }
        });
    }

    window.applyBlogTypographyCustomization = function () {
        applyGroup(BLOG_TITLE_SELECTORS, 'blog-title', {
            fontFamily: readCssVariable('--blog-title-font', 'Georgia, Times New Roman, serif'),
            color: readCssVariable('--blog-title-color', '#3f3128'),
            fontSize: readCssVariable('--blog-title-size', '44px')
        });

        applyGroup(POST_TITLE_SELECTORS, 'post-title', {
            fontFamily: readCssVariable('--post-title-font', 'Georgia, Times New Roman, serif'),
            color: readCssVariable('--post-title-color', '#111827'),
            fontSize: readCssVariable('--post-title-size', '32px')
        });

        applyGroup(BOX_TITLE_SELECTORS, 'box-title', {
            fontFamily: readCssVariable('--box-title-font', 'Georgia, Times New Roman, serif'),
            color: readCssVariable('--box-title-color', '#3f3128'),
            fontSize: readCssVariable('--box-title-size', '20px')
        });
    };

    document.addEventListener('DOMContentLoaded', function () {
        window.applyBlogTypographyCustomization();
    });
})();
