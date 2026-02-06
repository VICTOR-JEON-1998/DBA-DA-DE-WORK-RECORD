import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def connect_to_chrome(retries=5):
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    for i in range(retries):
        try:
            logger.info(f"🔌 Connecting to Chrome (Attempt {i+1}/{retries})...")
            driver = webdriver.Chrome(options=options)
            return driver
        except WebDriverException:
            time.sleep(2)
            
    return None

def wait_for_login(driver, approval_list_url):
    """
    Waits until the user is logged in.
    Condition for login: URL contains '/works/' or we are on the approval page.
    """
    logger.info("⏳ Waiting for user to log in... (Please login in the Chrome window)")
    
    while True:
        try:
            current_url = driver.current_url
            
            # Check for specific logged-in indicators
            # logic: if we are at 'dbsafer.mistobrand.com/works/...' we are likely logged in
            # If we are at 'login', we are definitely not.
            
            if "login" in current_url or "signin" in current_url:
                # User is on login page
                pass
            elif "/works/" in current_url:
                # User has logged in and is in the workspace
                logger.info("✅ Login detected! (URL contains '/works/')")
                return
            
            # Print heart beat every once in a while? 
            # logger.info(f"   Current URL: {current_url}")
            time.sleep(2)
            
        except Exception as e:
            logger.error(f"⚠️ Error checking URL: {e}")
            time.sleep(2)

