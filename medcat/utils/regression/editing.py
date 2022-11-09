
import logging
from pathlib import Path
from typing import Optional
import yaml

from medcat.utils.regression.converting import UniqueNamePreserver, get_matching_case
from medcat.utils.regression.checking import RegressionChecker

logger = logging.getLogger(__name__)


def combine_dicts(base_dict: dict, add_dict: dict, in_place: bool = False, ignore_identicals: bool = True) -> dict:
    base = RegressionChecker.from_dict(base_dict)
    add = RegressionChecker.from_dict(add_dict)
    name_preserver = UniqueNamePreserver()
    name_preserver.unique_names = set(
        base_case.name for base_case in base.cases)
    for case in add.cases:
        existing = get_matching_case(base.cases, case.filters)
        if existing:
            if ignore_identicals and existing == case:
                logger.warning(
                    'Found two identical case: %s and %s in base and addon', existing, case)
                continue
            logging.info(
                'Found existing case (%s), adding phrases: %s', existing, case.phrases)
            existing.phrases.extend(case.phrases)
            continue
        new_name = name_preserver.get_unique_name(case.name)
        if new_name != case.name:
            logging.info('Renaming case from "%s" to "%s"',
                         case.name, new_name)
            case.name = new_name
        logging.info('Adding new case %s', case)
        base.cases.append(case)
    new_dict = base.to_dict()
    if in_place:
        base_dict.clear()
        base_dict.update(new_dict)
        return base_dict
    else:
        return new_dict


def combine_contents(base_yaml: str, add_yaml: str, ignore_identicals: bool = True) -> str:
    base_dict = yaml.safe_load(base_yaml)
    add_dict = yaml.safe_load(add_yaml)
    combined_dict = combine_dicts(
        base_dict, add_dict, in_place=True, ignore_identicals=ignore_identicals)
    return yaml.safe_dump(combined_dict)


def combine_yamls(base_file: str, add_file: str, new_file: Optional[str] = None, ignore_identicals: bool = True) -> str:
    base_yaml = Path(base_file).read_text()
    add_yaml = Path(add_file).read_text()
    combined_yaml = combine_contents(
        base_yaml, add_yaml, ignore_identicals=ignore_identicals)
    if new_file is None:
        new_file = base_file  # overwrite base
    Path(new_file).write_text(combined_yaml)
    return new_file
