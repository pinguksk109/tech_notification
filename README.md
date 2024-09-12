# Deploy手順

## 1 作業用ディレクトリの作成
mkdir -p target/modules

## 2 依存関係のインストール
pip install -r requirements.txt -t target/modules

## 3 Lambda関数のPythonファイルをコピー
cp lambda_function.py target/

<!-- rsync -av --exclude='.gitignore' --exclude='venv/' --exclude='function.zip' --exclude='target/' ./ deploy_package/ -->

## 4 ZIPファイルの作成
cd target
zip -r ../function.zip .

## 5 Lambdaに手動でアップロード
手動で

## 6 削除
cd ..
rm -rf target
rm function.zip
