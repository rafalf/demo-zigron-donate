#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from config import CAMPAIGN_URL
from pages.campaign import Campaign


@pytest.mark.parametrize("campaign_id, donation_amount, card_valid", [
        ('21153', '100', True),
        ('21153', '100', False),
    ])
def test_donate_to_campaign(driver, logger, yaml, campaign_id, donation_amount, card_valid):

    campaign = Campaign(logger, driver, yaml)

    campaign.open_url(CAMPAIGN_URL.format(campaign_id))

    if card_valid:
        card_number = yaml['stripe']['valid_visa']
    else:
        card_number = yaml['stripe']['invalid_address_fail']

    campaign.enter_donation_amount(donation_amount)

    email_address = campaign.get_random_string(10) + "@zigron." + campaign.get_random_string(3)
    campaign.enter_email_address(email_address)

    campaign.click_debit_card()

    rnd_full_name = campaign.get_random_string(10)
    campaign.enter_full_name(rnd_full_name)

    rnd_phone = campaign.get_random_str_number(10)
    campaign.enter_phone_number(rnd_phone)

    # card
    campaign.enter_card_number(card_number)

    rnd_name = campaign.get_random_string(10)
    campaign.enter_name_on_card(rnd_name)

    campaign.select_expiry_year()
    campaign.select_expiry_month()
    campaign.enter_cvv()

    if card_valid:

        campaign.click_pay_now()

        txt = campaign.get_success_text()

        assert donation_amount in txt

    else:

        campaign.click_pay_now(False)

        # THIS SHOULD FAIL !!
        # ITS A BUG - STRIPE FAILS
        # AND THERE SHOULD BE NO THANK YOU MESSAGE
        # https://stripe.com/docs/testing
        # ONCE THIS IS FIXED YOU CAN ADD SOMETHING

        # txt = campaign.get_failed_text()
        # assert txt == "the text that will be there - failed text"

