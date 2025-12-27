import requests
import time
URL = "http://127.0.0.1:8000/api/add_title_from_omdb/"

yabanci_diziler = [
    "The Bear", "Succession", "The White Lotus", "Beef", "The Last of Us", "House of the Dragon",
    "Andor", "The Mandalorian", "Ted Lasso", "Severance", "Squid Game", "Dark", "Mindhunter",
    "Narcos: Mexico", "Peaky Blinders", "Vikings", "The Boys", "Invincible", "Arcane",
    "The Queen's Gambit", "Fleabag", "Ozark", "Better Call Saul", "Fargo", "Yellowstone",
    "The Crown", "Stranger Things", "Cobra Kai", "The Witcher", "The Sandman", "Euphoria",
    "Money Heist", "Elite", "Lupin", "Kingdom", "Crash Landing on You", "The Glory",
    "All of Us Are Dead", "Vincenzo", "Signal", "Stranger", "My Mister", "Alchemy of Souls"
]

yabanci_filmler = [
    "Inception", "Interstellar", "The Matrix", "The Dark Knight", "Blade Runner 2049", "Dune", "Arrival",
    "The Martian", "Gravity", "Avatar", "Star Wars: A New Hope", "The Empire Strikes Back",
    "The Lord of the Rings: The Fellowship of the Ring", "The Lord of the Rings: The Two Towers",
    "The Lord of the Rings: The Return of the King", "Harry Potter and the Sorcerer's Stone",
    "The Prestige", "Tenet", "The Fifth Element", "Edge of Tomorrow", "District 9", "Looper",

    "The Shawshank Redemption", "The Godfather", "The Godfather Part II", "Pulp Fiction", "Schindler's List",
    "Fight Club", "Forrest Gump", "Goodfellas", "The Silence of the Lambs", "Se7en", "The Green Mile",
    "The Departed", "The Pianist", "American History X", "Leon: The Professional", "Gladiator",
    "Joker", "Parasite", "Once Upon a Time in Hollywood", "The Wolf of Wall Street", "Taxi Driver",
    "Scarface", "The Usual Suspects", "Heat", "No Country for Old Men", "Prisoners", "Nightcrawler",

    "Mad Max: Fury Road", "John Wick", "Gladiator", "Top Gun: Maverick", "Mission: Impossible - Fallout",
    "Kill Bill: Vol. 1", "Kill Bill: Vol. 2", "The Bourne Identity", "Casino Royale", "Skyfall",
    "Fast & Furious", "Die Hard", "Terminator 2: Judgment Day", "Aliens", "Indiana Jones: Raiders of the Lost Ark",
    "The Revenant", "Extraction", "Greyhound", "Baby Driver", "The Fugitive", "Taken",

    "Shutter Island", "Memento", "The Sixth Sense", "Gone Girl", "The Truman Show",
    "Eternal Sunshine of the Spotless Mind",
    "Oldboy", "A Clockwork Orange", "Black Swan", "The Illusionist", "Vanilla Sky", "Mulholland Drive",
    "Gone Baby Gone", "The Girl with the Dragon Tattoo", "Donnie Darko", "Arrival", "Split", "Glass",

    "The Lion King", "Toy Story", "Spirited Away", "Spider-Man: Into the Spider-Verse", "Coco", "Up",
    "WALL-E", "How to Train Your Dragon", "Shrek", "Finding Nemo", "Ratatouille", "The Incredibles",
    "Kimi no Na wa", "Princess Mononoke", "Soul", "Inside Out", "Zootopia", "Frozen",

    "Saving Private Ryan", "1917", "Dunkirk", "Braveheart", "Inglourious Basterds", "Hacksaw Ridge",
    "Full Metal Jacket", "Apocalypse Now", "The Last Samurai", "Troy", "300", "All Quiet on the Western Front",
    "Fury", "Letters from Iwo Jima", "Bridge of Spies", "The King's Speech", "Lincoln",

    "The Grand Budapest Hotel", "The Hangover", "Superbad", "The Big Lebowski", "The Nice Guys",
    "Deadpool", "Deadpool 2", "La La Land", "About Time", "500 Days of Summer", "Before Sunrise",
    "Before Sunset", "Before Midnight", "The Notebook", "Crazy Rich Asians", "Mean Girls",
    "The 40-Year-Old Virgin", "The Intouchables", "Green Book", "Jojo Rabbit",

    "Oppenheimer", "Barbie", "Everything Everywhere All At Once", "The Batman", "Poor Things",
    "Anatomy of a Fall", "The Zone of Interest", "The Banshees of Inisherin", "Top Gun: Maverick",
    "Bullet Train", "Spider-Man: Across the Spider-Verse", "The Whale", "Babylon", "Elvis",
    "Glass Onion", "The Menu", "Prey", "The Northman", "Tár", "Triangle of Sadness",

    "Requiem for a Dream", "Trainspotting", "Snatch", "Lock, Stock and Two Smoking Barrels",
    "Reservoir Dogs", "The Hateful Eight", "Whiplash", "Slumdog Millionaire", "Life is Beautiful",
    "Gran Torino", "Million Dollar Baby", "The Social Network", "The Big Short", "Moneyball",
    "Spotlight", "Ford v Ferrari", "Hidden Figures", "Bohemian Rhapsody", "Rocketman"
    "The Green Mile", "The Pianist", "City of God", "The Silence of the Lambs", "Schindler's List",
    "Green Book", "Joker", "The Wolf of Wall Street", "Goodfellas", "Casino", "Heat", "Scarface",
    "Taxi Driver", "The Departed", "Snatch", "Lock, Stock and Two Smoking Barrels", "Gran Torino",
    "Prisoners", "Nightcrawler", "Gone Girl", "The Hateful Eight", "Once Upon a Time in Hollywood",
    "Tenet", "Dunkirk", "Blade Runner 2049", "Arrival", "Dune", "Prometheus", "The Martian",
    "Gravity", "Ex Machina", "Looper", "Source Code", "Edge of Tomorrow", "Mad Max: Fury Road",
    "Logan", "Deadpool", "Gladiator", "Braveheart", "The Last of the Mohicans", "300",
    "John Wick", "John Wick: Chapter 2", "John Wick: Chapter 3", "Extraction", "Top Gun: Maverick",
    "The Lion King", "Finding Nemo", "Toy Story 3", "Toy Story 4", "Inside Out", "Zootopia",
    "Soul", "Up", "WALL-E", "Ratatouille", "The Incredibles", "Spider-Man: Into the Spider-Verse",
    "Spider-Man: Across the Spider-Verse", "How to Train Your Dragon", "Kung Fu Panda", "Shrek 2",
    "Hereditary", "Midsommar", "The Conjuring", "A Quiet Place", "Get Out", "Us", "The Invisible Man",
    "Sinister", "Insidious", "The Ring", "The Sixth Sense", "The Others", "Split", "Glass",
    "The Grand Budapest Hotel", "Moonrise Kingdom", "The Truman Show", "Big Fish", "La La Land",
    "Whiplash", "Birdman", "The Revenant", "Ford v Ferrari", "1917", "All Quiet on the Western Front",
    "Parasite", "Oldboy", "Another Round", "Roma", "Seven Samurai", "Amelie", "The Platform"
]
turk_dizileri = [
    "Şahsiyet", "Ezel", "Leyla ile Mecnun", "Behzat Ç.", "Avrupa Yakası", "İkinci Bahar", "Yedi Numara", "Asmalı Konak",
    "Kuzey Güney", "Aşk-ı Memnu", "Muhteşem Yüzyıl", "Bir Başkadır", "Masum", "Fi", "Hakan: Muhafız", "Atiye",
    "Fatmagül'ün Suçu Ne?", "Yaprak Dökümü", "Elveda Rumeli", "Suskunlar", "İçerde", "Çukur", "Diriliş: Ertuğrul",
    "Kuruluş: Osman", "Yargı", "Gibi", "Ayak İşleri", "Prens", "Mevzu Derin", "Bozkır", "Sıfır Bir", "Kurtlar Vadisi",
    "Ekmek Teknesi", "En Son Babalar Duyar", "Tatlı Hayat", "Şahsiyet", "Kulüp", "Terzi", "Zeytin Ağacı", "Kuş Uçusu",
    "Şahmaran", "Kızılcık Şerbeti", "Yalı Çapkını", "Gönül Dağı", "Teşkilat", "Arka Sokaklar", "Kavak Yelleri",
    "Poyraz Karayel", "Medcezir", "Ufak Tefek Cinayetler", "Vatanım Sensin", "Karadayı", "Muhteşem Yüzyıl: Kösem",
    "Paramparça", "Kara Sevda", "Kiralık Aşk", "Erkenci Kuş", "Sen Çal Kapımı", "Bay Yanlış", "Dolunay", "Her Yerde Sen",
    "Afili Aşk", "Aşkın Tarifi", "Camdaki Kız", "Masumlar Apartmanı", "Kırmızı Oda", "Sadakatsiz", "Mucize Doktor",
    "Hekimoğlu", "Babil", "Şeref Bey", "Hükümsüz", "Saygı", "Alef", "Börü", "Söz", "Savaşçı", "Nöbet", "Alparslan: Büyük Selçuklu",
    "Uyanış: Büyük Selçuklu", "Barbaroslar", "Destan", "Veda Mektubu", "Adım Farah", "Aile", "Ömer", "Çöp Adam",
    "Gülcemal", "Tetikçinin Oğlu", "Kuzgun", "Çarpışma", "Siyah Beyaz Aşk", "Cesur ve Güzel", "Anne", "Kadın", "Bizim Hikaye",
    "Mucize Doktor", "Zalim İstanbul", "Hercai", "Sefirin Kızı", "Son Yaz", "Alev Alev", "Akrep", "Maraşlı", "Cam Tavanlar",
    "Ada Masalı", "Aşk Mantık İntikam", "Baht Oyunu", "Kalp Yarası", "İkimizin Sırrı", "Uzak Şehrin Masalı", "İçimizden Biri",
    "Yalancı", "Elbet Bir Gün", "Aziz", "Alparslan: Büyük Selçuklu", "Mahkum", "Annenin Sırrıdır Çocuk", "İyilik",
    "Seversin", "Senden Daha Güzel", "Tozluyaka", "Gelsin Hayat Bildiği Gibi", "Duy Beni", "Kusur", "Bir Peri Masalı",
    "Aldatmak", "Ben Bu Cihana Sığmazam", "O Kız", "Tuzak", "Yürek Çıkmazı", "Sipahi", "Sancaktar", "EGO", "Adım Farah",
    "Kızıl Goncalar", "Bahar", "İnci Taneleri", "Gaddar", "Kara Ağaç Destanı", "Taş Kağıt Makas", "Yaban Çiçekleri",
    "Mehmed: Fetihler Sultanı", "Aziz Mahmud Hüdayi", "Korkma Ben Yanındayım", "Yanımda Kal", "Dönence", "Ruhun Duymaz",
    "Kendi Düşen Ağlamaz", "Yaz Şarkısı", "Vermem Seni Ellere", "Hayatımın Neşesi", "Benim Güzel Ailem", "Maviye Sürgün",
    "Taçsız Prenses", "Adım Farah", "EGO", "Gülümse Kaderine", "İyilik", "Kasaba Doktoru", "Kusursuz Kiracı",
    "Bir Küçük Gün Işığı", "Gecenin Ucunda", "Yürek Çıkmazı", "Sipahi", "Sıfırıncı Gün", "Al Sancak", "Dokuz Oğuz",
    "Adım Farah", "EGO", "Tetikçinin Oğlu", "Gülcemal", "Maviye Sürgün", "Kendi Düşen Ağlamaz", "Dönence",
    "Ruhun Duymaz", "Yaz Şarkısı", "Vermem Seni Ellere", "Benim Güzel Ailem", "Hayatımın Neşesi", "Bambaşka Biri",
    "Dilek Taşı", "Yabani", "Kirli Sepeti", "Kader Bağları", "Şahane Hayatım", "Ne Gemiler Yaktım", "Aşka Düşman"
]
turk_filmleri = [

    "Züğürt Ağa", "Çiçek Abbas", "Namuslu", "Banker Bilo", "Şalvar Davası", "Gurbetçi Şaban", "Katma Değer Şaban",
    "Pehlivan", "Sürü", "Anayurt Oteli", "Gizli Yüz", "Kara Köpekler Havlarken", "Vavien", "Korkuyorum Anne",
    "Kosmos", "Pandora'nın Kutusu", "Güneşe Yolculuk", "Bulantı", "Yeraltı", "Bekleme Odası", "İtirazım Var",
    "Limonata", "Uzaklarda Arama", "Sarmaşık", "Gişe Memuru", "Toll Booth", "Kelebekler", "Sibel", "Nuh Tepesi",
    "Görülmüştür", "Ceviz Ağacı", "Beni Çok Sev", "Geçen Yaz", "Aşıklar Bayramı", "Gönül", "Boğa Boğa",

    "Gora", "Arog", "Yahşi Batı", "Pek Yakında", "Ali Baba ve 7 Cüceler", "Arif V 216", "Karakomik Filmler 1",
    "Karakomik Filmler 2", "Hokkabaz", "Hacivat Karagöz Neden Öldürüldü?", "Neredesin Firuze", "Eyyvah Eyvah",
    "Eyyvah Eyvah 2", "Eyyvah Eyvah 3", "Berlin Kaplanı", "Olanlar Oldu", "Hedefim Sensin", "Bursa Bülbülü",
    "Düğün Dernek", "Düğün Dernek 2: Sünnet", "Çalgı Çengi", "Çalgı Çengi İkimiz", "Ailecek Şaşkınız",
    "Baba Parası", "Selçuk Aydemir", "Ölümlü Dünya", "Cinayet Süsü", "Bayi Toplantısı", "Yol Arkadaşım",
    "Kardeşim Benim", "Kardeşim Benim 2", "Dönerse Senindir", "Tatlım Tatlım", "Maide'nin Altın Günü",
    "Görümce", "Deliha", "Deliha 2", "Cici Babam", "Küçük Esnaf", "Kolpaçino", "Kolpaçino: Bomba",
    "Kolpaçino 3. Devre", "Kutsal Damacana", "Kutsal Damacana 2", "Kutsal Damacana: Dracoola",
    "Hep Yek", "Hep Yek 2", "Hep Yek 3", "Maskeli Beşler: İntikam Peşinde", "Maskeli Beşler: Irak",
    "Maskeli Beşler: Kıbrıs", "G.D.O. KaraKedi", "Vay Arkadaş", "Çakallarla Dans", "Çakallarla Dans 2",
    "Çakallarla Dans 3", "Çakallarla Dans 4", "Çakallarla Dans 5", "Çakallarla Dans 6",

    "Issız Adam", "Dedemin İnsanları", "Babam ve Oğlum", "Unutursam Fısılda", "Tamam mıyız?", "Prensesin Uykusu",
    "Aşk Tesadüfleri Sever", "Aşk Tesadüfleri Sever 2", "İncir Reçeli", "İncir Reçeli 2", "Bi Küçük Eylül Meselesi",
    "Hadi Be Oğlum", "Delibal", "Sadece Sen", "Evim Sensin", "Su ve Ateş", "İkimizin Yerine", "Sonsuz Aşk",
    "Kocan Kadar Konuş", "Kocan Kadar Konuş: Diriliş", "Ekşi Elmalar", "Görümce", "Cebimdeki Yabancı",
    "Ayla", "Müslüm", "Naim", "Bergen", "Dilberay", "7. Koğuştaki Mucize", "Bizim İçin Şampiyon",
    "Kelebeğin Rüyası", "Aşkın Kıyameti", "Yolun Açık Olsun", "Beni Çok Sev", "Kâğıttan Hayatlar",

    "Av Mevsimi", "Ejder Kapanı", "Kabadayı", "Börü", "Dağ", "Dağ 2", "Nefes: Vatan Sağolsun",
    "49", "Teşkilat", "Söz", "Kurtlar Vadisi Irak", "Kurtlar Vadisi Gladio", "Kurtlar Vadisi Filistin",
    "Kurtlar Vadisi Vatan", "Behzat Ç. Seni Kalbime Gömdüm", "Behzat Ç. Ankara Yanıyor",

    "Kuru Otlar Üstüne", "Ahlat Ağacı", "Kış Uykusu", "Bir Zamanlar Anadolu'da", "Üç Maymun",
    "İklimler", "Uzak", "Mayıs Sıkıntısı", "Kasaba", "Kader", "Masumiyet", "Yeraltı", "Bulantı",
    "Zerre", "Tepenin Ardı", "Abluka", "Emin Alper", "Kurak Günler", "Okul Tıraşı", "İki Şafak Arasında",
    "Bambaşka Bir Dünya", "Sen Ben Lenin", "Beni Sevenler Listesi", "Zuhal", "Çatlak", "Okul Tıraşı",
    "Bağlılık Aslı", "Bağlılık Hasan", "Kovan", "Hayaletler", "Gölgeler İçinde", "Aşk, Büyü vs.",
    "Propaganda", "Komser Şekspir", "Vizontele", "Vizontele Tuuba", "Gönül Yarası", "Dünyayı Kurtaran Adam",
    "Tarkan: Gümüş Eyer", "Tarkan: Viking Kanı", "Karaoğlan", "Battal Gazi Destanı", "Malkoçoğlu",
    "Hababam Sınıfı Merhaba", "Hababam Sınıfı Askerde", "Hababam Sınıfı Üç Buçuk", "Hababam Sınıfı Yeniden",
    "Dondurmam Gaymak", "Entelköy Efeköy'e Karşı", "Hükümet Kadın", "Hükümet Kadın 2", "Sümela'nın Şifresi: Temel",
    "Moskova'nın Şifresi: Temel", "Oflu Hoca'nın Şifresi", "Sağ Salim", "Sağ Salim 2: Sil Baştan",
    "Mandıra Filozofu", "Mandıra Filozofu İstanbul", "Limonata", "Ali Kundilli", "Ali Kundilli 2",
    "Cumali Ceber", "Enes Batur Hayal mi Gerçek mi?", "Kötü Çocuk", "4N1K", "4N1K 2", "Aşk Taktikleri",
    "Aşk Taktikleri 2", "Sen Yaşamaya Bak", "Merve Kült", "Aaahh Belinda", "Tamirhane", "Hava Muhalefeti",
    "Güven Bana", "Özel Ders", "Yılbaşı Gecesi", "Cici", "Azizler", "9 Kere Leyla", "Karakomik Filmler: Deli",
    "Karakomik Filmler: Emanet"
    "Hababam Sınıfı", "Tosun Paşa", "Süt Kardeşler", "Çöpçüler Kralı", "Kibar Feyzo", "Selvi Boylum Al Yazmalım",
    "Yol", "Umut", "Duvar", "Susuz Yaz", "Muhsin Bey", "Eşkiya", "Her Şey Çok Güzel Olacak", "G.O.R.A.", "Vizontele",
    "Babam ve Oğlum", "Issız Adam", "Kaybedenler Kulübü", "Neredesin Firuze", "Hacivat Karagöz Neden Öldürüldü?",
    "Kış Uykusu", "Bir Zamanlar Anadolu'da", "Uzak", "İklimler", "Mayıs Sıkıntısı", "Ahlat Ağacı", "Kader", "Masumiyet",
    "Zeki Demirkubuz", "Gemide", "Laleli'de Bir Azize", "Tabutta Rövaşata", "Ağır Roman", "Mustang", "Sivas",
    "Kelebeğin Rüyası", "Ayla", "Müslüm", "Cep Herkülü: Naim Süleymanoğlu", "7. Koğuştaki Mucize", "Bergen",
    "Kurak Günler", "Okul Tıraşı", "Nefes: Vatan Sağolsun", "Dağ", "Dağ II", "Börü", "Kurtlar Vadisi: Irak",
    "Av Mevsimi", "Gönül Yarası", "Kabadayı", "Ejder Kapanı", "Organize İşler", "Organize İşler: Sazan Sarmalı",
    "Hokkabaz", "Yahşi Batı", "Pek Yakında", "Arif V 216", "Karakomik Filmler", "Aile Arasında", "Ölümlü Dünya",
    "Ölümlü Dünya 2", "Cinayet Süsü", "Düğün Dernek", "Çalgı Çengi", "Ailecek Şaşkınız", "Bursa Bülbülü",
    "Eyvah Eyvah", "Eyvah Eyvah 2", "Eyvah Eyvah 3", "Berlin Kaplanı", "Olanlar Oldu", "Hedefim Sensin",
    "Recep İvedik", "Mucize", "Mucize 2: Aşk", "Beyaz Melek", "Güneşi Gördüm", "New York'ta Beş Minare",
    "Kelebekler", "Sarmaşık", "Gişe Memuru", "Anons", "Kız Kardeşler", "Tepenin Ardı", "Abluka", "Emin Alper",
    "Kar", "Mavi Dalga", "Şarkı Söyleyen Kadınlar", "Küskün Çiçekler", "Aşk Tesadüfleri Sever", "İncir Reçeli",
    "Bi Küçük Eylül Meselesi", "Unutursam Fısılda", "Delibal", "İkimizin Yerine", "Sonsuz Aşk", "Dünyanın En Güzel Kokusu",
    "Fakat Müzeyyen Bu Derin Bir Tutku", "Limonata", "Kocan Kadar Konuş", "Görümce", "Deliha", "Sadece Sen",
    "Evim Sensin", "Su ve Ateş", "İkinci Şans", "Mutluluk Zamanı", "Yanımda Kal", "Aşk Bu mu?", "Bize Müsaade",
    "Bayi Toplantısı", "Yol Arkadaşım", "Yol Arkadaşım 2", "Kardeşim Benim", "Kardeşim Benim 2", "Dönerse Senindir",
    "Tatlım Tatlım", "Ekşi Elmalar", "Görümce", "Deliha 2", "Cici Babam", "Hedefim Sensin", "Aman Reis Duymasın",
    "Hababam Sınıfı Yeniden", "Hababam Sınıfı Yaz Oyunları", "Maskeli Beşler", "Maskeli Beşler: Irak",
    "Maskeli Beşler: Kıbrıs", "Hababam Sınıfı Merhaba", "Hababam Sınıfı Askerde", "Hababam Sınıfı Üç Buçuk",
    "Kutsal Damacana", "Kutsal Damacana: Dracoola", "Kutsal Damacana: İtmen", "Kolpaçino", "Kolpaçino: Bomba",
    "Kolpaçino 3. Devre", "Hep Yek", "Hep Yek 2", "Hep Yek 3", "Cumali Ceber", "Enes Batur Hayal mi Gerçek mi?",
    "Siccin", "Siccin 2", "Siccin 3", "Siccin 4", "Siccin 5", "Siccin 6", "Musallat", "Musallat 2", "Dabbe",
    "Dabbe 2", "Dabbe: Bir Cin Vakası", "Dabbe: Cin Çarpması", "Dabbe: Zehr-i Cin", "Dabbe 6", "Magi",
    "Baskın", "Evdeki Yabancılar", "Seni Seviyorum Adamım", "Hadi Be Oğlum", "Can Feda", "Direniş Karatay",
    "Türk İşi Dondurma", "Cicero", "Annem", "Yedinci Koğuştaki Mucize", "Biz Böyleyiz", "Eltilerin Savaşı",
    "9 Kere Leyla", "Azizler", "Kağıttan Hayatlar", "Gönül", "Aşkın Kıyameti", "Cici", "Boğa Boğa",
    "Merve Kült", "Sen Yaşamaya Bak", "Kuluçka", "Aşk Taktikleri", "Özel Ders", "Aaahh Belinda", "Rüyanda Görürsün",
    "Bihter", "Adresi", "Atatürk 1881-1919", "Lohusa", "Kolpaçino 4 4'lük", "Mutluyuz", "Kardeş Takımı"
]
animeler = [
    "Death Note", "Attack on Titan", "Fullmetal Alchemist: Brotherhood", "Naruto", "Naruto: Shippuden",
    "One Piece", "Dragon Ball Z", "Dragon Ball", "Hunter x Hunter", "Steins;Gate",
    "Cowboy Bebop", "Neon Genesis Evangelion", "Code Geass", "Bleach", "Fairy Tail",
    "My Hero Academia", "One Punch Man", "Demon Slayer: Kimetsu no Yaiba", "Jujutsu Kaisen", "Tokyo Ghoul",
    "Sword Art Online", "No Game No Life", "Psycho-Pass", "Mob Psycho 100", "Haikyu!!",
    "Your Lie in April", "Anohana: The Flower We Saw That Day", "Clannad", "Clannad: After Story", "Toradora!",
    "Gintama", "Black Clover", "Vinland Saga", "The Rising of the Shield Hero", "That Time I Got Reincarnated as a Slime",
    "Re:Zero - Starting Life in Another World", "The Promised Neverland", "Made in Abyss", "Dr. Stone", "Fire Force",
    "Assassination Classroom", "Blue Exorcist", "Soul Eater", "Kill la Kill", "Gurren Lagann",
    "Akame ga Kill!", "Parasyte: The Maxim", "Deadman Wonderland", "Highschool of the Dead", "Mirai Nikki",
    "Samurai Champloo", "Trigun", "Hellsing Ultimate", "Black Butler", "Durarara!!",
    "Bungou Stray Dogs", "Noragami", "Blue Spring Ride", "Kimi ni Todoke", "Maid Sama!",
    "Ouran High School Host Club", "Fruits Basket", "Kamisama Kiss", "Say 'I Love You'", "Wolf Girl and Black Prince",
    "My Little Monster", "Nisekoi", "Golden Time", "Plastic Memories", "Angel Beats!",
    "Charlotte", "Guilty Crown", "Fate/Zero", "Fate/stay night: Unlimited Blade Works", "Berserk",
    "Claymore", "D.Gray-man", "InuYasha", "YuYu Hakusho", "Saint Seiya",
    "Sailor Moon", "Cardcaptor Sakura", "Digimon Adventure", "Pokémon", "Yu-Gi-Oh!",
    "Great Teacher Onizuka", "Slam Dunk", "Kuroko's Basketball", "Ace of Diamond", "Hajime no Ippo",
    "Monster", "Mushi-Shi", "Ergo Proxy", "Serial Experiments Lain", "Texhnolyze",
    "Darker than Black", "Baccano!", "Banana Fish", "Terror in Resonance", "Erased",
    "ReLIFE", "Orange", "March Comes in Like a Lion", "Chihayafuru", "Hyouka",
    "K-On!", "Lucky Star", "Azumanga Daioh", "Nichijou", "Daily Lives of High School Boys",
    "The Melancholy of Haruhi Suzumiya", "Bakemonogatari", "Monogatari Series: Second Season", "Oregairu", "Haganai",
    "A Lull in the Sea", "Violet Evergarden", "Ancient Magus' Bride", "Land of the Lustrous", "Houseki no Kuni",
    "Ranking of Kings", "Chainsaw Man", "SPY x FAMILY", "Blue Lock", "Hell's Paradise",
    "86 Eighty-Six", "Mushoku Tensei: Jobless Reincarnation", "Kaguya-sama: Love is War", "Horimiya", "My Dress-Up Darling",
    "Cyberpunk: Edgerunners", "Devilman Crybaby", "Castlevania", "Arcane", "DOTA: Dragon's Blood",
    "The Seven Deadly Sins", "Overlord", "Log Horizon", "Goblin Slayer", "Konosuba",
    "Danganronpa", "Persona 4 the Animation", "Persona 5 the Animation", "Devil is a Part-Timer!", "Noragami Aragoto",
    "Monthly Girls' Nozaki-kun", "Wotakoi: Love is Hard for Otaku", "Sk8 the Infinity", "Free!", "Yuri!!! on Ice",
    "Run with the Wind", "Stars Align", "Welcome to the Ballroom", "Bakuman.", "Silver Spoon",
    "Grand Blue Dreaming", "Prison School", "Shokugeki no Soma", "Yakitate!! Japan", "Food Wars!",
    "Beelzebub", "Gintama'", "Arakawa Under the Bridge", "The Disastrous Life of Saiki K.", "Sakamoto Desu ga?",
    "Great Pretender", "Lupin the Third", "City Hunter", "Fist of the North Star", "Rurouni Kenshin",
    "Dorohedoro", "Dankon no Suguru", "JoJo's Bizarre Adventure", "Stardust Crusaders", "Diamond is Unbreakable",
    "Golden Wind", "Stone Ocean", "Dororo", "Kingdom", "Arslan Senki",
    "Magi: The Labyrinth of Magic", "Magi: The Kingdom of Magic", "Sinbad no Bouken", "Seraph of the End", "Kabaneri of the Iron Fortress",
    "Aldnoah.Zero", "Mobile Suit Gundam", "Eureka Seven", "Darling in the Franxx", "SSSS.Gridman",
    "Vision of Escaflowne", "Magic Knight Rayearth", "Revolutionary Girl Utena", "Princess Tutu", "Puella Magi Madoka Magica"
]

