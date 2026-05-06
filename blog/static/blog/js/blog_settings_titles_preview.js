document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('[data-design-live-form]');
    const previewFrame = document.querySelector('[data-design-preview-frame]');

    if (!form || !previewFrame) {
        return;
    }

    const cssBindings = [
        {
            selector: '[name="blog_title_font"]',
            variable: '--blog-title-font',
            type: 'font'
        },
        {
            selector: '[name="blog_title_color"]',
            variable: '--blog-title-color',
            type: 'value'
        },
        {
            selector: '[name="blog_title_size"]',
            variable: '--blog-title-size',
            type: 'px'
        },
        {
            selector: '[name="post_title_font"]',
            variable: '--post-title-font',
            type: 'font'
        },
        {
            selector: '[name="post_title_color"]',
            variable: '--post-title-color',
            type: 'value'
        },
        {
            selector: '[name="post_title_size"]',
            variable: '--post-title-size',
            type: 'px'
        },
        {
            selector: '[name="box_title_font"]',
            variable: '--box-title-font',
            type: 'font'
        },
        {
            selector: '[name="box_title_color"]',
            variable: '--box-title-color',
            type: 'value'
        },
        {
            selector: '[name="box_title_size"]',
            variable: '--box-title-size',
            type: 'px'
        }
    ];

    function getPreviewDocument() {
        try {
            return previewFrame.contentDocument || (previewFrame.contentWindow && previewFrame.contentWindow.document) || null;
        } catch (error) {
            return null;
        }
    }

    function getPreviewBody() {
        const doc = getPreviewDocument();
        return doc ? doc.body : null;
    }


    function syncFrameHeight() {
        const doc = getPreviewDocument();
        if (!doc) {
            return;
        }

        const body = doc.body;
        const html = doc.documentElement;
        if (!body || !html) {
            return;
        }

        const height = Math.max(
            body.scrollHeight || 0,
            body.offsetHeight || 0,
            html.scrollHeight || 0,
            html.offsetHeight || 0,
            700
        );

        previewFrame.style.height = height + 'px';
    }

    function getBindingValue(binding) {
        const field = form.querySelector(binding.selector);
        if (!field) {
            return '';
        }

        if (binding.type === 'font') {
            const option = field.options[field.selectedIndex];
            return option ? (option.dataset.fontStack || '') : '';
        }

        if (binding.type === 'px') {
            return field.value ? field.value + 'px' : '';
        }

        return field.value || '';
    }

    function applyPreviewStyles() {
        const body = getPreviewBody();
        if (!body) {
            return;
        }

        cssBindings.forEach(function (binding) {
            const value = getBindingValue(binding);
            if (value) {
                body.style.setProperty(binding.variable, value);
            }
        });

        if (previewFrame.contentWindow && typeof previewFrame.contentWindow.applyBlogTypographyCustomization === 'function') {
            previewFrame.contentWindow.applyBlogTypographyCustomization();
        }
    }

    function syncLinkedInputs(changedInput) {
        const syncName = changedInput.dataset.syncName;
        if (!syncName) {
            return;
        }

        const linked = form.querySelector('[name="' + syncName + '"]');
        if (!linked) {
            return;
        }

        linked.value = changedInput.value;
    }

    function clampValue(input) {
        if (input.type !== 'number' && input.type !== 'range') {
            return;
        }

        const min = input.min !== '' ? Number(input.min) : null;
        const max = input.max !== '' ? Number(input.max) : null;
        let value = Number(input.value);

        if (!Number.isFinite(value)) {
            return;
        }

        if (min !== null) {
            value = Math.max(min, value);
        }

        if (max !== null) {
            value = Math.min(max, value);
        }

        input.value = String(value);
    }

    function clearHighlights() {
        const doc = getPreviewDocument();
        if (!doc) {
            return;
        }

        doc.querySelectorAll('[data-editor-highlighted="1"]').forEach(function (element) {
            element.style.boxShadow = '';
            element.style.outline = '';
            element.style.outlineOffset = '';
            element.style.borderRadius = element.dataset.editorHighlightRadius || '';
            element.dataset.editorHighlighted = '0';
        });
    }

    function applyHighlight(role) {
        const doc = getPreviewDocument();
        if (!doc) {
            return;
        }

        clearHighlights();

        const targets = doc.querySelectorAll('[data-editor-role="' + role + '"]');
        targets.forEach(function (element, index) {
            if (!element.dataset.editorHighlightRadius) {
                const computedRadius = doc.defaultView.getComputedStyle(element).borderRadius || '0px';
                element.dataset.editorHighlightRadius = computedRadius;
            }

            element.style.outline = '2px solid rgba(13, 110, 253, 0.45)';
            element.style.outlineOffset = '4px';
            element.style.boxShadow = '0 0 0 8px rgba(13, 110, 253, 0.10)';
            element.style.borderRadius = element.dataset.editorHighlightRadius || '10px';
            element.dataset.editorHighlighted = '1';

            if (index === 0 && typeof element.scrollIntoView === 'function') {
                element.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'nearest' });
            }
        });
    }

    form.querySelectorAll('input, select').forEach(function (field) {
        field.addEventListener('input', function () {
            clampValue(field);
            syncLinkedInputs(field);
            applyPreviewStyles();
            syncFrameHeight();
        });

        field.addEventListener('change', function () {
            clampValue(field);
            syncLinkedInputs(field);
            applyPreviewStyles();
            syncFrameHeight();
        });
    });

    form.querySelectorAll('[data-preview-role]').forEach(function (card) {
        const role = card.dataset.previewRole;
        card.addEventListener('mouseenter', function () {
            applyHighlight(role);
        });
        card.addEventListener('mouseleave', function () {
            clearHighlights();
        });
        card.addEventListener('focusin', function () {
            applyHighlight(role);
        });
        card.addEventListener('focusout', function () {
            clearHighlights();
        });
    });

    previewFrame.addEventListener('load', function () {
        applyPreviewStyles();
        syncFrameHeight();
        setTimeout(syncFrameHeight, 200);
        setTimeout(syncFrameHeight, 700);
    });

    window.addEventListener('resize', function () {
        syncFrameHeight();
    });

    applyPreviewStyles();
    syncFrameHeight();
});
