# PremiumTV Relay — deployable image
#
#   docker build -f relay/Dockerfile -t premiumtv-relay .
#   docker run -p 8099:8099 -e PUBLIC_ORIGIN=https://relay.example premiumtv-relay
#
# Or on Fly.io / Render / Railway: see relay/fly.toml and relay/README.md.

FROM node:22-alpine

WORKDIR /app

# Only the relay and the playlist it allowlists are needed; the rest of the
# repository (guides, artwork, the 12 MB library) stays out of the image.
COPY relay/relay.js relay/relay.json ./relay/
COPY playlists/live/USA.m3u ./playlists/live/USA.m3u

ENV PORT=8099
# Set this to the public https URL the relay is reachable at, so rewritten
# playlists hand absolute URLs back to the player.
ENV PUBLIC_ORIGIN=""

EXPOSE 8099

HEALTHCHECK --interval=30s --timeout=5s \
  CMD node -e "fetch('http://127.0.0.1:'+(process.env.PORT||8099)+'/healthz').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"

CMD ["node", "relay/relay.js", "--playlist", "playlists/live/USA.m3u", "--port", "8099"]
