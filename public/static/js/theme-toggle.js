/**
 * Theme Toggle - IshikawaUta Portfolio
 * ==========================================================================
 * Handles light/dark mode switching with:
 * - localStorage persistence (key: 'uta-color-mode')
 * - System preference detection (prefers-color-scheme)
 * - View Transitions API circular clip-path animation
 * - MutationObserver callback for tech icon refresh
 *
 * Usage: Automatically initializes on script load.
 *        Toggle button must have id="theme-toggle".
 * ==========================================================================
 */
(function() {
  'use strict';

  // localStorage key for persisting theme preference
  var STORAGE_KEY = 'uta-color-mode';

  // ---------------------------------------------------------------------------
  // Theme detection helpers
  // ---------------------------------------------------------------------------

  /** Get stored theme from localStorage (returns null if not set) */
  function getStoredMode() {
    try {
      return localStorage.getItem(STORAGE_KEY);
    } catch (e) {
      return null;
    }
  }

  /** Detect system color scheme preference */
  function getSystemMode() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  /** Get effective theme: stored preference > system preference */
  function getMode() {
    return getStoredMode() || getSystemMode();
  }

  // ---------------------------------------------------------------------------
  // Theme application
  // ---------------------------------------------------------------------------

  /** Apply theme by setting class on <html> and persisting to localStorage */
  function setMode(mode) {
    document.documentElement.classList.remove('light', 'dark');
    document.documentElement.classList.add(mode);
    try {
      localStorage.setItem(STORAGE_KEY, mode);
    } catch (e) {}
  }

  /** Check if current theme is dark */
  function isDark() {
    return document.documentElement.classList.contains('dark');
  }

  // Initialize theme on page load (before first paint to avoid flash)
  setMode(getMode());

  // ---------------------------------------------------------------------------
  // Toggle button click handler
  // ---------------------------------------------------------------------------

  var btn = document.getElementById('theme-toggle');
  if (!btn) return;

  btn.addEventListener('click', function(event) {
    var wasDark = isDark();
    var newMode = wasDark ? 'light' : 'dark';

    // Check if View Transitions API is supported and user hasn't reduced motion
    var isAppearanceTransition = document.startViewTransition
      && !window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // Fallback: no animation, just switch theme immediately
    if (!isAppearanceTransition) {
      setMode(newMode);
      // Notify tech-circles.js to refresh icon themes (light/dark)
      if (window.refreshTechIcons) window.refreshTechIcons();
      return;
    }

    // Calculate circular clip-path radius from click position to farthest corner
    var x = event.clientX;
    var y = event.clientY;
    var endRadius = Math.hypot(
      Math.max(x, window.innerWidth - x),
      Math.max(y, window.innerHeight - y)
    );

    // Start View Transition (updates DOM, then we animate the pseudo-element)
    var transition = document.startViewTransition(function() {
      setMode(newMode);
    });

    transition.ready.then(function() {
      // Clip-path direction depends on transition direction:
      // - Light->Dark: expand circle from click point (old theme revealed underneath)
      // - Dark->Light: contract circle to click point (new theme revealed)
      var isDarkAfter = !wasDark;
      var clipPath = [
        'circle(0px at ' + x + 'px ' + y + 'px)',
        'circle(' + endRadius + 'px at ' + x + 'px ' + y + 'px)'
      ];

      document.documentElement.animate(
        { clipPath: isDarkAfter ? clipPath.slice().reverse() : clipPath },
        {
          duration: 400,
          easing: 'ease-in',
          fill: 'both',
          pseudoElement: isDarkAfter
            ? '::view-transition-old(root)'   // Animate old theme out
            : '::view-transition-new(root)'   // Animate new theme in
        }
      );
    }).then(function() {
      // After transition: refresh tech icons to match new theme
      if (window.refreshTechIcons) window.refreshTechIcons();
    });
  });

  // ---------------------------------------------------------------------------
  // System preference listener
  // Updates theme when OS preference changes (only if user hasn't manually set one)
  // ---------------------------------------------------------------------------
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
    if (!getStoredMode()) {
      setMode(e.matches ? 'dark' : 'light');
      if (window.refreshTechIcons) window.refreshTechIcons();
    }
  });
})();
