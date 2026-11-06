# Onboarding native invalid-date recovery

On caae326, native editing a date to an incomplete value produced validity.badInput=true. Moving to step3 and activating Spremi left the invalid date hidden in step2 and focus on Spremi; no POST occurred. This differs from the already repaired server-invalid-date response.

The form now captures invalid events and reveals the step containing its first invalid control before the browser focuses it and displays native validation. Native390 Enter on Spremi now opens step2, focuses id_author_birth_date and shows the browser validation bubble. The field remained visible and document/local overflow was zero at320/390/768/1440. Clearing the optional date, moving forward and pressing Enter saved successfully with the confirmation and owner-blog redirect. Logout/tab9close/viewport reset and servers66513/14706 stop confirmed.

Four paired initial samples retain control widths/heights/x positions/font/actual fill/background/local containment. Viewport y coordinates differ on phone/tablet due to uncontrolled scroll state; no blanket rectangle or pixel identity claim. The sampled tablet textarea remains182.046875px and buttons38px high; usability/target work remains open. No CSS changed. Native error bubble intentionally appears over surrounding content as browser UI.

Raw: z/work/native-date-proof.json (before/failure/after/fixed), native-date-widths.json, native-date-suite.txt. Inspected outputs/native-date-phone.png is a390px scrolled viewport showing focused partial date and validation bubble, not a full page. Existing six author journey tests cover server persistence and errors; the native event behavior is evidenced by the actual browser interaction, not those tests.

Check clean; migration check no changes. Full suite:250 tests passed in63.126s. Remaining: full Tab traversal, skip with incomplete native date, owner long-content, target sizes/tablet usability. Whole U04 remains partial.
