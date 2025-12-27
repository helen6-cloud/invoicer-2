import requests
import time

titles = [
    "Interstellar", "Inception", "The Dark Knight", "The Prestige",
    "Breaking Bad", "Stranger Things", "The Godfather", "Pulp Fiction",
    "The Last of Us", "Succession", "Gladiator", "The Bear",
    "Avatar", "Better Call Saul", "Fight Club", "The Sopranos",
"The Shawshank Redemption", "The Godfather", "The Godfather Part II", "The Dark Knight",
    "12 Angry Men", "Schindler's List", "The Lord of the Rings: The Return of the King",
    "Pulp Fiction", "The Good, the Bad and the Ugly", "Forrest Gump", "Fight Club",
    "Inception", "The Lord of the Rings: The Fellowship of the Ring", "The Matrix",
    "Goodfellas", "One Flew Over the Cuckoo's Nest", "Se7en", "Interstellar",
    "The Silence of the Lambs", "Saving Private Ryan", "The Green Mile", "Life is Beautiful",
    "The Usual Suspects", "Léon: The Professional", "Gladiator", "The Lion King",
    "American History X", "The Departed", "The Prestige", "Whiplash", "The Intouchables",
    "Parasite", "The Pianist", "Django Unchained", "Spider-Man: Across the Spider-Verse",

    # --- POPÜLER DİZİLER ---
    "Breaking Bad", "Game of Thrones", "The Sopranos", "The Wire", "Better Call Saul",
    "The Last of Us", "Succession", "The Bear", "Chernobyl", "Sherlock", "Fargo",
    "True Detective", "Stranger Things", "The Crown", "Narcos", "Black Mirror",
    "Mindhunter", "The Boys", "The Mandalorian", "Ted Lasso", "House of the Dragon",
    "The Witcher", "Squid Game", "Money Heist", "The Queen's Gambit", "Dark",
    "Peaky Blinders", "Vikings", "The Office", "Friends", "How I Met Your Mother",

    # --- BİLİM KURGU & FANTASTİK ---
    "Blade Runner 2049", "Arrival", "Dune", "Avatar", "Avatar: The Way of Water",
    "Star Wars: Episode IV - A New Hope", "The Empire Strikes Back", "Star Wars: Episode VI - Return of the Jedi",
    "Back to the Future", "Mad Max: Fury Road", "Jurrasic Park", "The Truman Show",
    "Eternal Sunshine of the Spotless Mind", "Everything Everywhere All at Once",

    # --- AKSİYON & SUÇ ---
    "John Wick", "Heat", "Die Hard", "The Dark Knight Rises", "Batman Begins",
    "Kill Bill: Vol. 1", "Kill Bill: Vol. 2", "Snatch", "The Wolf of Wall Street",
    "Casino", "Scarface", "No Country for Old Men", "Oldboy", "Sicario",

    # --- ANİMASYON ---
    "Spirited Away", "Spider-Man: Into the Spider-Verse", "Coco", "Toy Story",
    "Finding Nemo", "Up", "WALL-E", "How to Train Your Dragon", "Ratatouille",
    "Shrek", "Monsters, Inc.", "Inside Out", "Kimi no Na wa", "Princess Mononoke",

    # --- KORKU & GERİLİM ---
    "The Shining", "Psycho", "Alien", "Aliens", "The Thing", "Get Out",
    "The Sixth Sense", "Shutter Island", "Prisoners", "Memento", "The Others"
]

url = "http://127.0.0.1:8000/api/add-from-omdb/"

print(f"--- {len(titles)} içerik ekleme işlemi başlıyor ---\n")

for title in titles:
    data = {"title": title}
    try:
        response = requests.post(url, json=data)
        if response.status_code == 201:
            print(f"✅ Başarılı: {title}")
        else:
            print(f"❌ Hata ({title}): {response.json().get('error', 'Bilinmeyen hata')}")
    except Exception as e:
        print(f"⚠️ Bağlantı Hatası ({title}): {e}")

    # OMDb API'yi ve sunucuyu yormamak için kısa bir bekleme
    time.sleep(1)

print("\n--- İşlem Tamamlandı ---")