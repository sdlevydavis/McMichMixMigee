import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import pygame
import requests
from io import BytesIO
from checkbox import Checkbox
import playlist_features
import random

# TODO: edit function -> load_songs_points()      !!! only tested one feature
# TODO: add sorting algorithms


DATA_SET_SIZE = 10  # set data set size (can't be more than ~ 1 million)
DATA_FILE = "tracks_features_condensed.csv"  # set data set file name
GRAY = (128, 128, 128)  # set-up screen color
feature_indices = {"ID": 0, "NAME": 1, "ALBUM": 2, "ARTISTS": 3, "EXPLICIT": 4,
                   "DANCEABILITY": 5, "ENERGY": 6, "KEY": 7, "Mode": 8,
                   "ACOUSTICNESS": 9, "INSTRUMENTALNESS": 10, "VALENCE": 11,
                   "TEMPO": 12, "DURATION (mins)": 13, "YEAR": 14, "POINTS": 15}  # index of features data set file

# image url used for testing
link = 'https://static.wikia.nocookie.net/gensin-impact/images/2/21/' \
       'Neuvillette_Icon.png/revision/latest/scale-to-width/360?cb=20230927021051'


def main():
    # read file and put song data in a list
    songs_list = get_songs_from_file(DATA_FILE, DATA_SET_SIZE)
    display_playlist(songs_list)
    print("\nThank You For Using McMichMixMigee Playlist Generator :)")


def fake_get_user_input():
    user_requirements = {}
    welcome_msg = "Welcome to McMichMixMigee Playlist Generator!"
    msg_length = len(welcome_msg) / 2
    while msg_length > 0:
        print("_ ", end="")
        msg_length -= 1

    print()
    print(welcome_msg)
    print()
    print("Priority is an integer from 0 (no importance) to 19 (most important) ")
    print("You can give different features the same priorities.\n")
    print(f"Available Playlist Features:\n"
          f"1. EXPLICIT\n"
          f"2. DANCEABILITY\n"
          f"3. ENERGY\n"
          f"4. KEY\n"
          f"5. Mode\n"
          f"6. ACOUSTICNESS\n"
          f"7. INSTRUMENTALNESS\n"
          f"8. VALENCE\n"
          f"9. TEMPO\n"
          f"10. DURATION (mins)\n"
          f"11. YEAR\n")

    priority_points = input(f"Input priority for feature - DURATION (mins): ")
    while not priority_points.isnumeric() or int(priority_points) > 11 or int(priority_points) < 0:
        print("Invalid Input! Enter an integer from 1 to 19")
        priority_points = input(f"Input priority for feature - DURATION (mins): ")
    details = input(" --- feature details: ")
    user_requirements["DURATION (mins)"] = (priority_points, details)


    priority_points = input(f"Input priority for feature - YEAR: ")
    while not priority_points.isnumeric() or int(priority_points) > 11 or int(priority_points) < 0:
        print("Invalid Input! Enter an integer from 1 to 19")
        priority_points = input(f"Input priority for feature - YEAR: ")
    details = input(" --- feature details: ")
    user_requirements["YEAR"] = (priority_points, details)

    print()
    return user_requirements


