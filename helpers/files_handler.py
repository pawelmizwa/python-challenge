import ast
import json
from typing import List
from helpers.logger import log
from tenacity import retry, wait_exponential, stop_after_attempt
import logging

logger = logging.getLogger("example")


class FileHandler:
    def __init__(self, input_path: str, output_path: str, nesting_keys: List[str]):
        self.input_path = input_path
        self.output_path = output_path
        self.nesting_keys = nesting_keys

    @log()
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2, exp_base=2),
        reraise=True,
    )
    def get_data_from_file(self) -> List[dict]:
        with open(self.input_path, 'r') as f:
            data = ast.literal_eval(f.read())
        return data

    @log()
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2, exp_base=2),
        reraise=True,
    )
    def write_data_to_file(self, nested: dict):
        with open(self.output_path, 'w') as file:
            file.write(json.dumps(nested))

    @log()
    def convert_list_of_dicts_to_nested_dict(self, raw_data: List[dict], nesting_level: int) -> dict:
        if nesting_level >= len(self.nesting_keys):
            nesting_level = len(self.nesting_keys)

        result = dict()
        for level in range(nesting_level):
            if level == 0:
                for item in raw_data:
                    if nesting_level > 1:
                        result[item[self.nesting_keys[0]]] = dict()
                    else:
                        try:
                            result[item[self.nesting_keys[0]]].append(item)
                        except KeyError:
                            result[item[self.nesting_keys[0]]] = [item]
                        item.pop(self.nesting_keys[0])

            if level == 1:
                for item in raw_data:
                    if nesting_level > 2:
                        result[item[self.nesting_keys[0]]][item[self.nesting_keys[1]]] = dict()
                    else:
                        try:
                            result[item[self.nesting_keys[0]]][item[self.nesting_keys[1]]].append(item)
                        except KeyError:
                            result[item[self.nesting_keys[0]]][item[self.nesting_keys[1]]] = [item]
                        item.pop(self.nesting_keys[0])
                        item.pop(self.nesting_keys[1])

            if level == 2:
                for item in raw_data:
                    try:
                        result[item[self.nesting_keys[0]]][item[self.nesting_keys[1]]][
                            item[self.nesting_keys[2]]].append(item)
                    except KeyError:
                        result[item[self.nesting_keys[0]]][item[self.nesting_keys[1]]][
                            item[self.nesting_keys[2]]] = [item]
                    item.pop(self.nesting_keys[0])
                    item.pop(self.nesting_keys[1])
                    item.pop(self.nesting_keys[2])

        return result
