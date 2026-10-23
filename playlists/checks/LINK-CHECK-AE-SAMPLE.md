# Deep link check - archives and category shelf

- **Run:** manual deep quality check (AE sample) (`20261023T185739Z-14666`)
- **Started:** 2026-10-23T18:57:39Z  |  **Finished:** 2026-10-23T18:57:41Z  |  **Duration:** 2.3s
- **Mode:** deep (playlist + segment probe)
- **Unique links checked:** 69 from 69 playlist entries in 1 playlists

| Result | Links | Share | Meaning |
|---|---:|---:|---|
| working | 68 | 98.6% | answered with playable media |
| offline | 1 | 1.4% | confirmed dead - removed when patching |

## Per playlist

| Playlist | Entries | Working | Offline | Unreachable | Blocked | Other |
|---|---:|---:|---:|---:|---:|---:|
| `playlists/AE_Channels.m3u` | 69 | 68 | 1 | 0 | 0 | 0 |

## Hosts with the most failing links

| Host | Offline | Unreachable |
|---|---:|---:|
| `88.212.15.17` | 1 | 0 |

## Sample of confirmed-dead links

| Channel | Reason | URL |
|---|---|---|
| Crime + Investigation CEE | connection refused | `http://88.212.15.17/live/test_cai_hevc/playlist.m3u8` |
