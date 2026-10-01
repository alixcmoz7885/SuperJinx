# Security

- The owner login is `admin / admin` by design so the panel works with zero setup. Anyone who finds your domain can try it, so do not share your panel address publicly.
- The panel, the Xray core and all internal ports (8000, 10001-10005, 62050) listen on `127.0.0.1` only. The only public entry is nginx on port 8080 behind Railway's TLS.
- The internal node API key and TLS certificate are generated on first boot and stored on the volume.

Found a problem? Report it in the [Super JinX channel](https://t.me/+WvKFv0lU_i5lNGE0).
