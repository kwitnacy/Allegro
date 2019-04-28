from flask import Flask, request, send_file
import PIL.Image
import os
import requests
import random
from io import BytesIO

# structure helping resize pictures to proper size
# key:      amount of pictures
# value:    list of resolution for every picture (defined as ratio to given resolution)
scale = {
    1: [[1.0, 1.0]],
    2: [[0.5, 1.0], [0.5, 1.0]],
    3: [[0.33, 1.0], [0.33, 1.0], [0.34, 1.0]],
    4: [[0.5, 0.5], [0.5, 0.5], [0.5, 0.5], [0.5, 0.5]],
    5: [[0.5, 0.5], [0.5, 0.5], [0.33, 0.5], [0.33, 0.5], [0.34, 0.5]],
    6: [[0.33, 0.5], [0.33, 0.5], [0.34, 0.5], [0.33, 0.5], [0.33, 0.5], [0.34, 0.5]],
    7: [[0.33, 0.5], [0.33, 0.5], [0.34, 0.5], [0.25, 0.5], [0.25, 0.5], [0.25, 0.5], [0.25, 0.5]],
    8: [[0.25, 0.5], [0.25, 0.5], [0.25, 0.5], [0.25, 0.5], [0.25, 0.5], [0.25, 0.5], [0.25, 0.5], [0.25, 0.5]],
}

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/mozaika")
def mozaika():
    # random value
    random_val = request.args.get('losowo')

    # resolution values
    resolution = request.args.get('rozdzielczosc')

    # urls to pictures
    pictures_url = request.args.get('zdjecia').split(',')

    # list for pictures
    pictures = []

    # casting random_val
    if random_val is not None:
        random_val = int(random_val)
    else:
        random_val = 0

    # casting resolution values
    if resolution is not None:
        resolution = resolution.split('x')
        resolution_x = int(resolution[0])
        resolution_y = int(resolution[1])
    else:
        resolution_x = 2048
        resolution_y = 2048

    # shuffling pictures' urls if necessary
    if random_val == 1:
        random.shuffle(pictures_url)

    # getting pictures
    for pic in pictures_url:
        response = requests.get(pic)
        pictures.append(PIL.Image.open(BytesIO(response.content)))

    # resizing pictures, so they fit on mosaic
    for i in range(len(pictures)):
        pictures[i] = pictures[i].resize((int(resolution_x*scale[len(pictures)][i][0]),
                                          int(resolution_y*scale[len(pictures)][i][1])))

    # variables - output
    #           - position of next img in mosaic (X-axis)
    #           - position of next img in mosaic (Y-axis)
    output_img = PIL.Image.new(mode="RGB", size=(resolution_x, resolution_y), color="white")
    offset_x = 0
    offset_y = 0

    # creating mosaic
    # if given less than four images, then put them side by side in one row
    if len(pictures) < 4:
        for pic in pictures:
            output_img.paste(pic, (offset_x, 0))
            offset_x += pic.size[0]

    # if given more than 3 and less than nine, then put them side by side in two rows
    # if amount of pictures is odd, then the upper row will have less pictures
    elif 4 <= len(pictures) <= 8:
        i = 0

        # first row
        for i in range(int(len(pictures)/2)):
            output_img.paste(pictures[i], (offset_x, 0))
            offset_x += pictures[i].size[0]

        last_pic_index = i + 1
        offset_y += pictures[i].size[1]
        offset_x = 0

        # second row
        for i in range(last_pic_index, len(pictures), 1):
            output_img.paste(pictures[i], (offset_x, offset_y))
            offset_x += pictures[i].size[0]

    # saving output_img
    output_img.save(os.path.join("C:\\Users\\kwiat\\PycharmProjects\\allegro", "obraz1.jpeg"), 'JPEG')

    # returning output
    return send_file("obraz1.jpeg", mimetype='image/gif')


if __name__ == '__main__':
    app.run()



