# function to display playlist of selected songs
def display_playlist(songs_list):

    # positions that album images will be display at
    img_positions = [(125, 325), (275, 325), (425, 325), (575, 325), (125, 475), (275, 475), (425, 475), (575, 475)]

    # stops while-loop for displaying screen from reloading and sorting data
    skip_reloading_data = False

    # set-up button for playlist generation
    generate_text = "GENERATE PLAYLIST"
    generate_playlist_button_clicked = False
    generate_playlist_button_rect = pygame.Rect(325, 150, 150, 50)
    generate_playlist_button_color = (50, 150, 255)
    generate_playlist_button_hover_color = (100, 200, 255)
    current_generate_button_color = generate_playlist_button_color

    # Initialize Pygame
    pygame.init()

    # Set up display
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("McMichMixMigee Menu")

    clock = pygame.time.Clock()

    font = pygame.font.Font("SegUIVar.ttf", 14)
    surf = font.render(generate_text, True, (0, 0, 0))
    text_rect = surf.get_rect()
    text_rect.center = (400, 175)

    checkboxes = []
    slider_rects = []
    slider_color = (50, 150, 255)
    handle_radius = 10
    handle_color = (255, 255, 255)

    slider_values = [0] * len(playlist_features.available_features)

    index = 0
    x_dimension = 15
    y_dimension = 15
    prev_x_dimension = 0
    for feature in playlist_features.available_features:
        if index % 5 == 0:
            x_dimension = 15
            y_dimension = 15 * (index + 1)
        else:
            x_dimension = prev_x_dimension + 165
        checkboxes.append(Checkbox(x_dimension, y_dimension, feature))
        slider_rects.append(pygame.Rect(x_dimension + 8, y_dimension + 25, 140, 10))
        index += 1
        prev_x_dimension = x_dimension

    # Main game loop
    running = True
    mouse_drag = False
    while running:
        screen.fill(GRAY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for checkbox in checkboxes:
                        if checkbox.rect.collidepoint(event.pos):
                            checkbox.checked = not checkbox.checked
                mouse_drag = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_drag = False


        for checkbox in checkboxes:
            checkbox.display(screen, font)


        for i in range(len(slider_rects)):
            if checkboxes[i].checked:
                if mouse_drag and slider_rects[i].collidepoint(event.pos):
                    slider_values[i] = max(0, min((event.pos[0] - slider_rects[i].left) / slider_rects[i].width, 1))

                pygame.draw.rect(screen, slider_color, slider_rects[i])
                handle_x = slider_rects[i].left + int(slider_rects[i].width * slider_values[i])
                pygame.draw.circle(screen, handle_color, (handle_x, slider_rects[i].centery), handle_radius)


        # get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # check if mouse is over generate playlist button
        if generate_playlist_button_rect.collidepoint(mouse_x, mouse_y):
            current_generate_button_color = generate_playlist_button_hover_color
            # button clicked
            if pygame.mouse.get_pressed()[0]:  # Left mouse button
                # print("Button clicked!") # for debugging purposes
                generate_playlist_button_clicked = True
        else:
            current_generate_button_color = generate_playlist_button_color

        if generate_playlist_button_clicked:
            # handles loading/sorting of song data from csv file
            # stops it from loading/sorting repeatedly
            if not skip_reloading_data:
                skip_reloading_data = True
                # list of user's decided feature priorities
                user_requirements = fake_get_user_input()  # delete this later and replace with data from scroll_bars
                song_id_points_pair_list = load_songs_points(songs_list, user_requirements)
                # print(song_id_points_pair_list)  # for debugging purposes

                """ 
                # 1. sort song_id_points_pair_list
                # 2. get top 8 songs and their corresponding album cover images
                    song_id_points_pair_list = sort(song_id_points_pair_list)
                    selected_song_ids = [] # top 8 songs from sorted song_id_points_pair_list
                    image_urls = []
                    for song_id in selected_song_ids:
                        image_urls.append(get_album_track_img(song_id)
                    
                    print_playlist_data(selected_song_ids)  # prints generated playlist data
                """
                selected_song_ids = []
                image_urls = []
                song_count = 1
                max_index = len(songs_list) - 1
                while song_count < 9:
                    rand_index = random.randint(0, max_index)
                    song = songs_list[rand_index]
                    selected_song_ids.append(song[feature_indices["ID"]])
                    image_urls.append(get_album_track_img(song[feature_indices["ID"]]))
                    song_count += 1

                print_playlist_data(selected_song_ids)  # prints generated playlist data

            # Load images from urls
            images = []
            for url in image_urls:
                images.append(load_image_from_url(url))

            # draw album images on screen
            img_index = 0
            for image in images:
                square_rect = image.get_rect()
                mask = pygame.Surface((int(square_rect.width), int(square_rect.width)), pygame.SRCALPHA)
                pygame.draw.circle(mask, (255, 255, 255, 255), (square_rect.width // 2, square_rect.width // 2),
                                   square_rect.width // 2)

                screen.blit(image, img_positions[img_index])
                screen.blit(mask, img_positions[img_index], special_flags=pygame.BLEND_RGBA_MULT)
                img_index += 1
            # print("loaded data")  # for debugging purposes

        # draw generate playlist button
        pygame.draw.rect(screen, current_generate_button_color, generate_playlist_button_rect)

        screen.blit(surf, text_rect)

        # Update the display
        pygame.display.flip()

    # quit Pygame
    pygame.quit()
    clock.tick(60)


# function to update and return list of song ids and their point
def load_songs_points(songs_list, user_requirements):

    # (percentage of points allocated based on how close it is to user's desired mins)

    # this loop updates all songs' total points
    # *** points is 0th index of pair user_requirements in map || details is 1st index of pair in  user_requirements map
    # song_num = 1
    for song in songs_list:

        # -- Feature: Duration --
        duration_feature_points = user_requirements["DURATION (mins)"][0]
        actual_duration = song[feature_indices["DURATION (mins)"]]
        expected_duration = user_requirements["DURATION (mins)"][1]
        percent_error = abs(float(expected_duration) - float(actual_duration)) / float(expected_duration)
        if percent_error > 1:
            points_to_allocate = 0  # difference in values was too large so no points added
        else:
            points_to_allocate = (1 - percent_error) * float(duration_feature_points)
        song[feature_indices["POINTS"]] = str(float(song[feature_indices["POINTS"]]) + points_to_allocate)

        # TODO: this has not been tested ---------------------
        # -- Feature Year --
        year_feature_points = user_requirements["YEAR"][0]
        actual_year = song[feature_indices["YEAR"]]
        expected_year = user_requirements["YEAR"][1]
        percent_error = abs(float(expected_year) - float(actual_year)) / float(expected_year)
        if percent_error > 1:
            points_to_allocate = 0  # difference in values was too large so no points added
        else:
            points_to_allocate = (1 - percent_error) * float(year_feature_points)
        song[feature_indices["POINTS"]] = str(float(song[feature_indices["POINTS"]]) + points_to_allocate)

        """
        # TODO: this has not been tested ---------------------
        # -- Feature Tempo --
        tempo_feature_points = user_requirements["TEMPO"][0]
        actual_tempo = song[feature_indices["TEMPO"]]
        expected_tempo = user_requirements["TEMPO"][1]
        percent_error = abs(float(expected_tempo) - float(actual_tempo)) / float(expected_tempo)
        if percent_error > 1:
            points_to_allocate = 0  # difference in values was too large so no points added
        else:
            points_to_allocate = (1 - percent_error) * float(tempo_feature_points)
        song[feature_indices["POINTS"]] = str(float(song[feature_indices["POINTS"]]) + points_to_allocate)        
        
        # TODO: this has not been tested ---------------------
        # -- Feature Valence --
        valence_feature_points = user_requirements["VALENCE"][0]
        actual_valence = song[feature_indices["VALENCE"]]
        expected_valence = user_requirements["VALENCE"][1]
        percent_error = abs(float(expected_valence) - float(actual_valence)) / float(expected_valence)
        if percent_error > 1:
            points_to_allocate = 0  # difference in values was too large so no points added
        else:
            points_to_allocate = (1 - percent_error) * float(valence_feature_points)
        song[feature_indices["POINTS"]] = str(float(song[feature_indices["POINTS"]]) + points_to_allocate)

        # TODO: this has not been tested ---------------------
        # -- Feature Instrumentalness --
        instr_feature_points = user_requirements["INSTRUMENTALNESS"][0]
        actual_instr = song[feature_indices["INSTRUMENTALNESS"]]
        expected_instr = user_requirements["INSTRUMENTALNESS"][1]
        percent_error = abs(float(expected_instr) - float(actual_instr)) / float(expected_instr)
        if percent_error > 1:
            points_to_allocate = 0  # difference in values was too large so no points added
        else:
            points_to_allocate = (1 - percent_error) * float(instr_feature_points)
        song[feature_indices["POINTS"]] = str(float(song[feature_indices["POINTS"]]) + points_to_allocate)

        # TODO: this has not been tested ---------------------
        # -- Feature Acousticness --
        acoustic_feature_points = user_requirements["ACOUSTICNESS"][0]
        actual_acoustic = song[feature_indices["ACOUSTICNESS"]]
        expected_acoustic = user_requirements["ACOUSTICNESS"][1]
        percent_error = abs(float(expected_acoustic) - float(actual_acoustic)) / float(expected_acoustic)
        if percent_error > 1:
            points_to_allocate = 0  # difference in values was too large so no points added
        else:
            points_to_allocate = (1 - percent_error) * float(acoustic_feature_points)
        song[feature_indices["POINTS"]] = str(float(song[feature_indices["POINTS"]]) + points_to_allocate)

        # TODO: this has not been tested ---------------------
        # -- Feature Mode --
        mode_feature_points = user_requirements["MODE"][0]
        actual_mode = song[feature_indices["MODE"]]
        expected_mode = user_requirements["MODE"][1]
        percent_error = abs(float(expected_mode) - float(actual_mode)) / float(expected_mode)
        if percent_error > 1:
            points_to_allocate = 0  # difference in values was too large so no points added
        else:
            points_to_allocate = (1 - percent_error) * float(mode_feature_points)
        song[feature_indices["POINTS"]] = str(float(song[feature_indices["POINTS"]]) + points_to_allocate)

        # TODO: this has not been tested ---------------------
        # -- Feature Key --
        key_feature_points = user_requirements["KEY"][0]
        actual_key = song[feature_indices["KEY"]]
        expected_key = user_requirements["KEY"][1]
        percent_error = abs(float(expected_key) - float(actual_key)) / float(expected_key)
        if percent_error > 1:
            points_to_allocate = 0  # difference in values was too large so no points added
        else:
            points_to_allocate = (1 - percent_error) * float(key_feature_points)
        song[feature_indices["POINTS"]] = str(float(song[feature_indices["POINTS"]]) + points_to_allocate)

        # TODO: this has not been tested ---------------------
        # -- Feature Energy --
        energy_feature_points = user_requirements["ENERGY"][0]
        actual_energy = song[feature_indices["ENERGY"]]
        expected_energy = user_requirements["ENERGY"][1]
        percent_error = abs(float(expected_energy) - float(actual_energy)) / float(expected_energy)
        if percent_error > 1:
            points_to_allocate = 0  # difference in values was too large so no points added
        else:
            points_to_allocate = (1 - percent_error) * float(energy_feature_points)
        song[feature_indices["POINTS"]] = str(float(song[feature_indices["POINTS"]]) + points_to_allocate)

        # TODO: this has not been tested ---------------------
        # -- Feature Danceability --
        dance_feature_points = user_requirements["DANCEABILITY"][0]
        actual_dance = song[feature_indices["DANCEABILITY"]]
        expected_dance = user_requirements["DANCEABILITY"][1]
        percent_error = abs(float(expected_dance) - float(actual_dance)) / float(expected_dance)
        if percent_error > 1:
            points_to_allocate = 0  # difference in values was too large so no points added
        else:
            points_to_allocate = (1 - percent_error) * float(dance_feature_points)
        song[feature_indices["POINTS"]] = str(float(song[feature_indices["POINTS"]]) + points_to_allocate)
        
        # TODO: this has not been tested ---------------------
        # -- Feature Explicit --
        explicit_feature_points = user_requirements["EXPLICIT"][0]
        actual_explicit = song[feature_indices["EXPLICIT"]]
        expected_explicit = user_requirements["EXPLICIT"][1]
        if actual_explicit == expected_explicit:
            points_to_allocate = explicit_feature_points
        else:
            points_to_allocate = 0
        song[feature_indices["POINTS"]] = str(float(song[feature_indices["POINTS"]]) + points_to_allocate)
        """

    # makes a new list from song list that stores pairs (track_id, total points)
    # TODO: ask michael if pair should be (total points, track_id)
    song_id_points_pair_list = []
    for song in songs_list:
        song_id_points_pair_list.append((song[feature_indices["ID"]], float(song[feature_indices["POINTS"]].replace("\n", ""))))

    return song_id_points_pair_list


# funtion to load an image from a URL
def load_image_from_url(url, img_dimensions=(100, 100)):
    response = requests.get(url)
    img_data = BytesIO(response.content)
    img = pygame.image.load(img_data)
    img = pygame.transform.scale(img, img_dimensions)
    return img


# reads file and returns list of songs data
def get_songs_from_file(filename, num_of_songs=5):
    lines = []
    file = open(filename, encoding='utf-8')
    line_index = 0
    for line in file:
        if line_index != 0:
            if len(lines) < num_of_songs:
                lines.append(line.split(","))
            else:
                break
        line_index += 1
    return lines


# gets image url of the album that a given track ID is located in
def get_album_track_img(track_id):
    # Spotify API credentials
    client_id = '57967a08baed431fb902b7838d372a34'
    client_secret = 'ab81e2878da04d85a25deb6f9886d2b5'
    redirect_uri = 'http://127.0.0.1:5000/redirect/'

    # Set up Spotipy client
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope='user-library-read')  # change scope depending on if you want to search through specific user data
    )

    track = sp.track(track_id)
    if track['album']['images']:
        img_link = track['album']['images'][0]['url']
        return img_link
    return None


def print_playlist_data(song_ids):
    # Spotify API credentials
    client_id = '57967a08baed431fb902b7838d372a34'
    client_secret = 'ab81e2878da04d85a25deb6f9886d2b5'
    redirect_uri = 'http://127.0.0.1:5000/redirect/'

    # Set up Spotipy client
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope='user-library-read')  # change scope depending on if you want to search through specific user data
    )

    song_count = 1
    for song_id in song_ids:
        audio_details = sp.audio_features(song_id)
        track_features = audio_details[0]

        track_data = sp.track(song_id)

        artists_data = track_data["artists"]
        artist_names = []
        for artist in artists_data:
            artist_names.append(artist["name"])

        print(f'{song_count}.{track_data["name"]} by {artist_names}\n'
              f'  Song ID: {song_id}\n'
              f'  Spotify Link: {track_data["uri"]}\n'
              f'  Preview Link: {track_data["preview_url"]}\n'
              f'  -- Danceability: {track_features["danceability"]}\n'
              f'  -- Energy: {track_features["energy"]}\n'
              f'  -- Key: {track_features["key"]}\n'
              f'  -- Mode: {track_features["mode"]}\n'
              f'  -- Acousticness: {track_features["acousticness"]}\n'
              f'  -- Instrumentalness: {track_features["instrumentalness"]}\n'
              f'  -- Valence: {track_features["valence"]}\n'
              f'  -- Tempo: {track_features["tempo"]}\n'
              f'  -- Duration: {track_features["duration_ms"] / 60000.0} mins\n'
              f'  -- Year: {track_data["album"]["release_date"][:4]}\n')
        song_count += 1


if __name__ == '__main__':
    main()
