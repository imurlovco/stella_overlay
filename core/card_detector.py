import cv2

def split_into_cards(frame):
    h, w, _ = frame.shape
    card_width = w // 3
    cards = []

    for i in range(3):
        x1 = i * card_width
        x2 = x1 + card_width
        cards.append(frame[:, x1:x2])

    return cards