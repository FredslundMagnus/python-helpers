from __future__ import annotations
from inspect import signature, Signature
from dataclasses import dataclass
import inspect
annotations: dict[str, type] = {}


def generate():
    print(2)


def createSignature(f):
    print(signature(f))
    # dataclass(f).__init__

    def generate(b: float = 3.0, a: int = 1, c: bool = True, d: str = "3") -> None:
        print(f"{b = }")
        print(f"{a = }")
        print(f"{c = }")
        print(f"{d = }")

    a = """def generate(b: float = 2.0, a: int = 1) -> None:
        print(3)\nb["f"] = generate"""
    # eval(a)
    b = {}
    exec(a)
    # print(signature(b["f"]))

    # b["f"].__signature__ = signature(b["f"])

    # if locals is None:
    #     locals = {}
    # if 'BUILTINS' not in locals:
    #     locals['BUILTINS'] = builtins
    # return_annotation = ''
    # if return_type is not MISSING:
    #     locals['_return_type'] = return_type
    #     return_annotation = '->_return_type'
    # args = ','.join(args)
    # body = '\n'.join(f'  {b}' for b in body)

    # # Compute the text of the entire function.
    # txt = f' def {name}({args}){return_annotation}:\n{body}'

    # local_vars = ', '.join(locals.keys())
    # txt = f"def __create_fn__({local_vars}):\n{txt}\n return {name}"

    # ns = {}
    # exec(txt, globals, ns)

    print(signature(generate))
    return generate


class Parameters(type):
    def __new__(cls, name, bases, dct):
        print("meta: creating %s %s" % (name, bases))
        return type.__new__(cls, name, bases, dct)

    @createSignature
    def generate(self: Parameters):
        pass


def parameters(defaults: Parameters):
    global annotations
    print(defaults)
    print(dir(defaults))
    annotations = defaults.__annotations__
    print(annotations)
    a = """def generate(b: float = 2.0, a: int = 1) -> None:
        print(3)
b["f"] = generate"""
    # eval(a)
    b = {}
    exec(a, None, {"b": b})
    print(signature(b["f"]))

    # def generate(b: float = 3.0, a: int = 1, c: bool = True, d: str = "3") -> None:
    #     pass

    # defaults.generate = b["f"]
    # def generate(b: float = 2.0, a: int = 1) -> None:
    #     pass
    # defaults.generate = generate

    return defaults


@dataclass
class test:
    b: int = 2


# test()


# def create_signature(f):
#     print("her", annotations)
#     print(type(signature(f)))
#     return f


# @create_signature
# def generate():
#     pass
