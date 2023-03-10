## Introduction

**db-storage1111 is an extension for [AUTOMATIC1111's Stable Diffusion Web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui).**

It allows to store pictures to databases.At the moment it only supports MongoDB.
## Features

- **Store images on a MongoDB instance**

## Installation


1. Visit the **Extensions** tab of Automatic's WebUI.
2. Visit the **Install from URL** subtab.
3. Paste this repo's URL into the first field: `https://github.com/takoyaro/db-storage1111
4. Click **Install**.

## Usage
Set environment variables if needed before starting the app:
| Variable | Default       |
|----------|---------------|
| `DB_HOST`  | `'localhost'` |
| `DB_PORT`  | `27017`       |
| `DB_USER`  | `""`          |
| `DB_PASS`  | `""`          |

Then, simply check the `Save to DB` checkbox and generate!


## Contributing
I barely write any python, I have no doubt this extension could be improved and optimized. Feel free to submit PRs!
