# 概要
テック記事からおすすめの記事を抽出して、Lineに通知する  
LINEの環境変数は自分でLine Developerで発行する

対応記事
* Qiita

# ロジック
Qiita
* 直近3日間くらいの記事を取得して、いいねが多い数に5つ抽出する

# ローカルで動かす
QiitaAPIは1時間に60回までなので注意(1度の実行で10回リクエストする)
```sh
python driver.py
```

# Deploy手順
Lambdaで動かす

## 1 作業用ディレクトリの作成
mkdir lambda_package

## 2 依存関係のインストール
pip install -r requirements.txt -t lambda_package/

## 3 Lambda関数のPythonファイルをコピー
cp -r application domain infrastructure lambda_function.py lambda_package/

## 4 ZIPファイルの作成
cd lambda_package
zip -r ../lambda_package.zip .

## 5 Lambdaに手動でアップロード
手動で

## 6 削除
cd ..
rm -rf lambda_package
rm -rf lambda_package.zip

# pychacheをいったん消したいとき
```
find . -type d -name __pycache__ -exec rm -r {} \+
```