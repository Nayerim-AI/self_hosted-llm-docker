#!/bin/sh
set -e

if [ -f "/app/llama.cpp/build/bin/llama-cli" ]; then
  echo "[SKIP] llama.cpp sudah terbangun."
  exit 0
fi

echo "[BUILD] Memulai build llama.cpp..."

if [ ! -d "/app/llama.cpp" ]; then
  git clone https://github.com/ggerganov/llama.cpp /app/llama.cpp
fi

cd /app/llama.cpp

rm -rf build/
mkdir -p build

cmake -S . -B build -DLLAMA_CURL=OFF
cmake --build build --target llama-cli

if [ ! -f "build/bin/llama-cli" ]; then
  echo "[ERROR] Binary tidak ditemukan!"
  exit 1
fi

echo "[DONE] llama.cpp berhasil dibuild."
