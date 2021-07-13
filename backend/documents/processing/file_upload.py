from pdf2image import convert_from_path, convert_from_bytes

JPEG = 'JPEG'


def pdf_image_generator(pdf,
                        save_local=False,
                        image_format=JPEG
                        ):
    """
    Extracts the pages out of a pdf
    Returns:

    """

    try:
        images = convert_from_path(pdf,
                                   fmt=image_format)
    except:
        try:
            images = convert_from_bytes(pdf,
                                        fmt=image_format)
        except Exception as e:
            raise e

    for i, image in enumerate(images):
        # Save pages as images in the pdf
        if save_local:
            image.save('page' + str(i) + '.jpg', image_format)

        yield image
