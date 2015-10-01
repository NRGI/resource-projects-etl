import pytest
from selenium import webdriver
import os
import time


server_url = os.environ['SERVER_URL']
prefix = '/'

@pytest.fixture(scope="module")
def browser(request):
    browser = webdriver.Firefox()
    browser.implicitly_wait(3)
    request.addfinalizer(lambda: browser.quit())
    return browser


def test_humanize_naturaltime(browser):
    '''
      This test loads a file from a url into the resourceprojects interface.
      You should then be taken to a /dataload/x page
      Click the each of the 'X now' buttons in turn
      Check to see that the status message is filtered by the naturaltime filter
    '''

    source_url = 'https://raw.githubusercontent.com/NRGI/resource-projects-etl/ee55c2956d23ebfc7a71cb1994a149d966a3c2a7/fts/fixtures/statoil-4-rows.csv'

    browser.get(server_url + prefix)
    browser.find_element_by_partial_link_text('Link').click()
    time.sleep(0.5)
    browser.find_element_by_id('id_source_url').send_keys(source_url)
    browser.find_element_by_css_selector("#fetchURL > div.form-group > button.btn.btn-primary").click()

    dataset_url = browser.current_url
    dataload_url = server_url + prefix + 'dataload/'

    # Click each of the buttons

    for process_id in ['fetch', 'convert', 'staging', 'live']:
        browser.get(dataset_url)
        browser.find_element_by_css_selector("button.btn.btn-default.{}".format(process_id)).click()
        assert 'now' in browser.find_element_by_tag_name('body').text
        browser.get(dataload_url)
        assert 'now' in browser.find_element_by_tag_name('body').text or \
            'second ago' in browser.find_element_by_tag_name('body').text or \
            'seconds ago' in browser.find_element_by_tag_name('body').text



    

