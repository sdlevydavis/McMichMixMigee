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
ARTISTS = 3
EXPLICIT = 4
DANCEABILITY = 5
ENERGY = 6
KEY = 7
LOUDNESS = 8
MODE = 9
SPEECHINESS = 10
ACOUSTICNESS = 11
INSTRUMENTALNESS = 12
LIVENESS = 13
VALENCE = 14
TEMPO = 15
DURATION_milsecs = 16
YEAR = 17
DURATION_mins = 18
link = 'https://static.wikia.nocookie.net/gensin-impact/images/2/21/Neuvillette_Icon.png/revision/latest/scale-to-width/360?cb=20230927021051'

# TODO: it would be easier to get/print user input data through the terminal
#  so maybe dont have the check boxes on pygame
#  and instead just display the playlist and the new/clear buttons


# TODO: start making the data structures and algorithms

def main():
    songs_list = get_songs_from_file("tracks_features_condensed.csv", 5)

    img_urls = [link, link, link, link, link, link, link, link]
    # img_urls = []
    # for song in songs_list:
    # img_urls.append(get_album_track_img(song[ID]))


    #commentted out to test pygame
    #user_priorities = get_user_input()

    print()
    next_step = input("Type (Y) to open playlist recommendation screen or type any other key to exit the program: ")
    if next_step.lower() == "y":
        display_playlist(img_urls)
    print()
    print("Thank You For Using McMichMixMigee Playlist Generator :)")


def get_user_input():
    user_priorities = []
    welcome_msg = "Welcome to McMichMixMigee Playlist Generator!"
    msg_length = len(welcome_msg) / 2
    while msg_length > 0:
        print("_ ", end="")
        msg_length -= 1
    print()
    print(welcome_msg)
    print()
    print("Priority is an integer from 1 (most important) to 19 (least important)")
    print("You can give different features the same priorities.\n")
    print(f"Available Playlist Features:\n"
          f"1. INSTRUMENTALNESS\n"
          f"2. LOUDNESS\n"
          f"3. ALBUM\n"
          f"4. ARTISTS\n"
          f"5. EXPLICIT\n"
          f"6. ACOUSTICNESS\n"
          f"7. RELEASE_DATE\n"
          f"8. KEY\n"
          f"9. NAME\n"
          f"10. MODE\n"
          f"11. DANCEABILITY\n"
          f"12. LIVENESS\n"
          f"13. VALENCE\n"
          f"14. TEMPO\n"
          f"15. SPEECHINESS\n"
          f"16. DURATION (mins)\n"
          f"17. ENERGY\n")
    for feature in playlist_features.available_features:
        p = input(f"Input priority for feature - {feature}: ")
        while not p.isnumeric() or int(p) > 19 or int(p) < 1:
            print("Invalid Input! Enter an integer from 1 to 19")
            p = input(f"Input priority for feature - {feature}: ")
        user_priorities.append((p, feature))
    print()
    return user_priorities


# Function to display playlist of selected songs
def display_playlist(image_urls):
    generate_playlist_button_clicked = False
    new_playlist_button_clicked = False

    # Initialize Pygame
    pygame.init()

    # Set up display
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("McMichMixMigee Menu")

    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 18)

    # Load image from URL
    images = []
    for url in image_urls:
        images.append(load_image_from_url(url))

    # checkboxes section
    checkboxes = []
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
        index += 1
        prev_x_dimension = x_dimension

    # Main game loop
    running = True
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

        for checkbox in checkboxes:
            checkbox.display(screen, font)

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
                #creating a circular mask which over
                square_rect = image.get_rect()
                mask = pygame.Surface((int(square_rect.width), int(square_rect.width)), pygame.SRCALPHA)
                pygame.draw.circle(mask, (255, 255, 255, 255), (square_rect.width//2, square_rect.width//2), square_rect.width//2)

                screen.blit(image, img_positions[img_index])
                screen.blit(mask, img_positions[img_index], special_flags=pygame.BLEND_RGBA_MULT)
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


if __name__ == '__main__':
    main()

