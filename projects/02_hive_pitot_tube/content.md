### Overview
This capstone research project evaluates the aerodynamic performance and pressure recovery behavior of a nose-cone-integrated pitot-static probe for high-powered sounding rockets. By coupling advanced 3D CAD modeling with wall-resolved compressible computational fluid dynamics (CFD), the study establishes precise operational envelopes and identifies flow-field limitations across realistic flight incidence angles.

### Engineering Problem & Requirements
Under the supervision of Professor Gary Bryant (Physics department, School of Science, RMIT University), this research investigated the aerodynamic performance and pressure recovery characteristics of a nose-cone-mounted pitot-static tube designed for high-powered sounding rockets to quantify total and static pressure measurement errors when encountering varying angles of attack during flight. Reliable air-data sensing is fundamental to flight dynamics, guidance, and post-flight analysis, requiring the probe to maintain a normalised total-pressure error within plus or minus 1 percent across expected flight angles.

### Approach & Architecture
* **CAD Modeling:** Developed parametric 3D models and technical assemblies in **Onshape** and **Fusion 360**, integrating the 165 mm pitot-static probe directly into the aluminum sounding rocket nose cone tip.
* **Computational Domain & Meshing:** Generated high-resolution structured and unstructured computational grids in **ANSYS Meshing**, applying rigorous boundary layer refinement around the static ports and stagnation inlet to evaluate cell skewness and orthogonality.
* **CFD Solver Execution:** Implemented steady-state compressible flow simulations in **ANSYS Fluent** and **SimScale** across an angle of attack range from zero to 60 degrees at Mach 0.6.

### Results & Validation
* **Low-Angle Stability:** Simulation results confirm that total-pressure measurement error remains negligible for angles of attack up to 5 degrees.
* **High-Angle Flow Separation:** Demonstrated that beyond 30 degrees, flow separation and cross-flow velocity components introduce severe pressure distortion, successfully aligning with historical NACA benchmark criteria for cylindrical pitot geometries.