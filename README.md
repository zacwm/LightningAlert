# Lightning Alert
## [Features](#features) &bull; [Setup](#setup) &bull; [Photos/Screenshots](#photosscreenshots) &bull; [Contributing](#contributing)

My first Python project that I made so I can be alerted of nearby lightning so I know when to unplug stuff.

**Why?** I live in a old house that has old underground phone lines for internet, so when theres a lightning striking nearby, it kills physical hardware :(

I run this project as a service on my Raspberry PI 4, and you can too (on whatever) by reading through the [setup](#setup)

This will alert whenever there is a strike **within a 30km radius** (nearby) and **within a 15km radius** (close) of the specified location in the config.


## Features
- Configurable location to check around.
- Discord webhook notifications with a map of the strikes, or when the lighting is no longer nearby/close for 15 minutes.
- (If RPI GPIO is available/installed) GPIO Outputs of No nearby lightning, nearby lightning, or close lightning.


## Setup
1. Ensure Python 3+ is installed - You can check this by running `python -v` in your terminal
2. Download the project and extract to a folder.
3. Navigate to the folder in your terminal.
4. Download pip packages - Run `pip install datetime discord_webhook websocket-client`
5. Edit the `config.py` file.
6. Run with `python main.py`


## Photos/Screenshots
<img src="https://zachary.lol/assets/lightning_discord_example.png" />


## Contributing
Please... This is my first actual Python project I'm publicly sharing. If you know any ways to make this better feel free to make a pull request. I typically work with JS/TS, but i'm trying to make things in other languages.

Not only would it help me to better use for my home, it would help me learn and help others who would like to use this too...

I don't know if theres a way to easially make it install all required pip packages that are used, and if theres a way to make it run in background and on startup for someone who is just setting it up too...
