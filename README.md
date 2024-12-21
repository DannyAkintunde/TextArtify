# TextArtify: Text to Image API

Welcome to the _Text to Image API_, a simple Flask-based API that allows you to generate images from text, add text to existing images, and more. This API is designed to be easy to use and integrate into your applications.

> [!NOTE]
> if you want to integrate this api into you personal or commercial projects I'll recommend you deploy the api rather than use e publicly available one.

## Features

-   Convert text into images with customizable fonts, sizes, colors, and alignment.
-   Add text overlays to existing images.
-   Caching for improved performance.

## Requirements

-   Python 3.x
-   Other depedencies in the requirements.txt

### Table of Contents

-   [Installation](#installation)
-   [Usage](#usage)
-   [API Endpoints](#api-endpoints)
    -   [Text to Image](#text-to-image)
    -   [Add Text to Image](#add-text-to-image)
    -   [Test Image](#test-image)
-   [Fonts](#fonts)
-   [Logging](#logging)
-   [Contributing](#contributing)
-   [License](#license)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/DannyAkintunde/TextArtify.git
    cd TextArtify
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:

    ```bash
    flask run
    ```

The API will be available at `http://127.0.0.1:5000`.

## Usage

You can interact with the API using tools like Postman or cURL. Below are the available endpoints.

### API Endpoints

#### Text to Image

_Endpoint:_ `/api/v1/text-to-image`  
_Method:_ `GET` or `POST`  
_Parameters:_

-   `text` (required): The text to be converted into an image.
-   `font`: The font to use (optional).
-   `font_size`: The size of the font (default: 52).
-   `color`: The text color in hex format (default: `#FFFFFFFF`).
-   `bg_color`: The background color in hex format (default: `#000000FF`).
-   `min_size`: Minimum size of the image (optional).
-   `max_size`: Maximum size of the image (optional).
-   `text_align`: Alignment of the text (optional, can be `center`, `left`, or `right`).
-   `padding_ratio`: Padding ratio for the text (default: 0.1).

_Example Request:_

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/text-to-image" -H "Content-Type: application/json" -d '{"text": "Hello World", "font": "arimo-bold-italic"}' -o out.png
```

#### Add Text to Image

_Endpoint:_ `/api/v1/add-text-to-img`  
_Method:_ `GET` or `POST`  
_Parameters:_

-   `text` (required): The text to overlay on the image.
-   `bg` (required): URL of the background image.
-   `font`: The font to use (optional).
-   `font_size`: The size of the font (default: 52).
-   `color`: The text color in hex format (default: `#FFFFFFFF`).
-   `text_align`: Alignment of the text (optional, can be `center`, `left`, or `right`).
-   `padding_ratio`: Padding ratio for the text (default: 0.1).

_Example Request:_

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/add-text-to-img" -H "Content-Type: application/json" -d '{"text": "Sample Text", "bg": "https://example.com/image.jpg"}'
```

## Fonts

These are the currently supported fonts

-   arimo
    -   arimo-regular
    -   arimo-italic
    -   arimo-bold
    -   arimo-bold-italic
    -   arimo-medium
    -   arimo-medium-italic
    -   arimo-semibold
    -   arimo-semibold-italic
-   arizonia - arizonia-regular

to use any of this fonts just add it to the font param in your request

### Example:

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/text-to-image" -H "Content-Type: application/json" -d '{"text": "Hello World", "font": "arizonia-regular"}' -o out.png
```

## Logging

Logging is configured to log messages at the INFO level. Errors and warnings are logged appropriately to help with debugging.

## Deploy

Deploy your personal TextArtify server for more control.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FDannyAkintunde%2FTextArtify&project-name=text-to-image&repository-name=TextArtify&demo-title=TextArtify&demo-description=TextArtify%20api%20demo&demo-url=https%3A%2F%2Ftext-artify-seven.vercel.app&demo-image=https%3A%2F%2Fi.ibb.co%2F5jJpc7T%2Ftext-to-image.png)

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
