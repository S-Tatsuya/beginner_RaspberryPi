# 作業中に本以外で調べたことを残す。

## I2Cの初期設定の仕方
[参考URL](https://www.qoosky.io/techs/2316d68b2e)

Raspberry Pi初期設定画面のコマンド  
` sudo raspi-config `

## シリアル通信の3種類
 - SPI通信
   - 50Mbpsの高速通信
   - クロック有り
   - 信号線が4本(3本と記載しているサイトもあった)
   - マスター1 ⇔ スレーブ複数 
 - I2C通信
   - 1Mbpsの低速通信
   - クロック有り
   - 信号線が2本
   - マスター複数 ⇔ スレーブ複数 
 - URAT通信
   - 500Kbpsの低速通信
   - クロック無し
   - 信号線が2本
   - デバイス1 ⇔ デバイス1 

## Gitのコミット時のエディタをVimに変更
[参考URL](https://qiita.com/yktk435/items/0383747c58ce82d94a51)

コマンド
` git config --global core.editor vim `