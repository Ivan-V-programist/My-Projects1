from PIL import Image, ImageGrab
import time
import cv2
import sys
import os


def print_large_block(text):
    global save_ascii_art_in
    print('', end='', flush=True)
    sys.stdout.flush()
    print('\n', end=text, flush=True)

def get_ascii_from_image(im):
    global char_list, mirrored
    lines = []
    x_range = range(im.size[0])[::-1] if mirrored else range(im.size[0])
    for y in range(im.size[1]):
        line = []
        for x in x_range:
            pix = sum(im.getpixel((x, y)))/3
            char_list_pos = int((len(char_list)-1)*pix/255)
            line.append(char_list[char_list_pos])
        lines.append(''.join(line))
    return '\n'.join(lines)


def get_video_frms(path, format="cv2"):
    cap = cv2.VideoCapture(path)
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == True:
            if format == 'PIL':
                yield cv2_to_PIL(frame)
            else:
                yield frame
        else:
            cap.release()
            cv2.destroyAllWindows()
            break


def cv2_to_PIL(frame):
    color_mode_converted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_im = Image.fromarray(color_mode_converted)
    return pil_im



def print_ascii_from_im(im):
    global horizontal, vertical, save_ascii_art_in
    horizontal = int(vertical*horizontal_scale*im.size[0]/im.size[1])
    im = im.resize((horizontal, vertical))
    ascii_art = get_ascii_from_image(im)+'\n'
    print_large_block(ascii_art)


def play_ascii_video(path):
    global frames_to_play
    i = 0
    for im in get_video_frms(path, 'PIL'):
        print_ascii_from_im(im)
        i += 1
        if i > frames_to_play and frames_to_play != 0:
            break


def play_webcam(num):
    play_ascii_video(int(num))


def main():
    play_webcam(0)

char_list = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`'.")
horizontal_scale = 1.5
vertical = 75
yt_video_path = None
frames_to_play = 0
mirrored = 1
save_ascii_art_in = None

        
if __name__ == '__main__':
    main()