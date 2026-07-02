/**
 * Tech Stack Orbiting Circles - IshikawaUta Portfolio
 * ==========================================================================
 * Creates animated orbiting tech icons using CSS animations.
 *
 * Architecture:
 * - Reads icon data from window.__techIcons (set by index.html inline script)
 * - Creates <div> elements with <img> inside, positioned absolutely
 * - Uses CSS @keyframes 'orbit' animation with custom properties:
 *   - --radius: orbit distance from center
 *   - --duration: animation speed in seconds
 * - Icons counter-rotate to stay upright while orbiting
 *
 * Features:
 * - Responsive: icons and circles scale down on mobile (< 640px)
 * - Theme-aware: detects dark/light mode for skillicons.dev API
 * - Auto-refresh: MutationObserver watches <html> class changes (theme toggle)
 * - Error handling: failed icon loads are hidden gracefully
 *
 * Global API:
 * - window.initTechCircles(innerIcons, outerIcons) - manual initialization
 * - window.refreshTechIcons() - refresh icons (called by theme-toggle.js)
 * ==========================================================================
 */
(function() {
  'use strict';

  // ---------------------------------------------------------------------------
  // Configuration
  // ---------------------------------------------------------------------------

  var INNER_RADIUS = 55;   // Inner orbit radius in pixels (base, scaled on mobile)
  var OUTER_RADIUS = 110;  // Outer orbit radius in pixels (base, scaled on mobile)
  var DURATION = 20;       // Orbit animation duration in seconds

  // ---------------------------------------------------------------------------
  // Theme detection for icon API
  // ---------------------------------------------------------------------------

  /** Detect current theme from <html> class list */
  function getIconTheme() {
    var cls = document.documentElement.className || '';
    if (cls.indexOf('dark') !== -1) return 'dark';
    return 'light';
  }

  /** Build skillicons.dev URL with theme parameter */
  function iconUrl(icon) {
    return 'https://skillicons.dev/icons?i=' + icon + '&theme=' + getIconTheme();
  }

  /** Check if viewport is mobile size */
  function isMobile() {
    return window.innerWidth < 640;
  }

  // ---------------------------------------------------------------------------
  // Icon creation
  // ---------------------------------------------------------------------------

  /**
   * Create orbiting icon elements inside a container.
   *
   * @param {string} containerId - DOM element ID ('inner-icons' or 'outer-icons')
   * @param {string[]} icons - Array of icon names (e.g., ['python', 'js'])
   * @param {number} radius - Orbit radius in pixels
   * @param {boolean} reverse - If true, orbit direction is reversed (outer ring)
   */
  function createIcons(containerId, icons, radius, reverse) {
    var container = document.getElementById(containerId);
    if (!container) return;
    container.innerHTML = '';  // Clear previous icons

    // Scale down icons and radius on mobile for better fit
    var scale = isMobile() ? 0.72 : 1;
    var actualRadius = radius * scale;
    // Outer icons are larger than inner icons
    var size = reverse ? (isMobile() ? 28 : 34) : 22;

    icons.forEach(function(icon, index) {
      // Create wrapper div (positioned absolutely, animated via CSS)
      var el = document.createElement('div');
      el.className = 'absolute z-10 flex items-center justify-center rounded-full border-none bg-transparent';
      el.style.width = size + 'px';
      el.style.height = size + 'px';
      // Center the element on the orbit path
      el.style.left = '50%';
      el.style.top = '50%';
      el.style.marginLeft = (-size / 2) + 'px';
      el.style.marginTop = (-size / 2) + 'px';

      // Set CSS custom properties for the orbit animation
      el.style.setProperty('--duration', DURATION);
      el.style.setProperty('--radius', actualRadius);

      // Apply orbit animation
      el.style.animationName = 'orbit';
      el.style.animationDuration = DURATION + 's';
      el.style.animationTimingFunction = 'linear';
      el.style.animationIterationCount = 'infinite';
      // Stagger each icon evenly around the orbit
      el.style.animationDelay = (-(index * DURATION) / icons.length) + 's';
      if (reverse) {
        el.style.animationDirection = 'reverse';
      }

      // Create icon image element
      var img = document.createElement('img');
      img.src = iconUrl(icon);
      img.alt = icon + ' icon';
      img.className = 'h-full w-full object-contain';
      img.loading = 'lazy';
      // Gracefully hide failed icon loads
      img.onerror = function() {
        img.style.display = 'none';
      };

      el.appendChild(img);
      container.appendChild(el);
    });
  }

  // ---------------------------------------------------------------------------
  // SVG circle radius updates
  // ---------------------------------------------------------------------------

  /**
   * Update SVG circle radii to match current viewport.
   * Called on resize and initial load to keep circles aligned with icons.
   */
  function updateCircles() {
    var scale = isMobile() ? 0.72 : 1;
    var innerCircle = document.getElementById('inner-circle');
    var outerCircle = document.getElementById('outer-circle');
    if (innerCircle) innerCircle.setAttribute('r', INNER_RADIUS * scale);
    if (outerCircle) outerCircle.setAttribute('r', OUTER_RADIUS * scale);
  }

  // ---------------------------------------------------------------------------
  // Initialization
  // ---------------------------------------------------------------------------

  /**
   * Initialize both inner and outer orbiting icon circles.
   * Called on page load and whenever theme changes.
   */
  function initTechCircles(innerIcons, outerIcons) {
    if (!innerIcons || !outerIcons) return;
    updateCircles();
    createIcons('inner-icons', innerIcons, INNER_RADIUS, false);
    createIcons('outer-icons', outerIcons, OUTER_RADIUS, true);
  }

  /**
   * Refresh icons using data from window.__techIcons.
   * Called by theme-toggle.js after theme change.
   */
  function refreshIcons() {
    if (window.__techIcons) {
      initTechCircles(window.__techIcons.inner, window.__techIcons.outer);
    }
  }

  // Expose global API for external calls
  window.initTechCircles = initTechCircles;
  window.refreshTechIcons = refreshIcons;

  // ---------------------------------------------------------------------------
  // Event listeners
  // ---------------------------------------------------------------------------

  // Re-create icons on window resize (responsive radius + icon size)
  window.addEventListener('resize', function() {
    updateCircles();
    refreshIcons();
  });

  // MutationObserver: watch <html> class changes for theme toggle
  // When dark/light class changes, refresh icons with new theme
  var observer = new MutationObserver(function() {
    refreshIcons();
  });
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });

  // ---------------------------------------------------------------------------
  // Initial load
  // ---------------------------------------------------------------------------

  // Wait for DOM to be ready, then create icons
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      refreshIcons();
    });
  } else {
    refreshIcons();
  }
})();
