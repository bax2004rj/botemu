import pygame
import fileHandler
import eventHandler

# Function to draw rectangles
def draw_rectangle(screen, rx, ry, px, py, rgb="#FFFFFF", transparent=False, alpha=100):
    rectangle = pygame.Surface((rx, ry))
    if transparent:
        rectangle.set_alpha(alpha)
    rectangle.fill(rgb)
    screen.blit(rectangle, (px, py))


# Function to create rectangles
def get_rectangle(rx, ry, rgb="#FFFFFF", transparent=False, alpha=100):
    rectangle = pygame.Surface((rx, ry))
    if transparent:
        rectangle.set_alpha(alpha)
    rectangle.fill(rgb)
    return rectangle, rectangle.get_rect()


# Function to draw text
def draw_text(screen, x, y, font, text, rgb="#000000", aa=False):
    string = font.render(text, aa, rgb)  # Text to be drawn, and color.
    string_rect = string.get_rect()  # Grab the rectangle borders for the text.
    string_rect.center = (x, y)  # Coordinates for text to be drawn at.
    screen.blit(string, string_rect)  # Render 'string' to the screen at the position of 'string_rect'.


# Function to create text
def get_text(font, text, rgb="#000000", aa=False):
    rendered_text = font.render(text, aa, rgb)  # Text to be drawn, and color.
    text_rect = rendered_text.get_rect()  # Grab the rectangle borders for the text.
    return rendered_text, text_rect

# Mini window system
class window:
    def __init__(self,screen,title,rect,closable,resizable,borderColor,active):
        content = pygame.Surface((rect[2],rect[3]))
        content.set_alpha(50)
        content.fill("#1c1c1c")
        border = pygame.Surface((rect[2],24))
        border.fill(borderColor)
        draw_text(screen,rect[0],rect[1]+12,fileHandler.font_small,title,"#FFFFFF")
        self.title = title
        self.borderColor = borderColor
        self.active = active
        self.closable = closable
        self.resizable = resizable
        self.rect = rect
        # create objects
        self.border = pygame.Surface((self.rect[2],24))
        self.border.fill(self.borderColor)
        self.content = pygame.Surface((self.rect[2],self.rect[3]))
        self.content.set_alpha(50)
        self.content.fill("#1c1c1c")
        if closable:
            self.closeButton = Button(fileHandler.font_small,24,24,0,0,0,text_color="#ffffff",hover_text_color="#ffffff",hover_box_color="#ff0000",box_color="#870000",selected_box_color="#ff8787",selected_text_color="#ffffff",text="X")
        self.panStartX = 0
        self.panStartY = 0
        self.dragging = False
        self.dragStartx = 0
        self.dragStarty = 0
        self.panOffsetX = 0
        self.panOffsetY = 0
        self.adjustedRectX = self.rect[0] + self.panOffsetX
        self.adjustedRectY = self.rect[1] + self.panOffsetY
        self.adjustedWidth = self.rect[2] + self.panOffsetX
        self.adjustedHeight = self.rect[3] + self.panOffsetY
    def update(self,screen,cursor_rect,events):
        # Blit content
        if self.active:
            self.adjustedRectX = self.rect[0] + self.panOffsetX
            self.adjustedRectY = self.rect[1] + self.panOffsetY
            self.adjustedWidth = self.rect[2] + self.panOffsetX
            self.adjustedHeight = self.rect[3] + self.panOffsetY
            self.checkRect = pygame.Rect((self.adjustedRectX,self.adjustedRectY),(self.adjustedWidth,self.adjustedHeight))
            screen.blit(self.content,(self.adjustedRectX,self.adjustedRectY))
            screen.blit(self.border,(self.adjustedRectX,self.adjustedRectY))
            draw_text(screen,(self.adjustedRectX+self.adjustedWidth)/2,self.adjustedRectY+12,fileHandler.font_small,self.title,"#FFFFFF")
            try:
                self.closeButton.button_box_rect.topleft = self.adjustedWidth,self.adjustedRectY
                self.closeButton.outline_rect.topleft = self.adjustedWidth,self.adjustedRectY
                self.closeButton.update(screen,cursor_rect,events)
                if self.closeButton.clicked_up:
                    self.active = False
            except Exception:
                pass
            if "mouse_button_down" in events:
                if eventHandler.eventButton == 1 and self.checkRect.collidepoint(cursor_rect.x,cursor_rect.y):
                    self.dragging = True
                    self.dragStartx,self.dragStarty = eventHandler.eventPos
                    self.panStartX = self.panOffsetX - self.dragStartx
                    self.panStartY = self.panOffsetY - self.dragStarty
            elif "mouse_button_up" in events:
                self.dragging = False
            elif "mouse_motion" in events:
                if self.dragging and self.checkRect.collidepoint(cursor_rect.x,cursor_rect.y):
                    self.dragStartx,self.dragStarty = eventHandler.eventPos
                    self.panOffsetX = self.dragStartx + self.panStartX
                    self.panOffsetY = self.dragStarty + self.panStartY

