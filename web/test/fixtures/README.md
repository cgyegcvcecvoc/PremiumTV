# Browser playback fixture

`hls/` is a six-second HLS rendition of the repository's synthetic PremiumTV
test card (`playlists/vod/media/premiumtv-test-card.mp4`, CC0). It exists only
so browser tests can prove HLS playback without depending on a public provider.
It is not part of the deployed channel/movie library.

Regenerate with FFmpeg:

```sh
ffmpeg -i playlists/vod/media/premiumtv-test-card.mp4 -t 6 \
  -c:v libx264 -preset veryfast -crf 28 -c:a aac -b:a 64k \
  -f hls -hls_time 2 -hls_playlist_type vod \
  -hls_segment_filename web/test/fixtures/hls/segment-%02d.ts \
  web/test/fixtures/hls/index.m3u8
```
