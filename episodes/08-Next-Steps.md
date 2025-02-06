---
title: "Development Cycle and Next Steps"
teaching: 10
exercises: 0
---
# Next Steps

In this section, we will outline the process for taking an application like the one we\'ve created in this tutorial and deploying it to the NOVA/NDIP platform. While we won\'t actually perform the deployment in this tutorial, we will cover the key steps and resources involved.

## Containerizing Your Application

The first step in deploying your application to the NOVA/NDIP platform is to package it as a Docker container. Docker containers provide a lightweight and portable way to package your application and all of its dependencies. This ensures that your application will run consistently across different environments.

Fortunately, the template application we used in this tutorial already includes a `Dockerfile` that you can use as a starting point. The Dockerfile is a set of instructions that Docker uses to build your container image. 

Here\'s what the Dockerfile typically includes:
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

::::::::::::::::::::::::::::::::::::::::: callout
GPU acceleration in a container is possible but beyond the scope of this tutorial. Typically, a base container is chosen which already has all of the gpu dependencies installed such as ```regproxy.ornl.gov/hub_proxy/kitware/trame:py3.10-glvnd-2024-12```. The team has built similar containers already which can be used as a reference for development, such as, ```https://code.ornl.gov/ndip/trame-apps/ct-scan-visualizer/```
::::::::::::::::::::::::::::::::::::::::::::::::::

## Defining Your Tool with XML

Once your application is containerized, you will also need to define your tool using an XML file. This XML file describes your tool to the NDIP platform, including its inputs, outputs, parameters, and the Docker container image that should be used to run the tool. The NDIP platform makes use of the Galaxy tool framework.

The XML file includes:
*   **Tool ID:** A unique identifier for your tool.
*   **Name and Description:** User-friendly name and description of the tool.
*   **Inputs:** Defines the input parameters, including their types, labels, and optional constraints.
*   **Outputs:** Describes the output files or datasets produced by the tool.
*   **Container Image:** Specifies the Docker image that should be used to run the tool.
*   **Command:** Specifies the command line that is executed inside the docker container.

You can find numerous examples of Galaxy tool XML files in the NDIP GitLab repository:
[https://code.ornl.gov/ndip/galaxy-tools](https://code.ornl.gov/ndip/galaxy-tools)

Detailed documentation on creating tool XML files is available on the Calvera documentation site:
[calvera.ornl.gov/docs/dev](calvera.ornl.gov/docs/dev)

## Development Lifecycle

### How to get a new tool on NDIP

After creating your tool\'s XML file, it needs to be added to the NDIP platform. For testing your tool on the platform, it should be uploaded to the *prototype* branch of the GitLab repository linked above. An automated CI job will push your tool to the calvera-test instance. Test your application via the web browser interface. After you\'ve verified that your tool is performing as expected, submit a merge request to the repository\'s *dev* branch and engage with our team. When first adding a tool to the platform, Calvera admins will need to configure Calvera to use the tool.

Create an issue in the [galaxy tools](https://code.ornl.gov/ndip/galaxy-tools/-/issues/new) repository providing the following information:
The name of the XML file you've created (see more about XML files here)
The tool ID (i.e. neutrons_my_new_tool)
The section name where your tool should appear in the tool panel
Whether the tool will need a GPU
Additional developers who will be working on the tool (if this is their first time contributing to this repository)

The *dev* branch is used as a staging branch for tools that are ready to be put in front of users. Tools here will be added to the NDIP production instance, Calvera, during the next deployment. 

### Continued Development

The process for continuing development on an existing tool is very similar to getting a new tool on the platform except that the initial configuration does not need to be repeated. You will continue to develop on the *prototype* branch, where you can push and test changes. Once you are satisified with the new version of your tool, submit a merge request to update the the tool in the *dev* branch. Our team will review these changes, perform the merge, and the new version of the tool will be updated on the NDIP production instance, Calvera, during the next deployment.

## Putting It All Together

Once you have your Docker container and tool XML file, you would:
1. Upload the Docker image to a container registry.
2. Upload the XML file to the NDIP platform.
3. Make sure that the API_KEY and GALAXY_URL are passed to the application as environmental variables.
4. Test your application via the web browser interface.

After performing these steps, your application will be available to NDIP users.

## Additional Resources

*   **NDIP GitHub Repository**: [https://code.ornl.gov/ndip](https://code.ornl.gov/ndip)
*   **Galaxy Tool XML Examples**: [https://code.ornl.gov/ndip/galaxy-tools](https://code.ornl.gov/ndip/galaxy-tools)
*   **Calvera Documentation**: [calvera.ornl.gov/docs/dev](calvera.ornl.gov/docs/dev)
*   **Nova Documentation**: https://nova-application-development.readthedocs.io/en/latest/
*   **nova-galaxy documentation**: https://nova-application-development.readthedocs.io/projects/nova-galaxy/en/latest/
*   **nova-trame documentation**: https://nova-application-development.readthedocs.io/projects/nova-trame/en/stable/
*   **nova-mvvm documentation**: https://nova-application-development.readthedocs.io/projects/mvvm-lib/en/latest/

By following the steps outlined in this section, you can deploy your own applications to the NDIP platform and make them available to the wider scientific community.
```