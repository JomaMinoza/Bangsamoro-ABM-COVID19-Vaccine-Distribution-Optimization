# -*- coding: utf-8 -*-
"""
Batchrunner
===========

A single class to manage a batch run or parameter sweep of a given model.

"""
import copy
from itertools import product, count
import pandas as pd
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
import os

import random

class ParameterError(TypeError):
    MESSAGE = (
        "parameters must map a name to a value. "
        "These names did not match paramerets: {}"
    )

    def __init__(self, bad_names):
        self.bad_names = bad_names

    def __str__(self):
        return self.MESSAGE.format(self.bad_names)


class VariableParameterError(ParameterError):
    MESSAGE = (
        "variable_parameters must map a name to a sequence of values. "
        "These parameters were given with non-sequence values: {}"
    )

    def __init__(self, bad_names):
        super().__init__(bad_names)


class FixedBatchRunner:
    """ This class is instantiated with a model class, and model parameters
    associated with one or more values. It is also instantiated with model and
    agent-level reporters, dictionaries mapping a variable name to a function
    which collects some data from the model or its agents at the end of the run
    and stores it.

    Note that by default, the reporters only collect data at the *end* of the
    run. To get step by step data, simply have a reporter store the model's
    entire DataCollector object.
    """

    def __init__(
        self,
        model_cls,
        parameters_list=None,
        fixed_parameters=None,
        iterations=1,
        max_steps=1000,
        model_reporters=None,
        agent_reporters=None,
        display_progress=True,
    ):
        """ Create a new BatchRunner for a given model with the given
        parameters.

        Args:
            model_cls: The class of model to batch-run.
            parameters_list: A list of dictionaries of parameter sets.
                The model will be run with dictionary of paramters.
                For example, given parameters_list of
                    [{"homophily": 3, "density": 0.8, "minority_pc": 0.2},
                    {"homophily": 2, "density": 0.9, "minority_pc": 0.1},
                    {"homophily": 4, "density": 0.6, "minority_pc": 0.5}]
                3 models will be run, one for each provided set of parameters.
            fixed_parameters: Dictionary of parameters that stay same through
                all batch runs. For example, given fixed_parameters of
                    {"constant_parameter": 3},
                every instantiated model will be passed constant_parameter=3
                as a kwarg.
            iterations: The total number of times to run the model for each set
                of parameters.
            max_steps: Upper limit of steps above which each run will be halted
                if it hasn't halted on its own.
            model_reporters: The dictionary of variables to collect on each run
                at the end, with variable names mapped to a function to collect
                them. For example:
                    {"agent_count": lambda m: m.schedule.get_agent_count()}
            agent_reporters: Like model_reporters, but each variable is now
                collected at the level of each agent present in the model at
                the end of the run.
            display_progress: Display progresss bar with time estimation?

        """
        self.model_cls = model_cls

        if parameters_list is None:
            parameters_list = []
        self.parameters_list = list(parameters_list)
        self.fixed_parameters = fixed_parameters or {}
        self._include_fixed = len(self.fixed_parameters.keys()) > 0
        self.iterations = iterations
        self.max_steps = max_steps

        self.model_reporters = model_reporters
        self.agent_reporters = agent_reporters

        if self.model_reporters:
            self.model_vars = {}

        if self.agent_reporters:
            self.agent_vars = {}

        self.display_progress = display_progress

    def _make_model_args(self):
        """Prepare all combinations of parameter values for `run_all`

        Returns:
            Tuple with the form:
            (total_iterations, all_kwargs, all_param_values)
        """
        total_iterations = self.iterations
        all_kwargs = []

        count = len(self.parameters_list)
        if count:
            for params in self.parameters_list:
                kwargs = params.copy()
                kwargs.update(self.fixed_parameters)
                #run each iterations specific number of times
                for iter in range(self.iterations):
                    kwargs_repeated = kwargs.copy()
                    all_kwargs.append([self.model_cls, kwargs_repeated, self.max_steps, iter])

        elif len(self.fixed_parameters):
            count = 1
            kwargs = self.fixed_parameters.copy()
            all_kwargs.append(kwargs)

        total_iterations *= count

        return all_kwargs, total_iterations
        #return (total_iterations, all_kwargs, all_param_values)

    def run_all(self):
        """ Run the model at all parameter combinations and store results. """
        run_count = count()
        total_iterations, all_kwargs, all_param_values = self._make_model_args()

        with tqdm(total_iterations, disable=not self.display_progress) as pbar:
            for i, kwargs in enumerate(all_kwargs):
                param_values = all_param_values[i]
                for _ in range(self.iterations):
                    self.run_iteration(kwargs, param_values, next(run_count))
                    pbar.update()

    @staticmethod
    def run_wrapper(iter_args):
        model_i = iter_args[0]
        kwargs = iter_args[1]
        max_steps = iter_args[2]
        iteration = iter_args[3]

        def run_iteration(model_i, kwargs, max_steps, iteration):
            #instantiate version of model with correct parameters
            model = model_i(**kwargs)
            while model.running and model.schedule.steps < max_steps:
                model.step()

            #add iteration number to dictionary to make unique_key
            kwargs["iteration"] = iteration


            if model.datacollector:
                return kwargs, model.datacollector.get_model_vars_dataframe()
            else:
                return kwargs, "no datacollector in model"

        return run_iteration(model_i, kwargs, max_steps, iteration)