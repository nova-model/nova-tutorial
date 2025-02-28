---
title: "Development Cycle and Next Steps"
teaching: 20
exercises: 0
---
# 8. Development Cycle and Next Steps

In this section, we will look at other resources you may want to integrate with your application.

## ONCat Integration

If needed, you can integrate your application with ONCat via [pyoncat](https://pypi.org/project/pyoncat/2.1/). If you need to access non-public information with the API then you will need to use an authenticated client in `pyoncat`. We strongly recommend you email oncat-support@ornl.gov explaining the use case for your ONCat integration as they can advise you on the most appropriate form of authentication for your application and how to set it up.

## Advanced Container Configurations

The basic container configuration we created in Episode 2 works well for most applications, but there are some advanced configurations that may be useful for more complex applications.

::::::::::::::::::::::::::::::::::::::::: callout
GPU acceleration in a container is possible but beyond the scope of this tutorial. Typically, a base container is chosen which already has all of the GPU dependencies installed such as ```regproxy.ornl.gov/hub_proxy/kitware/trame:py3.10-glvnd-2024-12```. The team has built similar containers already which can be used as a reference for development, such as ```https://code.ornl.gov/ndip/trame-apps/ct-scan-visualizer/```
::::::::::::::::::::::::::::::::::::::::::::::::::


## Development Lifecycle

As we saw in Episode 2, we can deploy our tools to the NDIP platform by adding XML files to the galaxy-tools repository's prototype branch. Let's discuss what happens after that initial deployment.

### Continued Development

Once your tool is deployed to the platform, you may want to continue development to fix bugs or add new features. The process for continuing development on an existing tool is similar to getting a new tool on the platform.

You will continue to develop on the *prototype* branch, where you can push and test changes. Once you are satisfied with the new version of your tool, submit a merge request to update the tool in the *dev* branch. The NDIP team will review these changes, perform the merge, and the new version of the tool will be updated on the NDIP production instance, Calvera, during the next deployment.

### Versioning Your Tools

As you continue to develop your tool, it's important to keep track of versions. The XML file we created in Episode 2 includes a version attribute that you should update whenever you make significant changes to your tool.

The *dev* branch is used as a staging branch for tools that are ready to be put in front of users. Tools here will be added to the NDIP production instance, Calvera, during the next deployment.

## Future Tool Enhancements

As you become more familiar with NDIP and the Galaxy platform, you might want to explore more advanced features:

- Creating complex workflows that combine multiple tools
- Integrating with high-performance computing resources
- Developing specialized data analysis pipelines

These topics are beyond the scope of this introductory tutorial, but the NDIP team is available to help you explore these possibilities as your tools mature.

## Additional Resources

*   **NDIP GitHub Repository**: [https://code.ornl.gov/ndip](https://code.ornl.gov/ndip)
*   **Galaxy Tool XML Examples**: [https://code.ornl.gov/ndip/galaxy-tools](https://code.ornl.gov/ndip/galaxy-tools)
*   **Calvera Documentation**: [calvera.ornl.gov/docs/dev](calvera.ornl.gov/docs/dev)
*   **Nova Documentation**: https://nova-application-development.readthedocs.io/en/latest/
*   **nova-galaxy documentation**: https://nova-application-development.readthedocs.io/projects/nova-galaxy/en/latest/
*   **nova-trame documentation**: https://nova-application-development.readthedocs.io/projects/nova-trame/en/stable/
*   **nova-mvvm documentation**: https://nova-application-development.readthedocs.io/projects/mvvm-lib/en/latest/
*   **Calvera documentation**: https://calvera-test.ornl.gov/docs/

By following this tutorial, you've learned how to create and deploy a NOVA application to the NDIP platform. You can now build on this foundation to create more complex scientific applications that can be easily shared with the wider scientific community.

:::::::::::::::::::::::::::::::::::::::: keypoints
- Tools must be containerized to run on NDIP.
- NDIP requires tools to have an XML file which defines inputs, outputs, tool ID, and the container location.
- Tool XML files must be added to the Galaxy Tools Repository.
- The development lifecycle involves continuous testing on the prototype branch before promoting to dev.
::::::::::::::::::::::::::::::::::::::::::::::::::
