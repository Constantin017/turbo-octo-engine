from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import requests_random_user_agent


def get_title(html):
    """Get page title"""
    title = None
    if html.title.string:
        title = html.title.string
    elif html.head.title.string:
        title = html.head.title.string
    return title


def get_h1(html:BeautifulSoup):
    """Get page H1 tag"""
    h1 = None
    if html.h1:
        h1 = html.h1.text.replace('\n', '')
    return h1


def get_h2(html):
    """Get page H2 tag"""
    h2 = None
    if html.h2:
        h2 = html.h2.text.replace('\n', '')
    return h2


def get_page_data(url):
    """Get page struct data url, title, h1, h2"""
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    return {
        "url": url,
        "title": get_title(soup),
        "h1": get_h1(soup),
        "h2": get_h2(soup),
    }


def is_valid_uri(uri):
    try:
        result = urlparse(url=uri)
        return all([result.scheme, result.netloc])
    except:
        return False


def get_links_data(links):
    results = []
    for url in links:
        if is_valid_uri(url):
            results.append(get_page_data(url))
    return results


def get_google_search_links(html):
    links = []
    _links = html.select('#search .r a')
    for link in _links:
        links.append(link.get('href'))
    return links[0:10]


def search(query):
    """Get search result from google search page be query"""
    results = None
    message = 'Error'
    url = "https://google.com/search?q="+query.replace(' ', '+')
    session = requests.Session()
    req = session.get(url)

    if req.status_code == 200:
        message = 'Success'
        google = BeautifulSoup(req.content, 'html.parser')
        links = get_google_search_links(google)
        results = get_links_data(links)

    return {
        "query": query,
        "url": url,
        "message": message,
        "results": results
    }
