# Factory Default: isolated browser baseline

At d4fbcae, synthetic user2680 `qa_factory_default_20261029` uses Profile.template=default with no legacy JSON entry and no UserBlogPreference record. Post272 is published synthetic content. Preparation asserts the database basename is `.qa100e.sqlite3`. This is a true factory baseline, unlike legacy user1.

Eight browser states cover blog and canonical post detail at320/390/768/1440. Document horizontal excess is0; sampled headings, calendar children, archive links and like controls have no local horizontal excess above1px. Raw state records include actual webkit text fill, fonts, rectangles and ancestor background/image/opacity chains. This does not establish all contrast, overlap, keyboard or populated-comment requirements.

The inspected390px viewport capture exposes a mobile reading-order problem: the left calendar column precedes the post. Exact blog geometry: title y114.188; layout y191.281; left column y191.281/h595.828/order-1; calendar y351.281; content column y787.109; post title y947.109. Both the sidebar and post retain a160px top offset. Absence of document overflow therefore does not make this a mobile acceptance pass. Next implementation should scope phone content-first ordering and top spacing to Default, then compare both routes at all four widths and preserve desktop. Dense-calendar and populated-comment cases still need coverage.

Native `Otvori post` navigation reached `/post/272/factory-default-acceptance-story/`. No password, email or production data mutation. No application changes and no suite rerun; latest suite remains237 tests57.491s at d4fbcae. Own QA server79584 stopped; temporary tab5 closed and viewport reset.

Raw files: `C:/Users/mario/Documents/Codex/2026-10-10/z/work/factory-default/fixture.json`, `states.json`, `phone-order.json`; preparation script `prepare.py`. Screenshot: `C:/Users/mario/Documents/Codex/2026-10-10/z/outputs/factory-default-phone.png` (390px viewport, not full page). Initial interactive-shell script execution failed after fixture creation; subsequent whole-script execution completed and verified the same fixture without duplication.
