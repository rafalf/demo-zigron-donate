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
from selenium.webdriver.support.ui import Select
import pytest
from .page import Page


class Campaign(Page):

    def __init__(self, logger, driver, yaml):
        self.logger = logger
        self.driver = driver

        self.name = self.__class__.__name__
        self.conf = yaml

        super().__init__(logger, driver, yaml)
        self.css['success'] = '.thankyou'

    def enter_donation_amount(self, value):
        self.send_by_css('#donation_amount', value)

    def enter_email_address(self, value):
        self.send_by_css('#user_email', value)

    def click_debit_card(self):
        self.click_by_css('[for="payment_mode_stripe"]')

    def enter_full_name(self, value):
        selector = '#user_fullname'
        self.wait_for_element_visible_by_css(selector)
        self.send_by_css(selector, value)

    def enter_phone_number(self, value):
        selector = '#user_cellphone'
        self.wait_for_element_visible_by_css(selector)
        self.send_by_css(selector, value)

    def enter_card_number(self, value):
        self.send_by_css('#stripe_cardno', value)

    def enter_name_on_card(self, value):
        self.send_by_css('#stripe_fullname', value)

    def enter_cvv(self, value="555"):
        self.send_by_css('#stripe_cvv', value)

    def click_pay_now(self, success=True):
        self.click_by_css("#stripe_payment_btn")

        if success:
            self.wait_for_element_by_css(self.css['success'])

    def select_expiry_year(self, year="2020"):
        select = Select(self.get_element_by_css("#stripe_expiry_year"))
        select.select_by_visible_text(year)

    def select_expiry_month(self, month="May"):
        select = Select(self.get_element_by_css("#stripe_expiry_month"))
        select.select_by_visible_text(month)

    def get_success_text(self):
        return self.get_element_by_css(self.css['success'] + " h4").text

    def get_failed_text(self):
        # not working yet
        return self.get_element_by_css().text
