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

## 2. Configure Environment Variables

The NOVA framework requires you to set environment variables for your NDIP URL and API key. These variables are used to authenticate with the NDIP platform.

::::::::::::::::::::::::::::::::::::::::: callout

For this tutorial, we will be using calvera-test.ornl.gov as our galaxy endpoint. Please use that for your GALAXY_URL environment variable. For NDIP, calvera-test is platform that we use for testing and development of platform tools. Once tools are mature and ready for users, they'll be migrated to calvera.ornl.gov. This process is explained in more detail at the end of the tutorial.

::::::::::::::::::::::::::::::::::::::::::::::::::


1.  **Set `GALAXY_URL`:** Set the `GALAXY_URL` environment variable to the URL of your NDIP instance. Replace `<your_ndip_url>` with the actual URL:

    ```bash
    export GALAXY_URL=<your_ndip_url>  # Linux/macOS
    set GALAXY_URL=<your_ndip_url>     # Windows (Command Prompt)
    $env:GALAXY_URL="<your_ndip_url>"  # Windows (PowerShell)
    ```

2.  **Set `GALAXY_API_KEY`:** Set the `GALAXY_API_KEY` environment variable to your NDIP API key. Replace `<your_api_key>` with your actual API key:

    ```bash
    export GALAXY_API_KEY=<your_api_key>  # Linux/macOS
    set GALAXY_API_KEY=<your_api_key>     # Windows (Command Prompt)
    $env:GALAXY_API_KEY="<your_api_key>"  # Windows (PowerShell)
    ```

    **Important:** For security reasons, it is recommended to avoid hardcoding your API key directly in your code. Using environment variables is a more secure and flexible approach.

## 3. Verify Your Setup

To ensure your setup is correct, run the following command in your terminal within the `nova_tutorial` directory:

```bash
echo $GALAXY_URL
echo $GALAXY_API_KEY
```

This should print the values of your `GALAXY_URL` and `GALAXY_API_KEY` environment variables. If the values are printed correctly, your setup is complete.

You are now ready to start building your NOVA application! We will proceed in the next episode.
