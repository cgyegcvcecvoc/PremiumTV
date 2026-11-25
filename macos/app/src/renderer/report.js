/**
 * A prefilled GitHub issue for a channel or server that will not play.
 *
 * PremiumTV has no report server and no account system, so a report is a
 * normal GitHub issue the viewer chooses to open: the app fills in what it
 * already knows (channel, feed number, stream URL, the player's message and the
 * app version) and the viewer presses Submit on GitHub. Nothing is sent until
 * they do, and the app never posts on its own.
 *
 * The same helper is used by the macOS app and the web player; Android builds
 * the same URL from ChannelReport.kt so every platform reports the same fields.
 */
(function (root) {
  'use strict';

  const ISSUE_URL = 'https://github.com/cgyegcvcecvoc/PremiumTV/issues/new';
  const MAX_BODY = 4200;
  const MAX_URL = 1200;

  function text(value, limit) {
    const cleaned = String(value == null ? '' : value)
      .replace(/\r\n?/g, '\n')
      // A pasted provider error can carry control characters; keep the report
      // readable and never let one break the issue form.
      .replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/g, '')
      .trim();
    return cleaned.length > limit ? cleaned.slice(0, Math.max(0, limit - 1)) + '…' : cleaned;
  }

  function serverPosition(index, count) {
    const number = Number(index);
    const total = Number(count);
    if (!Number.isFinite(number) || !Number.isFinite(total) || total < 1) return 'unknown';
    const current = Math.min(Math.max(0, Math.floor(number)), total - 1) + 1;
    return `${current} of ${total}`;
  }

  /**
   * Build the issue URL.
   *
   * `channel` and `url` are the only required fields; everything else is
   * optional so a caller with less context still produces a useful form.
   */
  function issueUrl(info) {
    const details = info && typeof info === 'object' ? info : {};
    const channel = text(details.channel || details.name, 90) || 'Unknown channel';
    const group = text(details.group, 60);
    const stream = text(details.url, MAX_URL);
    const error = text(details.error, 900);
    const version = text(details.appVersion, 90) || 'unknown build';
    const platform = text(details.platform, 220) || 'unknown platform';
    const server = serverPosition(details.serverIndex, details.serverCount);
    const title = `[Channel report] ${channel} — server ${server} will not play`;

    const lines = [
      '### Channel report',
      '',
      `**Channel:** ${channel}`,
      ...(group ? [`**Category:** ${group}`] : []),
      `**Server:** ${server}`,
      ...(stream ? [`**Stream:** ${stream}`] : []),
      '',
      '**What the player reported:**',
      '',
      '> ' + (error || 'The feed did not play.').replace(/\n/g, '\n> '),
      '',
      '**App:** ' + version,
      '**Platform:** ' + platform,
      '**Reported:** ' + new Date().toISOString(),
      '',
      '_Opened from PremiumTV. Please add anything else you saw, then press Submit._',
    ];

    let body = lines.join('\n');
    if (body.length > MAX_BODY) body = body.slice(0, MAX_BODY - 40) + '\n\n_Report shortened._';
    return `${ISSUE_URL}?title=${encodeURIComponent(title)}&body=${encodeURIComponent(body)}`;
  }

  const api = { ISSUE_URL, issueUrl, serverPosition };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  root.PremiumReport = api;
})(typeof window !== 'undefined' ? window : globalThis);
