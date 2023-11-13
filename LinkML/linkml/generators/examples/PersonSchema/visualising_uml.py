import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def show_image_with_zoom(image_path):
    # Laad de afbeelding
    img = mpimg.imread(image_path)

    # Maak een figuur en een as
    fig, ax = plt.subplots()

    # Toon de afbeelding
    ax.imshow(img)

    # Verwijder assen
    ax.axis('off')

    # Voeg de standaard Matplotlib navigatiebalk toe
    plt.gcf().canvas.manager.set_window_title("Afbeeldingsviewer")

    # Toon het venster
    plt.show()

# Gebruik de functie
show_image_with_zoom("personinfo.png")
