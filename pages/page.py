#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pytest
import time
import random
import string
from datetime import datetime
from datetime import timedelta
import re


class Page(object):

    def __init__(self, logger, driver, yaml):
        self.logger = logger
        self.driver = driver
        self.css = {}

        self.name = self.__class__.__name__
        self.conf = yaml

    def log_info(self, message):
        self.logger.info("{}: {}".format(self.name, message))

    def log_warning(self, message):
        self.logger.warning("{}: {}".format(self.name, message))

    def log_debug(self, message):
        self.logger.debug("{}: {}".format(self.name, message))

    def log_error(self, message):
        self.logger.error("{}: {}".format(self.name, message))

    def open_url(self, url):
        self.driver.get(url)

    @property
    def get_current_url(self):
        c = self.driver.current_url
        self.logger.debug('current_url: {}'.format(c))
        return c

    @property
    def get_current_title(self):
        return self.driver.title

    def refresh_browser(self):
        self.driver.refresh()

    def get_random_string(self, chars=1):
        return "".join(random.choice(string.ascii_letters) for _ in range(chars))

    def get_random_str_number(self, digits=1):
        return "".join(str(random.randint(1, 10)) for _ in range(digits))

    def get_todays_date(self, with_time=False):
        today = datetime.now()
        if with_time:
            return today.strftime('%hh:%mm %Y-%m-%d')
        else:
            return today.strftime('%Y-%m-%d')

    def get_offset_days(self, days):
        offset = datetime.now() + timedelta(days=days)
        return offset

    @property
    def random_email(self):
        email = self.get_random_string(10) + "@coupdog.com"
        self.logger.debug('random email: {}'.format(email))
        return email

    def delete_all_cookies(self):
        self.driver.delete_all_cookies()

    def clean_browser_storage(self):
        self.driver.execute_script('window.sessionStorage.clear();')
        self.driver.execute_script('window.localStorage.clear();')

    def get_alert_accept(self):

        alert = self.driver.switch_to_alert()
        alert_text = alert.text
        alert.accept()
        self.logger.info('alert: {}'.format(alert_text))
        return alert_text

    def wait_for_windows(self, count):
        a = self.driver.window_handles
        for _ in range(10):
            if len(a) == count:
                self.logger.debug('window count: {} ok'.format(len(a)))
                break
            else:
                time.sleep(0.5)
        else:
            pytest.fail('wait_for_windows: window count: {} != {}'.format(len(a), count))

    def get_current_window_handle(self):
        return self.driver.current_window_handle

    def switch_to_new_window(self):
        h = self.driver.window_handles[-1]
        self.driver.switch_to.window(h)
        self.logger.debug('switched to: {}'.format(self.driver.title))

    def switch_to_main_window(self):
        h = self.driver.window_handles[0]
        self.driver.switch_to.window(h)
        self.logger.debug('switched to: {}'.format(self.driver.title))

    def close_window(self):
        self.driver.close()

    def wait_for_iframe(self):
        self.wait_for_element_by_css('iframe')

    def switch_to_iframe(self):
        self.wait_for_iframe()
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    # -----------------------------
    # waiters, getters and clickers
    # -----------------------------

    def get_element_clickable_by_css(self, selector):

        try:
            return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                                                 ,'get_element_clickable_by_css: timed out on: %s' % selector)

        except TimeoutException as e:
            pytest.fail('TimeoutException: %s' % e)
        except Exception as e:
            pytest.fail('UnexpectedException: %s' % e)

    def get_element_clickable_by_xpath(self, selector):

        try:
            return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, selector))
                                                 ,'get_element_clickable_by_xpath: timed out on: %s' % selector)

        except TimeoutException as e:
            pytest.fail('TimeoutException: %s' % e)
        except Exception as e:
            pytest.fail('UnexpectedException: %s' % e)

    def get_element_by_css(self, selector):

        try:
            return WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                                                        ,'get_element_by_css: timed out on: %s' % selector)

        except TimeoutException as e:
            pytest.fail('TimeoutException: %s' % e)
        except Exception as e:
            pytest.fail('UnexpectedException: %s' % e)

    def wait_for_element_by_css(self, selector, time_out=30):

        try:
            WebDriverWait(self.driver, time_out).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                                                        ,'wait_for_element_by_css: timed out on: %s' % selector)

        except TimeoutException as e:
            pytest.fail('TimeoutException: %s' % e)
        except Exception as e:
            pytest.fail('UnexpectedException: %s' % e)

    def wait_for_element_visible_by_css(self, selector, time_out=30):

        try:
            WebDriverWait(self.driver, time_out).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
                                                        ,'wait_for_element_by_css: timed out on: %s' % selector)

        except TimeoutException as e:
            pytest.fail('TimeoutException: %s' % e)
        except Exception as e:
            pytest.fail('UnexpectedException: %s' % e)

    def get_element_by_css_no_throw(self, selector, wait_time=1):

        try:
            return WebDriverWait(self.driver, wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        except Exception:
            return None

    def get_all_elements_by_css(self, selector, wait_time=30):

        try:
            return WebDriverWait(self.driver, wait_time).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                                                 ,'get_all_elements_by_css: timed out on: %s' % selector)

        except TimeoutException as e:
            pytest.fail('TimeoutException: %s' % e)
        except Exception as e:
            pytest.fail('UnexpectedException: %s' % e)

    def get_all_elements_by_css_no_throw(self, selector, wait_time=30):

        try:
            return WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
        except Exception as e:
            return None

    def wait_until_element_not_present(self, selector, wait_time=30):

        try:
            WebDriverWait(self.driver, wait_time).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                                                 ,'wait_until_element_not_present: timed out on: %s' % selector)

        except TimeoutException as e:
            pytest.fail('TimeoutException: %s' % e)
        except Exception as e:
            pytest.fail('UnexpectedException: %s' % e)

    def ensure_element_not_present(self, selector):

        try:
            self.driver.find_element_by_css_selector(selector)
            pytest.fail('ensure_element_not_present: element {} found!' % selector)
        except Exception as e:
            pass

    def click_by_css(self, selector):
        try:
            el = self.get_element_clickable_by_css(selector)
            el.click()
        except StaleElementReferenceException as e:
            pytest.fail('StaleElementReferenceException: %s' % e)
        except WebDriverException as e:
            pytest.fail('WebDriverException: %s' % e)
        except Exception as e:
            pytest.fail('UnexpectedException: %s' % e)

    def click_if_clickable_by_css(self, el):
        try:
            for _ in range(30):
                if el.is_enabled() and el.is_displayed():
                    el.click()
                    return
                else:
                    self.logger.debug("Element visible: %s, element enabled: %s", el.is_displayed(), el.is_enabled())
                    time.sleep(1)
        except StaleElementReferenceException as e:
            pytest.fail('StaleElementReferenceException: %s' % e)
        except WebDriverException as e:
            pytest.fail('WebDriverException: %s' % e)
        except Exception as e:
            pytest.fail('UnexpectedException: %s' % e)

    def click_by_xpath(self, selector):
        try:
            el = self.get_element_clickable_by_xpath(selector)
            el.click()
        except StaleElementReferenceException as e:
            pytest.fail('StaleElementReferenceException: %s' % e)
        except WebDriverException as e:
            pytest.fail('WebDriverException: %s' % e)
        except Exception as e:
            pytest.fail('UnexpectedException: %s' % e)

    def clear_input(self, selector):
        for _ in range(2):
            el = self.get_element_by_css(selector)
            el.clear()
            value = self.get_element_by_css(selector).get_attribute('value')
            if value == "":
                self.logger.debug('%s: ok: %s' % (self.name, selector))
                break
            else:
                self.logger.debug('%s: not yet cleared: %s' % (self.name, selector))
                time.sleep(0.5)

    def send_by_css(self, selector, value, clear=True):
        try:
            el = self.get_element_by_css(selector)
            if clear:
                el.clear()
            el.send_keys(value)
        except StaleElementReferenceException as e:
            pytest.fail('StaleElementReferenceException: %s' % e)
        except WebDriverException as e:
            pytest.fail('WebDriverException: %s' % e)
        except Exception as e:
            pytest.fail('UnexpectedException: %s' % e)

    def get_href_attribute(self, selector):
        el = self.get_element_by_css(selector)
        return el.get_attribute('href')

    def get_attribute(self, el, attrib):
        return el.get_attribute(attrib)

    def ensure_element_settles(self, selector):
        position = {}
        for _ in range(10):
            el = self.get_element_by_css(selector)
            if el.location == position:
                break
            else:
                self.logger.debug('{} != {}'.format(position, el.location))
                position = el.location
                time.sleep(0.5)

    def assert_table(self, tbl1, tbl2):

        """to assert both tables are equal
        's': skip
        'i:{}': assert in e.g cell1 = i:{2020} in 10.10.2020 would pass
        """

        assert len(tbl1) == len(tbl2)

        self.logger.info('tbl1: %s', tbl1)
        self.logger.info('tbl2: %s', tbl2)

        for cell1, cell2 in zip(tbl1, tbl2):
            self.logger.debug('tbl1 cell: %s, tbl2 cell: %s', cell1, cell2)
            if cell1 == 's' or cell2 == 's':
                self.logger.debug('(s) => skipped')
            elif cell1.count('i:{'):
                cell_in = cell1[3:-1]
                assert cell_in in cell2
            else:
                assert cell1 == cell2

    def assert_match(self, pattern, string):

        """to assert regex pattern matches string"""

        search_obj = re.search(pattern, string, flags=0)
        if search_obj:
            self.logger.debug('Pattern: {} found in str: {}'.format(pattern, string))
        else:
            raise AssertionError('Pattern: {} not found in str: {}'.format(pattern, string))

    def scroll_top_page(self):
        self.driver.execute_script('window.scrollTo(0, 0);')

    def set_js_value(self, css, value):
        exec_js = "document.querySelector('{}').value = '{}'".format(css, value)
        self.driver.execute_script(exec_js)

