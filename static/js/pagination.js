/**
 * Project Pagination - IshikawaUta Portfolio
 * ==========================================================================
 * Client-side pagination for Project Experience section.
 * Reads project data from window.__projectsData (set by index.html inline script).
 *
 * Features:
 * - Arrow navigation (prev/next)
 * - Dot indicators
 * - Keyboard support (ArrowLeft, ArrowRight)
 * - Smooth fade transition between pages
 * - Responsive: hides on mobile if <= 1 project
 *
 * Global API:
 * - window.initProjectPagination() - manual re-initialization
 * ==========================================================================
 */
(function() {
  'use strict';

  var currentPage = 0;
  var projects = [];
  var container = null;

  // ---------------------------------------------------------------------------
  // DOM helpers
  // ---------------------------------------------------------------------------

  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function(k) {
        if (k === 'className') node.className = attrs[k];
        else if (k === 'innerHTML') node.innerHTML = attrs[k];
        else if (k.indexOf('on') === 0) node.addEventListener(k.slice(2).toLowerCase(), attrs[k]);
        else node.setAttribute(k, attrs[k]);
      });
    }
    if (children) {
      children.forEach(function(c) { if (c) node.appendChild(c); });
    }
    return node;
  }

  // ---------------------------------------------------------------------------
  // Render
  // ---------------------------------------------------------------------------

  function renderNav() {
    if (!container) return;
    var existing = container.querySelector('.pagination-nav');
    if (existing) existing.remove();
    if (projects.length <= 1) return;

    var nav = el('div', { className: 'pagination-nav mt-3 flex items-center justify-between' });

    // Prev button
    var prevBtn = el('button', {
      className: 'pagination-btn flex items-center gap-1 text-xs text-muted-foreground transition-colors hover:text-foreground disabled:opacity-30 disabled:cursor-not-allowed',
      'aria-label': 'Previous project',
      onClick: function() { goTo(currentPage - 1); }
    }, [
      document.createTextNode('\u2190 Prev')
    ]);

    // Dots
    var dots = el('div', { className: 'flex items-center gap-1.5' });
    for (var i = 0; i < projects.length; i++) {
      (function(idx) {
        var dot = el('button', {
          className: 'pagination-dot size-1.5 rounded-full transition-all ' + (idx === 0 ? 'bg-foreground' : 'bg-muted-foreground/40 hover:bg-muted-foreground/70'),
          'aria-label': 'Go to project ' + (idx + 1),
          onClick: function() { goTo(idx); }
        });
        dots.appendChild(dot);
      })(i);
    }

    // Next button
    var nextBtn = el('button', {
      className: 'pagination-btn flex items-center gap-1 text-xs text-muted-foreground transition-colors hover:text-foreground disabled:opacity-30 disabled:cursor-not-allowed',
      'aria-label': 'Next project',
      onClick: function() { goTo(currentPage + 1); }
    }, [
      document.createTextNode('Next \u2192')
    ]);

    nav.appendChild(prevBtn);
    nav.appendChild(dots);
    nav.appendChild(nextBtn);
    container.appendChild(nav);

    updateNavState();
  }

  function updateNavState() {
    if (!container) return;
    var nav = container.querySelector('.pagination-nav');
    if (!nav) return;

    var btns = nav.querySelectorAll('.pagination-btn');
    var prevBtn = btns[0];
    var nextBtn = btns[1];
    var dots = nav.querySelectorAll('.pagination-dot');

    if (prevBtn) prevBtn.disabled = currentPage === 0;
    if (nextBtn) nextBtn.disabled = currentPage === projects.length - 1;

    dots.forEach(function(dot, i) {
      if (i === currentPage) {
        dot.className = 'pagination-dot size-1.5 rounded-full transition-all bg-foreground';
      } else {
        dot.className = 'pagination-dot size-1.5 rounded-full transition-all bg-muted-foreground/40 hover:bg-muted-foreground/70';
      }
    });
  }

  function goTo(index) {
    if (index < 0 || index >= projects.length || index === currentPage) return;

    var pages = container.querySelectorAll('.project-page');
    if (pages[currentPage]) {
      pages[currentPage].style.opacity = '0';
      pages[currentPage].style.transform = 'translateY(4px)';
    }

    currentPage = index;

    setTimeout(function() {
      pages.forEach(function(p, i) {
        p.style.display = i === currentPage ? 'block' : 'none';
      });
      if (pages[currentPage]) {
        pages[currentPage].style.opacity = '1';
        pages[currentPage].style.transform = 'translateY(0)';
      }
      updateNavState();
    }, 150);
  }

  // ---------------------------------------------------------------------------
  // Keyboard navigation
  // ---------------------------------------------------------------------------

  function handleKeydown(e) {
    if (projects.length <= 1) return;
    if (e.key === 'ArrowLeft') goTo(currentPage - 1);
    else if (e.key === 'ArrowRight') goTo(currentPage + 1);
  }

  // ---------------------------------------------------------------------------
  // Initialization
  // ---------------------------------------------------------------------------

  function initProjectPagination() {
    container = document.getElementById('project-pagination');
    if (!container || !window.__projectsData || window.__projectsData.length === 0) return;

    projects = window.__projectsData;
    currentPage = 0;

    // Build project pages
    projects.forEach(function(project, idx) {
      var page = document.createElement('div');
      page.className = 'project-page';
      page.style.transition = 'opacity 150ms ease, transform 150ms ease';
      page.style.display = idx === 0 ? 'block' : 'none';
      page.style.opacity = idx === 0 ? '1' : '0';

      var html = '<h3 class="mb-2 text-lg font-bold text-foreground">' + project.title + '</h3>';

      // Badges
      html += '<div class="mb-3 flex flex-wrap gap-2">';
      project.badges.forEach(function(badge) {
        if (badge.href) {
          html += '<a href="' + badge.href + '" target="_blank" rel="noopener noreferrer" class="inline-block">';
          html += '<img src="' + badge.img + '" alt="' + badge.alt + '" class="h-5">';
          html += '</a>';
        } else {
          html += '<span class="inline-block">';
          html += '<img src="' + badge.img + '" alt="' + badge.alt + '" class="h-5">';
          html += '</span>';
        }
      });
      html += '</div>';

      // Description
      html += '<div class="prose">' + project.description + '</div>';

      // Links
      html += '<div class="mt-3 flex items-center gap-3">';
      if (project.github) {
        html += '<a href="' + project.github + '" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1 text-xs text-muted-foreground transition-colors hover:text-foreground">';
        html += 'View on GitHub';
        html += '<svg class="size-3" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M5 5h14v14h-2V8.41L6.41 19 5 17.59 15.59 7H5V5Z"></path></svg>';
        html += '</a>';
      }
      if (project.demo) {
        html += '<a href="' + project.demo + '" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1 text-xs text-muted-foreground transition-colors hover:text-foreground">';
        html += 'Live Demo';
        html += '<svg class="size-3" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M5 5h14v14h-2V8.41L6.41 19 5 17.59 15.59 7H5V5Z"></path></svg>';
        html += '</a>';
      }
      html += '</div>';

      page.innerHTML = html;
      container.appendChild(page);
    });

    renderNav();
    document.addEventListener('keydown', handleKeydown);
  }

  // Expose global API
  window.initProjectPagination = initProjectPagination;

  // ---------------------------------------------------------------------------
  // Auto-initialize on DOM ready
  // ---------------------------------------------------------------------------

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initProjectPagination);
  } else {
    initProjectPagination();
  }
})();
