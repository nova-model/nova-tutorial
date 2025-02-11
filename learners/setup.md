---
title: Setup
---
# Setup

This section guides you through setting up your development environment to follow along with the NOVA tutorial. It builds upon the prerequisites outlined earlier and provides specific instructions to ensure you have the necessary tools and libraries installed and configured.

## 1. Verify Prerequisites

Before proceeding, ensure you have met the following prerequisites:

*   **Basic Python Knowledge:** A basic understanding of Python programming concepts is required.
*   **Python Installation:** You must have Python 3.8 or higher installed on your system.  Verify your Python version by running `python --version` or `python3 --version` in your terminal.
*   **Python's `copier` Library:** We will be using this library to generate a starting application from a template. Install it using `pip install copier`.
*   **Poetry:** The code samples provided in this tutorial leverage Poetry for dependency management.  If you don't have Poetry installed, follow the instructions on the official Poetry website: [https://python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation).
*   **NDIP Access:** You should have access to a working NDIP system. (Specific details about NDIP access will need to be provided by the instructor.)  Ensure you have the necessary credentials (API key and NDIP URL) to connect to NDIP. These will be set as environment variables, as described later.
*   **NOVA Libraries:**  While Poetry will manage these dependencies for you, it's helpful to be aware of the core NOVA libraries: `nova-galaxy`, `nova-trame`, and `nova-mvvm`.  You can find documentation for these libraries on ReadTheDocs (links provided in the "References" section).
*   **A Text Editor or IDE:** You will need a text editor or IDE (such as VS Code, Sublime Text, or Atom) for writing code.
*   **Familiarity with the Command Line:** You will need to be comfortable using the command line or terminal.

## 2. Getting your Galaxy API Key

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

## 3. Configure Environment Variables

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


## 4. Verify Your Setup

To ensure your setup is correct, run the following command in your terminal within the `nova_tutorial` directory:

```bash
echo $GALAXY_URL
echo $GALAXY_API_KEY
```

This should print the values of your `GALAXY_URL` and `GALAXY_API_KEY` environment variables. If the values are printed correctly, your setup is complete.

You are now ready to start building your NOVA application! We will proceed in the next episode.
