from pathlib import Path
import re

HTML_PATH = Path('blog/templates/blog/settings/_settings_tab.html')
if not HTML_PATH.exists():
    raise SystemExit(f'Ne mogu pronaći {HTML_PATH}.')
html = HTML_PATH.read_text(encoding='utf-8')

# Ukloni CSS blok.
html = re.sub(
    r'\n?<style>\s*/\* avatar-buttons-compact-fix:start \*/.*?/\* avatar-buttons-compact-fix:end \*/\s*</style>\s*',
    '\n',
    html,
    flags=re.DOTALL,
)

# Ukloni inline stilove s tri gumba samo ako su dodani ovim fixom.
for bid in ('avatarRotateBtn', 'avatarResetBtn', 'avatarApplyBtn'):
    pattern = rf'(<button\b[^>]*id="{re.escape(bid)}"[^>]*>)'
    def clean(m):
        tag = m.group(1)
        if 'style=' not in tag:
            return tag
        def clean_style(sm):
            style = sm.group(1)
            parts = [p.strip() for p in style.split(';') if p.strip()]
            blocked_prefixes = ('padding:', 'font-size:', 'line-height:', 'border-radius:', 'min-height:')
            parts = [p for p in parts if not p.replace(' ', '').lower().startswith(tuple(b.replace(' ', '').lower() for b in blocked_prefixes))]
            return ('style="' + '; '.join(parts) + '"') if parts else ''
        tag = re.sub(r'\s*style="([^"]*)"', clean_style, tag, count=1)
        return tag
    html = re.sub(pattern, clean, html, count=1)

HTML_PATH.write_text(html, encoding='utf-8')
print('Rollback gotov: uklonjen je compact button fix.')
