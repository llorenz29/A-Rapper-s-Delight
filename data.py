import json
from pathlib import Path
import re
import spotipy
   
# 
# Gets the number of unique words an arists has used within their first x words
# 
def get_vocab(x):
    directory_path = '/Users/lukelorenz/Desktop/IndependentProjects/2021/Rappa'
    vocab = {}
    num_songs = 0
    word_cap = x
    tot_words = 0
    
    for file in Path(directory_path).glob('*.json'):
        print(file.name)
        #for each artist
        if(file.name != 'artist_lyrics.json'):  
            f = open(file.name)
            artist = json.load(f)
            count = set()
            word_max = 0
        
            #For each song in the artists discog
            for element in artist['songs']:
                #increase the number of songs
                num_songs +=1
                #Song title
                # print("{} by {}".format(element['title'],element['primary_artist']['name']))

                # eliminating [Chorus: Kanye West], among [Verse:...]
                e = re.sub("([\[]).*?([\]])", "", element['lyrics'])
                x = e.split()
                # gets rid of weird last part
                x = x[:-1]
                for word in x[:-1]:
                    tot_words +=1
                    #if we are still under lyric cap
                    if(word_max <word_cap):
                        # Strip word and make lowercase
                        strip_word = re.sub(r'[^\w\s]', '', word).lower()
                        if 'EmbedShare' in word:
                            word = word[:-12]
                        # print(word)
                        count.add(strip_word)
                        word_max +=1
            if(word_max == word_cap):
                print("ARTIST REACHED WORD MAX")
            else:
                print("ARTIST DID NOT REACH WORD MAX")
            vocab[element['primary_artist']['name']] = len(count)
    # sort the vocab dict
    sort_vocab = {}
    sorted_keys = sorted(vocab, key=vocab.get, reverse=True)  # [1, 3, 2]
    # Printing vocab dict
    for w in sorted_keys:
        sort_vocab[w] = vocab[w]
    for element, li in sort_vocab.items():
        print(element, ',', li)

    print("numsongs: {}".format(num_songs))
    print("totwords: {}".format(tot_words))
 
class artistObj():
    def __init__(self,artistName):
        self.name = artistName
        self.dictionary = {}
        self.pos_song = ""
        self.neg_song = ""
        self.pos_song_score = ""
        self.neg_song_score = ""
    
    def add_keyword(self,keyword, pct):
        self.dictionary[keyword] = pct

    def add_neg(self,song, score):
        self.pos_song = song
        self.pos_song_score = score
    
    def add_pos(self,song, score):
        self.neg_song = song
        self.neg_song_score = score

def get_tone():
    directory_path = '/Users/lukelorenz/Desktop/IndependentProjects/2021/Rappa'
    num_songs = 0
    tot_words = 0
    #for ranking word connotation
    rate_words = dict(map(lambda kv: (kv[0],int(kv[1])), 
            [ line.split('\t') for line in open("AFINN-111.txt") ]))
    most_neg_song = ''
    most_neg_count = 0
    most_pos_song = ''
    most_pos_count = 0

    for file in Path(directory_path).glob('*.json'):
        print(file.name)
        #for each artist
        if(file.name != 'artist_lyrics.json'):  
            f = open(file.name)
            artist = json.load(f)
        
            print("hello there")
            #For each song in the artists discog
            for element in artist['songs']:
                #increase the number of songs
                num_songs +=1
        
                #Temp vars for checking connotation
                tone = 0

                # eliminating [Chorus: Kanye West], among [Verse:...]
                e = re.sub("([\[]).*?([\]])", "", element['lyrics'])
                x = e.split()
                # gets rid of weird last part
                x = x[:-1]
                for word in x[:-1]:
                    tot_words += 1
                    # If the word has a connotation documented, add it to tone of song
                    if word in rate_words:
                        tone += rate_words.get(word)
                print("Tone of {} by {}: {}".format(element['title'],element['primary_artist']['name'],tone))
                #most negative tone, set the song
                if(tone < most_neg_count):
                    print("NEW MOST NEGATIVE SONG")
                    # Elims long freestyles
                    if('Freestyle' not in element['title']): 
                        most_neg_count = tone 
                        most_neg_song = "{} by {}".format(element['title'],element['primary_artist']['name'])
                    # reset tone counter
                    tone = 0
                elif(tone > most_pos_count):
                    # Getting rid of this one bc love is like every other word lol, same w thuggers 30 min freestlye
                    if('Love Me Long Time' not in element['title'] and 'Thug N 30' not in element['title']):
                        print("NEW MOST POSITIVE SONG")
                        most_pos_count = tone
                        most_pos_song = "{} by {}".format(element['title'],element['primary_artist']['name'])
                    # reset tone counter
                    tone = 0
                

            print("The most negative song is currently rated at {} and the song is {}".format(most_neg_count,most_neg_song))
            print("The most positive song is currently rated at {} and the song is {}".format(most_pos_count,most_pos_song))

    print("numsongs: {} ".format(num_songs))
    print("totwords: {}".format(tot_words))

