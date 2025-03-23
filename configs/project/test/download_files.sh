#!/bin/bash

# Repositório e release
REPO="raynnersc/ics_project"
RELEASE="embench"
BASE_URL="https://github.com/$REPO/releases/download/$RELEASE"

# Lista de arquivos
FILES=(
  "aha-mont64"
  "crc32"
  "cubic"
  "edn"
  "huffbench"
  "matmult-int"
  "minver"
  "nbody"
  "nettle-aes"
  "nettle-sha256"
  "nsichneu"
  "picojpeg"
  "qrduino"
  "sglib-combined"
  "slre"
  "st"
  "statemate"
  "ud"
  "wikisort"
)

# Criar diretório para os binários
mkdir -p embench_binaries
cd embench_binaries || exit

# Baixar cada arquivo individualmente
for file in "${FILES[@]}"; do
  echo "Baixando: $file"
  wget -q --show-progress "$BASE_URL/$file"
done

echo "Download concluído!"
