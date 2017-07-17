# Spound

## Before start

Make sure you have created a [Spotify application] and have the client id and
secret

## Getting Started

- Clone the project.

    ```
    git clone git@github.com:cacarrara/spound.git
    ```

- Change directory into your newly cloned project.

    ```
    cd spound
    ```

- Upgrade packaging tools (create a virtualenv before).

    ```
    pip install --upgrade pip setuptools
    ```

- Install the project in editable mode with its testing requirements.

    ```
    pip install -e ".[testing]"
    ```

- Create your config file and edit it properly.

    ```
    cp local.env .env
    ```

- Run your project.

    ```
    pserve development.ini --reload
    ```


[Spotify application]: https://developer.spotify.com/my-applications/#!/applications
