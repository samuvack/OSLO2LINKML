
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.widgets import Button
import matplotlib.image as mpimg
from tkinter import simpledialog, Tk
import matplotlib
print(matplotlib.get_backend())
matplotlib.use('Qt5Agg')
import cairosvg
import io
import os


class ImageAnnotator:
    def __init__(self, ax, fig, img):
        self.ax = ax
        self.fig = fig
        self.img = img
        self.annotating = False
        self.annotations = []
        self.root = Tk()
        self.root.withdraw()  # Verberg het hoofdvenster van Tk
        self.button = None
        self.original_xlim = self.ax.get_xlim()
        self.original_ylim = self.ax.get_ylim()
        
        
    def onclick(self, event):
        if self.annotating and event.inaxes == self.ax and event.xdata is not None and event.ydata is not None:
            annotation_text = simpledialog.askstring("Annotatie", "Voer annotatietekst in:", parent=self.root)
            if annotation_text:
                annot = self.ax.annotate(annotation_text, (event.xdata, event.ydata), 
                                         textcoords="offset points", xytext=(0,10), ha='center',
                                         bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", edgecolor="black", lw=1))
                self.annotations.append(annot)
                self.fig.canvas.draw()

    def on_double_click(self, event):
        if event.dblclick:
            for annot in self.annotations:
                if annot.contains(event)[0]:
                    new_text = simpledialog.askstring("Bewerk Annotatie", "Voer nieuwe annotatietekst in:", initialvalue=annot.get_text(), parent=self.root)
                    if new_text is not None:
                        annot.set_text(new_text)
                        self.fig.canvas.draw()
                        break

    def toggle_annotating(self, event):
        self.annotating = not self.annotating
        if self.annotating:
            self.button.color = 'lightgreen'
            self.cid_click = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        else:
            self.button.color = '0.85'
            self.fig.canvas.mpl_disconnect(self.cid_click)
        self.button.hovercolor = self.button.color
        self.button.ax.figure.canvas.draw()

    def on_scroll(self, event):
        if event.inaxes == self.ax:
            x, y = event.xdata, event.ydata
            scale_factor = 1.5 if event.button == 'up' else 1 / 1.5

            cur_xlim = self.ax.get_xlim()
            cur_ylim = self.ax.get_ylim()

            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

            self.ax.set_xlim([x - new_width / 2, x + new_width / 2])
            self.ax.set_ylim([y - new_height / 2, y + new_height / 2])

            self.fig.canvas.draw()

    
    def on_resize(self, event):
        # Pas de grootte van de ax aan om de afbeelding correct weer te geven
        self.ax.set_position([0, 0, 1, 1])  # Vul het volledige figuur
        self.ax.set_xlim(0, self.img.shape[1])
        self.ax.set_ylim(self.img.shape[0], 0)
        self.fig.canvas.draw_idle()
        
def load_image(image_path):
    _, ext = os.path.splitext(image_path)
    if ext.lower() in ['.png', '.jpg', '.jpeg']:
        return mpimg.imread(image_path)
    elif ext.lower() == '.svg':
        # Gebruik pycairo om SVG te laden
        surface = cairo.SVGSurface(image_path, 1280, 720)  # Pas de grootte aan indien nodig
        context = cairo.Context(surface)
        surface.write_to_png('temp.png')  # Tijdelijk PNG-bestand
        img = mpimg.imread('temp.png')
        os.remove('temp.png')  # Verwijder het tijdelijke bestand
        return img
    else:
        raise ValueError("Ondersteunt alleen PNG, JPG en SVG bestanden")

def maximize_window(mng):
    backend = matplotlib.get_backend()
    if backend == 'TkAgg':
        mng.window.state('zoomed')
    elif backend == 'Qt5Agg':
        mng.window.showMaximized()
    elif backend == 'Gtk3Agg':
        mng.window.maximize()
            
def show_image_with_annotations(image_path):
    fig, ax = plt.subplots()
    img = load_image(image_path)
    ax.imshow(img)
    ax.axis('off')

    annotator = ImageAnnotator(ax, fig, img)

    ax_button = plt.axes([0.9, 0.01, 0.08, 0.05])
    annotator.button = Button(ax_button, 'Annoteren', color='0.85', hovercolor='0.85')
    annotator.button.on_clicked(annotator.toggle_annotating)

    fig.canvas.mpl_connect('button_press_event', annotator.on_double_click)
    fig.canvas.mpl_connect('scroll_event', annotator.on_scroll)
    fig.canvas.mpl_connect('resize_event', annotator.on_resize)

    annotator.on_resize(None)  # Zorg ervoor dat de afbeelding initieel het volledige venster vult

    # Maximaliseer het venster
    mng = plt.get_current_fig_manager()
    maximize_window(mng)
    plt.rcParams["figure.autolayout"] = True
    plt.show()



# Gebruik de functie
show_image_with_annotations("test.svg")