class checkButton:
    def __init__(self,font,text,mode="checkbox",posRect = [0,0,150,24],enabledColor = "#ffffff",
              disabledColor = "#0f0f0f",checkBoxUsesColors = False,hover_sound = None,
              click_sound = None,default_color = "#1f1f1f",default_state = False,text_color = "#ffffff",active = True):
            self.mode = mode # Modes availiable: checkbox, togglebutton, switch
            self.text = text
            self.font = font
            self.text_color = text_color
            self.posRect = posRect
            self.textPlacement = [self.posRect[2]/2+(24+self.posRect[0]),self.posRect[1]]
            self.data = False
            self.active = active
            self.defaultStateText = " "
            if mode == "checkbox":
                if default_state:
                    self.defaultStateText = "✓"
                    self.data = True
                self.button = Button(font,14,14,posRect[1],posRect[2],1,box_color=default_color,text=self.defaultStateText)
    def update(self,screen,cursor_rect,events):
        if self.mode == "checkbox" and self.active:
            if self.button.clicked_up and not self.data:
                self.data = True
                self.button.text = "✓"
            elif self.button.clicked_up and self.data:
                self.data = False
                self.button.text = " "
            self.button.update(screen,cursor_rect,events)
            draw_text(screen,self.textPlacement[0],self.textPlacement[1],self.font,self.text,self.text_color)
    def updatePos(self,x,y,w,h):
        self.posRect = (x,y,w,h)
        self.textPlacement = [self.posRect[2]/2+(24+self.posRect[0]),self.posRect[1]]        
        self.button.outline_rect.x=x
        self.button.outline_rect.y=y-12
        self.button.button_box_rect.x = x
        self.button.button_box_rect.y = y-12
