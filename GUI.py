from numpy.lib.stride_tricks import DummyArray
import pygame
from pygame import key
from pygame.draw import rect
from pygame.locals import *
import cv2
from pynput.mouse import Button, Controller
from pynput.keyboard import Controller as KeyboardController


class HandRecogGUI:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Hand Recognition Project!")
        self.display = pygame.display.set_mode((1280, 600))
        self.text_pos = []
        self.text_text = ['02_l', '04_two','09_c', '10_down', '06_index', '08_three', '07_ok', '05_thumb', '01_palm', '03_bunny', 
                         'kb_left', 'kb_right','kb_up', 'kb_down', 'kb_select', 'm_up', 'm_down', 'm_right', 'm_left', 'm_select',
                         "Submit",
                         '01_palm: None', '02_l: None', '03_bunny: None', '04_two: None', '05_thumb: None', '06_index: None', '07_ok: None', '08_three: None', '09_c: None', '10_down: None',
                         'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 
                         'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                         'u', 'v', 'w', 'x', 'y', 'z', '(', ')', '[', ']']
        self.selected_gesture = []
        self.selected_action = []
        self.rectangles = []
        self.gesture_to_action = dict()
        self.key_board_pos = [0,0]
        self.last_actions = []
        self.controller = Controller()
        self.keyController = KeyboardController()

        # initialize setting surface for setting the guestures
        self.set_surface = pygame.Surface((640,400))
        pygame.draw.line(self.set_surface, pygame.Color(255, 255, 255), (0,0), (0,400),1)
        pygame.draw.line(self.set_surface, pygame.Color(255, 255, 255), (0,400), (640,400),1)
        self.reverse_loopup = dict()
        for x in range(2):
            for i in range(5):
                self.rectangles.append([pygame.Color(0, 255, 0), Rect(30 + (120*i), 40 + (60*x), 100, 30)])
                self.reverse_loopup[(30 + (120*i), 40 + (60*x))] = self.text_text[(x * 5) + i]
                self.text_pos.append((675 + (120 * i), 45 + (60*x)))
        for x in range(2):
            for i in range(5):
                self.rectangles.append([pygame.Color(0, 255, 255), Rect(30 + (120*i), 280 + (60*x), 100, 30)])
                self.reverse_loopup[(30 + (120*i), 280 + (60*x))] = self.text_text[10 + (x * 5) + i]
                self.text_pos.append((675 + (120 * i), 285 + (60*x)))
        self.rectangles.append([pygame.Color(255, 255, 0), Rect(280, 185, 80, 30)])
        self.submit = Rect(280, 185, 80, 30)
        self.text_pos.append((937, 194)) # text pos for submit button

        # initialize the getting surface for seeing the guestures to commands
        self.get_surface = pygame.Surface((640, 200))
        pygame.draw.line(self.get_surface, pygame.Color(255, 255, 255), (0,0), (0, 200))
        pygame.draw.line(self.get_surface, pygame.Color(255, 255, 255), (0,0), (640, 0))
        for i in range(2):
            for x in range(5):
                self.text_pos.append((830 + (160*i), 440 + (22*x)))

        # initialize typing surface for typing
        self.typing_surface = pygame.Surface((640, 360))
        pygame.draw.line(self.typing_surface, pygame.Color(255, 255, 255), (0,0), (640, 0),1)
        pygame.draw.line(self.typing_surface, pygame.Color(255, 255, 255), (640,0), (640, 360),1)
        for x in range(3):
            for i in range(10):
                if x == 0 and i == 0:
                    self.rectangles.append([pygame.Color(255, 255, 255), Rect(60 + (50*i), 45 + (60*x), 30, 30)])
                else:    
                    self.rectangles.append([pygame.Color(0, 255, 255), Rect(60 + (50*i), 45 + (60*x), 30, 30)])
                self.text_pos.append((65 + (50*i), 290 + (60*x)))
        self.rectangles.append([pygame.Color(0,204,170), Rect(140, 240, 300, 80)])
        self.pointer = [pygame.Color(0, 0, 0), (295, 280)]
        # font
        self.font1 = pygame.font.SysFont(None,20) 

    def reset_last_action (self):
        if len(self.last_actions) != 0:
            action = max(set(self.last_actions), key=self.last_actions.count)
            if action == "kb_left":
                if self.key_board_pos[0] > 0:
                    self.rectangles[21 + (self.key_board_pos[1]*10)+self.key_board_pos[0]][0] = pygame.Color(0, 255, 255)
                    self.key_board_pos[0] -= 1
                    self.rectangles[21 + (self.key_board_pos[1]*10)+self.key_board_pos[0]][0] = pygame.Color(255, 255, 255)
            elif action == "kb_right":
                if self.key_board_pos[0] < 9:
                    self.rectangles[21 + (self.key_board_pos[1]*10)+self.key_board_pos[0]][0] = pygame.Color(0, 255, 255)
                    self.key_board_pos[0] += 1
                    self.rectangles[21 + (self.key_board_pos[1]*10)+self.key_board_pos[0]][0] = pygame.Color(255, 255, 255)
            elif action == "kb_down":
                if self.key_board_pos[1] < 2:
                    self.rectangles[21 + (self.key_board_pos[1]*10)+self.key_board_pos[0]][0] = pygame.Color(0, 255, 255)
                    self.key_board_pos[1] += 1
                    self.rectangles[21 + (self.key_board_pos[1]*10)+self.key_board_pos[0]][0] = pygame.Color(255, 255, 255)
            elif action == "kb_up":
                if self.key_board_pos[1] > 0:
                    self.rectangles[21 + (self.key_board_pos[1]*10)+self.key_board_pos[0]][0] = pygame.Color(0, 255, 255)
                    self.key_board_pos[1] -= 1
                    self.rectangles[21 + (self.key_board_pos[1]*10)+self.key_board_pos[0]][0] = pygame.Color(255, 255, 255)
            elif action == "kb_select":
                key_press = self.text_text[31 + (self.key_board_pos[1]*10)+self.key_board_pos[0]]
                print(f"pressed: {key_press}")
                self.keyController.press(key_press)
                self.keyController.release(key_press)
            elif action == "m_select":
                self.controller.click(Button.left, 1)
            self.last_actions = []

    def execute_action (self, action):
        if action == "kb_left":
            if self.key_board_pos[0] > 0:
                self.last_actions.append("kb_left")
        elif action == "kb_right":
            if self.key_board_pos[0] < 9:
                self.last_actions.append("kb_right")
        elif action == "kb_down":
            if self.key_board_pos[1] < 2:
                self.last_actions.append("kb_down")
        elif action == "kb_up":
            if self.key_board_pos[1] > 0:
                self.last_actions.append("kb_up")
        elif action == "kb_select":
            self.last_actions.append("kb_select")
        elif action == "m_up":
            self.controller.move(0, -10)
        elif action == "m_down":
            self.controller.move(0, 10)
        elif action == "m_right":
            self.controller.move(10, 0)
        elif action == "m_left":
            self.controller.move(-10, 0)
        elif action == "m_select":
            self.last_actions.append("m_select")

    def draw (self, camera_frame, prediction): 
        surf = pygame.surfarray.make_surface(cv2.resize(camera_frame, (640, 240)).T)
        # camera 
        self.display.blit(surf, (0,0))
        # surfaces
        self.display.blit(self.set_surface, (640,0))
        self.display.blit(self.typing_surface, (0, 240))
        self.display.blit(self.get_surface, (640, 400))
        # text
        self.display.blit(self.font1.render(prediction, True, pygame.Color(255, 255, 255)), (290, 20)) 
        for i in range(len(self.text_text)):
            color = pygame.Color(0,0,0)
            if i > 20:
                color = pygame.Color(255, 255, 255)
            if i > 30:
                color = pygame.Color(0, 0, 0)
            self.display.blit(self.font1.render(self.text_text[i], True, color), self.text_pos[i])
        # rectangles
        for index, rectangle in enumerate(self.rectangles):
            surface = self.set_surface 
            if index > 20:
                surface = self.typing_surface
            pygame.draw.rect(surface, rectangle[0], rectangle[1])
        # execute action based prediction
        if prediction != '' and prediction in self.gesture_to_action:
            self.execute_action(self.gesture_to_action[prediction])

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    pygame.quit()
                    return True
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                gesture_pos_x = pos[0]
                gesture_pos_x -= 640
                pos = (gesture_pos_x, pos[1])    

                # selecting gesture
                rect = [(s[1], i) for i, s in enumerate(self.rectangles) if s[1].collidepoint(pos)]
                if len(rect) != 0 and (rect[0][0].x, rect[0][0].y) in self.reverse_loopup:
                    rect = rect[0]
                    name = self.reverse_loopup[(rect[0].x, rect[0].y)]
                    if name[0:2].isdigit():
                        # it is a gesture         
                        if len(self.selected_gesture) != 0:
                            self.rectangles[self.selected_gesture[1][1]][0] = pygame.Color(0, 255, 0)

                        self.rectangles[rect[1]][0] = pygame.Color(166, 166, 166)
                        self.selected_gesture = [name, rect]
                    else:
                        # it is an action
                        if len(self.selected_action) != 0:
                            self.rectangles[self.selected_action[1][1]][0] = pygame.Color(0, 255, 255)

                        self.rectangles[rect[1]][0] = pygame.Color(166, 166, 166)
                        self.selected_action = [name, rect]
                # submitted gesture
                if self.submit.collidepoint(pos): 
                    print(self.selected_gesture)
                    print(self.selected_action)
                    if len(self.selected_gesture) != 0 and len(self.selected_action) != 0:
                        print("Submit")
                        self.gesture_to_action[self.selected_gesture[0]] = self.selected_action[0]
                        self.text_text[20 + int(self.selected_gesture[0][0:2])] = self.selected_gesture[0] + ": " + self.selected_action[0]
                        self.rectangles[self.selected_gesture[1][1]][0] = pygame.Color(0, 255, 0)
                        self.rectangles[self.selected_action[1][1]][0] = pygame.Color(0, 255, 255)
                        self.selected_gesture = []
                        self.selected_action = []


        return False