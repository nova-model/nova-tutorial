---
site: sandpaper::sandpaper_site
---

# Neutrons Open Visualization and Analysis Framework Tutorial

This tutorial guides you through the process of building applications for neutron data analysis using the NOVA *framework*. NOVA provides key components to create applications that range from simple scripts, all the way to full user interfaces with advanced visualization capabilities. It leverages a Model-View-ViewModel (MVVM) architectural pattern and three key NOVA libraries: `nova-galaxy`, `nova-trame`, and `nova-mvvm`, to simplify interaction with the Neutron Data Interpretation Platform (NDIP).

**Key Learning Objectives:**

*   **Introduction to NDIP and NOVA:** Understand the purpose of NDIP as a workflow management system for neutron data and NOVA as a framework for simplifying NDIP application development.
*   **Project Setup:** Learn how to use the `copier` library to clone a template application, providing a basic project structure and pre-configured files.
*   **NDIP Interaction with `nova-galaxy`:** Master the use of `nova-galaxy` to connect to NDIP, define and run tools, and manage input parameters.
*   **MVVM Implementation with `nova-mvvm` and Pydantic:** Grasp the principles of the MVVM design pattern and implement it using `nova-mvvm`. Utilize Pydantic for data validation and defining data models for inputs.
*   **Web UI Development with `nova-trame`:** Build a web-based user interface using `nova-trame` and Vuetify components. Implement two-way data binding between UI elements and the ViewModel.
*   **Advanced Pydantic Validation:** Explore advanced Pydantic features like nested models and custom validators for more robust data validation.
*   **Advanced Visualization Techniques:** Integrate libraries like Plotly, PyVista and VTK with Trame to produce sophisticated 2D and 3D data visualizations.
*   **Deployment to NOVA/NDIP:** Learn the steps for containerizing your application with Docker, defining your tool with an XML file, and deploying it to the NOVA/NDIP platform.

**Core Components and Workflow:**

1.  **Start with the NOVA Template:** Use `copier` to create a starting point.
2.  **Define Data with Pydantic:** Create Pydantic models for structured data and validation.
3.  **Implement the MVVM Pattern:**
    *   Use the `Model` layer to define the application data and business logic, including connecting to NDIP via `nova-galaxy`.
    *   Create a `ViewModel` to serve as an intermediary between the `Model` and `View`, exposing data and handling user interactions.
    *   Construct the `View` (UI) using `nova-trame` and Vuetify, binding UI elements to the ViewModel.
4.  **Interact with NDIP:** Use `nova-galaxy` to connect to NDIP, run tools, and manage data.
5.  **Develop the User Interface:** Build a web-based user interface using `nova-trame` and Trame.
6.  **Create advanced visualizations:** Integrate Plotly, PyVista, and VTK libraries to visualize data in the UI.
7.  **Deploy the Application:** Containerize your application and deploy it to the NDIP platform for others to use.

**Outcome:**

By the end of this tutorial, you will have a solid understanding of the NOVA *framework*, its core libraries, and the MVVM design pattern. You will be able to build interactive web applications that connect to NDIP, run neutron data analysis tools, and visualize the results, empowering you to create custom tools for the neutron scattering community. The tutorial also provides a pathway for deploying your application to the NOVA/NDIP platform.