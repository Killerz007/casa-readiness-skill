# Official upstream material

The canonical upstream source is `appdefensealliance/ASA-WG`.

`upstream-manifest.json` records the released CASA version and GitHub blob SHAs used as the repository baseline.

`scripts/sync_official_spec.py --sync` downloads the released CASA Specification, CASA Test Guide and ADA Burp audit configuration into `official/current/`, rebuilds generated catalogues, and writes an upstream-change review when content changes.

Upstream App Defense Alliance content is licensed by its owner under **CC BY-SA 4.0**. This repository's Apache-2.0 license does not replace the upstream license for copied upstream material.
