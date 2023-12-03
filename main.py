import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

import pygame
import requests
from io import BytesIO

from checkbox import Checkbox
import playlist_features

# set-up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
Dark_GRAY = (64, 64, 64)
GRAY = (128, 128, 128)

ID = 0
NAME = 1
ALBUM = 2
ALBUM_ID = 3
ARTISTS = 4
ARTIST_IDS = 5
TRACK_NUMBER = 6
DISC_NUMBER = 7
EXPLICIT = 8
DANCEABILITY = 9
ENERGY = 10
KEY = 11
LOUDNESS = 12
MODE = 13
SPEECHINESS = 14
ACOUSTICNESS = 15
INSTRUMENTALNESS = 16
LIVENESS = 17
VALENCE = 18
TEMPO = 19
DURATION_ms = 20
TIME_SIGNATURE = 21
YEAR = 22
RELEASE_DATE = 23
link = 'https://static.wikia.nocookie.net/gensin-impact/images/2/21/Neuvillette_Icon.png/revision/latest/scale-to-width/360?cb=20230927021051'

# TODO: it would be easier to get/print user input data through the terminal
#  so maybe dont have the check boxes on pygame
#  and instead just display the playlist and the new/clear buttons


# TODO: start making the data structures and algorithms
# priority queue (heap) vs ????
# maybe add this feature: option to upload generated playlist to user's spotify account

def main():
    songs_list = get_songs_from_file(5, "tracks_features.csv")

    img_urls = [link, link, link, link, link, link, link, link]
    # img_urls = []
    # for song in songs_list:
    # img_urls.append(get_album_track_img(song[ID]))

    display_playlist(img_urls)


# Function to display playlist of selected songs
def display_playlist(image_urls):
    generate_playlist_button_clicked = False
    new_playlist_button_clicked = False

    # Initialize Pygame
    pygame.init()

    # Set up display
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("GrooveCraft Menu")

    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 18)

    # Load image from URL
    images = []
    for url in image_urls:
        images.append(load_image_from_url(url))

    checkboxes = []
    slider_rects = []
    slider_color = (50, 150, 255)
    handle_radius = 10
    handle_color = (255, 255, 255)

    slider_values = [0]*len(playlist_features.available_features)

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









        # button for playlist generation
        generate_playlist_button_rect = pygame.Rect(500, 200, 100, 50)

        # button for new playlist
        new_playlist_button_rect = pygame.Rect(650, 200, 100, 50)

        generate_playlist_button_color = (50, 150, 255)
        generate_playlist_button_hover_color = (100, 200, 255)

        new_playlist_button_color = (200, 25, 0)
        new_playlist_hover_color = (250, 50, 0)

        # get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # check if mouse is over generate playlist button
        if generate_playlist_button_rect.collidepoint(mouse_x, mouse_y):
            current_generate_button_color = generate_playlist_button_hover_color
            # button clicked
            if pygame.mouse.get_pressed()[0]:  # Left mouse button
                print("Button clicked!")
                generate_playlist_button_clicked = True
        # check if mouse is over new playlist button
        elif new_playlist_button_rect.collidepoint(mouse_x, mouse_y):
            current_new_playlist_button_color = new_playlist_hover_color
            # button clicked
            if pygame.mouse.get_pressed()[0]:  # Left mouse button
                print("new clicked!")
                new_playlist_button_clicked = True
        else:
            current_generate_button_color = generate_playlist_button_color
            current_new_playlist_button_color = new_playlist_button_color

        if generate_playlist_button_clicked:
            # draw album images on screen
            img_positions = [(125, 325), (275, 325), (425, 325), (575, 325),
                             (125, 475), (275, 475), (425, 475), (575, 475)]
            img_index = 0
            for image in images:
                screen.blit(image, img_positions[img_index])
                img_index += 1

            if new_playlist_button_clicked:
                screen.fill(BLACK)
                generate_playlist_button_clicked = False
                new_playlist_button_clicked = False

        # Draw generate playlist button
        pygame.draw.rect(screen, current_generate_button_color, generate_playlist_button_rect)

        # Draw new playlist button
        pygame.draw.rect(screen, current_new_playlist_button_color, new_playlist_button_rect)

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    clock.tick(60)


# Function to load an image from a URL
def load_image_from_url(url, img_dimensions=(100, 100)):
    response = requests.get(url)
    img_data = BytesIO(response.content)
    img = pygame.image.load(img_data)
    img = pygame.transform.scale(img, img_dimensions)
    return img


# reads file and returns list of songs data
def get_songs_from_file(num_of_songs=5, filename="tracks_features.csv"):
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


if __name__ == '__main__':
    main()

def heapSort(array):
    for index in range(len(array)/2 - 1):
        i = index
        while i < len(array)/2 - 1:
            if array[i] < array[i * 2 + 1] < array[i * 2 + 2]:
                array[i], array[i*2 + 1] = array[i*2+1], array[i]
                i = i * 2 + 1
            elif array[i] < array[i*2 + 2]:
                array[i], array[i*2 + 2] = array[i*2 + 2], array[i]
                i = i*2 + 2

    for y in range(len(array) - 1, 0, -1):
        i = 0
        array[0], array[y] = array[y], array[0]
        while i < y/2 - 1:
            if array[i] < array[i * 2 + 1] < array[i * 2 + 2]:
                array[i], array[i * 2 + 1] = array[i * 2 + 1], array[i]
                i = i * 2 + 1
            elif array[i] < array[i * 2 + 2]:
                array[i], array[i * 2 + 2] = array[i * 2 + 2], array[i]
                i = i * 2 + 2
