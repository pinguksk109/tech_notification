# Overview

This system collects and recommends trending tech articles and sends notifications to a LINE account.
It is designed to run on **AWS Lambda** and currently supports:

* ✅ Qiita
* ✅ Zenn
* 🚇 Osaka Metro train status
* ☀️ Weather forecast in Osaka

> LINE credentials (User ID, Bearer Token) must be obtained from [LINE Developers](https://developers.line.biz/en/).

---

# Features

* Fetches articles from Qiita and Zenn
* Selects the top 5 most liked articles from each platform within the last 3 days
* Scrapes Osaka Metro's delay information
* Gets daily weather forecast from the Japan Meteorological Agency (JMA)
* Formats and sends all data as LINE messages

---

# Required Environment Variables

The following environment variables must be set to run the Lambda function:

| Variable Name       | Description                         |
| ------------------- | ----------------------------------- |
| `LINE_USER_ID`      | LINE user ID to send messages to    |
| `LINE_BEARER_TOKEN` | Bearer token for LINE Messaging API |

These should be securely stored using AWS Lambda's environment variable settings.

# Run Locally

```bash
python driver.py
```

> ⚠️ The Qiita API has a rate limit of 60 requests per hour.
> One execution makes 10 requests, so be careful not to exceed the limit.

---

# Run Unit Tests

```bash
python -m pytest
```

---

# Deploy to AWS Lambda

## Step 1: Create a working directory

```bash
mkdir lambda_package
```

## Step 2: Install dependencies

```bash
pip install -r requirements.txt -t lambda_package/
```

## Step 3: Copy project files

```bash
cp -r application domain infrastructure lambda_function.py lambda_package/
```

## Step 4: Create a ZIP file

```bash
cd lambda_package
zip -r ../lambda_package.zip .
```

## Step 5: Upload to AWS Lambda

* Go to AWS Console
* Choose the Lambda function
* Upload the `lambda_package.zip` manually

## Step 6: Clean up

```bash
cd ..
rm -rf lambda_package lambda_package.zip
```

---

# Clear `__pycache__` (Optional)

```bash
find . -type d -name __pycache__ -exec rm -r {} \+
```