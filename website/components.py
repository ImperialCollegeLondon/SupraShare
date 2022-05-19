import dash_bootstrap_components as dbc
from dash import html


def jsme(id=None):
    try:
        import dash_bio as dashbio

        return dashbio.Jsme(id=id)
    except ImportError:
        return html.Img(id=id)


def image_card(src, caption=None):
    """Generate a card with an image and an optional caption.

    Args:
        src (str): The URL of the image.
        caption (str, optional): The caption describing the image.

    Returns:
        dbc.Card: A card with an image and caption as footer, if provided.
    """
    if caption:
        caption = dbc.CardFooter(caption, style={"text-align": "center"})
    return dbc.Card([dbc.CardImg(src=src, top=True), caption])


def captioned_image_row(images):
    """Takes a list of image sources and captions and puts them in a dbc.Row

    Args:
        images (list): A list of dictionaries containing the source and captions for
            the images. The captions are optional. Allowed keywords in dictionary:
                - src: The URL of the image.
                - caption (optional): The caption for the image.


    Returns:
        dbc.Row: A row of images, the number of images is the length of the input list.
    """
    return dbc.Row([dbc.Col(image_card(**im)) for im in images])
