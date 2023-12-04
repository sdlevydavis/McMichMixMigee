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


DATA_SET_SIZE = 100  # set data set size (can't be more than ~ 1 million)
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


def fake_get_user_input(slider_values, checkboxes, check_order):
    priority_points = [0] * len(slider_values)
    details = [1] * len(slider_values)
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

    for i in range(len(slider_values)):
        if checkboxes[i].checked:
            priority_points[i] = 12
            found = False
            while not found:
                priority_points[i] -= 1
                found = (check_order[11 - priority_points[i]] == i)

            match playlist_features.available_features[i]:
                case 'YEAR':
                    details[i] = round(slider_values[i] * 83) + 1940
                case 'DURATION (mins)':
                    details[i] = slider_values[i] * 4.5 + 0.5
                case 'EXPLICIT':
                    details[i] = round(slider_values[i])
                case 'MODE':
                    details[i] = round(slider_values[i])
                case 'KEY':
                    details[i] = round(slider_values[i] * 11)
                case 'TEMPO':
                    details[i] = slider_values[i] * 248
                case 'INSTRUMENTALNESS':
                    details[i] = slider_values[i]
                case 'DANCEABILITY':
                    details[i] = slider_values[i]
                case 'ACOUSTICNESS':
                    details[i] = slider_values[i]
                case 'VALENCE':
                    details[i] = slider_values[i]
                case 'ENERGY':
                    details[i] = slider_values[i]

        user_requirements[playlist_features.available_features[i]] = (priority_points[i], details[i])

    print()
    return user_requirements


