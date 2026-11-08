# Author question label contrast

The public author page used #0d6efd over its .12-alpha blue badge on white, yielding3.827 for the12px Javno text. Question/answer labels used black at .5 alpha over .06-alpha blue/green bubbles, yielding3.915/3.918. These values come from actual child fill and ancestor backgrounds, including the opaque white question card, not assumed body color.

The scoped author_detail.html change makes the public badge #084298 and qa-bubble-label #495057. Badge backing, all fonts and layout rules remain unchanged. Ratios are7.961 (public badge),7.547 (question label),7.579 (answer label). The shared bubble-label rule also applies to private questions; private-specific browser visual acceptance remains open. Contact/info labels are unchanged and are not accepted by this work.

Four fresh paired320/390/768/1440 samples show all16 rectangles/fonts/backgrounds identical and document/local overflow0. Older baseline-versus-after measurements had small geometry differences between browser environments; they are retained but superseded for geometry by author-label-paired-before.json and author-label-paired-after.json. The exact tested file was saved, only the two color changes temporarily reverted for the fresh baseline, then restored with a QA server restart. No new implementation change after the suite.

Durable evidence under C:/Users/mario/Documents/Codex/2026-10-10/z/work: author-badge-baseline.json, author-badge-contrast.json, author-badge-after.json, author-label-paired-before.json, author-label-paired-after.json, author-label-suite.txt. Inspected outputs/author-label-desktop.png is a scrolled desktop viewport showing both labels and public badge. A safe Tab from the public sign-in link reached the footer Home link; no form or private data submitted. This is not complete public keyboard acceptance.

Check and migration dry-run passed;251 tests313.329s passed. QA servers89130/54770/60221 stopped, tabs17/18closed and viewport reset. No complete U04/all37 acceptance claim; remaining focus, private states, info labels and matrix gates stay open.
