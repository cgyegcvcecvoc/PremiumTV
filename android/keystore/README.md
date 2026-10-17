# Android update signing key

PremiumTV is side-loaded (there is no Play Store listing), so **every APK must
be signed by the same key**. Android refuses to install a new build over an
installed one when the signing certificates differ
(`INSTALL_FAILED_UPDATE_INCOMPATIBLE`), which would make
**Settings → App updates** fail at the last step.

GitHub's hosted runners do not have a debug keystore, so the old "standard
debug key" was actually a new random key on every build. That is why 1.0.0
through 1.0.3 each had a different certificate and had to be uninstalled
before installing the next version.

`premiumtv-updates.p12` is the long-lived identity used from 1.0.4 onward. It
is deliberately checked in: this is an open-source, ad-hoc distributed app, and
the key only protects the update chain, not a Play Store identity or any
payment data. Anyone can reproduce an installable, self-updating build.

- Keystore type: PKCS#12
- Alias: `premiumtv-updates`
- Store/key password: `premiumtv-updates`
- Certificate SHA-256: see `fingerprint.txt`

`android/app/build.gradle.kts` signs the debug build with this key and the
Android workflow verifies the built APK's certificate against
`fingerprint.txt` on every run. To use a private key instead, set
`PREMIUMTV_ANDROID_KEYSTORE` (absolute path),
`PREMIUMTV_ANDROID_KEYSTORE_PASSWORD`, `PREMIUMTV_ANDROID_KEY_ALIAS` and
`PREMIUMTV_ANDROID_KEY_PASSWORD` in the build environment.

**Do not replace this file.** Losing or changing the key breaks in-place
updates for every installed 1.0.4+ app; users would have to uninstall and
install by hand again.