kore_dizileri = [
    "Squid Game", "Kingdom", "Crash Landing on You", "The Glory", "All of Us Are Dead",
    "Vincenzo", "Signal", "Stranger", "My Mister", "Alchemy of Souls", "Goblin",
    "Descendants of the Sun", "Itaewon Class", "Business Proposal", "Hometown Cha-Cha-Cha",
    "Hotel Del Luna", "Mr. Sunshine", "Hospital Playlist", "Twenty-Five Twenty-One",
    "Extracurricular", "Move to Heaven", "Beyond Evil", "Flower of Evil", "Mouse",
    "The World of the Married", "Sky Castle", "Penthouse", "Healer", "Kill Me, Heal Me",
    "Strong Woman Do Bong-soon", "Weightlifting Fairy Kim Bok-joo", "Boys Over Flowers",
    "The King: Eternal Monarch", "It's Okay to Not Be Okay", "Start-Up", "Sweet Home",
    "Hellbound", "D.P.", "Taxi Driver", "Through the Darkness", "Weak Hero Class 1",
    "Reborn Rich", "Extraordinary Attorney Woo", "Under the Queen's Umbrella",
    "Little Women", "Big Mouth", "Our Blues", "My Liberation Notes", "Twenty Five Twenty One",
    "Snowdrop", "Youth of May", "Navillera", "Doom at Your Service", "Nevertheless",
    "My Name", "Sisyphus: The Myth", "The Silent Sea", "Juvenile Justice", "Tomorrow",
    "The Sound of Magic", "Anna", "Alchemy of Souls: Light and Shadow", "The Interest of Love",
    "Crash Course in Romance", "The Good Bad Mother", "Dr. Romantic", "Atypical Family",
    "Queen of Tears", "Marry My Husband", "Lovely Runner", "Connection", "The 8 Show",
    "Bloodhounds", "Gyeongseong Creature", "Death's Game", "Mask Girl", "Celebrity",
    "A Time Called You", "King the Land", "See You in My 19th Life", "Daily Dose of Sunshine",
    "Night Has Come", "Vigilante", "The Bequeathed", "A Killer Paradox", "Pyramid Game",
    "Doctor Slump", "Wonderful World", "Parasyte: The Grey", "Chief Detective 1958",
    "Frankly Speaking", "The Midnight Romance in Hagwon", "Dreaming of a Freaking Fairytale",
    "The Player 2: Master of Swindlers", "Hierarchy", "Miss Night and Day", "Sweet Home 2",
    "Gyeongseong Creature 2", "The Whirlwind", "Red Swan", "The Auditors", "Serendipity's Embrace",
    "Your Honor", "Pachinko", "The Frog", "No Gain No Love", "The Judge from Hell",
    "What Comes After Love", "Dear Hyeri", "Jeongnyeon: The Star Is Born", "A Virtuous Business",
    "Doubt", "Hellbound 2", "Brewing Love", "The Fiery Priest 2", "Mr. Plankton",
    "The Trunk", "When the Phone Rings", "Light Shop", "Squid Game 2", "Signal 2",
    "All of Us Are Dead 2", "Weak Hero Class 2", "Knock Off", "Hyper Knife", "Nine Puzzles",
    "Trigger", "Low Life", "The Mantis", "Whirlwind", "Mercy for None", "Black Salt Dragon",
    "Bunny and Her Boys", "My Dearest", "Moving", "Twinkling Watermelon", "Castaway Diva",
    "Perfect Marriage Revenge", "Moon in the Day", "The Story of Park's Marriage Contract",
    "Welcome to Samdal-ri", "Maestra: Strings of Truth", "Death's Game", "Like Flowers in Sand",
    "Gyeongseong Creature", "Marry My Husband", "Love Song for Illusion", "Knight Flower",
    "Captivating the King", "Flex X Cop", "Doctor Slump", "Branding in Seongsu",
    "A Killer Paradox", "The Impossible Heir", "Wonderful World", "Queen of Tears",
    "Chicken Nugget", "The Midnight Studio", "Hide", "The Escape of the Seven: Resurrection",
    "Parasyte: The Grey", "Lovely Runner", "Blood Free", "Missing Crown Prince",
    "Chief Detective 1958", "Goodbye Earth", "The Atypical Family", "Frankly Speaking",
    "The Midnight Romance in Hagwon", "Uncle Samsik", "The 8 Show", "Connection",
    "Dreaming of a Freaking Fairytale", "Hierarchy", "My Sweet Mobster", "Miss Night and Day",
    "The Whirlwind", "Red Swan", "The Auditors", "Good Partner", "Serendipity's Embrace",
    "No Way Out: The Roulette", "Bad Memory Eraser", "Romance in the House", "Your Honor",
    "Perfect Family", "Black Out", "Love Next Door", "Pachinko 2", "The Frog",
    "No Gain No Love", "Queen Woo", "The Judge from Hell", "What Comes After Love", "Dear Hyeri"
]

