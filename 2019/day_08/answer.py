from collections import Counter


def p1(data, is_sample):
    pixels = data[0]

    if is_sample:
        width = 3
        height = 2
        return "N/A"
    else:
        width = 25
        height = 6

    leastzeroes = width * height + 1

    needle_layer = None
    layer = 1
    while True:
        pixel_from = (layer - 1) * (width * height)
        pixel_to = layer * (width * height)
        layerpixels = pixels[pixel_from:pixel_to]
        if not layerpixels:
            break
        layerdata = Counter(layerpixels)
        if layerdata["0"] < leastzeroes:
            needle_layer = layerdata
            leastzeroes = layerdata["0"]
        layer += 1

    return needle_layer["1"] * needle_layer["2"]


def render_image(imagedata: list[str], width: int, height: int):
    print()
    for r in range(height):
        for c in range(width):
            index = r * width + c
            pixel = imagedata[index]
            if pixel == "0":
                char = " "
            elif pixel == "1":
                char = "#"
            elif pixel == "2":
                print("transparent pixel in image?")
                char = " "
            else:
                print(f"unknown pixel type found: {pixel}")
            print(char, end="")
        print()


def p2(data, is_sample):
    pixels = data[0]

    if is_sample:
        width = 2
        height = 2
    else:
        width = 25
        height = 6

    final_image = ["2"] * width * height

    layer = 1
    while True:
        pixel_from = (layer - 1) * (width * height)
        pixel_to = layer * (width * height)
        layerpixels = pixels[pixel_from:pixel_to]
        if not layerpixels:
            break
        for index, pixel in enumerate(layerpixels):
            if final_image[index] == "2":
                final_image[index] = pixel
        layer += 1

    render_image(final_image, width, height)
