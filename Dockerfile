# PremiumTV Download Hub — single-container deploy (Render / Railway / Fly.io / any Docker host)
#
#   docker build -t premiumtv-hub .
#   docker run -p 8000:8000 premiumtv-hub
#
# Set MIRROR_MAC=1 as a build arg to also self-host the ~1.1 GB of macOS
# installers:  docker build --build-arg MIRROR_MAC=1 -t premiumtv-hub .

FROM python:3.12-slim

WORKDIR /app

# Repo content the hub serves (playlists, EPG, categories) + the hub itself.
COPY . .

ARG MIRROR_MAC=0
ENV MIRROR_MAC=${MIRROR_MAC}

# 1) Pull released APKs (and optionally macOS installers) from public release storage.
# 2) Scan everything, hash APKs, build the zip bundles and data.json.
RUN python hub/fetch_assets.py && python hub/build_data.py

EXPOSE 8000
ENV PORT=8000

HEALTHCHECK --interval=30s --timeout=5s CMD python -c "import urllib.request,os;urllib.request.urlopen('http://127.0.0.1:'+os.environ.get('PORT','8000')+'/healthz')"

CMD ["python", "hub/server.py"]
