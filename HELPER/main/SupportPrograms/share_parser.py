import requests
from bs4 import BeautifulSoup


def share_rate_parser(name: str, a=1):
    """
    Parses the stock prices from Google search results for a list of stock symbols.
    """

    # Define cookies for the HTTP request
    cookies = {
        'SEARCH_SAMESITE': 'CgQIm5sB',
        'receive-cookie-deprecation': '1',
        '__Secure-ENID': '20.SE=GD0zRuDOFSKbIhXBAqtSDqOW4njQ19UEXf2ov1NSygkMRn7E6kAt5clULSEK_ZX3fFosJ3c8C9FXCf03iBEPf6XjACL7o8FSrvnDO1k80ih3qSvVQD751xuULzHNLZqZL2un5FHkW3TUyQAOe_0pzHiJVZeY9NGIbW8me9_hRks',
        'SID': 'g.a000lAjTgjYdMsM_WjPKN98BUphTkYVHMFHU37dNcquW7_3bsTE-fYBKcQzF7IfeRXkeBSmMYwACgYKAc4SARISFQHGX2MiV4TZXyaXO9eqIVq5h_bESRoVAUF8yKp4CITVov7a1UWlhvdXGypo0076',
        '__Secure-1PSID': 'g.a000lAjTgjYdMsM_WjPKN98BUphTkYVHMFHU37dNcquW7_3bsTE-nKBqTzbxDg-MSjxPkUUs7wACgYKAWsSARISFQHGX2Mi-afdd25tNBHo2nsuE1ZO3BoVAUF8yKr1a2GbWFFsrhK0W5s7h8hR0076',
        '__Secure-3PSID': 'g.a000lAjTgjYdMsM_WjPKN98BUphTkYVHMFHU37dNcquW7_3bsTE-63sMBkpkFSwB1EZoTFkelwACgYKAZ0SARISFQHGX2MivhW41ElZqW3sZm3c4VOishoVAUF8yKo8F9b_nfBlVTGotcKKosw_0076',
        'HSID': 'AKiIMTXGdgi1Yawm8',
        'SSID': 'AdU2qe_Kj5RjaAl5i',
        'APISID': 'D8noz0Qt5ZNkUoVz/ATLXyZGXUtJn5b3pg',
        'SAPISID': '0JeuGlphVZoJwzQg/AOukhJnwMd8jCguGu',
        '__Secure-1PAPISID': '0JeuGlphVZoJwzQg/AOukhJnwMd8jCguGu',
        '__Secure-3PAPISID': '0JeuGlphVZoJwzQg/AOukhJnwMd8jCguGu',
        'AEC': 'AQTF6Hw2WH3wJQCzBQQTAEiV-nurouXEkJKLEqvB9GHgij-M7opuxteSB58',
        'NID': '515=WxCeFOcKeOKJvzc8B66a3E48gmnCvkraY5AYpP6KLHtCo4e5CuBPoGn17a97fUZT8S-3q_nS6x6X-Qq41GRWHs1zkDyLaqAcvBg_SDstETU-W1--46zDhA3RFuSynAT-_-w0u9WPXzEVv6NkLyQd1uD8cFa9A4mVr2zerPE2it9B3Q70iin22dNLgz1AUUDoVsdWYeIAzouj5DcHOAl5GsiRSyPAEce9AtL_QgIhiKO_jI3HLHYrMFmU9yjqC0FfuUZTVnnrbWzcJhbOne0YevT9uwKVQvpVSary_UfvdgKzvD1RnBLEZFw8CwsnR_wSmIAKABN3ApHU-7ivP2j4veO3oAv64lGjZ-eFmGrqDFlQvLGW8gHW6jyvNbRDffYVZSfKC-OyrnwGQqx6JEJHi6caacQOu0OMKSuHYqEDpKZVDxoSMQuRtL64LaFc6-_sxQhlHIOVWNVjChfIqisGpi7tXFq6dp08Ac8ZRUNP0Rluhbg7WckO0NyQn-PuqCOL',
        'DV': 'E0icvrStCcBdgPVShWwBWS9uLb4MBVmdS42dMzB-6AMAAEAIMU5ewDV2EAEAADSuK0_N0U9ZSAAAAPsO5o687XqkFAAAAA',
        '__Secure-1PSIDTS': 'sidts-CjIB3EgAErccYTIlQWIRb0eMv8C6o23gWbFK2QQb3svCyRI68kxWNKE0uMNMxRHi7Qv_HhAA',
        '__Secure-3PSIDTS': 'sidts-CjIB3EgAErccYTIlQWIRb0eMv8C6o23gWbFK2QQb3svCyRI68kxWNKE0uMNMxRHi7Qv_HhAA',
        'SIDCC': 'AKEyXzWB0cedbhqVqSaSx-ulHnmBJoMtHCu2wuxZTnTbbk0IC2wQKATv6UL6KHDhFeLZzUn6toM',
        '__Secure-1PSIDCC': 'AKEyXzUBeqYilsCuD4oa5YEbhRG-2qaR93cBMdr9en5Sd3LKdwXrSQ_Z2xCixn-CMNlISUSh6Ng',
        '__Secure-3PSIDCC': 'AKEyXzXziKYNmuIYE4Afepz0A6bGqHOpkEhmnNrWACoAe7X2SPiEO0lTjF2vTI14hQ3wS8KnFA',
    }
    # Define headers for the HTTP request
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        # 'cookie': '...cookie string...', # Uncomment if cookies are required
        'priority': 'u=0, i',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"126.0.6478.114"',
        'sec-ch-ua-full-version-list': '"Not/A)Brand";v="8.0.0.0", "Chromium";v="126.0.6478.114", "Google Chrome";v="126.0.6478.114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"15.0.0"',
        'sec-ch-ua-wow64': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'x-client-data': 'CIS2yQEIo7bJAQipncoBCPmBywEIlaHLAQiFoM0BCOmTzgEI45fOAQjym84BCMadzgEIs5/OAQj9oM4BCKaizgEY9snNARjX680BGKGdzgE=',
    }
    # Parameters for the Google search query
    params = {
        'q': f'стоимость акции {name}',  # Query string: stock price for symbol `i`
        'sca_esv': '37db28bfa134011b',
        'sxsrf': 'ADLYWIJSmHy5HsPdFrpsYxXBDx0CUmQoYA:1719341554694',
        'ei': '8hF7ZvGPKo3GwPAP1vKMmAM',
        'oq': 'стоимость акции go',
        'gs_lp': 'Egxnd3Mtd2l6LXNlcnAiINGB0YLQvtC40LzQvtGB0YLRjCDQsNC60YbQuNC4IGdvKgIIADIEECMYJzIFEAAYgAQyCBAAGKIEGIkFMggQABiABBiiBEjWKVC8A1j_EXABeAGQAQGYAYMDoAHUBqoBBTYuMy0xuAEByAEA-AEBmAIHoALyA8ICChAAGLADGNYEGEfCAg0QABiABBiwAxhDGIoFwgINECMYgAQYJxiKBRidAsICBhAAGBYYHsICEhAjGIAEGCcYigUYnQIYRhj6AcICHBAAGIAEGIoFGJ0CGEYY-gEYlwUYjAUY3QTYAQHCAggQABgWGB4YD5gDAIgGAZAGCroGBggBEAEYE5IHATegB9dE',
        'sclient': 'gws-wiz-serp',
    }

    # Perform the GET request
    try:
        response = requests.get('https://www.google.com/search', params=params, cookies=cookies, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')

        # Find the element containing the stock price
        prise_tag = soup.find_all('div', class_='PZPZlf')[2]

        # Extract and clean the stock price
        final_numb = str(prise_tag.text.split('USD')[0])

        return float(final_numb.replace(',', '.'))

    except:
         return None



if __name__ == '__main__':
    print(share_rate_parser("nvda"))