def run_stealth_bot(max_approvals=None, run_duration_minutes=None):
    """
    Run bot by attaching to existing Chrome instance (Port 9222)
    """
    driver = connect_to_chrome()
    if not driver:
        logger.error("❌ Could not connect to Chrome.")
        logger.error("🛑 ACTION REQUIRED: Run 'run_chrome.bat' first.")
        return

    wait = WebDriverWait(driver, 15)
    
    start_time = datetime.now()
    approval_list_url = "https://dbsafer.mistobrand.com/works/workflow/approval/running"

    logger.info("✅ Connected successfully.")
    
    # 1. Wait for Login
    wait_for_login(driver, approval_list_url)
    
    # 2. Ensure we are on the approval list page
    logger.info("📂 strict navigation to approval list...")
    if "/approval/running" not in driver.current_url:
        driver.get(approval_list_url)
        time.sleep(3)

    logger.info("🚀 Starting Approval Monitoring Loop...")
    
    approval_count = 0

    try:
        while True:
            # Check runtime duration
            if run_duration_minutes:
                elapsed_minutes = (datetime.now() - start_time).total_seconds() / 60
                if elapsed_minutes >= run_duration_minutes:
                    logger.info(f"⏱️ Run duration limit reached ({run_duration_minutes} minutes)")
                    break
            
            # Check approval count limit
            if max_approvals and approval_count >= max_approvals:
                logger.info(f"✅ Approval limit reached ({max_approvals} approvals)")
                break
            
            try:
                # Verify still on approval page
                if "/approval/running" not in driver.current_url:
                    logger.warning("⚠️ Not on approval list page. Navigating there...")
                    # If user logged out, wait_for_login will block effectively? 
                    # Actually, if user logs out, URL usually changes to login.
                    if "login" in driver.current_url:
                        logger.warning("⚠️ Detected logout. Waiting for login again...")
                        wait_for_login(driver, approval_list_url)
                        continue
                        
                    try:
                        driver.get(approval_list_url)
                    except:
                        logger.error("❌ Failed to navigate. Browser might be closed.")
                        break
                    time.sleep(5)
                    continue
                
                # Refresh to check for new items
                driver.refresh()
                time.sleep(3)  # Allow time for page to load
                
                # Check for table rows - Column 6 Title
                title_xpath = "//table/tbody/tr[1]/td[6]/a"
                
                try:
                    request_link = wait.until(EC.element_to_be_clickable((By.XPATH, title_xpath)))
                    
                    logger.info(f"🚀 New Request Found: {request_link.text}")
                    request_link.click()
                    time.sleep(2)  # Wait for detail page to load

                    # Detail Page Logic
                    try:
                        # Strategy: User says button is at the bottom.
                        # 1. Scroll to bottom.
                        # 2. Find ALL candidates.
                        # 3. Sort by Y position (find the lowest one).
                        # 4. Highlight and click.
                        
                        logger.info("📜 Scrolling to bottom of page...")
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(1)

                        candidates_xpath = "//*[(self::button or self::a or self::div or self::span or self::input) and contains(., '결재') and not(contains(., '변경')) and not(contains(., '결재선')) and not(contains(., '반려')) and not(contains(., '목록'))]"
                        
                        elements = driver.find_elements(By.XPATH, candidates_xpath)
                        
                        # Filter for visible and clickable
                        valid_candidates = []
                        for el in elements:
                            try:
                                if el.is_displayed() and el.size['height'] > 0:
                                    valid_candidates.append(el)
                            except:
                                continue
                        
                        if not valid_candidates:
                            logger.warning("🔍 No visible '결재' elements found (Strict filter applied).")
                            raise TimeoutException("No candidates")

                        # Sort by Y location (descending -> higher Y means lower on page)
                        valid_candidates.sort(key=lambda x: x.location['y'], reverse=True)
                        
                        target_btn = valid_candidates[0]
                        
                        # Refinement: If target is a DIV/SPAN, check if it wraps a real button
                        # The user log showed we clicked a DIV wrapper.
                        if target_btn.tag_name.lower() in ['div', 'span']:
                            try:
                                # Try to find a child button/a
                                child_btns = target_btn.find_elements(By.XPATH, ".//button | .//a | .//input")
                                if child_btns:
                                    logger.info(f"   ↳ Refined selection: Found {len(child_btns)} child clickable items inside {target_btn.tag_name}. Using the first one.")
                                    target_btn = child_btns[0]
                            except:
                                pass

                        logger.info(f"🎯 Selected Bottom-Most Candidate: '{target_btn.text}' (Tag: {target_btn.tag_name}, Y: {target_btn.location['y']})")
                        
                        # DEBUG: Highlight the button
                        driver.execute_script("arguments[0].style.border='5px solid red'; arguments[0].style.backgroundColor='yellow';", target_btn)
                        time.sleep(1) # Let user see it

                        # Use JavaScript click to work even if window is minimized/background
                        logger.info("🖱️ Clicking button via JavaScript (Background safe)...")
                        
                        # Try standard click first, then JS click if it fails (or do both to be safe)
                        try:
                            # 1. Javascript Click (Most reliable for hidden/background)
                            driver.execute_script("arguments[0].click();", target_btn)
                            
                            # 2. Check for unexpected alert (confirmation dialog)
                            try:
                                alert = wait.until(EC.alert_is_present())
                                logger.info(f"🔔 Alert detected: {alert.text}")
                                alert.accept()
                                logger.info("✅ Alert accepted.")
                            except TimeoutException:
                                # No alert, which is fine
                                pass
                                
                        except Exception as e:
                            logger.error(f"⚠️ Click error: {e}")
                        
                        approval_count += 1
                        logger.info(f"✔️ Approval action triggered. (Total: {approval_count})")
                        time.sleep(3) # Wait for server to process 

                    except (TimeoutException, IndexError) as e:
                         pass # Quietly return to list to retry
                         # logger.error(f"❌ Could not find/click approval button: {e}")
                    
                    # Return to approval list
                    driver.get(approval_list_url)
                    time.sleep(2)

                except TimeoutException:
                    # No new items found
                    logger.info(f"[{time.strftime('%H:%M:%S')}] No requests found. Monitoring... (Next check in 5s)")
                    # English line: Set the monitoring interval to 5 seconds.
                    # 한국어 줄: 모니터링 간격을 5초로 설정합니다.
                    time.sleep(5)

            except Exception as e:
                logger.error(f"❌ Unexpected error in loop: {e}")
                time.sleep(60) # Prevent tight loop on error

    except KeyboardInterrupt:
        logger.info("⏹️ Program interrupted by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {type(e).__name__}: {e}")
    finally:
        logger.info(f"✨ Auto approval completed. Total approvals: {approval_count}")
        # NOTE: Do not quit driver here as it closes the user's browser
        logger.info("👋 Detaching from browser (Window will remain open)")


if __name__ == "__main__":
    run_stealth_bot()
