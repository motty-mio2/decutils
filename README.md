# decutils
## Install
### Install
基本的に win でも linux でも 下記コマンドでインストール可能（のはず）
```bash 
pip install -U git+https://github.com/motty-mio2/decutils.git@release
```

## Usage
- float2binary
  - 単精度浮動小数点数 を 32bit のバイナリに変換する
  - 引数 (fltnum, sep)
      - fltnum : float の値
      - sep : 区切り（_）の挿入
        - 指定なし : 何もしない
        - mean : 符号，指数，仮数の意味区切り
        - length : 8 文字ずつの長さ区切り
- binary2float
  - 32bit のバイナリを 単精度浮動小数点数に変換する
  - 引数 (binary)
    - binary : 32bit の 2 進数
- float2hex
 - 単精度浮動小数点数を 32bit の16進数に変換する
  - 引数 (fltnum)
      - fltnum : float の値
- hex2float
  - 32bit の16進数を 単精度浮動小数点数に変換する
  - 引数 (hex)
    - hex : 32bit の 16 進数

```python
import decutils as du
m2.float2binary(3.14)
```
他も同様

## その他
- 現時点では pip で公開する予定はなし，あくまで個人用

## Reference
- https://ja.wikipedia.org/wiki/%E5%8D%98%E7%B2%BE%E5%BA%A6%E6%B5%AE%E5%8B%95%E5%B0%8F%E6%95%B0%E7%82%B9%E6%95%B0
- https://note.nkmk.me/python-float-hex/
