import pytest
from selenium import webdriver
import os
import time


server_url = os.environ['SERVER_URL']


@pytest.fixture(scope="module")
def browser(request):
    browser = webdriver.Firefox()
    browser.implicitly_wait(3)
    request.addfinalizer(lambda: browser.quit())
    return browser


@pytest.mark.parametrize(('prefix', 'source_filename', 'expected_text', 'conversion_successful'), [
    ('/', 'tenders_releases_2_releases.json', 'Fetch now', True),
    ])
def test_humanize_naturaltime(browser, source_filename, prefix, expected_text, conversion_successful):
    '''
      This test loads a file from a url into the resourceprojects interface.
      You should then be taken to a /dataload/x page
      Click the e.g. Fetch Now button
      Check to see that the fetch now message is filtered by the naturaltime filter
    '''

    source_url = 'https://raw.githubusercontent.com/NRGI/resource-projects-etl/6a3a62a0e60eeac9f5b6c61954d231036fd3d3cf/process/statoil/sources/statoil-2014-project-overview-refined.csv'

    browser.get(server_url + prefix)
    browser.find_element_by_partial_link_text('Link').click()
    time.sleep(0.5)
    browser.find_element_by_id('id_source_url').send_keys(source_url)
    browser.find_element_by_css_selector("#fetchURL > div.form-group > button.btn.btn-primary").click()
    body_text = browser.find_element_by_tag_name('body').text
    assert expected_text in body_text
    
    # We should still be in the correct app
    if prefix == '/':
        assert 'ResourceProjects DataLoad Dashboard' in browser.find_element_by_tag_name('body').text
    #Click the Fetch now button
    browser.find_element_by_css_selector("button.btn.btn-default.fetch").click()
    assert 'now' in browser.find_element_by_tag_name('body').text
    #Click the convert button
    #browser.find_element_by_css_selector("button.btn.btn-default.convert").click()
    #Click the Push to Staging button
    #browser.find_element_by_css_selector("button.btn.btn-default.staging-push").click()
    #Click the Remove from Staging button
    #browser.find_element_by_css_selector("button.btn.btn-default.staging-remove").click()
    #Click the Push to Live button
    #browser.find_element_by_css_selector("button.btn.btn-default.staging-push").click()
    #Click the Remove from Live button
    #browser.find_element_by_css_selector("button.btn.btn-default.staging-remove").click()
    browser.get(server_url + prefix + 'dataload/')
    assert 'now' in browser.find_element_by_tag_name('body').text or \
        'second ago' in browser.find_element_by_tag_name('body').text or \
        'seconds ago' in browser.find_element_by_tag_name('body').text

    

