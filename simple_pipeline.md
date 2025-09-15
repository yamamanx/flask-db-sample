# シンプルパイプラインハンズオンリソース

シンプルなCodePipelineのハンズオンを実行してもらうためのサンプルアプリケーションを構築します。

## 必要なもの

* デプロイ先のEC2とRDS、SecretsManagerを起動するためのCloudFormationテンプレート  
* GitHubに保存するソースコードのリポジトリファイル一式

## 構成

* EC2(t3.micro)上にFlask Python
* RDS(db.t3.micro) MySQL
* RDSのパスワードはSecrets Manager

## リポジトリの内容

* EC2にデプロイするPythonのコード
* ビルドするためのbuildspec.yml
* requirements.txt (boto3, pymysql)
* pytestを使ったテストコード
* テストはCodeBuildレポートで表示できるようにする
* CloudFormationテンプレート

### Pythonコード

ブラウザからアクセス可能。
メモ帳アプリ(タイトルと本文)。
メモの新規作成、一覧表示、更新、削除。

### CloudFormationテンプレート

スタック作成時にEC2のユーザーデータで必要なモジュールインストール。
ユーザーデータで、MySQLにデータベース、テーブルを作成。
EC2のIAMロールにSecretsManagerのGetSecretValueを許可。
RDSインスタンスが作成完了してから、EC2を起動させる。
