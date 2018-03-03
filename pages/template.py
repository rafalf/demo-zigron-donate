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
from config import get_config
import time
import random
import string
from datetime import datetime
from datetime import timedelta
import re
from jsonschema import validate
from jsonschema.exceptions import ErrorTree, FormatError, RefResolutionError, SchemaError, ValidationError


class Template(object):

    def __init__(self, logger, driver, yaml):
        self.logger = logger
        self.driver = driver

        self.name = self.__class__.__name__
        self.conf = yaml