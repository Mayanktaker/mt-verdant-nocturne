# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Extended symbolic wireframes for MT-Verdant-Icons suite.
# Covers empty states, Libadwaita navigation, GNOME screenshot UI, and all Settings panels.

EXTENDED_SYMBOLIC_ICONS = {
    # ---------------------------------------------------------------------
    # Empty View & Navigation Placeholders (Fixes Clocks Screenshot 1 & Settings Screenshot 2)
    # ---------------------------------------------------------------------
    "globe-centered-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <line x1="2" y1="8" x2="14" y2="8" stroke="currentColor" stroke-width="1.2"/>
  <line x1="8" y1="2" x2="8" y2="14" stroke="currentColor" stroke-width="1.2"/>
  <path d="M 8 2 C 5.5 4 4.5 6 4.5 8 C 4.5 10 5.5 12 8 14 C 10.5 12 11.5 10 11.5 8 C 11.5 6 10.5 4 8 2 Z" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <path d="M 3.2 5 C 5.2 6.2 10.8 6.2 12.8 5 M 3.2 11 C 5.2 9.8 10.8 9.8 12.8 11" fill="none" stroke="currentColor" stroke-width="1"/>
</svg>''',

    "globe-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <line x1="2" y1="8" x2="14" y2="8" stroke="currentColor" stroke-width="1.2"/>
  <line x1="8" y1="2" x2="8" y2="14" stroke="currentColor" stroke-width="1.2"/>
  <path d="M 8 2 C 5.5 4 4.5 6 4.5 8 C 4.5 10 5.5 12 8 14 C 10.5 12 11.5 10 11.5 8 C 11.5 6 10.5 4 8 2 Z" fill="none" stroke="currentColor" stroke-width="1.2"/>
</svg>''',

    "map-globe-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <line x1="2" y1="8" x2="14" y2="8" stroke="currentColor" stroke-width="1.2"/>
  <line x1="8" y1="2" x2="8" y2="14" stroke="currentColor" stroke-width="1.2"/>
  <path d="M 8 2 C 5.5 4 4.5 6 4.5 8 C 4.5 10 5.5 12 8 14 C 10.5 12 11.5 10 11.5 8 C 11.5 6 10.5 4 8 2 Z" fill="none" stroke="currentColor" stroke-width="1.2"/>
</svg>''',

    # Libadwaita Split Views (Fixes missing headerbar toggle in GNOME Settings)
    "view-sidebar-start-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <rect x="1.5" y="2" width="13" height="12" rx="2" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <line x1="6" y1="2" x2="6" y2="14" stroke="currentColor" stroke-width="1.3"/>
  <rect x="2" y="2.5" width="3.5" height="11" fill="currentColor" opacity="0.85"/>
</svg>''',

    "view-sidebar-end-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <rect x="1.5" y="2" width="13" height="12" rx="2" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <line x1="10" y1="2" x2="10" y2="14" stroke="currentColor" stroke-width="1.3"/>
  <rect x="10.5" y="2.5" width="3.5" height="11" fill="currentColor" opacity="0.85"/>
</svg>''',

    "view-sidebar-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <rect x="1.5" y="2" width="13" height="12" rx="2" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <line x1="6" y1="2" x2="6" y2="14" stroke="currentColor" stroke-width="1.3"/>
  <rect x="2" y="2.5" width="3.5" height="11" fill="currentColor" opacity="0.85"/>
</svg>''',

    "widget-split-views-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <rect x="1.5" y="2" width="13" height="12" rx="2" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <line x1="6" y1="2" x2="6" y2="14" stroke="currentColor" stroke-width="1.3"/>
  <rect x="2" y="2.5" width="3.5" height="11" fill="currentColor" opacity="0.85"/>
</svg>''',

    # ---------------------------------------------------------------------
    # GNOME Interactive Screenshot & Screencast Suite
    # ---------------------------------------------------------------------
    "camera-photo-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" fill-rule="evenodd" d="M 5.5 2 L 6.5 3 L 9.5 3 L 10.5 2 Z M 2 4 C 1.45 4 1 4.45 1 5 L 1 12 C 1 12.55 1.45 13 2 13 L 14 13 C 14.55 13 15 12.55 15 12 L 15 5 C 15 4.45 14.55 4 14 4 Z M 8 6 C 9.66 6 11 7.34 11 9 C 11 10.66 9.66 12 8 12 C 6.34 12 5 10.66 5 9 C 5 7.34 6.34 6 8 6 Z M 8 7.3 C 7.06 7.3 6.3 8.06 6.3 9 C 6.3 9.94 7.06 10.7 8 10.7 C 8.94 10.7 9.7 9.94 9.7 9 C 9.7 8.06 8.94 7.3 8 7.3 Z"/>
</svg>''',

    "camera-video-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" fill-rule="evenodd" d="M 2 4 C 1.45 4 1 4.45 1 5 L 1 11 C 1 11.55 1.45 12 2 12 L 9.5 12 C 10.05 12 10.5 11.55 10.5 11 L 10.5 9.5 L 14.2 11.7 C 14.6 11.9 15 11.7 15 11.2 L 15 4.8 C 15 4.3 14.6 4.1 14.2 4.3 L 10.5 6.5 L 10.5 5 C 10.5 4.45 10.05 4 9.5 4 Z"/>
</svg>''',

    "screenshot-ui-area-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" d="M 2 2 L 6 2 L 6 3.5 L 3.5 3.5 L 3.5 6 L 2 6 Z M 10 2 L 14 2 L 14 6 L 12.5 6 L 12.5 3.5 L 10 3.5 Z M 2 10 L 3.5 10 L 3.5 12.5 L 6 12.5 L 6 14 L 2 14 Z M 12.5 10 L 14 10 L 14 14 L 10 14 L 10 12.5 L 12.5 12.5 Z"/>
  <circle cx="8" cy="8" r="1.3" fill="currentColor"/>
</svg>''',

    "screenshot-ui-display-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" fill-rule="evenodd" d="M 2 2 C 1.45 2 1 2.45 1 3 L 1 10 C 1 10.55 1.45 11 2 11 L 6.5 11 L 5.5 13.5 L 4 13.5 L 4 14.5 L 12 14.5 L 12 13.5 L 10.5 13.5 L 9.5 11 L 14 11 C 14.55 11 15 10.55 15 10 L 15 3 C 15 2.45 14.55 2 14 2 Z M 2.5 3.5 L 13.5 3.5 L 13.5 9.5 L 2.5 9.5 Z"/>
</svg>''',

    "screenshot-ui-window-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" fill-rule="evenodd" d="M 2 2 C 1.45 2 1 2.45 1 3 L 1 13 C 1 13.55 1.45 14 2 14 L 14 14 C 14.55 14 15 13.55 15 13 L 15 3 C 15 2.45 14.55 2 14 2 Z M 2.5 5.5 L 13.5 5.5 L 13.5 12.5 L 2.5 12.5 Z M 3 3.8 C 3 4.2 3.3 4.5 3.7 4.5 C 4.1 4.5 4.4 4.2 4.4 3.8 C 4.4 3.4 4.1 3.1 3.7 3.1 C 3.3 3.1 3 3.4 3 3.8 Z M 5.2 3.8 C 5.2 4.2 5.5 4.5 5.9 4.5 C 6.3 4.5 6.6 4.2 6.6 3.8 C 6.6 3.4 6.3 3.1 5.9 3.1 C 5.5 3.1 5.2 3.4 5.2 3.8 Z M 7.4 3.8 C 7.4 4.2 7.7 4.5 8.1 4.5 C 8.5 4.5 8.8 4.2 8.8 3.8 C 8.8 3.4 8.5 3.1 8.1 3.1 C 7.7 3.1 7.4 3.4 7.4 3.8 Z"/>
</svg>''',

    "screenshot-ui-show-pointer-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" d="M 3 1.5 L 3 12.5 L 6.2 9.7 L 8.7 14.5 L 10.5 13.5 L 8 8.8 L 12.5 8.8 Z"/>
</svg>''',

    "record-screen-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="8" cy="8" r="3.2" fill="currentColor"/>
</svg>''',

    "media-record-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="8" cy="8" r="3.2" fill="currentColor"/>
</svg>''',

    "screencast-stop-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <circle cx="8" cy="8" r="6.5" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <rect x="5.5" y="5.5" width="5" height="5" rx="0.8" fill="currentColor"/>
</svg>''',

    "screenshooter-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" fill-rule="evenodd" d="M 5.5 2 L 6.5 3 L 9.5 3 L 10.5 2 Z M 2 4 C 1.45 4 1 4.45 1 5 L 1 12 C 1 12.55 1.45 13 2 13 L 14 13 C 14.55 13 15 12.55 15 12 L 15 5 C 15 4.45 14.55 4 14 4 Z M 8 6 C 9.66 6 11 7.34 11 9 C 11 10.66 9.66 12 8 12 C 6.34 12 5 10.66 5 9 C 5 7.34 6.34 6 8 6 Z M 8 7.3 C 7.06 7.3 6.3 8.06 6.3 9 C 6.3 9.94 7.06 10.7 8 10.7 C 8.94 10.7 9.7 9.94 9.7 9 C 9.7 8.06 8.94 7.3 8 7.3 Z"/>
</svg>''',

    "screencast-recorded-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="8" cy="8" r="3.2" fill="currentColor"/>
</svg>''',

    "screenshot-recorded-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" fill-rule="evenodd" d="M 5.5 2 L 6.5 3 L 9.5 3 L 10.5 2 Z M 2 4 C 1.45 4 1 4.45 1 5 L 1 12 C 1 12.55 1.45 13 2 13 L 14 13 C 14.55 13 15 12.55 15 12 L 15 5 C 15 4.45 14.55 4 14 4 Z M 8 6 C 9.66 6 11 7.34 11 9 C 11 10.66 9.66 12 8 12 C 6.34 12 5 10.66 5 9 C 5 7.34 6.34 6 8 6 Z"/>
</svg>''',

    # ---------------------------------------------------------------------
    # Complete GNOME Settings Suite (All Panels)
    # ---------------------------------------------------------------------
    "org.gnome.Settings-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" d="M 7 1 L 9 1 L 9.4 3 C 9.9 3.2 10.4 3.5 10.8 3.9 L 12.7 3.2 L 13.7 4.9 L 12.2 6.3 C 12.3 6.8 12.3 7.2 12.3 7.7 L 13.9 8.9 L 13.1 10.7 L 11.2 10.2 C 10.8 10.6 10.4 10.9 9.9 11.1 L 9.3 13 L 7.3 13 L 6.9 11.1 C 6.4 10.9 5.9 10.6 5.5 10.2 L 3.6 10.9 L 2.6 9.2 L 4.1 7.8 C 4 7.4 4 6.9 4 6.5 L 2.4 5.2 L 3.2 3.4 L 5.1 3.9 C 5.5 3.5 5.9 3.2 6.4 3 L 7 1 Z M 8 5 C 6.6 5 5.5 6.1 5.5 7.5 C 5.5 8.9 6.6 10 8 10 C 9.4 10 10.5 8.9 10.5 7.5 C 10.5 6.1 9.4 5 8 5 Z"/>
</svg>''',

    "org.gnome.Settings-about-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <circle cx="8" cy="8" r="6.5" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <circle cx="8" cy="5" r="1" fill="currentColor"/>
  <rect x="7.2" y="7" width="1.6" height="5" rx="0.5" fill="currentColor"/>
</svg>''',

    "org.gnome.Settings-accessibility-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <circle cx="8" cy="3" r="1.3" fill="currentColor"/>
  <path fill="currentColor" d="M 3 6 L 13 6 L 13 7.3 L 10 7.3 L 10 14 L 8.6 14 L 8.6 10 L 7.4 10 L 7.4 14 L 6 14 L 6 7.3 L 3 7.3 Z"/>
</svg>''',

    "org.gnome.Settings-accessibility-hearing-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" d="M 6.5 14 C 4 14 3 11.5 3 9 C 3 5 5 2 9 2 C 12 2 13.5 4 13.5 6.5 C 13.5 9 11.5 10.5 10 11.5 L 9 12.5"/>
  <path fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" d="M 7.5 7 C 9.5 7 10.5 8 10 9.5 C 9.5 11 8 11 8 11"/>
</svg>''',

    "org.gnome.Settings-accessibility-pointing-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" d="M 4 2 L 4 13 L 7 10.5 L 9.5 15 L 11.2 14 L 8.8 9.5 L 13 9.5 Z"/>
</svg>''',

    "org.gnome.Settings-accessibility-seeing-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" d="M 1.5 8 C 3 4.5 6 3 8 3 C 10 3 13 4.5 14.5 8 C 13 11.5 10 13 8 13 C 6 13 3 11.5 1.5 8 Z"/>
  <circle cx="8" cy="8" r="2.2" fill="currentColor"/>
</svg>''',

    "org.gnome.Settings-accessibility-typing-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <rect x="2" y="3.5" width="12" height="9" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <rect x="4" y="5.5" width="1.5" height="1.5" rx="0.3" fill="currentColor"/>
  <rect x="7.2" y="5.5" width="1.5" height="1.5" rx="0.3" fill="currentColor"/>
  <rect x="10.5" y="5.5" width="1.5" height="1.5" rx="0.3" fill="currentColor"/>
  <rect x="5.5" y="8.5" width="5" height="1.5" rx="0.3" fill="currentColor"/>
</svg>''',

    "org.gnome.Settings-accessibility-zoom-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <circle cx="6.5" cy="6.5" r="4.5" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <line x1="10" y1="10" x2="14" y2="14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="4.5" y1="6.5" x2="8.5" y2="6.5" stroke="currentColor" stroke-width="1.2"/>
  <line x1="6.5" y1="4.5" x2="6.5" y2="8.5" stroke="currentColor" stroke-width="1.2"/>
</svg>''',

    "org.gnome.Settings-appearance-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" fill-rule="evenodd" d="M 8 1 C 4.1 1 1 4.1 1 8 C 1 11.9 4.1 15 8 15 C 9.5 15 10.5 14 10.5 12.8 C 10.5 12.2 10.3 11.7 9.9 11.3 C 9.5 10.9 9.3 10.5 9.3 10 C 9.3 9.1 10.1 8.3 11 8.3 L 12.5 8.3 C 14 8.3 15 7.1 15 5.7 C 15 3.1 11.9 1 8 1 Z M 4 7 C 3.4 7 3 6.6 3 6 C 3 5.4 3.4 5 4 5 C 4.6 5 5 5.4 5 6 C 5 6.6 4.6 7 4 7 Z M 7 4.5 C 6.4 4.5 6 4.1 6 3.5 C 6 2.9 6.4 2.5 7 2.5 C 7.6 2.5 8 2.9 8 3.5 C 8 4.1 7.6 4.5 7 4.5 Z M 10.5 4.5 C 9.9 4.5 9.5 4.1 9.5 3.5 C 9.5 2.9 9.9 2.5 10.5 2.5 C 11.1 2.5 11.5 2.9 11.5 3.5 C 11.5 4.1 11.1 4.5 10.5 4.5 Z"/>
</svg>''',

    "org.gnome.Settings-applications-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <rect x="2" y="2" width="3" height="3" rx="0.6" fill="currentColor"/>
  <rect x="6.5" y="2" width="3" height="3" rx="0.6" fill="currentColor"/>
  <rect x="11" y="2" width="3" height="3" rx="0.6" fill="currentColor"/>
  <rect x="2" y="6.5" width="3" height="3" rx="0.6" fill="currentColor"/>
  <rect x="6.5" y="6.5" width="3" height="3" rx="0.6" fill="currentColor"/>
  <rect x="11" y="6.5" width="3" height="3" rx="0.6" fill="currentColor"/>
  <rect x="2" y="11" width="3" height="3" rx="0.6" fill="currentColor"/>
  <rect x="6.5" y="11" width="3" height="3" rx="0.6" fill="currentColor"/>
  <rect x="11" y="11" width="3" height="3" rx="0.6" fill="currentColor"/>
</svg>''',

    "org.gnome.Settings-bluetooth-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" d="M 4.5 4.5 L 11 10 L 8 13.5 L 8 2.5 L 11 6 L 4.5 11.5"/>
</svg>''',

    "org.gnome.Settings-camera-access-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" fill-rule="evenodd" d="M 5.5 2.5 L 6.5 3.5 L 9.5 3.5 L 10.5 2.5 Z M 2 4.5 C 1.45 4.5 1 4.95 1 5.5 L 1 12 C 1 12.55 1.45 13 2 13 L 14 13 C 14.55 13 15 12.55 15 12 L 15 5.5 C 15 4.95 14.55 4.5 14 4.5 Z M 8 6.5 C 9.4 6.5 10.5 7.6 10.5 9 C 10.5 10.4 9.4 11.5 8 11.5 C 6.6 11.5 5.5 10.4 5.5 9 C 5.5 7.6 6.6 6.5 8 6.5 Z"/>
</svg>''',

    "org.gnome.Settings-color-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <path d="M 8 2 A 6 6 0 0 1 14 8 L 8 8 Z" fill="currentColor"/>
</svg>''',

    "org.gnome.Settings-desktop-sharing-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <circle cx="12" cy="4" r="2" fill="currentColor"/>
  <circle cx="4" cy="8" r="2" fill="currentColor"/>
  <circle cx="12" cy="12" r="2" fill="currentColor"/>
  <line x1="5.6" y1="7.2" x2="10.4" y2="4.8" stroke="currentColor" stroke-width="1.3"/>
  <line x1="5.6" y1="8.8" x2="10.4" y2="11.2" stroke="currentColor" stroke-width="1.3"/>
</svg>''',

    "org.gnome.Settings-device-diagnostics-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" d="M 1 9 L 4 9 L 6 3 L 8 13 L 10 7 L 12 9 L 15 9"/>
</svg>''',

    "org.gnome.Settings-device-security-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="none" stroke="currentColor" stroke-width="1.3" d="M 8 2 L 14 4.5 L 14 8 C 14 11.5 11 13.8 8 15 C 5 13.8 2 11.5 2 8 L 2 4.5 Z"/>
  <polyline points="5.5,8 7.5,10.5 11,5.5" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
</svg>''',

    "org.gnome.Settings-display-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <rect x="1.5" y="2.5" width="13" height="9" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <line x1="8" y1="11.5" x2="8" y2="14" stroke="currentColor" stroke-width="1.4"/>
  <line x1="5" y1="14" x2="11" y2="14" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
</svg>''',

    "org.gnome.Settings-keyboard-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <rect x="1.5" y="3.5" width="13" height="9" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <rect x="3.5" y="5.5" width="1.5" height="1.5" rx="0.3" fill="currentColor"/>
  <rect x="6.2" y="5.5" width="1.5" height="1.5" rx="0.3" fill="currentColor"/>
  <rect x="9" y="5.5" width="1.5" height="1.5" rx="0.3" fill="currentColor"/>
  <rect x="11.5" y="5.5" width="1.5" height="1.5" rx="0.3" fill="currentColor"/>
  <rect x="4.5" y="8.5" width="7" height="1.5" rx="0.3" fill="currentColor"/>
</svg>''',

    "org.gnome.Settings-location-access-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" fill-rule="evenodd" d="M 8 1.5 C 5.5 1.5 3.5 3.5 3.5 6 C 3.5 9.5 8 14.5 8 14.5 C 8 14.5 12.5 9.5 12.5 6 C 12.5 3.5 10.5 1.5 8 1.5 Z M 8 4.3 C 8.9 4.3 9.7 5.1 9.7 6 C 9.7 6.9 8.9 7.7 8 7.7 C 7.1 7.7 6.3 6.9 6.3 6 C 6.3 5.1 7.1 4.3 8 4.3 Z"/>
</svg>''',

    "org.gnome.Settings-microphone-access-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <rect x="6" y="2" width="4" height="7" rx="2" fill="currentColor"/>
  <path fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" d="M 3.5 6.5 C 3.5 9 5.5 11 8 11 C 10.5 11 12.5 9 12.5 6.5"/>
  <line x1="8" y1="11" x2="8" y2="14" stroke="currentColor" stroke-width="1.4"/>
  <line x1="5.5" y1="14" x2="10.5" y2="14" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
</svg>''',

    "org.gnome.Settings-mobile-network-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <rect x="1.5" y="11.5" width="2" height="3" rx="0.4" fill="currentColor"/>
  <rect x="5" y="8.5" width="2" height="6" rx="0.4" fill="currentColor"/>
  <rect x="8.5" y="5.5" width="2" height="9" rx="0.4" fill="currentColor"/>
  <rect x="12" y="2.5" width="2" height="12" rx="0.4" fill="currentColor"/>
</svg>''',

    "org.gnome.Settings-mouse-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <rect x="4" y="2" width="8" height="12" rx="4" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <line x1="8" y1="2" x2="8" y2="6.5" stroke="currentColor" stroke-width="1.3"/>
</svg>''',

    "org.gnome.Settings-multitasking-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <rect x="1.5" y="2.5" width="5.5" height="11" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <rect x="9" y="2.5" width="5.5" height="11" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
</svg>''',

    "org.gnome.Settings-network-proxy-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <rect x="6" y="6" width="4" height="4" rx="1" fill="currentColor"/>
</svg>''',

    "org.gnome.Settings-network-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <rect x="2" y="3" width="12" height="7" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <line x1="8" y1="10" x2="8" y2="12.5" stroke="currentColor" stroke-width="1.3"/>
  <line x1="4" y1="12.5" x2="12" y2="12.5" stroke="currentColor" stroke-width="1.3"/>
  <line x1="4" y1="12.5" x2="4" y2="14" stroke="currentColor" stroke-width="1.3"/>
  <line x1="12" y1="12.5" x2="12" y2="14" stroke="currentColor" stroke-width="1.3"/>
</svg>''',

    "org.gnome.Settings-notifications-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" fill-rule="evenodd" d="M 8 1.5 C 8.6 1.5 9 1.9 9 2.5 L 9 3 C 11.2 3.6 12.5 5.5 12.5 8 L 13.5 11 L 2.5 11 L 3.5 8 C 3.5 5.5 4.8 3.6 7 3 L 7 2.5 C 7 1.9 7.4 1.5 8 1.5 Z M 6.5 12 C 6.5 12.8 7.2 13.5 8 13.5 C 8.8 13.5 9.5 12.8 9.5 12 Z"/>
</svg>''',

    "org.gnome.Settings-online-accounts-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" fill-rule="evenodd" d="M 8 2 C 5.5 2 3.5 4 3.5 6.5 C 3.5 8 4.2 9.4 5.3 10.2 C 2.8 11.2 1 13.4 1 16 L 15 16 C 15 13.4 13.2 11.2 10.7 10.2 C 11.8 9.4 12.5 8 12.5 6.5 C 12.5 4 10.5 2 8 2 Z"/>
</svg>''',

    "org.gnome.Settings-power-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <rect x="2" y="5" width="11" height="6.5" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <rect x="3.5" y="6.5" width="5.5" height="3.5" rx="0.5" fill="currentColor"/>
  <path d="M 13.5 7 L 14.5 7 C 14.8 7 15 7.4 15 8 C 15 8.6 14.8 9 14.5 9 L 13.5 9 Z" fill="currentColor"/>
</svg>''',

    "org.gnome.Settings-printers-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" d="M 4 2 L 12 2 L 12 4 L 4 4 Z M 2 5 L 14 5 C 14.6 5 15 5.4 15 6 L 15 11 C 15 11.6 14.6 12 14 12 L 12 12 L 12 9 L 4 9 L 4 12 L 2 12 C 1.4 12 1 11.6 1 11 L 1 6 C 1 5.4 1.4 5 2 5 Z M 4 10.5 L 12 10.5 L 12 14 L 4 14 Z"/>
</svg>''',

    "org.gnome.Settings-privacy-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <rect x="3" y="6.5" width="10" height="7.5" rx="1.5" fill="currentColor"/>
  <path fill="none" stroke="currentColor" stroke-width="1.5" d="M 5 6.5 L 5 4.5 C 5 2.8 6.3 1.5 8 1.5 C 9.7 1.5 11 2.8 11 4.5 L 11 6.5"/>
</svg>''',

    "org.gnome.Settings-region-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <line x1="2" y1="8" x2="14" y2="8" stroke="currentColor" stroke-width="1.2"/>
  <path d="M 8 2 C 5.5 4 4.5 6 4.5 8 C 4.5 10 5.5 12 8 14 C 10.5 12 11.5 10 11.5 8 C 11.5 6 10.5 4 8 2 Z" fill="none" stroke="currentColor" stroke-width="1.2"/>
</svg>''',

    "org.gnome.Settings-remote-desktop-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <rect x="1.5" y="2.5" width="13" height="9" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <polyline points="4,6 7,8 4,10" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
  <line x1="8" y1="10" x2="11" y2="10" stroke="currentColor" stroke-width="1.3"/>
</svg>''',

    "org.gnome.Settings-screen-lock-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <rect x="2" y="2.5" width="12" height="9" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <circle cx="8" cy="6.5" r="1.5" fill="currentColor"/>
  <rect x="6.5" y="8" width="3" height="3" rx="0.5" fill="currentColor"/>
</svg>''',

    "org.gnome.Settings-screen-time-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <polyline points="8,4.5 8,8 10.5,9.5" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
</svg>''',

    "org.gnome.Settings-search-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <circle cx="6.5" cy="6.5" r="4.5" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <line x1="10" y1="10" x2="14" y2="14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
</svg>''',

    "org.gnome.Settings-secure-shell-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <rect x="1.5" y="2.5" width="13" height="11" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <polyline points="4,6 7,8 4,10" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
  <line x1="8" y1="10" x2="11" y2="10" stroke="currentColor" stroke-width="1.3"/>
</svg>''',

    "org.gnome.Settings-sharing-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <circle cx="12" cy="4" r="2" fill="currentColor"/>
  <circle cx="4" cy="8" r="2" fill="currentColor"/>
  <circle cx="12" cy="12" r="2" fill="currentColor"/>
  <line x1="5.6" y1="7.2" x2="10.4" y2="4.8" stroke="currentColor" stroke-width="1.3"/>
  <line x1="5.6" y1="8.8" x2="10.4" y2="11.2" stroke="currentColor" stroke-width="1.3"/>
</svg>''',

    "org.gnome.Settings-sound-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" d="M 2 5 L 5 5 L 9 2 L 9 14 L 5 11 L 2 11 Z"/>
  <path fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" d="M 11 5.5 C 12 6.5 12.5 7.5 12.5 8 C 12.5 8.5 12 9.5 11 10.5 M 13 3.5 C 14.8 5 15.2 6.5 15.2 8 C 15.2 9.5 14.8 11 13 12.5"/>
</svg>''',

    "org.gnome.Settings-system-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <rect x="3.5" y="3.5" width="9" height="9" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <rect x="5.5" y="5.5" width="5" height="5" rx="0.8" fill="currentColor"/>
  <line x1="5.5" y1="1" x2="5.5" y2="3.5" stroke="currentColor" stroke-width="1.2"/>
  <line x1="10.5" y1="1" x2="10.5" y2="3.5" stroke="currentColor" stroke-width="1.2"/>
  <line x1="5.5" y1="12.5" x2="5.5" y2="15" stroke="currentColor" stroke-width="1.2"/>
  <line x1="10.5" y1="12.5" x2="10.5" y2="15" stroke="currentColor" stroke-width="1.2"/>
</svg>''',

    "org.gnome.Settings-thunderbolt-access-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <polygon points="9,1 4,9 8,9 7,15 12,7 8,7" fill="currentColor"/>
</svg>''',

    "org.gnome.Settings-time-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <polyline points="8,4.5 8,8 10.5,9.5" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
</svg>''',

    "org.gnome.Settings-trash-file-history-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" d="M 3 4 L 13 4 L 11.5 14 L 4.5 14 Z M 5 2 L 11 2 L 12 3 L 4 3 Z"/>
</svg>''',

    "org.gnome.Settings-users-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <circle cx="6" cy="5" r="2.2" fill="currentColor"/>
  <path d="M 1.5 13.5 C 1.5 11 3.5 9.5 6 9.5 C 8.5 9.5 10.5 11 10.5 13.5 Z" fill="currentColor"/>
  <circle cx="11.5" cy="5.5" r="1.8" fill="currentColor" opacity="0.7"/>
  <path d="M 9.5 13.5 C 9.5 11.5 10.8 10.2 12.5 10.2 C 13.8 10.2 14.8 11.2 14.8 13.5 Z" fill="currentColor" opacity="0.7"/>
</svg>''',

    "org.gnome.Settings-wacom-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <line x1="3" y1="13" x2="12" y2="4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
  <polygon points="2,14 4,14 2,12" fill="currentColor"/>
</svg>''',

    "org.gnome.Settings-wellbeing-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" d="M 8 14 C 8 14 2 10 2 6 C 2 3.8 3.8 2 6 2 C 7.2 2 8 2.8 8 2.8 C 8 2.8 8.8 2 10 2 C 12.2 2 14 3.8 14 6 C 14 10 8 14 8 14 Z"/>
</svg>''',

    # ---------------------------------------------------------------------
    # Common UI Navigation & Headerbar Controls
    # ---------------------------------------------------------------------
    "edit-find-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <circle cx="6.5" cy="6.5" r="4.5" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <line x1="10" y1="10" x2="14" y2="14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
</svg>''',

    "open-menu-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <line x1="2.5" y1="4" x2="13.5" y2="4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="2.5" y1="8" x2="13.5" y2="8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="2.5" y1="12" x2="13.5" y2="12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
</svg>''',

    "view-more-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <circle cx="3" cy="8" r="1.3" fill="currentColor"/>
  <circle cx="8" cy="8" r="1.3" fill="currentColor"/>
  <circle cx="13" cy="8" r="1.3" fill="currentColor"/>
</svg>''',

    "view-refresh-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" d="M 13.5 8 C 13.5 11 11 13.5 8 13.5 C 5 13.5 2.5 11 2.5 8 C 2.5 5 5 2.5 8 2.5 C 10.2 2.5 12.1 3.8 13 5.7"/>
  <polyline points="13.5,2.5 13.5,6 10,6" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
</svg>''',

    "go-previous-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <polyline points="10,3 5,8 10,13" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
</svg>''',

    "go-next-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <polyline points="6,3 11,8 6,13" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
</svg>''',

    "pan-down-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <polygon points="4,6 12,6 8,10.5" fill="currentColor"/>
</svg>''',

    "pan-up-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <polygon points="4,10 12,10 8,5.5" fill="currentColor"/>
</svg>''',

    "pan-start-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <polygon points="10,4 10,12 5.5,8" fill="currentColor"/>
</svg>''',

    "pan-end-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <polygon points="6,4 6,12 10.5,8" fill="currentColor"/>
</svg>''',

    "window-close-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <line x1="3.5" y1="3.5" x2="12.5" y2="12.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
  <line x1="12.5" y1="3.5" x2="3.5" y2="12.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
</svg>''',

    "window-minimize-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <line x1="3" y1="8" x2="13" y2="8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
</svg>''',

    "window-maximize-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <rect x="2.5" y="2.5" width="11" height="11" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.5"/>
</svg>''',

    "window-restore-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <rect x="4.5" y="4.5" width="9" height="9" rx="1" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <path d="M 6.5 2.5 L 11.5 2.5 C 12.6 2.5 13.5 3.4 13.5 4.5 L 13.5 9.5" fill="none" stroke="currentColor" stroke-width="1.3"/>
</svg>''',

    # ---------------------------------------------------------------------
    # Carousel & Pagination Arrows (Fixes App Folder Navigation in GNOME Shell)
    # ---------------------------------------------------------------------
    "carousel-arrow-previous-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <polyline points="10,3 5,8 10,13" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
</svg>''',

    "carousel-arrow-next-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <polyline points="6,3 11,8 6,13" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
</svg>''',

    "arrow-left-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <polyline points="9.5,3.5 5,8 9.5,12.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
</svg>''',

    "arrow-right-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <polyline points="6.5,3.5 11,8 6.5,12.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
</svg>''',

    "arrow-up-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <polyline points="3.5,9.5 8,5 12.5,9.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
</svg>''',

    "arrow-down-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <polyline points="3.5,6.5 8,11 12.5,6.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
</svg>''',

    "go-up-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <polyline points="3.5,9.5 8,5 12.5,9.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
</svg>''',

    "go-down-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <polyline points="3.5,6.5 8,11 12.5,6.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
</svg>''',

    "go-first-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <line x1="3" y1="3" x2="3" y2="13" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
  <polyline points="12,3 7,8 12,13" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
</svg>''',

    "go-last-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <line x1="13" y1="3" x2="13" y2="13" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
  <polyline points="4,3 9,8 4,13" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
</svg>''',

    # ---------------------------------------------------------------------
    # CCTV, Surveillance & Camera Symbolic Icons
    # ---------------------------------------------------------------------
    "camera-on-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" fill-rule="evenodd" d="M 2 4 C 1.45 4 1 4.45 1 5 L 1 11 C 1 11.55 1.45 12 2 12 L 9.5 12 C 10.05 12 10.5 11.55 10.5 11 L 10.5 9.5 L 14.2 11.7 C 14.6 11.9 15 11.7 15 11.2 L 15 4.8 C 15 4.3 14.6 4.1 14.2 4.3 L 10.5 6.5 L 10.5 5 C 10.5 4.45 10.05 4 9.5 4 Z M 5.5 6.5 C 6.3 6.5 7 7.2 7 8 C 7 8.8 6.3 9.5 5.5 9.5 C 4.7 9.5 4 8.8 4 8 C 4 7.2 4.7 6.5 5.5 6.5 Z"/>
</svg>''',

    "camera-off-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" fill-rule="evenodd" d="M 2 4 C 1.45 4 1 4.45 1 5 L 1 11 C 1 11.55 1.45 12 2 12 L 9.5 12 C 10.05 12 10.5 11.55 10.5 11 L 10.5 9.5 L 14.2 11.7 C 14.6 11.9 15 11.7 15 11.2 L 15 4.8 C 15 4.3 14.6 4.1 14.2 4.3 L 10.5 6.5 L 10.5 5 C 10.5 4.45 10.05 4 9.5 4 Z M 5.5 6.5 C 6.3 6.5 7 7.2 7 8 C 7 8.8 6.3 9.5 5.5 9.5 C 4.7 9.5 4 8.8 4 8 C 4 7.2 4.7 6.5 5.5 6.5 Z"/>
  <line x1="2" y1="2" x2="14" y2="14" stroke="#E5737F" stroke-width="1.6" stroke-linecap="round"/>
</svg>''',

    "camera-web-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <circle cx="8" cy="7" r="5" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <circle cx="8" cy="7" r="2.2" fill="currentColor"/>
  <line x1="8" y1="12" x2="8" y2="14.5" stroke="currentColor" stroke-width="1.4"/>
  <line x1="4.5" y1="14.5" x2="11.5" y2="14.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
</svg>''',

    "camera-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" fill-rule="evenodd" d="M 5.5 2 L 6.5 3 L 9.5 3 L 10.5 2 Z M 2 4 C 1.45 4 1 4.45 1 5 L 1 12 C 1 12.55 1.45 13 2 13 L 14 13 C 14.55 13 15 12.55 15 12 L 15 5 C 15 4.45 14.55 4 14 4 Z M 8 6 C 9.66 6 11 7.34 11 9 C 11 10.66 9.66 12 8 12 C 6.34 12 5 10.66 5 9 C 5 7.34 6.34 6 8 6 Z"/>
</svg>''',

    "cctv-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <rect x="2" y="2" width="2" height="7" rx="0.5" fill="currentColor"/>
  <line x1="3" y1="5.5" x2="6.5" y2="5.5" stroke="currentColor" stroke-width="1.4"/>
  <path d="M 6.5 3.5 L 14 6 L 14 9 L 6.5 9 Z" fill="currentColor"/>
  <circle cx="13" cy="7.5" r="1" fill="#122329"/>
  <polyline points="7,9 7,12 10,12" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
</svg>''',

    "security-camera-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <rect x="2" y="2" width="2" height="7" rx="0.5" fill="currentColor"/>
  <line x1="3" y1="5.5" x2="6.5" y2="5.5" stroke="currentColor" stroke-width="1.4"/>
  <path d="M 6.5 3.5 L 14 6 L 14 9 L 6.5 9 Z" fill="currentColor"/>
  <circle cx="13" cy="7.5" r="1" fill="#122329"/>
</svg>''',
}
