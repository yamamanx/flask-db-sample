import json
import boto3
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    codepipeline = boto3.client('codepipeline')
    job_id = event['CodePipeline.job']['id']
    logger.info(f"Starting Selenium test for job: {job_id}")
    
    try:
        # CodePipelineからURLを取得
        test_url = event['CodePipeline.job']['data']['actionConfiguration']['configuration']['UserParameters']
        logger.info(f"Test URL: {test_url}")
        
        # Chrome設定
        logger.info("Setting up Chrome driver")
        
        # パスと実行権限を確認
        import os
        logger.info(f"Chrome binary exists: {os.path.exists('/opt/chrome/chrome')}")
        logger.info(f"Chromedriver exists: {os.path.exists('/opt/chromedriver')}")
        logger.info(f"Chromedriver executable: {os.access('/opt/chromedriver', os.X_OK)}")
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--single-process")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.binary_location = "/opt/chrome/chrome"
        
        service = Service("/opt/chromedriver")
        driver = webdriver.Chrome(
            service=service,
            options=chrome_options
        )
        logger.info("Chrome driver initialized successfully")
        
        try:
            # 1. index.htmlにアクセス
            logger.info("Step 1: Accessing index.html")
            driver.get(test_url)
            logger.info("Successfully loaded index.html")
            
            # 2. 新規作成リンクをクリック
            logger.info("Step 2: Clicking create link")
            create_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "新規作成"))
            )
            create_link.click()
            logger.info("Successfully clicked create link")
            
            # 3. create.htmlでフォーム入力
            logger.info("Step 3: Filling form on create.html")
            title_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "title"))
            )
            content_input = driver.find_element(By.NAME, "content")
            submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            
            title_input.send_keys("テストタイトル")
            content_input.send_keys("テスト内容です")
            submit_button.click()
            logger.info("Successfully filled and submitted form")
            
            # 4. index-after.htmlで結果確認
            logger.info("Step 4: Verifying results on index-after.html")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "memo"))
            )
            
            title_element = driver.find_element(By.CSS_SELECTOR, ".memo h3")
            content_element = driver.find_element(By.CSS_SELECTOR, ".memo p")
            
            assert "テストタイトル" in title_element.text
            assert "テスト内容です" in content_element.text
            logger.info("All assertions passed successfully")
            
            # テスト成功
            logger.info("Test completed successfully")
            codepipeline.put_job_success_result(jobId=job_id)
            
        finally:
            logger.info("Closing Chrome driver")
            driver.quit()
            
    except Exception as e:
        # テスト失敗
        logger.error(f"Test failed with error: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        try:
            codepipeline.put_job_failure_result(
                jobId=job_id,
                failureDetails={'message': str(e), 'type': 'JobFailed'}
            )
        except Exception as job_error:
            logger.error(f"Failed to report job failure: {str(job_error)}")