import requests
from django.http import JsonResponse
from time import perf_counter


RESULT_MAPPING = { # Petite map pour vérifier le resultat d'une partie
    'win': 'win',
    'repetition': 'draw',
    'agreed': 'draw',
    'stalemate': 'draw',
    'insufficient': 'draw',
    '50move': 'draw',
    'timevsinsufficient': 'draw',
    'checkmated': 'lose',
    'timeout': 'lose',
    'resigned': 'lose',
    'lose': 'lose',
    'abandoned': 'lose'
}

def get_player_games(username, headers):
    url = f"https://api.chess.com/pub/player/{username}"
    headers = {
        "User-Agent": "ChessApp/1.0"  # Obligé de mettre un User-Agent sinon l'API refuse mon accès
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Retourne une erreur HTTP si il y a eu un soucis dans la requête
        return response.json()
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": f"Erreur lors de l'appel à l'API : {str(e)}"}, status=500)


def get_player_archives(username, headers):
    url = f"https://api.chess.com/pub/player/{username}/games/archives"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json() 
        return data.get('archives', [])  # Récupère la liste des archives, ou une liste vide
    except requests.exceptions.RequestException as e:
        return {"error": f"Erreur lors de l'appel à l'API pour les archives : {str(e)}"}


def analyse_game(result):
    return RESULT_MAPPING.get(result, '')


def compare_players(request, username1, username2):
    headers = {"User-Agent": "ChessApp/1.0"}
    start = perf_counter() # Je regarde marque un pointer au début de ma fonction pour calculer le temps de mon code

    try:
        user1 = get_player_games(username1, headers)
        user2 = get_player_games(username2, headers)

        if user1 and user2:

            # archives1 = user1.get('games/archives', []) ou user1['games']['archives']

            # Je voulais faire comme ça à la base mais l'API ne me renvoies rien
            # Je pense que https://api.chess.com/pub/player/{username}/ ne permets pas d'accéder aux archives, il faut direct aller sur l'url
            # correspondante de l'API :(
            # Je suis obligé de créer une fonction get_archives() même si ça fait du code pas propre

            archives1 = get_player_archives(username1, headers)


            stockage_games = []

            for archive_index in archives1: # Je parcours les archives du joueur 1

                response1 = requests.get(archive_index, headers=headers)
                response1.raise_for_status()
                games = response1.json().get('games', []) # Je récupère la partie de chaque archive

                for game in games:
                    if game['white']['username'] == username2 or game['black']['username'] == username2 or (game['white']['username'] == username2 and game['black']['username'] == username1):
                        stockage_games.append(game) # J'ajoute la partie à la liste des parties jouées

                results = []
                for game in stockage_games:
                    if game['white']['username'].strip().lower() == username1.strip().lower(): # Je dois nettoyer les username pour les comparer sinon ça marche pas
                        result = game['white'].get('result', [])
                        if result:
                            game_result = analyse_game(result)
                            results.append(game_result)
                    elif game['black']['username'].strip().lower() == username1.strip().lower():
                        result = game['black'].get('result', [])
                        if result:
                            game_result = analyse_game(result)
                            results.append(game_result)

            finish = perf_counter() # Fin du chrono pour estimé la performance de mon code    
            print(f"It took {finish-start} second(s) to finish.")            
            return JsonResponse({'Player1': user1, 'Player2': user2 ,'results': {
                'win': results.count('win'),
                'draw': results.count('draw'),
                'lose': results.count('lose'),
                'totalGames': len(results)
                } })

        
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": f"Erreur lors de l'appel à l'API : {str(e)}"}, status=500)