kore_filmleri = [
    "Parasite", "Oldboy", "The Handmaiden", "Train to Busan", "Memories of Murder",
    "The Wailing", "A Taxi Driver", "I Saw the Devil", "The Man from Nowhere", "Burning",
    "Lady Vengeance", "Sympathy for Mr. Vengeance", "Mother", "Thirst", "Joint Security Area",
    "A Bittersweet Life", "Spring, Summer, Fall, Winter... and Spring", "Poetry", "The Chaser",
    "Yellow Sea", "The Host", "The Good, the Bad, the Weird", "New World", "The Admiral: Roaring Currents",
    "Ode to My Father", "Along with the Gods: The Two Worlds", "Along with the Gods: The Last 49 Days",
    "Veteran", "The Assassination", "Extreme Job", "Miracle in Cell No. 7", "Masquerade",
    "Silenced", "The Attorney", "The Age of Shadows", "The Handmaiden", "Midnight Runners",
    "The Outlaws", "The Roundup", "The Gangster, the Cop, the Devil", "The Witch: Part 1. The Subversion",
    "Exit", "Ashfall", "Peninsula", "Space Sweepers", "The Call", "Night in Paradise",
    "Sweet & Sour", "The 8th Night", "Hostage: Missing Celebrity", "Sinkhole", "Escape from Mogadishu",
    "The Pirates: The Last Royal Treasure", "Love and Leashes", "Yaksha: Ruthless Operations",
    "The Roundup: Punishment", "Exhuma", "12.12: The Day", "Concrete Utopia", "Smugglers",
    "Project Wolf Hunting", "Hunt", "Decision to Leave", "Broker", "The Night Owl",
    "Kill Boksoon", "Ballerina", "Believer 2", "Jung_E", "Unlocked", "Dream", "The Moon",
    "Ransomed", "Honey Sweet", "Dr. Cheon and Lost Talisman", "Hopeless", "Brave Citizen",
    "Single in Seoul", "Our Season", "Noryang: Deadly Sea", "Alienoid", "Alienoid: Return to the Future",
    "Citizen of a Kind", "Picnic", "Dog Days", "Deadman", "Exhuma", "Following", "The Plot",
    "Wonderland", "Hijack 1971", "Handsome Guys", "Escape", "Project Silence", "Victory",
    "The Land of Happiness", "Revolver", "Mission: Cross", "I, the Executioner", "Harbin",
    "Uprising", "The Great Flood", "Moral Hazard", "The Match", "Opposition", "Hi.5",
    "Searching for the Elephant", "A Frozen Flower", "The Concubine", "Obsessed",
    "The Treacherous", "Portrait of a Beauty", "Scarlet Innocence", "Empire of Lust",
    "The Taste of Money", "The Housemaid", "Eungyo", "Lies", "Green Chair", "3-Iron",
    "The Isle", "Samaritan Girl", "Moebius", "Pieta", "The Net", "One on One", "Human, Space, Time and Human",
    "Shiri", "Silmido", "Taegukgi", "King and the Clown", "Tidal Wave", "Harmony", "The Tower",
    "Flu", "Pandora", "Deranged", "The Terror Live", "A Hard Day", "Tunnel", "Forgotten",
    "The Chase", "Gongui", "The Great Battle", "Ansi City", "The Fortress", "Svaha: The Sixth Finger",
    "The Divine Fury", "The Closet", "The 8th Night", "Collectors", "Hard Hit", "On the Line",
    "Spiritwalker", "The Killer: A Girl Who Deserves to Die", "A Company Man", "Suspect",
    "V.I.P.", "The Spy Gone North", "The Drug King", "Jo Pil-ho: The Dawning Rage",
    "Hit-and-Run Squad", "Man on High Heels", "Rough Play", "The Prison", "Default",
    "Money", "The Beast", "Tazza: The High Rollers", "Tazza: The Hidden Card",
    "Tazza: One Eyed Jack", "Friend", "Friend: The Great Legacy", "Breathless", "Bleak Night",
    "Dooku", "Han Gong-ju", "Microhabitat", "The House of Us", "Moving On", "Kim Ji-young, Born 1982",
    "Minari", "Past Lives"
]


