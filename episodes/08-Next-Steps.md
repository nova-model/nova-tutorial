---
title: "Next Steps"
teaching: 10
exercises: 0
---
# Next Steps

In this section, we will outline the process for taking an application like the one we've created in this tutorial and deploying it to the NOVA/NDIP platform. While we won't actually perform the deployment in this tutorial, we will cover the key steps and resources involved.

## Containerizing Your Application

The first step in deploying your application to the NOVA/NDIP platform is to package it as a Docker container. Docker containers provide a lightweight and portable way to package your application and all of its dependencies. This ensures that your application will run consistently across different environments.

Fortunately, the template application we used in this tutorial already includes a `dockerfiles/Dockerfile` that you can use as a starting point. The Dockerfile is a set of instructions that Docker uses to build your container image. 

Here's what the Dockerfile typically includes:
* **Base Image:** Specifies the base operating system and environment for your application.
* **Dependencies:** Describes how to install any required libraries or packages.
* **Application Files:** Defines how to copy your application code into the container.
* **Entrypoint:** Sets the command that is run when the container starts.

To containerize your application, you would:
1. Navigate to the top level of your project (where the `dockerfiles` folder is).
2. Run the docker build command in the following format `docker build -t <your_image_name>:<your_image_tag> -f dockerfiles/Dockerfile .`
3. Test your docker container using the command `docker run <your_image_name>:<your_image_tag>`.
4. Push your docker container to a container registry. 

After the docker container is deployed to a registry, it can then be used by the platform.

## Defining Your Tool with XML

Once your application is containerized, you will also need to define your tool using an XML file. This XML file describes your tool to the NDIP platform, including its inputs, outputs, parameters, and the Docker container image that should be used to run the tool. The NDIP platform makes use of the Galaxy tool framework.

The XML file includes:
*   **Tool ID:** A unique identifier for your tool.
*   **Name and Description:** User-friendly name and description of the tool.
*   **Inputs:** Defines the input parameters, including their types, labels, and optional constraints.
*   **Outputs:** Describes the output files or datasets produced by the tool.
*   **Container Image:** Specifies the Docker image that should be used to run the tool.
*   **Command:** Specifies the command line that is executed inside the docker container.

You can find numerous examples of Galaxy tool XML files in the NDIP GitHub repository:
[https://code.ornl.gov/ndip/galaxy-tools](https://code.ornl.gov/ndip/galaxy-tools)

Detailed documentation on creating tool XML files is available on the Calvera documentation site:
[calvera.ornl.gov/docs/dev](calvera.ornl.gov/docs/dev)

## Putting It All Together

Once you have your Docker container and tool XML file, you would:
1. Upload the Docker image to a container registry.
2. Upload the XML file to the NDIP platform.
3. Make sure that the API_KEY and GALAXY_URL are passed to the application as environmental variables.
4. Test your application via the web browser interface.

After performing these steps, your application will be available to NDIP users.

## Additional Resources

*   NDIP GitHub Repository: [https://code.ornl.gov/ndip](https://code.ornl.gov/ndip)
*   Galaxy Tool XML Examples: [https://code.ornl.gov/ndip/galaxy-tools](https://code.ornl.gov/ndip/galaxy-tools)
*   Calvera Documentation: [calvera.ornl.gov/docs/dev](calvera.ornl.gov/docs/dev)

By following the steps outlined in this section, you can deploy your own applications to the NOVA/NDIP platform and make them available to the wider scientific community.
```