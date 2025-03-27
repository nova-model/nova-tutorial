---
title: Setup
---
# Verify Prerequisites
*   **Basic Python Knowledge:** A basic understanding of Python programming concepts is required.
*   **A Text Editor or IDE:** You will need a text editor or IDE (such as VS Code, Sublime Text, or Atom) for writing code.
*   **Familiarity with the Command Line:** You will need to be comfortable using the command line or terminal.

# Setup

This section guides you through setting up your development environment to follow along with the NOVA tutorial. It builds upon the prerequisites outlined earlier and provides specific instructions to ensure you have the necessary tools and libraries installed and configured.

## 1. Mac and Linux

*   **Python Installation:** You must have Python 3.11 or higher installed on your system.  Verify your Python version by running `python --version` or `python3 --version` in your terminal. If python is already installed, it should be available on linux systems via your package manager. On macOS, download the installer from [https://www.python.org/downloads/](https://www.python.org/downloads/).
*   **Python's `copier` Library:** We will be using this library to generate a starting application from a template. Install it using pip (ex. `pip install copier`).
*   **Poetry:** The code samples provided in this tutorial leverage Poetry for dependency management. Run the command `poetry` to see if you already have Poetry installed. If you don't have Poetry installed, follow the instructions on the official Poetry website: [https://python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation).
*   **Git:** You must have git installed on your system. Try running `git version` command in your terminal to see if it is already installed. If not, please visit the git downloads page for installation instructions. [https://git-scm.com/downloads](https://git-scm.com/downloads)

## 2. Windows

For windows systems, it is recommended that you use the analysis cluster for this tutorial.


::::::::::::::::::::::::::::::::::::::::: callout

You can use the analysis cluster for this tutorial. This is recommended if you use Windows or otherwise can\'t meet the above prerequisites on your laptop. By default, the `python` command on the cluster will use 3.9, so please explicitly reference `python3.11` where needed.

You can create a virtual environment suitable for the tutorial on the cluster with:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install copier poetry
```

::::::::::::::::::::::::::::::::::::::::::::::::

## 3. Getting your Galaxy API Key

In order to run the code examples in this tutorial, an API Key is required. An API key is obtained from the NDIP instance directly.

::::::::::::::::::::::::::::::::::::::::: callout

For this tutorial, we will be using [https://calvera-test.ornl.gov](https://calvera-test.ornl.gov) as our NDIP instance. This is the instance that is used for testing and development of platform and NOVA tools. Once tools are mature and ready for users, they'll be migrated to [https://calvera.ornl.gov](https://calvera.ornl.gov). This process is explained in more detail at the end of the tutorial.

::::::::::::::::::::::::::::::::::::::::::::::::::

The steps to retrieve your API Key are:

1. Navigate to [https://calvera-test.ornl.gov](https://calvera-test.ornl.gov)
2. Log in using your UCAMS id if necessary
3. Under the Users dropdown menu, choose preferences
4. Select "Manage API Key"
5. You should now be on the "Manage API Key" page where you can view/copy the API Key.

## 4. Configure Environment Variables

The NOVA framework requires you to set environment variables for your NDIP URL and API key. These variables are used to authenticate with the NDIP platform.

1.  **Set `GALAXY_URL`:** Set the `GALAXY_URL` environment variable to the URL of your NDIP instance, in this case calvera-test.ornl.gov:

    ```bash
    export GALAXY_URL=calvera-test.ornl.gov  # Linux/macOS
    set GALAXY_URL=calvera-test.ornl.gov     # Windows (Command Prompt)
    $env:GALAXY_URL="calvera-test.ornl.gov"  # Windows (PowerShell)
    ```

2.  **Set `GALAXY_API_KEY`:** Set the `GALAXY_API_KEY` environment variable to your NDIP API key. Replace `<your_api_key>` with your actual API key:

    ```bash
    export GALAXY_API_KEY=<your_api_key>  # Linux/macOS
    set GALAXY_API_KEY=<your_api_key>     # Windows (Command Prompt)
    $env:GALAXY_API_KEY="<your_api_key>"  # Windows (PowerShell)
    ```

    **Important:** For security reasons, it is recommended to avoid hardcoding your API key directly in your code. Using environment variables is a more secure and flexible approach.


## 5. Create a GitLab Personal Access Token

::::::::::::::::::::::::::::::::::::::::: callout

If you currently use an ssh key for gitlab, you will still need to create a personal access token for the tutorial.

::::::::::::::::::::::::::::::::::::::::::::::::::
To interact with repositories on code.ornl.gov, you'll need to create a personal access token:

1. Navigate to [https://code.ornl.gov](https://code.ornl.gov) and log in with your credentials
2. In the left sidebar, select your avatar.
3. Select Edit Profile
4. On the left sidebar, select Access tokens
5. In Token name, enter a name for the token (such as Nova Tutorial)
6. Provide the desired scopes (at minimum, select "read repository", "write repository", and api)
7. Click Create personal access token.
8. **Important** Copy and save your token to your computer immediately. You will no longer have access to it after leaving the page.

## 6. Verify Your Setup

To ensure your setup is correct, run the following command in your terminal within the `nova_tutorial` directory:

```bash
echo $GALAXY_URL
echo $GALAXY_API_KEY
```

This should print the values of your `GALAXY_URL` and `GALAXY_API_KEY` environment variables. If the values are printed correctly, your setup is complete.

You are now ready to start building your NOVA application! We will proceed in the next episode.
