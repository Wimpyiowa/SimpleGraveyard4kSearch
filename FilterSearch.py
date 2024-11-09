from ossapi import *
import logging
from tkinter import *
api = Ossapi(user id, "[Use your client secret here]")

user = api.user("Wimpy Cursed", key=UserLookupKey.USERNAME)
print(user.id)


#       TEST
#beatmapSearch = api.beatmap(281219)

#user_most_played = api.user_beatmaps(user_id=24694032, type="most_played")[3]
#beatmap = user_most_played.beatmap()

#print(beatmapSearch)

#print(beatmap)

#beatmap = beatmapSearch.beatmapset().artist_unicode
#print(beatmap)



root = Tk()
root.title("Wimpy's Very Simple 4k Graveyard Map Filter")
root.geometry("500x500")
root.config(bg="black")
osuLabel = Label(root, text="Simple osu! Filter Search", font=200, bg="black", fg="white")
osuButton = Button(root, text="Next", command=lambda: (Filters(), osuLabel.destroy(), osuButton.destroy()))

osuLabel.place(rely= 0.225, relx=0.5, anchor=CENTER)
osuButton.place(rely= 0.4, relx=0.5, anchor=CENTER)



logging.basicConfig(filename="osu!Maps", filemode="a", level=logging.INFO)

def Filters():
    global text
    osuFilterLabel = Label(root, text="Enter query (Ex. Tech)", font=200, bg="black", fg="white")
    osuFilterInput = Entry(root)
    osuButtonFilter = Button(root, text="Next", command=lambda: (retrieve_input(), clickSearch(), difficultyFilters(), osuFilterLabel.destroy(), osuFilterInput.destroy(), osuButtonFilter.destroy()))


    osuFilterLabel.place(rely=0.225, relx=0.5, anchor=CENTER)
    osuFilterInput.place(rely=0.4, relx=0.5, anchor=CENTER)
    osuButtonFilter.place(relx=0.5, rely=0.5, anchor=CENTER)

    def retrieve_input():
        global text
        text = osuFilterInput.get()
        osuInput = open("TestData.txt", "w")
        osuInput.write(text)

def difficultyFilters():
    pass




# Loop through each beatmap set in the search results
def clickSearch():
    beatmapSearch = api.search_beatmapsets(query=text, mode=BeatmapsetSearchMode.MANIA, 
                                       category=BeatmapsetSearchCategory.GRAVEYARD, 
                                       genre=BeatmapsetSearchGenre.ANY, language=BeatmapsetSearchLanguage.ANY, 
                                       force_video=False, force_recommended_difficulty=False, 
                                       include_converts=False)
    
    Difficulty = DoubleVar()
    Popularity = DoubleVar()

    difficultyLabel = Label(root, text = "Difficulty/Star Rating", bg="black", fg="white")
    difficultySlider = Scale(root, variable=Difficulty, from_=0.0, to = 10.00, orient=HORIZONTAL, resolution=0.1)
    popularityLabel = Label(root, text = "Playcount", bg="black", fg="white")
    popularitySlider = Scale(root, variable=Popularity, from_=0.0, to = 10000.00, orient=HORIZONTAL, resolution=0.1)

    searchButton = Button(root, text="Search", command=lambda: (SearchBeatmaps(), difficultyLabel.destroy(), 
                                                                difficultySlider.destroy(), popularityLabel.destroy(),
                                                                popularitySlider.destroy(), searchButton.destroy()))

    difficultyLabel.place(rely=0.125, relx=0.5, anchor=CENTER)
    difficultySlider.place(rely=0.2, relx=0.5, anchor=CENTER)
    popularityLabel.place(rely=0.325, relx=0.5, anchor=CENTER)
    popularitySlider.place(rely=0.4, relx=0.5, anchor=CENTER)

    searchButton.place(rely=0.6, relx=0.5, anchor=CENTER)

    def SearchBeatmaps():
        difficulty = Difficulty.get()
        popularity = Popularity.get() 

        file = open("osu!map Data.txt", "a+")
        file.write(f"\nInstance for {text}, Difficulty: {difficulty}, playcount: {popularity}\n\n\n")
        file.close()

        for results in beatmapSearch.beatmapsets:
            results
        # Access individual beatmaps within each beatmap set
            for beatmap in results.beatmaps:
                if float(beatmap.difficulty_rating) > difficulty and float(beatmap.passcount) > popularity and beatmap.cs == 4 :
                    print(f"Name: {results.title}")
                    print(f"Difficulty Name: {beatmap.version}")
                    print(f"Stars: {beatmap.difficulty_rating}")
                    print(f"BPM {beatmap.bpm}")
                    print(f"Playcount: {beatmap.playcount}")
                    print(f"Link: {beatmap.url}")


                    

                    file = open("osu!map Data.txt", "a+")
                    file.write(f"\nName: {results.title}\nDifficulty Name: {beatmap.version}\nStars: {beatmap.difficulty_rating}\nBPM: {beatmap.bpm}\nPlaycount: {beatmap.playcount}\nLink: {beatmap.url}\n")
                    file.close()

                    logging.info(f"Name: {results.title}, Difficulty Name: {beatmap.version}, Difficulty {beatmap.difficulty_rating}, BPM: {beatmap.bpm}, Playcount: {beatmap.playcount}, Link: {beatmap.url}")
                else:
                    print("Wasteland.")

        finishedLabel = Label(root, text="Beatmaps Searched.\nFile has been created.\nYou can now close\nthis window.", bg="black", fg="white")

        finishedLabel.place(rely = 0.5, relx=0.5, anchor=CENTER)
#import pandas as pd
#df = pd.read_csv("osu!Maps.csv")

#print (df.head(5))


root.mainloop()
