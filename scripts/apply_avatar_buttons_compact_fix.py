from pathlib import Path
import re
from datetime import datetime

HTML_PATH = Path('blog/templates/blog/settings/_settings_tab.html')
MARKER_START = '/* avatar-buttons-compact-fix:start */'
MARKER_END = '/* avatar-buttons-compact-fix:end */'

if not HTML_PATH.exists():
    raise SystemExit(f'Ne mogu pronaći {HTML_PATH}. Pokreni skriptu iz root foldera projekta.')

html = HTML_PATH.read_text(encoding='utf-8')
backup_path = HTML_PATH.with_suffix(HTML_PATH.suffix + f'.bak_avatar_buttons_compact_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
backup_path.write_text(html, encoding='utf-8')

# Ukloni staru verziju ovog istog fixa ako postoji.
html = re.sub(
    r'\n?<style>\s*/\* avatar-buttons-compact-fix:start \*/.*?/\* avatar-buttons-compact-fix:end \*/\s*</style>\s*',
    '\n',
    html,
    flags=re.DOTALL,
)

compact_css = f'''
<style>
{MARKER_START}
#avatarCropModal .avatar-crop-controls {{
    margin-top: 10px !important;
}}

#avatarCropModal .avatar-crop-control-row {{
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
}}

#avatarCropModal .avatar-crop-control-row .form-label {{
    font-size: 14px !important;
    line-height: 1.1 !important;
    margin: 0 !important;
    min-width: 74px !important;
}}

#avatarCropModal #avatarZoomRange {{
    height: 6px !important;
    padding: 0 !important;
}}

#avatarCropModal .avatar-crop-controls .d-flex.flex-wrap {{
    margin-top: 10px !important;
    gap: 8px !important;
}}

#avatarCropModal #avatarRotateBtn,
#avatarCropModal #avatarResetBtn {{
    padding: 5px 10px !important;
    font-size: 13px !important;
    line-height: 1.2 !important;
    border-radius: 7px !important;
    min-height: 0 !important;
}}

#avatarCropModal #avatarApplyBtn {{
    padding: 7px 16px !important;
    font-size: 15px !important;
    line-height: 1.2 !important;
    border-radius: 8px !important;
    min-height: 0 !important;
}}

#avatarCropModal .btn {{
    min-height: 0 !important;
}}
{MARKER_END}
</style>
'''

# Dodaj CSS odmah prije modala ako možemo, inače na kraj datoteke.
modal_marker = '<div class="modal fade avatar-crop-modal" id="avatarCropModal"'
if modal_marker in html:
    html = html.replace(modal_marker, compact_css + '\n' + modal_marker, 1)
else:
    html += '\n' + compact_css

# Dodaj i inline stilove na gumbe, jer to sigurno pregazi globalni CSS.
def add_or_update_inline_style(match):
    tag = match.group(0)
    add_style = match.group(1)
    if 'style=' in tag:
        tag = re.sub(r'style="([^"]*)"', lambda m: f'style="{m.group(1).rstrip()}; {add_style}"', tag, count=1)
    else:
        tag = tag[:-1] + f' style="{add_style}">'
    return tag

small_btn_style = 'padding:5px 10px !important; font-size:13px !important; line-height:1.2 !important; border-radius:7px !important; min-height:0 !important;'
apply_btn_style = 'padding:7px 16px !important; font-size:15px !important; line-height:1.2 !important; border-radius:8px !important; min-height:0 !important;'

# Prvo očisti ranije dodane inline duplikate samo na ova 3 gumba.
def clean_inline_for_button(html, button_id):
    pattern = rf'(<button\b[^>]*id="{re.escape(button_id)}"[^>]*>)'
    def clean(m):
        tag = m.group(1)
        # Makni ponovljene vrijednosti koje su dodavali prijašnji pokušaji, ali ostavi ostali style ako postoji.
        if 'style=' in tag:
            def clean_style(sm):
                style = sm.group(1)
                parts = [p.strip() for p in style.split(';') if p.strip()]
                blocked = ('padding:', 'font-size:', 'line-height:', 'border-radius:', 'min-height:')
                parts = [p for p in parts if not p.replace(' ', '').lower().startswith(tuple(b.replace(' ', '').lower() for b in blocked))]
                return 'style="' + '; '.join(parts) + ('; ' if parts else '') + '"'
            tag = re.sub(r'style="([^"]*)"', clean_style, tag, count=1)
            tag = tag.replace('style=""', '')
        return tag
    return re.sub(pattern, clean, html)

for bid in ('avatarRotateBtn', 'avatarResetBtn', 'avatarApplyBtn'):
    html = clean_inline_for_button(html, bid)

html = re.sub(r'<button\b[^>]*id="avatarRotateBtn"[^>]*>', lambda m: add_or_update_inline_style(re.match(r'(.*)', m.group(0) + small_btn_style)), html)
# Gornji pristup nije dobar za lambda s matchom; popravi eksplicitno ispod.

# Vrati ako je slučajno napravljena kriva zamjena iznad.
html = html.replace(small_btn_style + '>', '>')

for bid, style in [('avatarRotateBtn', small_btn_style), ('avatarResetBtn', small_btn_style), ('avatarApplyBtn', apply_btn_style)]:
    pattern = rf'(<button\b[^>]*id="{re.escape(bid)}"[^>]*>)'
    def repl(m, style=style):
        tag = m.group(1)
        if 'style=' in tag:
            tag = re.sub(r'style="([^"]*)"', lambda sm: f'style="{sm.group(1).rstrip()}; {style}"', tag, count=1)
        else:
            tag = tag[:-1] + f' style="{style}">'
        return tag
    html = re.sub(pattern, repl, html, count=1)

HTML_PATH.write_text(html, encoding='utf-8')
print('Gotovo: smanjeni su gumbi i donje kontrole avatara.')
print(f'Backup: {backup_path}')
