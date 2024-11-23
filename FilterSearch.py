from ossapi import *
import logging
from tkinter import *
import random
import pandas as pd

api = Ossapi(user id, "Client Secret")

user = api.user("Wimpy Cursed", key=UserLookupKey.USERNAME)
print(user.id)

csv_file = "beatmap.csv"

header_written = False
try:
    with open(csv_file, 'x', newline='') as file:
        header_written = True
except FileExistsError:
    pass #File already exists; no need to write headers

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
   # osuFliterRemoveLabel = Label(root, text = "What to not include", font=200, bg="black", fg="white")
    #osuFilterRemove = Entry(root)
    osuButtonFilter = Button(root, text="Next", command=lambda: (retrieve_input(), clickSearch(), osuFilterLabel.destroy(), osuFilterInput.destroy(), osuButtonFilter.destroy()))#osuFliterRemoveLabel.destroy(), osuFilterRemove.destroy()))


    osuFilterLabel.place(rely=0.225, relx=0.5, anchor=CENTER)
    osuFilterInput.place(rely=0.4, relx=0.5, anchor=CENTER)
    #osuFliterRemoveLabel.place(rely=0.525, relx=0.5, anchor=CENTER)
    #osuFilterRemove.place(rely=0.6, relx=0.5, anchor=CENTER)
    osuButtonFilter.place(relx=0.5, rely=0.7, anchor=CENTER)

    def retrieve_input():
        global text
        #global remove
        text = osuFilterInput.get()
        #remove = osuFilterRemove.get()
        osuInput = open("TestData.txt", "w")
        osuInput.write(text)



# Loop through each beatmap set in the search results
def clickSearch():
    beatmapSearch = api.search_beatmapsets(query=text, mode=BeatmapsetSearchMode.MANIA, 
                                       category=BeatmapsetSearchCategory.ANY, 
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
        global header_written
        global text
        #global remove
        
        difficulty = Difficulty.get()
        popularity = Popularity.get() 

        difficultyRebound = Difficulty.get() + 1.50

        

        file = open("osu!map Data.txt", "a+")
        file.write(f"\nInstance for {text}, Difficulty: {difficulty}, playcount: {popularity}\n\n\n")
        file.close()

        random_beatmap = random.sample(beatmapSearch.beatmapsets, 40)

        search_tags = set(text.lower().split())
        #remove_tags = set(remove.lower().split())

        for results in random_beatmap:
            beatmapset_data = []
            print(f"Name: {results.title}")
            file = open("osu!map Data.txt", "a+")
            file.write(f"\nName: {results.title}")
            file.close()

        # Access individual beatmaps within each beatmap set
            for beatmap in results.beatmaps:
                beatmapset_tags = set(results.tags.lower().split())


                if float(beatmap.difficulty_rating) >= difficulty and float(beatmap.difficulty_rating) <= difficultyRebound and float(beatmap.playcount) >= popularity and beatmap.cs == 4 and search_tags & beatmapset_tags: 
                #and beatmapset_tags != remove_tags
                    
                    print(f"Difficulty Name: {beatmap.version}")
                    print(f"Stars: {beatmap.difficulty_rating}")
                    print(f"BPM {beatmap.bpm}")
                    print(f"Playcount: {beatmap.playcount}")
                    print(f"Link: {beatmap.url}")

                    file = open("osu!map Data.txt", "a+")
                    file.write(f"\nDifficulty Name: {beatmap.version}\nStars: {beatmap.difficulty_rating}\nBPM: {beatmap.bpm}\nPlaycount: {beatmap.playcount}\nLink: {beatmap.url}\n")
                    file.close()

                    logging.info(f"Name: {results.title}, Difficulty Name: {beatmap.version}, Difficulty {beatmap.difficulty_rating}, BPM: {beatmap.bpm}, Playcount: {beatmap.playcount}, Link: {beatmap.url}")
                    beatmap_info = {
                        "Title": results.title,
                        "Artist": results.artist,
                        "Difficulty": beatmap.difficulty_rating,
                        "BPM": beatmap.bpm,
                        "Playcount": beatmap.playcount,
                        "Link": beatmap.url
                    }

                    beatmapset_data.append(beatmap_info)
                else:
                    print("Wasteland.")

            df = pd.DataFrame(beatmapset_data)

            df.to_csv(csv_file, mode='a', index=False, header=not header_written)
            header_written = True

        finishedLabel = Label(root, text="Beatmaps Searched.\nFile has been created.\nYou can now close\nthis window.", bg="black", fg="white")

        finishedLabel.place(rely = 0.5, relx=0.5, anchor=CENTER)

root.mainloop()