def num_appearances(word, x):
    keyword = word
    directory_path = '/Users/lukelorenz/Desktop/IndependentProjects/2021/Rappa'
    num_songs = 0
    tot_words = 0
    counter = 0
    word_cap = x
    lg_pct = 0 
    sm_pct = 0

    least_used_song_count = 0
    most_used_song_count = 0
    least_used_song = ''
    most_used_song = ''

    for file in Path(directory_path).glob('*.json'):
        print(file.name)
        #for each artist, except NF. He messes everything up.
        if(file.name != 'artist_lyrics.json' and file.name != 'Lyrics_NF.json'):  
            f = open(file.name)
            artist = json.load(f)
            counter = 0
            word_max = 0
            #for getting percentage of words with the keyword
            artist_tot_words = 0
            artist_hit_words =  0

            #For each song in the artists discog
            for element in artist['songs']:
                #increase the number of songs
                num_songs +=1
                
                # eliminating [Chorus: Kanye West], among [Verse:...]
                e = re.sub("([\[]).*?([\]])", "", element['lyrics'])
                x = e.split()
                # gets rid of weird last part
                x = x[:-1]
                for word in x[:-1]:
                    tot_words+=1
                    if(word_max <word_cap):
                        artist_tot_words +=1
                        word_max +=1
                        if re.sub(r'[^\w\s]', '', word).lower() == keyword:
                            counter +=1
                            artist_hit_words +=1
            #Initializing first Artist, avoiding error where no artist is at the bottom
            if(element['primary_artist']['name'] == '50 Cent'):
                    least_used_song_count = counter 
                    least_used_song = "{}".format(element['primary_artist']['name'])
                    print("{} '%' of {}'s words were {}".format((artist_hit_words//artist_tot_words), element['primary_artist']['name'],keyword)) 
            else:
                #most negative tone, set the song
                if(counter < least_used_song_count):
                    print("NEW MOST NEGATIVE")
                    # Elims long freestyles
                    if('Freestyle' not in element['title']): 
                        least_used_song_count = counter 
                        least_used_song = "{}".format(element['primary_artist']['name'])
                        sm_pct = artist_hit_words/artist_tot_words *100
                    # reset tone counter
                    counter = 0
            if(counter > most_used_song_count):
                # Getting rid of this one bc love is like every other word lol, same w thuggers 30 min freestlye
                    print("NEW MOST POSITIVE")
                    most_used_song_count = counter
                    most_used_song = "{}".format(element['primary_artist']['name'])
                    lg_pct = artist_hit_words/artist_tot_words *100
                    # reset tone counter
                    counter = 0
            
            if(word_max == word_cap):
                print("ARTIST REACHED WORD MAX")
            else:
                print("ARTIST DID NOT REACH WORD MAX")
            
            # Percent
            prc = (artist_hit_words/artist_tot_words) *100
            print("{} '%' of {}'s words were {}".format((artist_hit_words/artist_tot_words), element['primary_artist']['name'],keyword)) 

    #When the loop has finished
            print("{} uses '{}' {} times in their first {} words, or {} percent of his words".format(most_used_song, keyword, most_used_song_count,word_cap, lg_pct))
            print("{} uses '{}' {} times in their first {} words, or {} percent of his words".format(least_used_song, keyword, least_used_song_count,word_cap, sm_pct))

    print("numsongs: {} ".format(num_songs))
    print("totwords: {}".format(tot_words))

def get_freq_of_term(terms):
    keywords = terms
    directory_path = '/Users/lukelorenz/Desktop/IndependentProjects/2021/Rappa'
 
    #for ranking percent of songs
    num_songs_artist = 0
    num_songs_contain = 0

    least_used_song_count = 0.0
    most_used_song_count = 0.0
    least_used_song = ''
    most_used_song = ''
    #list of all artist objects
    ARTIST_OBJS = []

    for file in Path(directory_path).glob('*.json'):
        print(file.name)
        #for each artist, except NF. He messes everything up.
        if(file.name != 'artist_lyrics.json' and file.name != 'Lyrics_NF.json'):  
            f = open(file.name)
            artist = json.load(f)
            pct = 0.0
            # Create artist obj
            artist_o = artistObj(artist['songs'][0]['primary_artist']['name'])
            for keyword in keywords:
                #for getting percentage of words with the keyword
            
                num_songs_artist = 0
                num_songs_contain = 0

                #For each song in the artists discog
                for element in artist['songs']:
                    #increase the number of songs
                    num_songs_artist +=1
                    # eliminating [Chorus: Kanye West], among [Verse:...]
                    e = re.sub("([\[]).*?([\]])", "", element['lyrics'])
                    x = e.split()
                    # gets rid of weird last part
                    x = x[:-1]
                    for word in x[:-1]:
                        if re.sub(r'[^\w\s]', '', word).lower() == keyword:
                            num_songs_contain +=1
                            break
                    pct = num_songs_contain/num_songs_artist *100
                    artist_o.add_keyword(keyword,pct)
            
            ARTIST_OBJS.append(artist_o)

    # print(ARTIST_OBJS[0].dictionary)
    return ARTIST_OBJS


#Gets the artists popularity
def popularity():
    SPOTIFY_CLIENT_ID = 'SECRET'
    SPOTIFY_CLIENT_SECRET = 'SECRET'
    SPOTIFY_CLIENT_URI = "https://google.com"
    oauth_object = spotipy.SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID
        ,client_secret=SPOTIFY_CLIENT_SECRET
        ,redirect_uri=SPOTIFY_CLIENT_URI
        # ,scope=scope
        )
    tokenDict = oauth_object.get_access_token()
    token = tokenDict['access_token']
    sp = spotipy.Spotify(auth=token)



def main():
    artistEras = {}
    artistEras["GZA" ] = "1990s"
    artistEras["MF DOOM"] = "1990s"
    artistEras["Black Thought"] = "1990s"
    artistEras["Ghostface Killah"] = "1990s"
    artistEras["Wu-Tang Clan"] = "1990s"
    artistEras["Inspectah Deck"] = "1990s"
    artistEras["Raekwon"] = "1990s"
    artistEras["Immortal Technique"] = "2000s"
    artistEras["Cappadonna"] = "1990s"
    artistEras["Lupe Fiasco"] = "2000s"
    artistEras["Pusha T"] = "2000s"
    artistEras["Fugees"] = "1990s"
    artistEras["Big Pun"] = "1990s"
    artistEras["Nas"] = "1990s"
    artistEras["Yasiin Bey"] = "1990s"
    artistEras["Cam’ron"] = "1990s"
    artistEras["Talib Kweli"] = "1990s"
    artistEras["Tech N9ne"] = "1990s"
    artistEras["Killer Mike"] = "1990s"
    artistEras["Big Daddy Kane"] = "1980s"
    artistEras["A Tribe Called Quest"] = "1980s"
    artistEras["Ab-Soul"] = "2000s"
    artistEras["Eminem"] = "2000s"
    artistEras["N.O.R.E."] = "1990s"
    artistEras["Slick Rick"] = "1980s"
    artistEras["JAY-Z"] = "1990s"
    artistEras["Obie Trice"] = "2000s"
    artistEras["KRS-One"] = "1980s"
    artistEras["Wyclef Jean"] = "1990s"
    artistEras["Sir Mix-a-Lot"] = "1980s"
    artistEras["The Game"] = "2000s"
    artistEras["Ol’ Dirty Bastard"] = "1990s"
    artistEras["Xzibit"] = "1990s"
    artistEras["Joey Bada$$"] = "2010s"
    artistEras["Proof"] = "1990s"
    artistEras["JID"] = "2010s"
    artistEras["LL Cool J"] = "2000s"
    artistEras["Big L"] = "1990s"
    artistEras["Cordae"] = "2010s"
    artistEras["A$AP Rocky"] = "2010s"
    artistEras["Heavy D"] = "1980s"
    artistEras["Dave"] = "2010s"
    artistEras["Lloyd Banks"] = "2000s"
    artistEras["Guru"] = "1980s"
    artistEras["Common"] = "1990s"
    artistEras["Ice-T"] = "1980s"
    artistEras["Tyler The Creator"] = "2010s"
    artistEras["Method Man"] = "1990s"
    artistEras["Q-Tip"] = "1990s"
    artistEras["Ice Cube"] = "1990s"
    artistEras["Macklemore"] = "2010s"
    artistEras["Lil Dicky"] = "2010s"
    artistEras["Mystikal"] = "1990s"
    artistEras["Biz Markie"] = "1980s"
    artistEras["Chamillionaire"] = "2000s"
    artistEras["Fat Joe"] = "1990s"
    artistEras["Bizzy Bone"] = "1990s"
    artistEras["Hopsin"] = "2000s"
    artistEras["Kurupt"] = "1990s"
    artistEras["Will Smith"] = "1990s"
    artistEras["B.o.B"] = "2000s"
    artistEras["Run–D.M.C."] = "1980s"
    artistEras["BROCKHAMPTON"] = "2010s"
    artistEras["Ski Mask the Slump God"] = "2010s"
    artistEras["E-40"] = "1980s"
    artistEras["Lil’ Kim"] = "2010s"
    artistEras["Busta Rhymes"] = "1990s"
    artistEras["Jay Rock"] = "2000s"
    artistEras["ScHoolboy Q"] = "2010s"
    artistEras["Denzel Curry"] = "2010s"
    artistEras["DJ Quik"] = "1990s"
    artistEras["Remy Ma"] = "2000s"
    artistEras["Public Enemy"] = "1990s"
    artistEras["Childish Gambino"] = "2010s"
    artistEras["A$AP Ferg"] = "2010s"
    artistEras["Kendrick Lamar"] = "2010s"
    artistEras["​The D.O.C."] = "1990s"
    artistEras["Kanye West"] = "2000s"
    artistEras["Layzie Bone"] = "1990s"
    artistEras["Big Sean"] = "2010s"
    artistEras["Lil Wayne"] = "2000s"
    artistEras["Headie One"] = "2010s"
    artistEras["Coolio"] = "1990s"
    artistEras["Ludacris"] = "2000s"
    artistEras["Nicki Minaj"] = "2010s"
    artistEras["Kevin Gates"] = "2010s"
    artistEras["MC Lyte"] = "1990s"
    artistEras["Bun B"] = "1990s"
    artistEras["Warren G"] = "1990s"
    artistEras["Krayzie Bone"] = "1990s"
    artistEras["Styles P"] = "1990s"
    artistEras["UGK"] = "1990s"
    artistEras["Skepta"] = "2010s"
    artistEras["Phife Dawg"] = "1990s"
    artistEras["Scarface"] = "1990s"
    artistEras["Twista"] = "2000s"
    artistEras["Queen Latifah"] = "1990s"
    artistEras["MC Ren"] = "2010s"
    artistEras["Machine Gun Kelly"] = "2010s"
    artistEras["Stormzy"] = "2010s"
    artistEras["Master P"] = "1990s"
    artistEras["Vince Staples"] = "2010s"
    artistEras["Isaiah Rashad"] = "2010s"
    artistEras["Big K.R.I.T."] = "2010s"
    artistEras["Gucci Mane"] = "2010s"
    artistEras["Joyner Lucas"] = "2010s"
    artistEras["Fabolous"] = "2000s"
    artistEras["2 Chainz"] = "2000s"
    artistEras["Travis Scott"] = "2010s"
    artistEras["Diddy"] = "1990s"
    artistEras["Afroman"] = "2000s"
    artistEras["G-Eazy"] = "2010s"
    artistEras["Meek Mill"] = "2010s"
    artistEras["Eve"] = "2000s"
    artistEras["Lil Yachty"] = "2010s"
    artistEras["Mac Miller"] = "2010s"
    artistEras["Anderson .Paak"] = "2010s"
    artistEras["T.I."] = "2000s"
    artistEras["Logic"] = "2010s"
    artistEras["Aminé"] = "2010s"
    artistEras["50 Cent"] = "2000s"
    artistEras["Snoop Dogg"] = "1990s"
    artistEras["Ace Hood"] = "2000s"
    artistEras["Polo G"] = "2010s"
    artistEras["XXXTENTACION"] = "2010s"
    artistEras["2Pac"] = "1990s"
    artistEras["Offset"] = "2010s"
    artistEras["Migos"] = "2010s"
    artistEras["Gunna"] = "2010s"
    artistEras["Eazy-E"] = "1990s"
    artistEras["J. Cole"] = "2010s"
    artistEras["Young Thug"] = "2010s"
    artistEras["21 Savage"] = "2010s"
    artistEras["NLE Choppa"] = "2010s"
    artistEras["Too $hort"] = "1980s"
    artistEras["Nelly"] = "2000s"
    artistEras["Jeezy"] = "2000s"
    artistEras["N.W.A"] = "1990s"
    artistEras["Swae Lee"] = "2000s"
    artistEras["Juvenile"] = "1990s"
    artistEras["Ma$e"] = "1990s"
    artistEras["Grandmaster Flash"] = "1980s"
    artistEras["Ja Rule"] = "1990s"
    artistEras["Waka Flocka Flame"] = "2000s"
    artistEras["Kodak Black"] = "2010s"
    artistEras["Future"] = "2010s"
    artistEras["Drake"] = "2010s"
    artistEras["Iggy Azalea"] = "2010s"
    artistEras["Roddy Ricch"] = "2010s"
    artistEras["DMX"] = "2000s"
    artistEras["Juice WRLD"] = "2010s"
    artistEras["NF"] = "2010s"
    artistEras["Juicy J"] = "2010s"
    artistEras["Nate Dogg"] = "1990s"
    artistEras["Kid Cudi"] = "2010s"
    artistEras["Lil Baby"] = "2010s"
    artistEras["Lil Durk"] = "2010s"
    artistEras["Lil Tjay"] = "2010s"
    artistEras["Trippie Redd"] = "2010s"
    artistEras["Lil Jon"] = "2000s"
    artistEras["DaBaby"] = "2010s"
    artistEras["Flo Rida"] = "2010s"
    artistEras["Kid Ink"] = "2010s"
    artistEras["Rich The Kid"] = "2010s"
    artistEras["MC Hammer"] = "1980s"
    artistEras["Ty Dolla $ign"] = "2010s"
    artistEras["Doja Cat"] = "2010s"
    artistEras["Lil Nas X"] = "2010s"
    artistEras["YNW Melly"] = "2010s"
    artistEras["Megan Thee Stallion"] = "2010s"
    artistEras["Lil Uzi Vert"] = "2010s"
    artistEras["Post Malone"] = "2010s"
    artistEras["YoungBoy Never Broke Again"] = "2010s"
    artistEras["Takeoff"] = "2010s"
    artistEras["A Boogie wit da Hoodie"] = "2010s"
    artistEras["T-Pain"] = "2000s"
    artistEras["Chief Keef"] = "2010s"
    artistEras["Lil Skies"] = "2010s"
    artistEras["King Von"] = "2010s"
    artistEras["Wiz Khalifa"] = "2010s"
    artistEras["Fetty Wap"] = "2010s"
    artistEras["Playboi Carti"] = "2010s"
    artistEras["Lil Tecca"] = "2010s"
    artistEras["Doug E. Fresh"] = "1990s"

    print("Running Main...")
    get_tone()
    get_vocab(20000)
    num_appearances('fuck',20000)
    #Get_freq_of_term gets much slower as you add more terms

    #Prints in CSV Format
    objs = get_freq_of_term(['fuck'])
    for obj in objs:
        for key, val in obj.dictionary.items():
            if(obj.name in artistEras):
                print("{},{},{},{}".format(obj.name,key,val,artistEras[obj.name]))
    

if __name__ == '__main__':
    main()

