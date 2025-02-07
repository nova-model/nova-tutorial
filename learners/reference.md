---
title: 'Reference'
---

## Glossary

Calvera
: The specific Galaxy instance for ORNL. Can be found at https://calvera.ornl.gov.

Design Pattern
: A reusable solution or blueprint to a commonly occurring problem in software design. 

Docker
: Docker is an open source containerization technology for building and containerizing your applications. https://docs.docker.com/

Galaxy
: An open source wofklow management platform. Facilitates job execution for the NDIP platform. 

Model-View-ViewModel (MVVM)
: An architectural design pattern specifically designed for applications with user interfaces (UIs). It aims to separate the UI (the View) from the underlying data and logic (the Model) by introducing an intermediary component called the ViewModel. This separation makes the application more maintainable, testable, and easier to evolve.

Neutrons Data Interpretation Platform (NDIP)
: A workflow management system built on top of the Galaxy platform. It is designed to enable modular scientific workflows for the analysis and interpretation of neutron data. NDIP provides a range of services including automated data ingestion, job submission, and computational resource management, and visualization and analysis tools.

Neutrons Open Visualization and Analysis Framework (NOVA)
: A framework that aims to simplify the development of applications that interact with NDIP. It consists of three core libraries: nova-galaxy, nova-trame, and nova-mvvm.

Nova-Galaxy
: A Python library that simplifies interaction with the NDIP platform's APIs. It allows developers to easily connect to NDIP, submit jobs, handle parameters, and monitor job progress. https://code.ornl.gov/ndip/public-packages/nova-galaxy

Nova-Trame
: A Python library that facilitates the creation of interactive user interfaces using Trame. nova-trame provides a consistent look and feel for NOVA applications by simplifying interactions with Trame components (such as Vuetify). https://code.ornl.gov/ndip/public-packages/nova-trame

Nova-mvvm
: A Python library that simplifies implementation of the Model-View-ViewModel (MVVM) design pattern. By utilizing this library, users can create structured applications that are more testable and easier to maintain. https://code.ornl.gov/ndip/public-packages/nova-mvvm

Plotly
: An interactive, open-source, and browser-based graphing library for Python. https://github.com/plotly/plotly.py

Pydantic
: A widely used Python library for data validation. https://docs.pydantic.dev/latest/

PyVista
: A library based on VTK that allows for easy 3D visualization and mesh analysis in Python. https://pyvista.org/

Tool
: A software application that runs in the NDIP platform and performs some sort of task. Can take input files and values as Parameters, and will produce results in the form of Outputs. 

Trame
: Trame is a powerful Python framework for building web-based UIs and visualizations. https://kitware.github.io/trame/

Visualization Toolkit (VTK)
: Open source software for manipulating and displaying scientific data. It comes with state-of-the-art tools for 3D rendering, a suite of widgets for 3D interaction, and extensive 2D plotting capability. https://vtk.org/