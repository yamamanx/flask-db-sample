# Selenium Lambda Test

CodePipelineから呼び出されるLambda関数でSeleniumテストを実行します。

## セットアップ

1. ECRにコンテナイメージをプッシュ:
```bash
./build-and-push.sh
```

2. Lambda関数を作成:
```bash
aws lambda create-function --cli-input-json file://lambda-config.json
```

3. CodePipelineでLambda関数を呼び出し:
```json
{
  "ActionTypeId": {
    "Category": "Invoke",
    "Owner": "AWS",
    "Provider": "Lambda",
    "Version": "1"
  },
  "Configuration": {
    "FunctionName": "selenium-test-function",
    "UserParameters": "{\"url\": \"https://example.com\"}"
  }
}
```