from __future__ import annotations
from dataclasses import dataclass
from inspect import signature
from random import randint

dataclass

def check(params, features):
    for key, value in params.items():
        if key not in features:
            raise Exception(f'The feature "{key}" does not exist.')
        if value.__class__ != features[key]:
            if value.__class__ == int and features[key] == float:
                params[key] = float(value)
            else:
                if value.__class__.__name__ != features[key].__name__:
                    raise Exception(f'The feature "{key}" should be of type {features[key].__name__}.')
                else:
                    params[key] = value.__name__


def createFolders(name, folders, file):
    for folder in folders:
        file.write(f"mkdir ../outputs/{name}/{folder}\n")


def genExperiments(features, folders, file, name, n, cpu, **params):
    createFolders(name, folders, file)
    check(params, features)
    for i in range(n):
        params['ID'] = i
        file.write(f'bsub -o "../outputs/{name}/Markdown/{name}_{i}.md" -J "{name}_{i}" -env MYARGS="-name {name}-{i} {" ".join(f"-{name} {value}" for name, value in params.items())}" < submit_{"cpu" if cpu else "gpu"}.sh\n')


class Parameters():
    ID: int = 0
    # folders: list[str] = []
    def __post_init__(self):
        file = open('experiments.sh', 'w')
        file.write('#!/bin/sh\n')
        file.write(f'#{"".join([str(randint(0, 9)) for _ in range(10)])}\n')
        features, folders = dict(self.__annotations__), ['', 'Markdown']
        # print(features)
        # print("dsfsdfsdfsdfs",[f for f in dir(self) if f[0] !="_"])
        # print()
        genExperiments(features, folders, file, self.name, self.instances, not self.GPU, **{k:v for k, v in self.__dict__.items() if k not in {"name", "instances"}})
        file.close()

    @classmethod
    def start(cls) -> None:
        values = {name: value for name, value in cls.__dict__.items() if name[0] !="_" and name != "run"}
        values['cls'] = cls
        values['self'] = cls
        args = [values[name] for name in signature(cls.run).parameters]
        annotations = [(v.name, v.annotation) for v in signature(cls.run).parameters.values() if v.name not in {"cls", "self"}]
        # print(annotations)
        # print(cls.__annotations__)
        isRunning: bool = cls.__module__ == "__main__"
        if isRunning:
            for name, annotation in annotations:
                if cls.__annotations__[name] != annotation:
                    raise TypeError(f"The type of '{name}' should be '{cls.__annotations__[name].__name__}' in run!")
            cls.run(*args)


