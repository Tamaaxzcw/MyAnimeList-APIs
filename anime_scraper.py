import requests
from bs4 import BeautifulSoup

def search_anime(query):
    """
    Mencari anime di MyAnimeList dan mengambil detail dari hasil pertama.
    """
    try:
        # URL pencarian anime
        url = f"https://myanimelist.net/anime.php?q={query.replace(' ', '%20')}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Menemukan hasil pencarian pertama
        search_result = soup.find('div', class_='js-categories-seasonal')
        if not search_result:
             return {"error": "Anime not found"}

        anime_link = search_result.find('a', class_='hoverinfo_trigger')['href']
        return get_anime_details(anime_link)

    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}

def get_anime_details(url):
    """
    Mengambil detail dari halaman spesifik anime.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.find('h1', class_='title-name').text.strip()
        image_url = soup.find('img', itemprop='image')['data-src']
        synopsis = soup.find('p', itemprop='description').text.strip()
        score = soup.find('div', class_='score-label').text.strip()

        # Mengambil info lainnya
        info = {}
        left_side = soup.find('div', class_='leftside')
        for div in left_side.find_all('div', class_='spaceit_pad'):
            key = div.find('span', class_='dark_text').text.strip().replace(':', '')
            value = ' '.join(span.text.strip() for span in div.find_all('span')[1:])
            info[key.lower()] = value.strip()

        return {
            "title": title,
            "url": url,
            "image_url": image_url,
            "synopsis": synopsis,
            "score": float(score) if score != 'N/A' else None,
            "information": info
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}
    except Exception as e:
        return {"error": f"An error occurred while fetching details: {e}"}