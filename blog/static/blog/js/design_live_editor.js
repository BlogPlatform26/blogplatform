document.addEventListener('DOMContentLoaded', function () {
    const iframe = document.getElementById('designLivePreviewFrame');
    const reloadBtn = document.getElementById('reloadPreviewBtn');
    const frameWrap = document.getElementById('designLiveFrameWrap');
    const frameShell = document.getElementById('designLiveFrameShell') || document.querySelector('.live-editor-frame-shell');
    const defaults = window.designLiveEditorDefaults || {};
    const config = window.designLiveEditorConfig || {};
    const tabButtons = document.querySelectorAll('[data-editor-tab]');
    const tabPanels = document.querySelectorAll('[data-editor-panel]');
    const uploadInput = document.querySelector('[data-live-background-upload]');
    const uploadPreview = document.getElementById('liveEditorUploadPreview');
    const systemImagePreview = document.getElementById('liveEditorSystemImagePreview');

    const highlightMap = {
        'blog-title': '.blog-page-title, .blog-page-title a',
        'post-title': '.blog-post-entry h4, .blog-post-title',
        'box-title': '.calendar-title, .archive-title, .sidebar-box-title, .blog-box-title',
        'post-date': '.blog-date-shell',
        'outer-background': 'body',
        'header-background': '.blog-header-main--simple',
        'content-background': '.blog-post-entry',
        'box-background': '.calendar-box, .archive-box, .sidebar-box, .live-analytics-widget, .sidebar-box--simple'
    };

    let previewNaturalWidth = 1360;
    let previewNaturalHeight = 720;
    let uploadedImageDataUrl = config.currentUploadImageUrl || '';

    function getIframeDocument() {
        try {
            return iframe && iframe.contentDocument ? iframe.contentDocument : null;
        } catch (error) {
            return null;
        }
    }

    function updatePreviewScale() {
        if (!iframe || !frameWrap || !frameShell) return;

        const availableWidth = Math.max(frameWrap.clientWidth - 4, 320);
        const scale = Math.min(1, availableWidth / previewNaturalWidth);

        iframe.style.transformOrigin = 'top left';
        iframe.style.transform = `scale(${scale})`;
        frameShell.style.width = Math.round(previewNaturalWidth * scale) + 'px';
        frameShell.style.height = Math.round(previewNaturalHeight * scale) + 'px';
        frameWrap.style.overflowX = 'hidden';
    }

    function resizeIframe() {
        const doc = getIframeDocument();
        if (!doc || !iframe) return;

        const body = doc.body;
        const html = doc.documentElement;
        const scrolling = doc.scrollingElement || html || body;

        const width = Math.max(
            scrolling ? scrolling.scrollWidth : 0,
            body ? body.scrollWidth : 0,
            html ? html.scrollWidth : 0,
            body ? body.offsetWidth : 0,
            html ? html.offsetWidth : 0,
            1180
        );

        const height = Math.max(
            scrolling ? scrolling.scrollHeight : 0,
            body ? body.scrollHeight : 0,
            html ? html.scrollHeight : 0,
            body ? body.offsetHeight : 0,
            html ? html.offsetHeight : 0,
            100
        );

        previewNaturalWidth = Math.max(width, 1180);
        previewNaturalHeight = height + 2;

        iframe.style.width = previewNaturalWidth + 'px';
        iframe.style.height = previewNaturalHeight + 'px';

        updatePreviewScale();
    }

    function ensureEditorStyle(doc) {
        if (!doc) return;
        let styleTag = doc.getElementById('design-live-editor-style');
        if (!styleTag) {
            styleTag = doc.createElement('style');
            styleTag.id = 'design-live-editor-style';
            doc.head.appendChild(styleTag);
        }
        styleTag.textContent = `
            .design-live-highlight-target {
                outline: 2px solid rgba(124, 58, 237, 0.55) !important;
                box-shadow: 0 0 0 6px rgba(124, 58, 237, 0.14) !important;
                border-radius: 10px !important;
                transition: box-shadow .16s ease, outline-color .16s ease;
            }
        `;

        let dynamicTag = doc.getElementById('design-live-editor-dynamic-style');
        if (!dynamicTag) {
            dynamicTag = doc.createElement('style');
            dynamicTag.id = 'design-live-editor-dynamic-style';
            doc.head.appendChild(dynamicTag);
        }
    }

    function getSelectedFontStack(selectName) {
        const select = document.querySelector(`[name="${selectName}"]`);
        if (!select) return '';
        const option = select.options[select.selectedIndex];
        return option ? option.dataset.fontStack || '' : '';
    }

    function withImportant(css) {
        return css.replace(/;/g, ' !important;');
    }

    function updateSystemImagePreview() {
        if (!systemImagePreview) return;
        const mode = (document.querySelector('[name="outer_background_mode"]') || {}).value || 'color';
        const imageKey = (document.querySelector('[name="outer_background_image"]') || {}).value || '';
        const imageUrl = (config.systemImageAssets || {})[imageKey] || '';

        if (mode === 'system_image' && imageUrl) {
            systemImagePreview.src = imageUrl;
            systemImagePreview.style.display = 'block';
        } else {
            systemImagePreview.style.display = 'none';
        }
    }

    function getPatternCss(patternKey, color) {
        const safeColor = color || '#efe4c9';
        const assets = config.patternAssets || {};
        const cssMap = {
            dots: `background-color:${safeColor};background-image:radial-gradient(rgba(255,255,255,0.58) 1.2px, transparent 1.2px);background-size:16px 16px;background-repeat:repeat;background-position:center;`,
            grid: `background-color:${safeColor};background-image:linear-gradient(rgba(255,255,255,0.34) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.34) 1px, transparent 1px);background-size:18px 18px;background-repeat:repeat;background-position:center;`,
            hearts: `background-color:${safeColor};background-image:url('${assets.hearts || ''}');background-size:120px 120px;background-repeat:repeat;background-position:center;`,
            flowers: `background-color:${safeColor};background-image:url('${assets.flowers || ''}');background-size:130px 130px;background-repeat:repeat;background-position:center;`,
            pencils: `background-color:${safeColor};background-image:url('${assets.pencils || ''}');background-size:150px 120px;background-repeat:repeat;background-position:center;`,
            paws: `background-color:${safeColor};background-image:url('${assets.paws || ''}');background-size:145px 120px;background-repeat:repeat;background-position:center;`,
            stars: `background-color:${safeColor};background-image:url('${assets.stars || ''}');background-size:135px 135px;background-repeat:repeat;background-position:center;`,
            music: `background-color:${safeColor};background-image:url('${assets.music || ''}');background-size:160px 120px;background-repeat:repeat;background-position:center;`,
            butterflies: `background-color:${safeColor};background-image:url('${assets.butterflies || ''}');background-size:155px 130px;background-repeat:repeat;background-position:center;`,
            books: `background-color:${safeColor};background-image:url('${assets.books || ''}');background-size:165px 138px;background-repeat:repeat;background-position:center;`,
            clouds: `background-color:${safeColor};background-image:url('${assets.clouds || ''}');background-size:180px 130px;background-repeat:repeat;background-position:center;`,
            bows: `background-color:${safeColor};background-image:url('${assets.bows || ''}');background-size:155px 138px;background-repeat:repeat;background-position:center;`,
            paper: `background-color:${safeColor};background-image:linear-gradient(180deg, rgba(255,255,255,0.14), rgba(255,255,255,0.06)), repeating-linear-gradient(135deg, rgba(255,255,255,0.12) 0px, rgba(255,255,255,0.12) 10px, rgba(0,0,0,0.03) 10px, rgba(0,0,0,0.03) 20px);background-size:auto;background-repeat:repeat;background-position:center;`
        };
        return withImportant(cssMap[patternKey] || cssMap.paper);
    }

    function updateModeBlocks() {
        const modeSelect = document.querySelector('[data-live-background-mode]');
        const mode = modeSelect ? modeSelect.value : '';
        document.querySelectorAll('[data-mode-panel]').forEach(function (panel) {
            panel.hidden = panel.dataset.modePanel !== mode;
        });
    }

    function updateBackgroundPreview() {
        if (!config.supportsBackgroundEditor) return;
        const doc = getIframeDocument();
        if (!doc) return;
        ensureEditorStyle(doc);

        const dynamicTag = doc.getElementById('design-live-editor-dynamic-style');
        if (!dynamicTag) return;

        const mode = (document.querySelector('[name="outer_background_mode"]') || {}).value || 'color';
        const color1 = (document.querySelector('[name="outer_background_color_1"]') || {}).value || '#efe4c9';
        const color2 = (document.querySelector('[name="outer_background_color_2"]') || {}).value || '#e1d0ac';
        const gradientDirection = (document.querySelector('[name="outer_background_gradient_direction"]') || {}).value || 'to bottom';
        const pattern = (document.querySelector('[name="outer_background_pattern"]') || {}).value || 'paper';
        const systemImage = (document.querySelector('[name="outer_background_image"]') || {}).value || '';
        const headerColor = (document.querySelector('[name="header_background_color_1"]') || {}).value || '#d98a37';
        const contentColor = (document.querySelector('[name="content_background_color"]') || {}).value || '#fffefb';
        const boxColor = (document.querySelector('[name="box_background_color"]') || {}).value || '#fffefb';
        const systemImageUrl = (config.systemImageAssets || {})[systemImage] || '';
        const imageUrl = uploadedImageDataUrl || systemImageUrl;
        const activeTemplate = config.activeTemplate || '';

        let bodyCss = '';
        let beforeCss = '';
        let afterCss = '';

        if (activeTemplate === 'simple_image') {
            if ((mode === 'system_image' || mode === 'upload_image') && imageUrl) {
                bodyCss = `background:${color1} !important; position:relative !important; min-height:100vh !important; overflow-x:hidden !important;`;
                beforeCss = `inset:0 !important; background-color:${color1} !important; background-image:url('${imageUrl}') !important; background-repeat:no-repeat !important; background-position:center center !important; background-size:cover !important; filter:blur(22px) saturate(1.02) !important; transform:scale(1.06) !important; opacity:0.16 !important;`;
                afterCss = `top:52px !important; left:0 !important; right:0 !important; height:clamp(240px, 31vw, 360px) !important; inset:auto !important; background-color:transparent !important; background-image:url('${imageUrl}') !important; background-repeat:no-repeat !important; background-position:center top !important; background-size:auto 100% !important; opacity:0.96 !important; -webkit-mask-image:linear-gradient(to bottom, rgba(0,0,0,1) 0%, rgba(0,0,0,1) 78%, rgba(0,0,0,0) 100%) !important; mask-image:linear-gradient(to bottom, rgba(0,0,0,1) 0%, rgba(0,0,0,1) 78%, rgba(0,0,0,0) 100%) !important;`;
            } else {
                bodyCss = `background:${color1} !important; position:relative !important; min-height:100vh !important; overflow-x:hidden !important;`;
                beforeCss = 'background-image:none !important; opacity:0 !important;';
                afterCss = 'background-image:none !important; opacity:0 !important;';
            }
        } else if (mode === 'gradient') {
            bodyCss = `background:linear-gradient(${gradientDirection}, ${color1}, ${color2}) !important;`;
        } else if (mode === 'pattern') {
            bodyCss = getPatternCss(pattern, color1);
        } else {
            bodyCss = `background:${color1} !important;`;
        }

        updateSystemImagePreview();

        dynamicTag.textContent = `
            body { ${bodyCss} }
            body::before { ${beforeCss} }
            body::after { ${afterCss} }
            .blog-header-main--simple { background:${headerColor} !important; }
            .blog-post-entry { background:${contentColor} !important; }
            .calendar-box,
            .archive-box,
            .sidebar-box,
            .live-analytics-widget,
            .sidebar-box--simple { background:${boxColor} !important; }
        `;

        resizeIframe();
    }

    function applyTitlePreviewValues() {
        const doc = getIframeDocument();
        if (!doc || !doc.body) return;
        ensureEditorStyle(doc);

        const blogColor = document.querySelector('[name="blog_title_color"]');
        const blogSize = document.querySelector('[name="blog_title_size"]');
        const postColor = document.querySelector('[name="post_title_color"]');
        const postSize = document.querySelector('[name="post_title_size"]');
        const boxColor = document.querySelector('[name="box_title_color"]');
        const boxSize = document.querySelector('[name="box_title_size"]');
        if (!blogColor || !blogSize || !postColor || !postSize || !boxColor || !boxSize) return;

        doc.body.style.setProperty('--blog-title-font', getSelectedFontStack('blog_title_font'));
        doc.body.style.setProperty('--blog-title-color', blogColor.value);
        doc.body.style.setProperty('--blog-title-size', blogSize.value + 'px');
        doc.body.style.setProperty('--post-title-font', getSelectedFontStack('post_title_font'));
        doc.body.style.setProperty('--post-title-color', postColor.value);
        doc.body.style.setProperty('--post-title-size', postSize.value + 'px');
        doc.body.style.setProperty('--box-title-font', getSelectedFontStack('box_title_font'));
        doc.body.style.setProperty('--box-title-color', boxColor.value);
        doc.body.style.setProperty('--box-title-size', boxSize.value + 'px');

        resizeIframe();
    }

    function updateDateEditorMode() {
        const effectSelect = document.querySelector('[name="post_date_effect"]');
        const secondaryWrap = document.querySelector('[data-date-secondary-wrap]');
        const color1Label = document.getElementById('postDateColor1Label');
        if (!effectSelect) return;

        const effect = effectSelect.value || 'solid';
        const usesTwoColors = effect !== 'solid';
        if (secondaryWrap) {
            secondaryWrap.hidden = !usesTwoColors;
        }
        if (color1Label) {
            color1Label.textContent = usesTwoColors ? 'Prva boja' : 'Boja';
        }
    }

    function applyDatePreviewValues() {
        const doc = getIframeDocument();
        if (!doc || !doc.body) return;

        const styleInput = document.querySelector('[name="post_date_style"]');
        const effectInput = document.querySelector('[name="post_date_effect"]');
        const color1Input = document.querySelector('[name="post_date_color_1"]');
        const color2Input = document.querySelector('[name="post_date_color_2"]');
        const sizeInput = document.querySelector('[name="post_date_size"]');
        if (!styleInput || !effectInput || !color1Input || !sizeInput) return;

        const style = styleInput.value || 'classic_vertical';
        const effect = effectInput.value || 'solid';
        const color1 = color1Input.value || '#d97706';
        const color2 = (color2Input && color2Input.value) ? color2Input.value : color1;
        const size = sizeInput.value || '100';

        doc.body.style.setProperty('--post-date-color', color1);
        doc.body.style.setProperty('--post-date-color-1', color1);
        doc.body.style.setProperty('--post-date-color-2', color2);
        doc.body.style.setProperty('--post-date-scale', size);
        doc.body.style.setProperty('--post-date-style', style);
        doc.body.style.setProperty('--post-date-effect', effect);

        doc.querySelectorAll('.blog-date-shell').forEach(function (element) {
            Array.from(element.classList).forEach(function (className) {
                if (className.indexOf('blog-date-style-') === 0 || className.indexOf('blog-date-effect-') === 0) {
                    element.classList.remove(className);
                }
            });
            element.classList.add('blog-date-style-' + style);
            element.classList.add('blog-date-effect-' + effect);
            element.setAttribute('data-date-style', style);
            element.setAttribute('data-date-effect', effect);
        });

        updateDateEditorMode();
        resizeIframe();
    }

    function applyPreviewValues() {
        applyTitlePreviewValues();
        applyDatePreviewValues();
        updateModeBlocks();
        updateBackgroundPreview();
    }

    function clearHighlights() {
        const doc = getIframeDocument();
        if (!doc) return;
        doc.querySelectorAll('.design-live-highlight-target').forEach(function (element) {
            element.classList.remove('design-live-highlight-target');
        });
    }

    function setHighlight(targetKey) {
        clearHighlights();
        const doc = getIframeDocument();
        if (!doc) return;
        const selector = highlightMap[targetKey];
        if (!selector) return;
        doc.querySelectorAll(selector).forEach(function (element) {
            element.classList.add('design-live-highlight-target');
        });
    }

    function activateTab(tabKey, syncUrl) {
        const finalTab = tabKey === 'pozadine' && !config.supportsBackgroundEditor ? 'naslovi' : tabKey;
        tabButtons.forEach(function (button) {
            button.classList.toggle('is-active', button.dataset.editorTab === finalTab);
        });
        tabPanels.forEach(function (panel) {
            panel.hidden = panel.dataset.editorPanel !== finalTab;
        });
        document.body.dataset.editorSection = finalTab;
        if (syncUrl && window.history && window.history.replaceState) {
            const url = new URL(window.location.href);
            url.searchParams.set('section', finalTab);
            window.history.replaceState({}, '', url.toString());
        }
    }

    tabButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            if (button.disabled) return;
            activateTab(button.dataset.editorTab, true);
        });
    });

    document.querySelectorAll('.editor-card[data-highlight-target]').forEach(function (card) {
        card.addEventListener('mouseenter', function () {
            card.classList.add('is-hovered');
            setHighlight(card.dataset.highlightTarget);
        });
        card.addEventListener('mouseleave', function () {
            card.classList.remove('is-hovered');
            clearHighlights();
        });
    });

    document.querySelectorAll('[data-size-range]').forEach(function (rangeInput) {
        const inputName = rangeInput.dataset.sizeRange;
        const numberInput = document.querySelector(`[data-size-input="${inputName}"]`);
        if (!numberInput) return;
        rangeInput.addEventListener('input', function () {
            numberInput.value = rangeInput.value;
            if (inputName === 'post_date_size') {
                applyDatePreviewValues();
            } else {
                applyTitlePreviewValues();
            }
        });
        numberInput.addEventListener('input', function () {
            rangeInput.value = numberInput.value;
            if (inputName === 'post_date_size') {
                applyDatePreviewValues();
            } else {
                applyTitlePreviewValues();
            }
        });
    });

    document.querySelectorAll('[data-live-font], [data-live-color], [data-live-size]').forEach(function (input) {
        input.addEventListener('input', applyTitlePreviewValues);
        input.addEventListener('change', applyTitlePreviewValues);
    });

    document.querySelectorAll('[data-live-date-style], [data-live-date-effect], [data-live-date-color], [data-live-date-size]').forEach(function (input) {
        input.addEventListener('input', applyDatePreviewValues);
        input.addEventListener('change', applyDatePreviewValues);
    });

    document.querySelectorAll('[data-live-background-mode], [data-live-background-color], [data-live-background-select]').forEach(function (input) {
        input.addEventListener('input', function () {
            updateModeBlocks();
            updateBackgroundPreview();
        });
        input.addEventListener('change', function () {
            updateModeBlocks();
            updateBackgroundPreview();
        });
    });

    if (uploadInput) {
        uploadInput.addEventListener('change', function () {
            const file = uploadInput.files && uploadInput.files[0];
            if (!file) {
                uploadedImageDataUrl = config.currentUploadImageUrl || '';
                updateBackgroundPreview();
                return;
            }
            const reader = new FileReader();
            reader.onload = function (event) {
                uploadedImageDataUrl = event.target && event.target.result ? event.target.result : '';
                if (uploadPreview) {
                    uploadPreview.src = uploadedImageDataUrl;
                    uploadPreview.style.display = uploadedImageDataUrl ? 'block' : 'none';
                }
                const modeSelect = document.querySelector('[data-live-background-mode]');
                if (modeSelect) {
                    modeSelect.value = 'upload_image';
                    updateModeBlocks();
                }
                updateBackgroundPreview();
            };
            reader.readAsDataURL(file);
        });
    }

    document.querySelectorAll('[data-reset-card]').forEach(function (button) {
        button.addEventListener('click', function () {
            const target = button.dataset.resetCard;
            const group = defaults[target];
            if (!group) return;
            const fieldMap = {
                blog: { font: 'blog_title_font', color: 'blog_title_color', size: 'blog_title_size' },
                post: { font: 'post_title_font', color: 'post_title_color', size: 'post_title_size' },
                box: { font: 'box_title_font', color: 'box_title_color', size: 'box_title_size' },
                date: { style: 'post_date_style', effect: 'post_date_effect', color1: 'post_date_color_1', color2: 'post_date_color_2', size: 'post_date_size' }
            };
            const fields = fieldMap[target];
            if (!fields) return;
            if (target === 'date') {
                const styleSelect = document.querySelector(`[name="${fields.style}"]`);
                const effectSelect = document.querySelector(`[name="${fields.effect}"]`);
                const color1Input = document.querySelector(`[name="${fields.color1}"]`);
                const color2Input = document.querySelector(`[name="${fields.color2}"]`);
                const sizeInput = document.querySelector(`[name="${fields.size}"]`);
                const sizeRange = document.querySelector(`[data-size-range="${fields.size}"]`);
                if (styleSelect) styleSelect.value = group.style;
                if (effectSelect) effectSelect.value = group.effect;
                if (color1Input) color1Input.value = group.color1;
                if (color2Input) color2Input.value = group.color2;
                if (sizeInput) sizeInput.value = group.size;
                if (sizeRange) sizeRange.value = group.size;
                applyDatePreviewValues();
                return;
            }
            const fontSelect = document.querySelector(`[name="${fields.font}"]`);
            const colorInput = document.querySelector(`[name="${fields.color}"]`);
            const sizeInput = document.querySelector(`[name="${fields.size}"]`);
            const sizeRange = document.querySelector(`[data-size-range="${fields.size}"]`);
            if (fontSelect) fontSelect.value = group.font;
            if (colorInput) colorInput.value = group.color;
            if (sizeInput) sizeInput.value = group.size;
            if (sizeRange) sizeRange.value = group.size;
            applyTitlePreviewValues();
        });
    });

    if (reloadBtn && iframe) {
        reloadBtn.addEventListener('click', function () {
            iframe.contentWindow.location.reload();
            setTimeout(function () {
                applyPreviewValues();
                resizeIframe();
                updatePreviewScale();
            }, 180);
            setTimeout(function () {
                applyPreviewValues();
                resizeIframe();
                updatePreviewScale();
            }, 800);
        });
    }

    if (iframe) {
        iframe.addEventListener('load', function () {
            applyPreviewValues();
            resizeIframe();
            const doc = getIframeDocument();
            if (!doc || !doc.body) return;
            const observer = new MutationObserver(function () {
                resizeIframe();
            });
            observer.observe(doc.body, {
                childList: true,
                subtree: true,
                attributes: true
            });
            setTimeout(resizeIframe, 180);
            setTimeout(resizeIframe, 700);
        });
    }

    window.addEventListener('resize', function () {
        resizeIframe();
        updatePreviewScale();
    });

    activateTab(config.activeSection || 'naslovi', false);
    updateModeBlocks();
    updateDateEditorMode();
    setTimeout(function () {
        applyPreviewValues();
        resizeIframe();
        updatePreviewScale();
    }, 120);
});

