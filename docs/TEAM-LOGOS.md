# Live event team logos

`playlists/team-logos.json` maps normalized, complete team names to image URLs.
The apps use a drawn badge if a name is unknown or its image cannot load; the
catalog does not imply a feed is live. The soccer and basketball club entries
are existing curated Wikimedia links. NFL, NBA, WNBA, MLB and NHL full-name
entries were added from the ESPN default PNG entries in the
[SportsDataverse logo archive manifest](https://github.com/sportsdataverse/sdv-assets/blob/61258c3ac56679e1db5b1314565e807c59db3f7e/manifest/marks.csv).
That project reports checking image content, not just HTTP status. Only full
names were imported, avoiding ambiguous abbreviations and historic identities;
no fuzzy matching is used. Logos remain third-party trademarks, and their URLs
may change or be blocked. This checkout cannot reach those image hosts, so their
current availability has not been verified here.

To extend coverage, identify the actual team and sport first, use a trustworthy
source's real crest URL, and add the exact normalized name (and only unambiguous
aliases). Do not derive arbitrary CDN URLs from names or reuse one sport's
crest for another team with the same name. Validate the image and its rights
before adding it. The catalog is bundled at app build time; a playlist refresh
alone does not add new logos.
