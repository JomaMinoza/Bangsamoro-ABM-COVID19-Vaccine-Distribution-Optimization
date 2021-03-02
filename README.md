# Title: A BARMM Case Study: COVID-19 Agent-Based Model with Goal Optimization for Vaccine Distribution

### Abstract

Preventive and control measures such as community quarantine, wearing face masks and social distancing have been widely used to limit the spread of COVID-19. Quarantine is used to lower the number of infectives, helping health facilities cope, but trade-offs with the economy can be observed.  Different health and economic policies have various implications in the community. Thus, the idea of emergence through an agent-based model (ABM) is developed to observe the impact of various health policies on the spread of the disease. 

Now that SARS-CoV-2 (COVID-19) vaccines are developed, it is very important to plan its distribution strategy. Combined with the ABM, a resource optimization model was proposed in this study to simulate the possible decisions of policymakers and to help them identify appropriate strategies for their constituents. Using the proposed model, it aims that it could simulate possible decisions of policymakers and could help them identify appropriate strategies for their constituents. 

In this case study, simulations for different vaccination scenarios for the Bangsamoro region were analyzed.

![Solution](https://github.com/JomaMinoza/Bangsamoro-ABM-COVID19-Vaccine-Distribution-Optimization/blob/main/Solution.png)

[Sample Implementation of Solution: https://barmm-abm-covid19-vaccination.herokuapp.com](https://barmm-abm-covid19-vaccination.herokuapp.com)

### To run the model, type

```
> python main.py
```


For more details of the model, please see the following preprints:

[COVID-19 Agent-Based Model with Multi-objective Optimization for Vaccine Distribution](https://arxiv.org/abs/2101.11400)

[Protection after Quarantine: Insights from a Q-SEIR Model with Nonlinear Incidence Rates Applied to COVID-19](https://www.medrxiv.org/content/10.1101/2020.06.06.20124388v1)

[Modeling the dynamics of COVID-19 using Q-SEIR model with age-stratified infection probability](https://www.medrxiv.org/content/10.1101/2020.05.20.20095406v1)

[Age-stratified Infection Probabilities Combined with Quarantine-Modified SEIR Model in the Needs Assessments for COVID-19](https://www.medrxiv.org/content/10.1101/2020.04.08.20057851v1)

### Jupyter Notebooks

[COVID19 Epidemiological Data - Exploratory Analysis](https://github.com/JomaMinoza/Bangsamoro-ABM-COVID19-Vaccine-Distribution-Optimization/blob/main/experiments/notebooks/COVID19%20Epidemiological%20Data%20-%20Exploratory%20Analysis.ipynb)

[Vaccine Distribution using Different Prioritization Factors](https://github.com/JomaMinoza/Bangsamoro-ABM-COVID19-Vaccine-Distribution-Optimization/blob/main/experiments/notebooks/Vaccine%20Distribution%20using%20Different%20Prioritization%20Factors.ipynb)

[Sensitivity Analysis](https://github.com/JomaMinoza/Bangsamoro-ABM-COVID19-Vaccine-Distribution-Optimization/blob/main/experiments/notebooks/)

### Scripts

[Slurm Scripts for High-Performance Computing (HPC) cluster ](https://github.com/JomaMinoza/Bangsamoro-ABM-COVID19-Vaccine-Distribution-Optimization/tree/main/experiments/scripts)

[Script for Summarized Results](https://github.com/JomaMinoza/Bangsamoro-ABM-COVID19-Vaccine-Distribution-Optimization/blob/main/scripts/summarize_results.py)

[Script for Summarized Sensitivity Analysis](https://github.com/JomaMinoza/Bangsamoro-ABM-COVID19-Vaccine-Distribution-Optimization/blob/main/scripts/summarize_results.py)

### Sensitivity Analysis

![Sensitivity Analysis on Infected Agents](https://github.com/JomaMinoza/Bangsamoro-ABM-COVID19-Vaccine-Distribution-Optimization/blob/main/experiments/notebooks/summarized/summary/vaccination_strategy-frontliners-infected.png?raw=true)

![Sensitivity Analysis on Died Agents](https://github.com/JomaMinoza/Bangsamoro-ABM-COVID19-Vaccine-Distribution-Optimization/blob/main/experiments/notebooks/summarized/summary/vaccination_strategy-frontliners-died.png?raw=true)

![Sensitivity Analysis on Recovered Agents](https://github.com/JomaMinoza/Bangsamoro-ABM-COVID19-Vaccine-Distribution-Optimization/blob/main/experiments/notebooks/summarized/summary/vaccination_strategy-frontliners-recovered.png?raw=true)

![Sensitivity Analysis on Vaccine Hesitancy effect on Infected Agents](https://github.com/JomaMinoza/Bangsamoro-ABM-COVID19-Vaccine-Distribution-Optimization/blob/main/experiments/notebooks/summarized/summary/vaccination_strategy-frontliners-infected-hesitancy.png?raw=true)

![Sensitivity Analysis on Vaccine Hesitancy effect on Died Agents](https://github.com/JomaMinoza/Bangsamoro-ABM-COVID19-Vaccine-Distribution-Optimization/blob/main/experiments/notebooks/summarized/summary/vaccination_strategy-frontliners-died-hesitancy.png?raw=true)

![Sensitivity Analysis on Vaccine Hesitancy effect on Recovered Agents](https://github.com/JomaMinoza/Bangsamoro-ABM-COVID19-Vaccine-Distribution-Optimization/blob/main/experiments/notebooks/summarized/summary/vaccination_strategy-frontliners-recovered-hesitancy.png?raw=true)


#BARMMOpenData

