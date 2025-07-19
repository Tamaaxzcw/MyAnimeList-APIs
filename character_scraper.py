import requests
from bs4 import BeautifulSoup

def search_character(query):
    """
    Mencari karakter di MyAnimeList dan mengambil data karakter pertama dari hasil pencarian.
    """
    try:
        # URL pencarian karakter di MyAnimeList
        url = f"https://myanimelist.net/character.php?q={query.replace(' ', '%20')}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Menemukan hasil pencarian pertama
        search_result = soup.find('td', class_='borderClass')
        if not search_result:
            return {"error": "Character not found"}

        character_url = search_result.find('a')['href']
        return get_character_details(character_url)

    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}

def get_character_details(url):
    """
    Mengambil detail dari halaman spesifik karakter.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        name = soup.find('h1', class_='title-name').text.strip()
        image_url = soup.find('td', class_='borderClass').find('img')['data-src']

        # Mengambil deskripsi
        content_div = soup.find('div', id='content')
        description_raw = content_div.find_all(text=True, recursive=False)
        description = ' '.join(t.strip() for t in description_raw if t.strip()).split('Voice Actors')[0].strip()

        # Mengambil animeography
        animeography = []
        anime_table = soup.find('table', class_='anime_character_related_anime')
        if anime_table:
            for row in anime_table.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) == 2:
                    anime_img = cells[0].find('img')['data-src']
                    anime_name = cells[1].find('a').text.strip()
                    anime_role = cells[1].contents[-1].strip()
                    animeography.append({
                        "name": anime_name,
                        "image_url": anime_img,
                        "role": anime_role
                    })

        return {
            "name": name,
            "url": url,
            "image_url": image_url,
            "description": description,
            "animeography": animeography
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}
    except Exception as e:
        return {"error": f"An error occurred while fetching details: {e}"}