# hevc_decode_benchmark

Estudo sobre decodificação de vídeo HEVC "ladrilhado".

## Descrição

- main.sh - prepara arquivo yuv, codifica, encapsula e segmenta os vídeos.
- gop.sh - escreve em arquivo a estrutura do GOP do vídeo
- gopall.sh - usar o gop.sh em todos os arquivos do diretório

## Dependências

- ffmpeg - https://ffmpeg.org/
- kvazaar - https://github.com/ultravideo/kvazaar
- gpac - https://github.com/gpac/gpac/
