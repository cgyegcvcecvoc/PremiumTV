'use strict';

/**
 * The picture a channel shows when it has no logo of its own.
 *
 * Before 1.0.5 a logo-less channel showed its category name inside an empty
 * box, which read as broken art. Now every logo-less channel gets a drawn
 * placeholder: the category decides the picture - a ball for Sports, a smile
 * for Comedy, a balloon for Kids - and the generic set is a television
 * outline, the app's own mark. Static SVG strings only; no remote data is
 * ever interpolated into them.
 */

window.PremiumIcons = (function () {
  /** Which placeholder picture a category gets. Pure so it can be unit tested. */
  function keyForGroup(group) {
    const key = String(group || '').toLowerCase();
    if (/sport|soccer|football|hockey|basketball|baseball|ufc|mma|boxing|wrestling|golf|tennis|formula 1|nascar|cricket|rugby/.test(key)) return 'ball';
    if (/comed/.test(key)) return 'smile';
    if (/weather/.test(key)) return 'weather';
    if (/news/.test(key)) return 'news';
    if (/kid|cartoon/.test(key)) return 'balloon';
    if (/music/.test(key)) return 'music';
    if (/movie/.test(key)) return 'movie';
    if (/documentar|education|culture/.test(key)) return 'book';
    if (/business/.test(key)) return 'chart';
    if (/religious/.test(key)) return 'cross';
    if (/legislative/.test(key)) return 'law';
    if (/lifestyle|relax|family/.test(key)) return 'heart';
    if (/series|celebrit|entertainment|game show|tv show|paranormal/.test(key)) return 'star';
    if (/international|global|online/.test(key)) return 'globe';
    return 'tv';
  }

  const PATHS = {
    tv: '<path d="M9 3.6 12 7l3-3.4M5 8h14a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2z"/>' +
      '<rect x="6.4" y="11" width="7.2" height="6" rx="0.6"/><path d="M17.2 11.6v4.8M8 20l-1.2 2.4M16 20l1.2 2.4"/>',
    ball: '<circle cx="12" cy="12" r="9"/><path d="M12 6.8 16.2 9.9 14.6 15H9.4L7.8 9.9z"/>' +
      '<path d="M12 3.1v3.7M20.6 9.4l-4.4.5M18.9 19.2l-4.3-4.2M5.1 19.2l4.3-4.2M3.4 9.4l4.4.5"/>',
    smile: '<circle cx="12" cy="12" r="9"/><path d="M8 14.2a5.4 5.4 0 0 0 8 0"/>' +
      '<circle cx="9" cy="9.5" r="1.1" fill="currentColor" stroke="none"/>' +
      '<circle cx="15" cy="9.5" r="1.1" fill="currentColor" stroke="none"/>',
    news: '<rect x="4" y="5" width="16" height="14" rx="1"/><path d="M7 9h10M7 12h10M7 15h6"/>',
    balloon: '<ellipse cx="12" cy="9.2" rx="4.4" ry="5.4"/><path d="M12 14.6v1.6M12 16.2c2.2 1.6-1.8 3 .4 5.2"/>',
    music: '<ellipse cx="8" cy="17.8" rx="2.4" ry="2.2"/><path d="M10.4 17.8V5.4L18.6 3.6v10"/>' +
      '<ellipse cx="16.2" cy="13.6" rx="2.4" ry="2.2"/>',
    movie: '<rect x="3" y="6" width="18" height="12" rx="1"/><path d="M7.2 6v12M16.8 6v12"/>' +
      '<path d="M10.4 9.4 14.2 12l-3.8 2.6z"/>',
    weather: '<circle cx="8.4" cy="8.4" r="2.8"/><path d="M8.4 2.4V4M2.8 8.4h1.4M12.6 8.4H14M4.4 4.4l1 1M12.4 4.4l-1 1"/>' +
      '<path d="M6.4 19.6h10.8a3 3 0 0 0-.6-5.8 4.4 4.4 0 0 0-7.4-.4 3.3 3.3 0 0 0-2.8 6.2z"/>',
    book: '<path d="M4 5c4-1.2 12-1.2 16 0v13.6c-4-1.2-12-1.2-16 0z"/><path d="M12 4.3v13.6"/>',
    chart: '<path d="M4 3.6v16.8H21"/><path d="M8 20.4v-6.8M12.4 20.4V8.8M16.8 20.4v-8.8"/>',
    star: '<path d="M12 3.4l2.7 5.8 6.2.7-4.6 4.3 1.3 6.2L12 17.2l-5.6 3.2 1.3-6.2-4.6-4.3 6.2-.7z"/>',
    heart: '<path d="M12 20.2C6.6 16 3.6 12.8 3.6 9.6A4.3 4.3 0 0 1 12 7.6a4.3 4.3 0 0 1 8.4 2c0 3.2-3 6.4-8.4 10.6z"/>',
    cross: '<path d="M10 3h4v6h6v4h-6v8h-4v-8H4V9h6z"/>',
    law: '<path d="M3 9l9-5.2L21 9M5.6 9v9M9.9 9v9M14.1 9v9M18.4 9v9M3 20.6h18"/>',
    globe: '<circle cx="12" cy="12" r="9"/><path d="M3.2 12h17.6"/>' +
      '<path d="M12 3.1c-3.4 3.5-3.4 14.3 0 17.8 3.4-3.5 3.4-14.3 0-17.8z"/>',
  };

  /** An inline SVG placeholder for a category. */
  function svgForGroup(group, className) {
    const key = keyForGroup(group);
    return `<svg class="${className || 'ph-icon'}" viewBox="0 0 24 24" aria-hidden="true" ` +
      'fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">' +
      `${PATHS[key] || PATHS.tv}</svg>`;
  }

  return { keyForGroup, svgForGroup };
})();
