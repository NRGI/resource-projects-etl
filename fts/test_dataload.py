import pytest
from selenium import webdriver
import os
import time
import requests
import random
import string


server_url = os.environ['SERVER_URL']
prefix = '/'
dataset_url = None

@pytest.fixture(scope="module")
def browser(request):
    browser = webdriver.Firefox()
    browser.implicitly_wait(3)
    request.addfinalizer(lambda: browser.quit())
    return browser


@pytest.fixture(scope="module")
def google_doc_dataset(request, browser):
    source_url = 'https://docs.google.com/spreadsheets/d/1lZBVe6TGfrPYtaP4bqP9OZ0WG26vh_jTzOOm1h2Qdc4/edit#gid=0'

    browser.get(server_url + prefix)
    browser.find_element_by_id('id_source_url').send_keys(source_url)
    browser.find_element_by_css_selector("#fetchURL > div.form-group > button.btn.btn-primary").click()

    browser.find_element_by_id("name").send_keys('googledoc_test_' + ''.join(random.sample(string.ascii_lowercase, 10)))
    browser.find_element_by_id("submit").click()

    dataset_url = browser.current_url

    browser.find_element_by_css_selector("button.btn.btn-default.convert").click()

    return dataset_url


def test_googledoc_input(browser, google_doc_dataset):
    browser.get(google_doc_dataset)
    ttl_href = browser.find_element_by_link_text('Outputted TTL').get_attribute('href')
    assert 'Block 15' in requests.get(ttl_href).text


@pytest.mark.parametrize('process_id,other_process_id', [ ('staging', 'live'), ('live', 'staging') ])
def test_push(browser, google_doc_dataset, process_id, other_process_id):
    browser.find_element_by_css_selector("button.btn.btn-default.{}".format(process_id)).click()
    # Check if it's in
    url = os.environ.get('SPARQL_ENDPOINT', 'http://localhost:8890/sparql') + '?default-graph-uri=&query=select+%3Fs+WHERE+%7B+%3Fs+a+%3Chttp%3A%2F%2Fresourceprojects.org%2Fdef%2FProject%3E+%7D&format=application%2Fsparql-results%2Bjson&timeout=0&debug=on'
    assert 'resourceprojects.org' in requests.get(url, headers={'Host': process_id}).text
    if other_process_id != 'staging':
        assert 'resourceprojects.org' not in requests.get(url, headers={'Host': other_process_id}).text
    browser.find_element_by_css_selector("button.btn.btn-default.rm_{}".format(process_id)).click()
    assert 'resourceprojects.org' not in requests.get(url, headers={'Host': process_id}).text


def test_humanize_naturaltime(browser):
    '''
      This test loads a file from a url into the resourceprojects interface.
      You should then be taken to a /dataload/x page
      Click the each of the 'X now' buttons in turn
      Check to see that the status message is filtered by the naturaltime filter
    '''

    source_url = 'https://raw.githubusercontent.com/NRGI/resource-projects-etl/ee55c2956d23ebfc7a71cb1994a149d966a3c2a7/fts/fixtures/statoil-4-rows.csv'

    browser.get(server_url + prefix)
    browser.find_element_by_id('id_source_url').send_keys(source_url)
    browser.find_element_by_css_selector("#fetchURL > div.form-group > button.btn.btn-primary").click()

    browser.find_element_by_id("name").send_keys('test_' + ''.join(random.sample(string.ascii_lowercase, 10)))
    browser.find_element_by_id("submit").click()

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



    

