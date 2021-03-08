import pandas as pd
import os

def get_genres(path):
    ids = []
    genres = []
    with open(path) as f:
        line = f.readline()
        while line:
            if line[0] != '#':
                [x, y, *_] = line.strip().split("\t")
                ids.append(x)
                genres.append(y)
            line = f.readline()
    genre_df = pd.DataFrame(data={"Genre": genres, "TrackID": ids})
    return genre_df

def get_matched_midi(midi_folder, genre_df):
    # Get All Midi Files
    track_ids, file_paths = [], []
    for dir_name, subdir_list, file_list in os.walk(midi_folder):
        #print(len(dir_name))
        if len(dir_name) == 36:
            track_id = dir_name[18:]
            file_path_list = ["/".join([dir_name, file]) for file in file_list]
            for file_path in file_path_list:
                track_ids.append(track_id)
                file_paths.append(file_path)
    all_midi_df = pd.DataFrame({"TrackID": track_ids, "Path": file_paths})

    # Inner Join with Genre Dataframe
    df = pd.merge(all_midi_df, genre_df, on='TrackID', how='inner')
    return df.drop(["TrackID"], axis=1)

if __name__ == "__main__":
    genre_path = "msd_tagtraum_cd2c.cls"
    genre_df = get_genres(genre_path)

    label_list = list(set(genre_df.Genre))
    label_dict = {lbl: label_list.index(lbl) for lbl in label_list}

    midi_path = "lmd_matched"
    matched_midi_df = get_matched_midi(midi_path, genre_df)

    sta_dict = {}
    for item in matched_midi_df['Genre'].values:
        sta_dict[item] = sta_dict.get(item, 0) + 1

    #print(sta_dict)
    #print(matched_midi_df.head())
    matched_midi_df.to_csv('dataset.csv', index=False)