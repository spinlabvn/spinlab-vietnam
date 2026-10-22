#!/bin/bash
# Bấm đúp để mở trang quản lý website Spinlab (http://127.0.0.1:8770/admin). Đóng cửa sổ Terminal để tắt.
cd "$(dirname "$0")"
if lsof -nP -iTCP:8770 -sTCP:LISTEN >/dev/null 2>&1; then
  open "http://127.0.0.1:8770/admin"
else
  python3 tools/admin.py
fi
