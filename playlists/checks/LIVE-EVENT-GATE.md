# Live-event pre-publish gate

- **Playlist:** `/workspace/chats/68e1513c8cc010bb378725fd/playlists/PremiumTV.m3u`
- **Run:** 2026-11-27T20:29:17Z
- **Entries / fixtures:** 96 / 61
- **Working:** 79
- **Non-matchup event feeds:** 11 (9 working)
- **Dropped:** 17 (403: 0, 404/410: 9, other: 8)
- **Publishable fixtures:** 55
- **Refused fixtures (no working feed):** 6

## Refused fixtures

| Fixture | Sport | Entries |
|---|---|---:|
| Grazer AK vs. Altach | Soccer | 1 |
| Sweden vs. Hungary | Basketball World Cup | 1 |
| Al Ittihad vs. Neom SC | Soccer | 1 |
| Modo vs. Almtuna | Sweden HockeyAllsvenskan | 1 |
| Nybro vs. Mora | Sweden HockeyAllsvenskan | 1 |
| Kriens vs. Aarau | Soccer | 1 |

## Dropped fixture entries

| Fixture | Feed | Outcome | HTTP | Reason |
|---|---|---|---:|---|
| Grazer AK vs. Altach | [Austria Bundesliga] Grazer AK vs Altach (FAWA) | dropped_404 | 404 | HTTP 404 |
| Sweden vs. Hungary | [Basketball World Cup] Sweden vs Hungary (FAWA) | dropped_404 | 404 | HTTP 404 |
| Akron vs. Buffalo | [CFB] Akron vs Buffalo (iSTRMEAST) | dropped_404 | 404 | HTTP 404 |
| Iowa vs. Nebraska | [CFB] Iowa vs Nebraska (iSTRMEAST) | dropped_404 | 404 | HTTP 404 |
| Levante vs. Racing Santander | [football] Levante vs. Racing Santander 1 (SPRTSBITE) | dropped_other | 503 | HTTP 503 |
| Nottingham Forest vs. Chelsea | [Football] Nottingham Forest vs. Chelsea 3 (SPRTSBITE) | dropped_other | 503 | HTTP 503 |
| Denver Broncos vs. Pittsburgh Steelers | [NFL] Denver Broncos vs Pittsburgh Steelers (MP66) | dropped_other | 200 | html page, not a stream |
| Boston Bruins vs. Toronto Maple Leafs | [NHL] Boston Bruins vs Toronto Maple Leafs (iSTRMEAST) | dropped_404 | 200 | playlist only, HTTP 404 |
| Boston Bruins vs. Toronto Maple Leafs | [NHL] Toronto Maple Leafs vs Boston Bruins (MP66) | dropped_other | 200 | html page, not a stream |
| Calgary Flames vs. New Jersey Devils | [NHL] Calgary Flames vs New Jersey Devils (MP66) | dropped_other | 200 | html page, not a stream |
| Dallas Stars vs. St. Louis Blues | [NHL] Dallas Stars vs St. Louis Blues (MP66) | dropped_other | 200 | html page, not a stream |
| Al Ittihad vs. Neom SC | [Saudi Premier League] Al Ittihad vs Neom SC (FAWA) | dropped_404 | 404 | HTTP 404 |
| Modo vs. Almtuna | [Sweden HockeyAllsvenskan] Modo vs Almtuna (FAWA) | dropped_404 | 404 | HTTP 404 |
| Nybro vs. Mora | [Sweden HockeyAllsvenskan] Nybro vs Mora (FAWA) | dropped_404 | 404 | HTTP 404 |
| Kriens vs. Aarau | [Switzerland Challenge League] Kriens vs Aarau (FAWA) | dropped_404 | 404 | HTTP 404 |

## Non-matchup event feeds

| Feed | Outcome | HTTP | Reason |
|---|---|---:|---|
| [American Football] Denver Broncos at Pittsburgh Steelers 1 (SPRTSBITE) | working | 200 | hls, segment ok (65536 bytes) |
| [American Football] Denver Broncos at Pittsburgh Steelers 2 (SPRTSBITE) | working | 200 | hls, segment ok (65536 bytes) |
| [American Football] Denver Broncos at Pittsburgh Steelers 3 (SPRTSBITE) | working | 200 | hls, segment ok (65536 bytes) |
| [American Football] Florida Gators at Florida State Seminoles 2 (SPRTSBITE) | working | 200 | hls, segment ok (65536 bytes) |
| [American Football] Nebraska Cornhuskers at Iowa Hawkeyes 1 (SPRTSBITE) | dropped_other | 503 | HTTP 503 |
| [American Football] Nebraska Cornhuskers at Iowa Hawkeyes 2 (SPRTSBITE) | dropped_other | 503 | HTTP 503 |
| [Darts] Darts Players Championship Finals (FAWA) | working | 200 | hls, segment ok (65536 bytes) |
| [Formula 1] Formula 1 2026 - Qatar GP (iSTRMEAST) | working | 200 | hls, segment ok (65536 bytes) |
| [Formula 1 GP] Formula 1 GP Qatar 2 (FAWA) | working | 200 | hls playlist |
| [NFL] Denver Broncos at Pittsburgh Steelers (SPRTSPASS) | working | 200 | hls, segment ok (65536 bytes) |
| [Pool] Pool Mosconi Cup 2026 (FAWA) | working | 200 | hls, segment ok (65536 bytes) |

## Derived playlists synchronized

| Playlist | Removed | Entries left |
|---|---:|---:|
| playlists/live/USA.m3u | 17 | 3903 |
| playlists/countries/USA.m3u | 17 | 3903 |
| playlists/categories/Sports.m3u | 17 | 787 |
| categories/USA.m3u | 17 | 3903 |
| categories/USA/Sports.m3u | 17 | 197 |
| categories/All/Sports.m3u | 17 | 787 |

## Interpretation

- Every entry was re-tested with its own `#EXTVLCOPT` headers and a deep HLS variant/media-segment probe.
- Only `working` feeds are publishable. A fixture with zero working feeds is refused entirely; no entry from it is published.
- 403 and 404/410 are counted separately because they are conclusive; other probe failures are also withheld rather than published unverified.