def veri_yukle(liste, grup_adi):

    if not liste:
        return

    if "turk" in grup_adi:
        grup_val = "turk"
    elif "anime" in grup_adi:
        grup_val = "anime"
    elif "kore" in grup_adi:
        grup_val = "kore"
    else:
        grup_val = "genel"

        # Film mi dizi mi ayrımı
    cesit_val = "dizi" if ("dizi" in grup_adi or "anime" in grup_adi) else "film"

    print(f"\n>>> {grup_adi.upper()} yükleniyor (Grup: {grup_val}, Çeşit: {cesit_val})")

    for isim in liste:
        payload = {
            "title": isim,
            "grup": grup_val,  # Modelindeki 'grup' alanı
            "cesit": cesit_val  # Modelindeki 'cesit' alanı
        }
        try:
            # timeout=10 ekleyerek sunucu donmalarını önle
            response = requests.post(URL, json=payload, timeout=30)

            if response.status_code == 201:
                print(f"✅ {isim} eklendi.")
            elif response.status_code == 200:  # Eğer backend mevcut kaydı güncelliyorsa
                print(f"🔄 {isim} güncellendi.")
            else:
                print(f"⚠️ {isim} atlandı (Hata: {response.status_code})")
        except Exception as e:
            print(f"❌ Hata: {str(e)}")

if __name__ == "__main__":


    veri_yukle(yabanci_filmler, "yabanci_filmler")
    veri_yukle(kore_filmleri, "kore_filmleri")
    veri_yukle(yabanci_diziler, "yabanci_diziler")
    veri_yukle(kore_dizileri, "kore_dizileri")
    veri_yukle(turk_filmleri, "turk_filmleri")
    veri_yukle(turk_dizileri, "turk_dizileri")
    veri_yukle(animeler, "animeler")
    print("\n[!] Tüm işlemler tamamlandı.")