# Button system
class Button:
    def __init__(self, font, rx=150, ry=100, px=0, py=0, outline_width=6, image_outline=False, aa=False,
                 button_type="procedural", selected_box_color="#196985", selected_text_color="#b2b2b2",
                 hover_box_color="#2596be", hover_text_color="#ffffff", box_color="#ffffff", text_color="#2596be",
                 outline_color="#000000", text="button", selected_button_image=None, hover_button_image=None,
                 button_image=None, hover_sound=None, click_sound=None, active=True, click_type="left"):
        self.clicked_down = False
        self.clicked_up = False
        self.hover = False

        self.button_type = button_type
        self.click_type = click_type

        self.selected_box_color = selected_box_color
        self.selected_text_color = selected_text_color
        self.hover_box_color = hover_box_color
        self.hover_text_color = hover_text_color
        self.box_color = box_color
        self.text_color = text_color
        self.outline_width = outline_width
        self.outline_color = outline_color
        self.image_outline = image_outline

        self.text = text
        self.rendered_text = None
        self.font = font
        self.aa = aa

        self.active = active

        self.hover_sound = hover_sound
        self.click_sound = click_sound

        self.hover_sound_played = False
        if self.button_type == "procedural" and button_image is None:
            self.button_box, self.button_box_rect = get_rectangle(rx, ry, self.box_color)
            self.outline, self.outline_rect = get_rectangle(rx + self.outline_width, ry + self.outline_width,
                                                            self.outline_color)

            self.button_box_rect.topleft = (px, py)
            self.outline_rect.topleft = (px - self.outline_width / 2, py - self.outline_width / 2)

            self.rendered_text, self.rendered_text_rect = get_text(self.font, self.text, self.text_color, self.aa)
            self.rendered_text_rect.center = self.button_box_rect.center

            self.button_image = self.button_box
            self.button_image_rect = self.button_box_rect
        elif self.button_type == "image" and button_image is not None:
            self.button_image = button_image
            self.selected_button_image = selected_button_image
            self.hover_button_image = hover_button_image

            self.button_image_rect = self.button_image.get_rect()
            self.selected_button_image_rect = self.selected_button_image.get_rect()
            self.hover_button_image_rect = self.hover_button_image.get_rect()

            self.button_image_rect.topleft = (px, py)
            self.selected_button_image_rect.topleft = (px, py)
            self.hover_button_image_rect.topleft = (px, py)

            self.button_mask = pygame.mask.from_surface(self.button_image)
            self.selected_button_mask = pygame.mask.from_surface(self.selected_button_image)
            self.hover_button_mask = pygame.mask.from_surface(self.hover_button_image)

            self.button_outline_points = []
            self.selected_button_outline_points = []
            self.hover_button_outline_points = []

            for point in self.button_mask.outline():
                x = point[0]+self.button_image_rect[0]
                y = point[1] + self.button_image_rect[1]
                self.button_outline_points.append((x, y))

            for point in self.selected_button_mask.outline():
                x = point[0]+self.hover_button_image_rect[0]
                y = point[1] + self.hover_button_image_rect[1]
                self.hover_button_outline_points.append((x, y))

            for point in self.hover_button_mask.outline():
                x = point[0]+self.selected_button_image_rect[0]
                y = point[1] + self.selected_button_image_rect[1]
                self.selected_button_outline_points.append((x, y))

            self.button_box = self.button_image
            self.button_box_rect = self.button_image_rect
        else:
            raise ValueError('Button_type is not procedural or image')

    def display_button(self, screen):
        if self.button_type == "procedural":
            if not self.clicked_down:
                if not self.hover:
                    self.button_box.fill(self.box_color)
                    self.rendered_text, self.rendered_text_rect = get_text(self.font, self.text, self.text_color)
                    self.rendered_text_rect.center = self.button_box_rect.center

                    screen.blit(self.outline, self.outline_rect)
                    screen.blit(self.button_box, self.button_box_rect)
                    screen.blit(self.rendered_text, self.rendered_text_rect)
                elif self.hover:
                    self.button_box.fill(self.hover_box_color)
                    self.rendered_text, self.rendered_text_rect = get_text(self.font, self.text, self.hover_text_color)
                    self.rendered_text_rect.center = self.button_box_rect.center

                    screen.blit(self.outline, self.outline_rect)
                    screen.blit(self.button_box, self.button_box_rect)
                    screen.blit(self.rendered_text, self.rendered_text_rect)
            elif self.clicked_down:
                self.button_box.fill(self.selected_box_color)
                self.rendered_text, self.rendered_text_rect = get_text(self.font, self.text, self.selected_text_color)
                self.rendered_text_rect.center = self.button_box_rect.center

                screen.blit(self.outline, self.outline_rect)
                screen.blit(self.button_box, self.button_box_rect)
                screen.blit(self.rendered_text, self.rendered_text_rect)
        elif self.button_type == "image":
            if not self.clicked_down:
                if not self.hover:
                    if self.image_outline:
                        for point in self.button_outline_points:
                            pygame.draw.circle(screen, self.outline_color, point, self.outline_width)
                    screen.blit(self.button_image, self.button_image_rect)
                elif self.hover and self.hover_button_image is not None:
                    if self.image_outline:
                        for point in self.hover_button_outline_points:
                            pygame.draw.circle(screen, self.outline_color, point, self.outline_width)
                    screen.blit(self.hover_button_image, self.hover_button_image_rect)
                else:
                    if self.image_outline:
                        for point in self.button_outline_points:
                            pygame.draw.circle(screen, self.outline_color, point, self.outline_width)
                    screen.blit(self.button_image, self.button_image_rect)
            elif self.clicked_down:
                if self.image_outline:
                    for point in self.selected_button_outline_points:
                        pygame.draw.circle(screen, self.outline_color, point, self.outline_width)
                screen.blit(self.selected_button_image, self.selected_button_image_rect)

    def click_check(self, cursor_rect, events):
        if self.button_box_rect.collidepoint(cursor_rect.topleft) or self.button_image_rect.collidepoint(cursor_rect.topleft):
            if self.click_type == "left":
                if self.clicked_down is False and "left_mouse_button_down" in events:
                    self.clicked_down = True
                    self.hover = False
                elif self.clicked_up is False and "left_mouse_button_up" in events:
                    if self.click_sound is not None:
                        pygame.mixer.Sound.play(self.click_sound)
                    self.clicked_down = False
                    self.clicked_up = True
                    self.hover = False
                elif "left_mouse_button_down" not in events and "left_mouse_button_up" not in events:
                    if self.hover_sound is not None:
                        if not self.hover_sound_played:
                            pygame.mixer.Sound.play(self.hover_sound)
                            self.hover_sound_played = True
                    self.clicked_up = False
                    self.hover = True
            elif self.click_type == "right":
                if self.clicked_down is False and "right_mouse_button_down" in events:
                    self.clicked_down = True
                    self.hover = False
                elif self.clicked_up is False and "right_mouse_button_up" in events:
                    if self.click_sound is not None:
                        pygame.mixer.Sound.play(self.click_sound)
                    self.clicked_down = False
                    self.clicked_up = True
                    self.hover = False
                elif "right_mouse_button_down" not in events and "right_mouse_button_up" not in events:
                    if self.hover_sound is not None:
                        if not self.hover_sound_played:
                            pygame.mixer.Sound.play(self.hover_sound)
                            self.hover_sound_played = True
                    self.clicked_up = False
                    self.hover = True
            elif self.click_type == "scroll":
                if self.clicked_down is False and "scroll_mouse_button_down" in events:
                    self.clicked_down = True
                    self.hover = False
                elif self.clicked_up is False and "scroll_mouse_button_up" in events:
                    if self.click_sound is not None:
                        pygame.mixer.Sound.play(self.click_sound)
                    self.clicked_down = False
                    self.clicked_up = True
                    self.hover = False
                elif "scroll_mouse_button_down" not in events and "scroll_mouse_button_up" not in events:
                    if self.hover_sound is not None:
                        if not self.hover_sound_played:
                            pygame.mixer.Sound.play(self.hover_sound)
                            self.hover_sound_played = True
                    self.clicked_up = False
                    self.hover = True
            elif self.click_type == "keyboard":
                pass
        else:
            self.clicked_down = False
            self.clicked_up = False
            self.hover = False
            self.hover_sound_played = False

    def update(self, screen, cursor_rect, events):
        try:
            if self.active:
                self.click_check(cursor_rect, events)
                self.display_button(screen)
            else:
                pass
        except AttributeError:
            print("Click check failed")

    def updatePos(self,x,y,w,h):    
        self.outline_rect.x=x
        self.outline_rect.y=y
        self.outline_rect.w=w
        self.outline_rect.w=h
        self.button_box_rect.x = x
        self.button_box_rect.y = y
        self.button_box_rect.w = w
        self.button_box_rect.h = h

class dropdown():
    def __init__(self,x,y,explainerText,options,defaultOption = None,w=70,h=14):
        self.x = x
        self.y = y 
        self.w = w
        self.h = h
        self.explainerText = explainerText
        self.options = options
        if defaultOption == None:
            self.buttonText = "Choose"
        else:
            self.buttonText = defaultOption

        self.optionButton = Button(fileHandler.font_small,self.x,self.y,self.w,self.h,text=self.defaultText)