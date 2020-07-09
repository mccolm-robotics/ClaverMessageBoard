import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GdkPixbuf
from interface.settings.SettingsMenuTemplate import SettingsMenuTemplate
import interface.settings.Settings as settings

class AboutMenu(SettingsMenuTemplate):

    __DEFAULT_CONTENT_WIDTH = 882  # ! NOTE !! - This is only true for 1280 * 720

    def __init__(self, settingsManager):
        """ Constructor """
        super().__init__(settingsManager)
        self.__headerImageFile = settings.res_dir['TEXTURES'] + "AboutHeader.png"
        self.__headerImageWidth = 800
        self.__headerImageHeight = 219
        self.__headerImage = None
        self.__portraitImageFile = settings.res_dir['TEXTURES'] + "ClaverCanvasMatthew.png"
        self.__portraitImageWidth = 250
        self.__portraitImageHeight = 350
        self.__portraitImage = None
        self.__layoutContainer = Gtk.Overlay()
        self.__build_content()

    def getLayoutContainer(self):
        """ Accessor function: returns Gtk layout container """
        return self.__layoutContainer

    @SettingsMenuTemplate.callback_on_resize
    def resizeAreaCallback(self):
        if super().getContentAreaSize()[0] != self.__DEFAULT_CONTENT_WIDTH:
            self.__DEFAULT_CONTENT_WIDTH = super().getContentAreaSize()[0]
            self.__updateHeaderImage()
            self.__updatePortraitImage()

    def __build_content(self):
        main_layer = Gtk.Grid(column_homogeneous=False, column_spacing=0, row_spacing=0)

        # Header Image
        self.image_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.image_box.set_hexpand(True)
        self.__headerImage = self.__constructHeaderImage(width=self.__headerImageWidth, height=self.__headerImageHeight, file=self.__headerImageFile, margin=15, hexpand=True)
        self.image_box.add(self.__headerImage)
        main_layer.attach(child=self.image_box, left=0, top=0, width=1, height=1)   # Add label to top of grid container

        # Information Area
        contentBox = Gtk.Box()
        contentBox.set_vexpand(True)
        contentBox.set_valign(Gtk.Align.START)
        contentBox.set_halign(Gtk.Align.CENTER)
        contentBox.get_style_context().add_class('test')
        self.__setAboutDetails(contentBox)
        main_layer.attach(child=contentBox, left=0, top=1, width=1, height=1)  # Add label to top of grid container
        self.__layoutContainer.add(main_layer)

        # Header Portrait
        self.__portrait_box = Gtk.Box()
        self.__portrait_box.set_halign(Gtk.Align.END)
        self.__portrait_box.set_valign(Gtk.Align.START)
        self.__portraitImage = self.__constructHeaderImage(width=self.__portraitImageWidth, height=self.__portraitImageHeight, file=self.__portraitImageFile, css='about-menu-portrait')
        self.__portrait_box.add(self.__portraitImage)
        self.__layoutContainer.add_overlay(self.__portrait_box)

    def __constructHeaderImage(self, width, height, file, margin=0, css=None, hexpand=False):
        buffer = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=file,
            width=width,
            height=height,
            preserve_aspect_ratio=True)
        image = Gtk.Image.new_from_pixbuf(buffer)
        image.set_hexpand(hexpand)
        image.set_margin_top(margin)
        if css is not None:
            image.get_style_context().add_class(css)
        return image

    def __updateHeaderImage(self):
        self.image_box.remove(self.__headerImage)
        self.__headerImage = self.__constructHeaderImage(width=0.9 * super().getContentAreaSize()[0], height=self.__headerImageWidth / self.__headerImageHeight * 0.9 * super().getContentAreaSize()[0], file=self.__headerImageFile, margin=15, hexpand=True)
        self.image_box.add(self.__headerImage)
        self.image_box.show_all()

    def __updatePortraitImage(self):
        self.__portrait_box.remove(self.__portraitImage)
        self.__portraitImage = self.__constructHeaderImage(width=0.283 * super().getContentAreaSize()[0], height=self.__portraitImageWidth / self.__portraitImageHeight * 0.9 * super().getContentAreaSize()[0], file=self.__portraitImageFile, css='about-menu-portrait')
        self.__portrait_box.add(self.__portraitImage)
        self.__portrait_box.show_all()

    def __setAboutDetails(self, contentBox):
        # - get required info details
        # - send off to convert to labels
        # - add to content box
        build = self.__addItemLabel("Build", settings.build_number)
        contentBox.add(build)

    def __addItemLabel(self, title, value):
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box.set_homogeneous(False)
        cat_title = Gtk.Label()
        cat_title.set_text(title)
        cat_value = Gtk.Label()
        cat_value.set_text(value)
        cat_value.get_style_context().add_class('test-size')
        box.add(cat_title)
        box.add(cat_value)
        return box
