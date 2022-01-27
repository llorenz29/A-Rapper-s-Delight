# A-Rappers-Delight
In Depth Lyric Analysis of ___ Rappers and ____ different songs, along with ____ total words

UNIQUE WORDS USED WITHIN AN ARTISTS FIRST 20K WORDS, GROUPED BY GENRE
![lyricsOverTime](Screenshots/lyricsOverTime.png)

This scrapes the top 250ish rappers on ___INSERT LINK___, downloads lyrics to their top songs,
and stores in Json files. We currenly store the data of ___ artists, and a total of ____ songs.

I also added in rap groups such as Outkast, NWA, Wu Tang Clan, A Tribe Called Quest, etc because the
website ranked solo rappers only. Though rappers such as Andre 3000, Dr. Dre, RZA, etc were on the list,
I felt it was equally important to include their respective groups


RATING THE VOCABULARY OF SONGS:
    The function get_vocab(x) returns a dict of the number of unique words used within
    the artist's first x words. 

    Insert


RATING THE TONE OF SONGS:
    The function get_tone() gets the tone of each song and returns the most positive 
    and negative songs, along with their score. To do this, I used AFINN

AFINN is a list of English words rated for valence with an integer
between minus five (negative) and plus five (positive). The words have
been manually labeled by Finn Årup Nielsen in 2009-2011. 

It's slightly flawed, words like (pardon my french) fuck and bitch are rated at -4 and -5, hard to use in context. Changing them
moves the most negative song around quite a bit. It would be better to use an AI to determine positivity
and negativity, but unfortunately I don't know how to do that yet

If I keep fuck, bitch, and N***** the same (-5):
The most negative song is currently -620 and the song is Dead Broke by Chief Keef:
Here's a snippet:
    ![DeadBroke](Screenshots/Dead_broke.png)
The most positive song is currently 209 and the song is Summertime Magic by Childish Gambino
Here's a snippet:
   ![Summertime](Screenshots/Summertime_magic.png)                        
Clearly, love is bringing up the total

Changing fuck, bitch, N**** to 0, yields:
The most negative song is currently rated at -406 and the song is Renincarnated by MC Ren

Here's a snippet from Reincarnated:        
   ![Reinc](Screenshots/Reincarnation.png)

The most positive song is currently rated at 209 and the song is Summertime Magic by Childish Gambino (wow, stays the same)


ARTISTS LOVE ___FILL IN THE BLANK_____
