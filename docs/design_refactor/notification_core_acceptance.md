# U11 notification core journey acceptance

Baseline b6fa304. Synthetic reader2672 received notification7 from2680/post272, initially unread. At390 native Enter opens dropdown; Tab reaches enabled mark-read, Vidi sve, and all seven links. Native Enter on dropdown mark-read POSTs read-all and returns to notifications showing Pročitano with no unread badge. Database readback: id7/is_read=True. Raw z/work/notification-phone-unread-tabs.json and notification-phone-unread-result.txt. Inspected outputs/notification-dropdown-read-phone.png is a390 viewport, not a full-page capture.

## Requirement-to-proof closure

| Original U11 requirement | Evidence |
|---|---|
| Empty/populated/read list | notification_read_workflow.md, four-width empty/populated evidence |
| Reader navigation and persisted read state | notification_read_workflow.md; notification_destination_acceptance.md covers like/follow/comment/mention, canonical post and comment anchor |
| Recipient isolation and guest protection | Four integration tests in blog/test_notification_workflow.py; opening foreign notice404, mark-all only own and POST-only |
| Phone/tablet containing layout and long text | notification_phone_flow.md, notification_long_content.md, notification_tablet_keyboard.md |
| Actual text contrast and local containment | notification_destination_acceptance.md; actual child fill/opaque row backing, composed metadata6.781, main15.426; four widths |
| Main action size and keyboard access | notification_target_menu.md (48px minimum, phone52); notification_tablet_keyboard.md (four-width list Tab); desktop menu Tab recovery; this phone unread-menu action |
| Shared dropdown positioning | Retained phase81b2 evidence in both shells; no dropdown style change in this series |

The core U11 scope from phase102t is accepted for these recorded representative fixtures/states. This is not universal custom-content or every shared-shell interaction acceptance, nor a whole-project pass. General U01-U12 and37-design gaps remain in the matrix. No application change or new suite run in this final browser follow-up; latest242 tests68.604s belongs to b5569a2. No SMTP or real-user mutation. Reader logged out, tab14 closed, viewport reset, server66232 stopped.