# function to display playlist of selected songs
def display_playlist(songs_list):
    # True is heap sort, False is bucket sort
    sort_mode = True

    # positions that album images will be display at
    img_positions = [(125, 325), (275, 325), (425, 325), (575, 325), (125, 475), (275, 475), (425, 475), (575, 475)]

    # stops while-loop for displaying screen from reloading and sorting data
    skip_reloading_data = False

    # set-up button for playlist generation
    generate_text = "GENERATE PLAYLIST"
    generate_playlist_button_clicked = False
    generate_playlist_button_rect = pygame.Rect(325, 220, 150, 50)
    generate_playlist_button_color = (50, 150, 255)
    generate_playlist_button_hover_color = (100, 200, 255)
    current_generate_button_color = generate_playlist_button_color

    # set-up toggle switch for sort mode
    heap_text = "HEAP SORT"
    bucket_text = "BUCKET SORT"
    sort_mode_instructions_text = "Press (H) for Heap Sort or (B) for Bucket Sort"
    sort_mode_button_rect = pygame.Rect(50, 220, 100, 50)
    sort_mode_button_color = (50, 150, 255)

    # Initialize Pygame
    pygame.init()

    # Set up display
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("McMichMixMigee Menu")
    clock = pygame.time.Clock()

    font = pygame.font.Font("SegUIVar.ttf", 14)
    font_big = pygame.font.Font("SegUIVar.ttf", 14)

    # generate button text set-up
    surf = font.render(generate_text, True, (255, 255, 255))
    text_rect = surf.get_rect()
    text_rect.center = (400, 245)  # +70 y to recbox


    checkboxes = []
    checkOrder = []
    slider_rects = []
    slider_color = (50, 150, 255)
    handle_radius = 10
    handle_color = (255, 255, 255)
    slider_decimal = [0] * len(playlist_features.available_features)


    index = 0
    x_dimension = 15
    y_dimension = 15
    prev_x_dimension = 0
    for feature in playlist_features.available_features:
        if index % 4 == 0:
            x_dimension = 15
            y_dimension = 15 * (index + 1)
        else:
            x_dimension = prev_x_dimension + 185
        checkboxes.append(Checkbox(x_dimension, y_dimension, feature))
        slider_rects.append(pygame.Rect(x_dimension + 8 + 60, y_dimension + 25 + 20, 140, 10))
        index += 1
        prev_x_dimension = x_dimension

    # Main game loop
    running = True
    mouse_drag = False
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i in range(len(checkboxes)):
                        if checkboxes[i].rect.collidepoint(event.pos):
                            checkboxes[i].checked = not checkboxes[i].checked
                            if checkboxes[i].checked:
                                checkOrder.append(i)
                                checkboxes[i].select = len(checkOrder)
                                user_requirements = fake_get_user_input(slider_decimal, checkboxes, checkOrder)
                            else:
                                checkOrder.remove(i)
                                for j in range(len(checkOrder)):
                                    checkboxes[checkOrder[j]].select = j + 1
                mouse_drag = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_drag = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    sort_mode = True
                elif event.key == pygame.K_b:
                    sort_mode = False

        for checkbox in checkboxes:
            checkbox.display(screen, font)

        for i in range(len(slider_rects)):
            if checkboxes[i].checked:
                if mouse_drag and slider_rects[i].collidepoint(event.pos):
                    slider_decimal[i] = max(0, min((event.pos[0] - slider_rects[i].left) / slider_rects[i].width, 1))
                    user_requirements = fake_get_user_input(slider_decimal, checkboxes, checkOrder)

                pygame.draw.rect(screen, slider_color, slider_rects[i])
                handle_x = slider_rects[i].left + int(slider_rects[i].width * slider_decimal[i])
                pygame.draw.circle(screen, handle_color, (handle_x, slider_rects[i].centery), handle_radius)
                if playlist_features.available_features[i] == "KEY":
                    value_surface = font.render(KEY_SIGNATURES[user_requirements[playlist_features.available_features[i]][1]], True, (255, 255, 255))
                elif playlist_features.available_features[i] == "MODE":
                    if user_requirements[playlist_features.available_features[i]][1] == 1:
                        value_surface = font.render(
                            "Major", True,
                            (255, 255, 255))
                    else:
                        value_surface = font.render(
                            "Minor", True,
                            (255, 255, 255))
                else:
                    value_surface = font.render(str(round(user_requirements[playlist_features.available_features[i]][1], 2)), True, (255, 255, 255))
                screen.blit(value_surface, (handle_x + 10, slider_rects[i].centery - 4))

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
                user_requirements = fake_get_user_input(slider_decimal, checkboxes,
                                                        checkOrder)  # delete this later and replace with data from scroll_bars
                song_id_points_pair_list = load_songs_points(songs_list, user_requirements)
                # print(song_id_points_pair_list)  # for debugging purposes

                """ 
                # 1. determine sort_mode to choose sort algorithm

                    if sort_mode:
                        heap_sort(song_points_pair_list)
                    else:
                        bucket_sort(song_points_pair_list)

                # 2. get top 8 songs and their corresponding album cover images

                    song_points_pair_list = sort(song_points_pair_list)
                    selected_song_ids = [] # top 8 songs from sorted song_points_pair_list
                    image_urls = []
                    for song_id in selected_song_ids:
                        image_urls.append(get_album_track_img(song_id)

                    print_playlist_data(selected_song_ids)  # prints generated playlist data

                """

                # replace below block of code after implementing sorting
                selected_song_ids = []
                selected_songs = []
                image_urls = []
                song_count = 1
                max_index = len(songs_list) - 1
                while song_count < 9:
                    rand_index = random.randint(0, max_index)
                    song = songs_list[rand_index]
                    selected_songs.append(song)
                    selected_song_ids.append(song[feature_indices["ID"]])
                    image_urls.append(get_album_track_img(song[feature_indices["ID"]]))
                    song_count += 1

                print_playlist_data(selected_song_ids)  # prints generated playlist data
            #song name list
            song_names = []
            for sel_song in selected_songs:
                song_names.append(sel_song[1])

            # Load images from urls
            images = []
            for url in image_urls:
                images.append(load_image_from_url(url))
            image_rect_list=[]
            # draw album images on screen
            img_index = 0
            for image in images:
                square_rect = image.get_rect()
                mask = pygame.Surface((int(square_rect.width), int(square_rect.width)), pygame.SRCALPHA)
                pygame.draw.circle(mask, (255, 255, 255, 255), (square_rect.width // 2, square_rect.width // 2),
                                   square_rect.width // 2)
                adjust = square_rect.width // 2

                screen.blit(image, img_positions[img_index])
                screen.blit(mask, img_positions[img_index], special_flags=pygame.BLEND_RGBA_MULT)
                pygame.draw.circle(screen, (255, 250, 250),
                                   ((img_positions[img_index][0] + adjust), img_positions[img_index][1] + adjust),
                                   square_rect.width // 2, width=3)
                hover_surface=mask.get_rect()
                hover_surface.topleft=img_positions[img_index]
                image_rect_list.append(hover_surface)
                #song name
                name_surface = font_big.render(song_names[img_index], True, (255, 255, 255))
                name_text_rect = name_surface.get_rect()
                name_text_rect.center = (170+img_index*150, 430)
                if img_index > 3:
                    name_text_rect.center = (170 + (img_index-4) * 150, 580)
                screen.blit(name_surface, name_text_rect)

                img_index += 1
            # print("loaded data")  # for debugging purposes

            #hover preiew feature
            counter=0
            hovered_song=""
            for rect in image_rect_list:
                if rect.collidepoint(mouse_x, mouse_y):
                    break
                counter += 1
            if(counter<8):
                hovered_song=selected_songs[counter]
                print(hovered_song[1])
                pygame.draw.rect(screen,(GRAY),((40,20),(700,150)),border_radius=20)
                count=0
                true_count=0
                # 1name 2album 4artist 6trackNum 8explicit 9dancibility 10energy 11key 12loudness 13mode
                for song in hovered_song:
                    if (count==1) or (count==2) or (count==4) or (count==6) or (count==8) or (count==9) or (count==10) or (count==11) or (count==12) or (count==13) or (count==18) or (count==19):
                        if(count==1): pre_text="Name:"
                        if (count == 2): pre_text = "Album:"
                        if (count == 4): pre_text = "Artist:"
                        if (count == 6): pre_text = "Track:"
                        if (count == 8): pre_text = "Explicit:"
                        if (count == 9): pre_text = "dancibility:"
                        if (count == 10): pre_text = "Energy:"
                        if (count == 11): pre_text = "Key:"
                        if (count == 12): pre_text = "Loudness:"
                        if (count == 13): pre_text = "Mode:"
                        if (count == 18): pre_text = "Valence:"
                        if (count == 19): pre_text = "Tempo:"


                        pre_text_surface = font.render(pre_text, True, (255, 255, 255))
                        pre_text_rect = pre_text_surface.get_rect()
                        pre_text_rect.topleft = (50 + true_count * 100, 30)
                        if true_count == 1:
                            pre_text_rect.topleft = (50 + (true_count - 1) * 100, 30 + 20)
                        elif true_count == 2:
                            pre_text_rect.topleft = (50 + (true_count - 2) * 100, 30 + 40)
                        elif true_count == 3:
                            pre_text_rect.topleft = (50 + (true_count - 3) * 100, 30 + 60)
                        elif true_count==4:
                            pre_text_rect.topleft = (50 + (true_count - 4) * 130, 30 + 80)
                        elif true_count==5:
                            pre_text_rect.topleft = (50 + (true_count - 5) * 130, 30 + 100)
                        elif true_count==6:
                            pre_text_rect.topleft = (50 + (true_count - 6) * 130+400, 30)
                        elif true_count==7:
                            pre_text_rect.topleft = (50 + (true_count - 7) * 130+400, 30+20)
                        elif true_count==8:
                            pre_text_rect.topleft = (50 + (true_count - 8) * 130+400, 30+40)
                        elif true_count == 9:
                            pre_text_rect.topleft = (50 + (true_count - 9) * 130 + 400, 30+60)
                        elif true_count == 10:
                            pre_text_rect.topleft = (50 + (true_count - 10) * 130 + 400, 30 + 80)
                        elif true_count == 11:
                            pre_text_rect.topleft = (50 + (true_count - 11) * 130 + 400, 30 + 100)
                        screen.blit(pre_text_surface, pre_text_rect)

                        text = hovered_song[count]
                        if (count==1) or (count==2) or (count==4):
                            text=text
                        else:
                            text=text[0:5]
                        info_text_surface=font.render(text,True,(255,255,255))
                        info_text_rect=info_text_surface.get_rect()
                        info_text_rect.topleft=(100+true_count*100,30)
                        if true_count==1:
                            info_text_rect.topleft = (100 + (true_count-1) * 100, 30+ 20)
                        elif true_count==2:
                            info_text_rect.topleft = (100 + (true_count - 2) * 100, 30 + 40)
                        elif true_count==3:
                            info_text_rect.topleft = (100 + (true_count - 3) * 100, 30 + 60)
                        elif true_count == 4:
                            info_text_rect.topleft = (100 + (true_count - 4) * 130, 30 + 80)
                        elif true_count == 5:
                            info_text_rect.topleft = (100 + (true_count - 5) * 130+20, 30 + 100)
                        elif true_count == 6:
                            info_text_rect.topleft = (100 + (true_count - 6) * 130 + 400, 30)
                        elif true_count == 7:
                            info_text_rect.topleft = (100 + (true_count - 7) * 130 + 400-20, 30+20)
                        elif true_count == 8:
                            info_text_rect.topleft = (100 + (true_count - 8) * 130 + 400+18, 30+40)
                        elif true_count == 9:
                            info_text_rect.topleft = (100 + (true_count - 9) * 130 + 400-4, 30+60)
                        elif true_count == 10:
                            info_text_rect.topleft = (100 + (true_count - 10) * 130 + 400+3, 30 + 80)
                        elif true_count == 11:
                            info_text_rect.topleft = (100 + (true_count - 11) * 130 + 400, 30 + 100)
                        screen.blit(info_text_surface,info_text_rect)
                        true_count+=1
                    count+=1



        # set sort-mode button text (H or B)
        if sort_mode:
            surf_sort = font_big.render(heap_text, True, (255, 255, 255))
        else:
            surf_sort = font_big.render(bucket_text, True, (255, 255, 255))
        text_rect_sort = surf_sort.get_rect()
        text_rect_sort.center = (100, 245)  # +70 y to recbox

        surf_sort_instruct = font.render(sort_mode_instructions_text, True, (255, 255, 255))
        text_rect_sort_instruct = surf_sort_instruct.get_rect()
        text_rect_sort_instruct.center = (150, 275)


        # draw generate playlist button
        pygame.draw.rect(screen, current_generate_button_color, generate_playlist_button_rect, border_radius=50)

        # draw sort mode button
        pygame.draw.rect(screen, sort_mode_button_color, sort_mode_button_rect, border_radius=50)

        # draw generate playlist button text
        screen.blit(surf, text_rect)
        # draw sort-mode button text
        screen.blit(surf_sort, text_rect_sort)
        screen.blit(surf_sort_instruct, text_rect_sort_instruct)

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
        song_id_points_pair_list.append(
            (song[feature_indices["ID"]], float(song[feature_indices["POINTS"]].replace("\n", ""))))

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
