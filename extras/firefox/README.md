# MT Verdant Nocturne — Firefox Theme (userChrome.css)

© Mayanktaker Computers & Web Development | https://mayanktaker.com

Companion dark theme for Mozilla Firefox matching the MT Verdant Nocturne palette.

## Installation
1. Open Firefox and navigate to `about:config`.
2. Search for `toolkit.legacyUserProfileCustomizations.stylesheets` and toggle it to **true**.
3. Open `about:support` and locate **Profile Directory** (click *Open Directory*).
4. Create a folder named `chrome` if it does not already exist.
5. Copy `userChrome.css` into that `chrome/` directory:
   ```sh
   cp userChrome.css ~/.mozilla/firefox/<your-profile>/chrome/
   ```
6. Restart Firefox.