/* BLOGPLATFORM_LIVE_PREVIEW_RUNTIME_FIX_START */
(function () {
    function onReady(callback) {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', callback);
        } else {
            callback();
        }
    }

    function getIframe() {
        return document.getElementById('designLivePreviewFrame');
    }

    function getPreviewDocument() {
        var iframe = getIframe();

        if (!iframe) {
            return null;
        }

        try {
            return iframe.contentDocument || (iframe.contentWindow && iframe.contentWindow.document) || null;
        } catch (error) {
            return null;
        }
    }

    function ensureStyle(doc, id) {
        if (!doc || !doc.head) {
            return null;
        }

        var style = doc.getElementById(id);

        if (!style) {
            style = doc.createElement('style');
            style.id = id;
            doc.head.appendChild(style);
        }

        return style;
    }

    function fieldValue(name, fallback) {
        var field = document.querySelector('[name="' + name + '"]');

        if (!field) {
            return fallback;
        }

        return field.value || fallback;
    }

    function toPx(value, fallback) {
        var raw = String(value || fallback || '').replace('px', '').trim();
        var number = parseInt(raw, 10);

        if (!Number.isFinite(number) || number <= 0) {
            number = parseInt(fallback, 10) || 16;
        }

        return number + 'px';
    }

    function selectedFontStack(name) {
        var select = document.querySelector('[name="' + name + '"]');

        if (!select) {
            return 'Georgia, "Times New Roman", serif';
        }

        var option = select.options[select.selectedIndex];

        if (option && option.dataset && option.dataset.fontStack) {
            return option.dataset.fontStack;
        }

        var value = (select.value || '').toLowerCase();

        var fallbackMap = {
            system: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
            arial: 'Arial, Helvetica, sans-serif',
            verdana: 'Verdana, Geneva, sans-serif',
            trebuchet: '"Trebuchet MS", Helvetica, sans-serif',
            times: '"Times New Roman", Times, serif',
            georgia: 'Georgia, "Times New Roman", serif',
            garamond: 'Garamond, Georgia, serif',
            palatino: '"Palatino Linotype", Palatino, serif',
            helvetica: 'Helvetica, Arial, sans-serif',
            tahoma: 'Tahoma, Geneva, sans-serif'
        };

        return fallbackMap[value] || 'Georgia, "Times New Roman", serif';
    }

    function setVar(target, name, value) {
        if (target && value !== undefined && value !== null && value !== '') {
            target.style.setProperty(name, value);
        }
    }

    function applyLiveTitles() {
        var doc = getPreviewDocument();

        if (!doc || !doc.body || !doc.documentElement) {
            return;
        }

        var blogColor = fieldValue('blog_title_color', '#3f3128');
        var postColor = fieldValue('post_title_color', '#111827');
        var boxColor = fieldValue('box_title_color', '#3f3128');

        var blogSize = toPx(fieldValue('blog_title_size', '54'), '54');
        var postSize = toPx(fieldValue('post_title_size', '32'), '32');
        var boxSize = toPx(fieldValue('box_title_size', '13'), '13');

        var blogFont = selectedFontStack('blog_title_font');
        var postFont = selectedFontStack('post_title_font');
        var boxFont = selectedFontStack('box_title_font');

        [doc.documentElement, doc.body].forEach(function (target) {
            setVar(target, '--blog-title-font', blogFont);
            setVar(target, '--blog-title-color', blogColor);
            setVar(target, '--blog-title-size', blogSize);

            setVar(target, '--post-title-font', postFont);
            setVar(target, '--post-title-color', postColor);
            setVar(target, '--post-title-size', postSize);

            setVar(target, '--box-title-font', boxFont);
            setVar(target, '--box-title-color', boxColor);
            setVar(target, '--box-title-size', boxSize);
        });

        var style = ensureStyle(doc, 'blogplatform-live-editor-title-runtime-css');

        if (!style) {
            return;
        }

        style.textContent = `
            .blog-page-title,
            .blog-page-title a,
            .blog-page-title .blog-link,
            .blog-header-main .blog-page-title,
            .blog-header-main .blog-page-title a {
                font-family: ${blogFont} !important;
                color: ${blogColor} !important;
                -webkit-text-fill-color: ${blogColor} !important;
                font-size: ${blogSize} !important;
            }

            .blog-page-subtitle {
                color: ${blogColor} !important;
                -webkit-text-fill-color: ${blogColor} !important;
            }

            .blog-post-entry h1,
            .blog-post-entry h2,
            .blog-post-entry h3,
            .blog-post-entry h4,
            .blog-post-entry h5,
            .blog-post-entry h6,
            .blog-post-entry h1 a,
            .blog-post-entry h2 a,
            .blog-post-entry h3 a,
            .blog-post-entry h4 a,
            .blog-post-entry h5 a,
            .blog-post-entry h6 a,
            .blog-post-title,
            .blog-post-title a,
            .post-title,
            .post-title a,
            .jus-post h4,
            .jus-post h4 a,
            .jus-post .blog-post-title,
            .mj-post h4,
            .mj-post h4 a,
            .mj-post .blog-post-title,
            .magazin-post-entry h4,
            .magazin-post-entry h4 a,
            .magazin-post-entry .blog-post-title {
                font-family: ${postFont} !important;
                color: ${postColor} !important;
                -webkit-text-fill-color: ${postColor} !important;
                font-size: ${postSize} !important;
            }

            .calendar-title,
            .archive-title,
            .sidebar-box-title,
            .blog-box-title,
            .box-title,
            .user-box-title,
            .live-analytics-widget .small.fw-semibold {
                font-family: ${boxFont} !important;
                color: ${boxColor} !important;
                -webkit-text-fill-color: ${boxColor} !important;
                font-size: ${boxSize} !important;
            }
        `;
    }

    function applyLiveDate() {
        var doc = getPreviewDocument();

        if (!doc || !doc.body || !doc.documentElement) {
            return;
        }

        var color1 = fieldValue('post_date_color_1', fieldValue('post_date_color', '#d97706'));
        var color2 = fieldValue('post_date_color_2', '#ffd200');
        var styleValue = fieldValue('post_date_style', 'classic_vertical');
        var effectValue = fieldValue('post_date_effect', 'solid');
        var sizeValue = fieldValue('post_date_size', '100');

        [doc.documentElement, doc.body].forEach(function (target) {
            setVar(target, '--post-date-color', color1);
            setVar(target, '--post-date-color-1', color1);
            setVar(target, '--post-date-color-2', color2);
            setVar(target, '--post-date-scale', sizeValue);
            setVar(target, '--post-date-style', styleValue);
            setVar(target, '--post-date-effect', effectValue);
        });

        doc.querySelectorAll('.blog-date-shell').forEach(function (element) {
            Array.from(element.classList).forEach(function (className) {
                if (className.indexOf('blog-date-style-') === 0 || className.indexOf('blog-date-effect-') === 0) {
                    element.classList.remove(className);
                }
            });

            element.classList.add('blog-date-style-' + styleValue);
            element.classList.add('blog-date-effect-' + effectValue);
            element.setAttribute('data-date-style', styleValue);
            element.setAttribute('data-date-effect', effectValue);
        });

        var style = ensureStyle(doc, 'blogplatform-live-editor-date-runtime-css');

        if (!style) {
            return;
        }

        style.textContent = `
            .blog-date-day,
            .blog-date-month,
            .blog-date-year,
            .blog-date-inline,
            .post-date,
            .post-date-display {
                color: ${color1} !important;
                -webkit-text-fill-color: ${color1} !important;
            }
        `;
    }

    function applyLiveBackgrounds() {
        var config = window.designLiveEditorConfig || {};

        if (!config.supportsBackgroundEditor) {
            return;
        }

        var doc = getPreviewDocument();

        if (!doc || !doc.body || !doc.documentElement) {
            return;
        }

        var headerColor = fieldValue('header_background_color_1', '#d98a37');
        var contentColor = fieldValue('content_background_color', '#fffefb');
        var boxColor = fieldValue('box_background_color', '#fffefb');

        var outerMode = fieldValue('outer_background_mode', 'color');
        var outer1 = fieldValue('outer_background_color_1', '#efe4c9');
        var outer2 = fieldValue('outer_background_color_2', '#e1d0ac');
        var direction = fieldValue('outer_background_gradient_direction', 'to bottom');

        var outerBackground = outer1;

        if (outerMode === 'gradient') {
            outerBackground = 'linear-gradient(' + direction + ', ' + outer1 + ', ' + outer2 + ')';
        }

        var style = ensureStyle(doc, 'blogplatform-live-editor-background-runtime-css');

        if (!style) {
            return;
        }

        style.textContent = `
            body {
                background: ${outerBackground} !important;
            }

            .blog-header-main--simple {
                background: ${headerColor} !important;
            }

            .blog-post-entry {
                background: ${contentColor} !important;
            }

            .calendar-box,
            .archive-box,
            .sidebar-box,
            .live-analytics-widget,
            .sidebar-box--simple {
                background: ${boxColor} !important;
            }
        `;
    }

    function applyLivePreviewNow() {
        applyLiveTitles();
        applyLiveDate();
        applyLiveBackgrounds();
    }

    function applyLivePreviewSoon() {
        applyLivePreviewNow();

        setTimeout(applyLivePreviewNow, 40);
        setTimeout(applyLivePreviewNow, 140);
        setTimeout(applyLivePreviewNow, 400);
    }

    function bindLivePreviewFix() {
        var iframe = getIframe();

        document.querySelectorAll(
            '[data-live-font], [data-live-color], [data-live-size], ' +
            '[data-size-range], [data-size-input], ' +
            '[data-live-date-style], [data-live-date-effect], [data-live-date-color], [data-live-date-size], ' +
            '[data-live-background-mode], [data-live-background-color], [data-live-background-select]'
        ).forEach(function (input) {
            input.addEventListener('input', applyLivePreviewSoon);
            input.addEventListener('change', applyLivePreviewSoon);
            input.addEventListener('keyup', applyLivePreviewSoon);
        });

        document.querySelectorAll('[data-reset-card]').forEach(function (button) {
            button.addEventListener('click', applyLivePreviewSoon);
        });

        var reloadBtn = document.getElementById('reloadPreviewBtn');

        if (reloadBtn) {
            reloadBtn.addEventListener('click', function () {
                setTimeout(applyLivePreviewSoon, 120);
                setTimeout(applyLivePreviewSoon, 700);
            });
        }

        if (iframe) {
            iframe.addEventListener('load', applyLivePreviewSoon);
        }

        applyLivePreviewSoon();
    }

    onReady(bindLivePreviewFix);
}());
/* BLOGPLATFORM_LIVE_PREVIEW_RUNTIME_FIX_END */
