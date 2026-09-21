#!/usr/bin/env bash
set -euo pipefail
if [[ "${CASA_AUTHORIZED_TARGET:-}" != "YES" ]]; then
  echo "Refusing runtime scan. Set CASA_AUTHORIZED_TARGET=YES only when you are authorized to test the target." >&2
  exit 2
fi
TARGET="${1:-}"
OUT="${2:-zap-output}"
if [[ -z "$TARGET" ]]; then echo "Usage: CASA_AUTHORIZED_TARGET=YES $0 https://authorized-target.example [output-dir]" >&2; exit 64; fi
mkdir -p "$OUT"
docker run --rm -v "$(pwd)/$OUT:/zap/wrk/:rw" -t ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py -t "$TARGET" -J zap-report.json -r zap-report.html -w zap-report.md || true
printf '%s\n' "ZAP baseline completed. Review/adjudicate all alerts; this does not establish CASA Pass status."
