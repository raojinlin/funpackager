## fcrelease

aliyun function Multiple function modules shared release


## Development directory struct

```text
/tmp/fctest/
├── dist
├── lib
│   ├── requests
├── pa
└── pb

```


## Config

```yaml
lib: ./lib
name: aliyun fc services
dist: ./dist
functions:
  - name: funca
    index: index.handler
    directory: ./funca
    requirements:
      - requests
      - pdfkit
    services:
      - printpdf
    modules:
      - utils.py

  - name: funcb
    index: index.handler
    directory: ./funcb
    requirements:
      - PyPDF2
      - requests
      - reportlab

  - name: funcc
    index: index.handler
    directory: ./funcc

```

## Install

```bash
$ python3 setup.py install
```


## Command line options

```text
  -h, --help            show this help message and exit
  --config c, -c c      配置文件, 支持json, yaml
  --dist [DIST], -d [DIST]
                        输出文件夹
  --release, -r         发布
  --list, -L            列出配置文件中的函数
  --function FUNCTION [FUNCTION ...], -f FUNCTION [FUNCTION ...]
                        指定函数
  --debug, -D           调试输出

```
