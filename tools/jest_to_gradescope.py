#!/usr/bin/env python3

import json
import argparse
import os
from pathlib import Path
import re

import itertools
flatten = itertools.chain.from_iterable

def jest_assertion_to_gradescope(assertion):
    visibility = get_visibility(assertion)
    the_test = {
        "name": get_name(assertion),
        "max_score": get_max_score(assertion),
        "score": get_score(assertion), 
        "output": get_output(assertion, visibility),
        "visibility": visibility
    }
    return the_test

def get_name(assertion):
    ancestors = map(lambda x:f'[{x}]', assertion["ancestorTitles"])
    #formatted_ancestors = ": ".join(map(lambda x: f'[{x}]', assertion["ancestors"])
    formatted_ancestors = "".join(ancestors)
    regex=r'^(\(\s*(\d+)\s*pt[s]?[\s]*\))?(.*?)(!!.+)?$'
    match = re.search(regex, assertion["title"])
    title = match.group(3)
    return f'{formatted_ancestors}: {title}'

def get_max_score(assertion):
    regex=r'^(\(\s*(\d+)\s*pt[s]?[\s]*\))?(.*)$'
    match = re.search(regex, assertion["title"])
    return match.group(2)

def get_visibility(assertion):
    regex=r'^(\(\s*(\d+)\s*pt[s]?[\s]*\))?(.*?)(!!.+)?$'
    match = re.search(regex, assertion["title"])
    status = match.group(4) or "visible"
    status = "hidden" if status == 'hide' else status
    return match.group(4)

def get_score(assertion):
    max_score = get_max_score(assertion)
    if assertion["status"]=="passed":
        return max_score
    else:
        return 0

def get_output(assertion, visibility):
    if visibility == 'secret':
        return "This test case is secret."
    return "\n".join(assertion["failureMessages"])

def main():

    # Initialize command line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", help="Input file to read (produced by jest)")
    parser.add_argument("-c", "--coverage", help="Coverage file to read (produced by jest)")
    parser.add_argument("-o", "--output", help="Output file to produce (in Gradescope format)")
    #parser.add_argument("-s", "--settings", help="Configuration settings file path")
    args = parser.parse_args()
    
    #if args.settings != None:
    #    with open(args.settings,'r') as settings_file:
    #        pass
    # TODO: Allow coverage configuration from grading.config
    # Default threshold before "success" is granted
    CONFIG_COVERAGE_THRESHOLD_LINES=80
    # Points to award for getting the given threshold
    CONFIG_COVERAGE_THRESHOLD_SCORE=5
    # Alternative mode to not run tests without sufficient code coverage
    CONFIG_COVERAGE_THRESHOLD_STRICT=False


    jest_data = {}

    if args.input != None:
        with open(args.input,'r') as json_data:
            jest_data = json.load(json_data)
            # We don't need the coverageMap, just takes up unnecessary space.
            jest_data.pop('coverageMap')
            
    if args.coverage != None:
        with open(args.coverage, 'r') as coverage_data:
            coverage_data = json.load(coverage_data)


    assertions = list(flatten(map(lambda x:x["assertionResults"], jest_data["testResults"])))
    gradescope_tests = list(map(jest_assertion_to_gradescope, assertions))

    if not jest_data["success"]:
        # TODO: Show this data based on whether there are any hidden/secret tests?
        #messages = "\n".join(list(map(lambda x:x["message"].replace("\"","\\\""), jest_data["testResults"])))
        messages = "One or more of the Jest tests failed."
        
        gradescope_tests.append({
            "name": "Jest test(s) failed",
            "max_score": 1,
            "score": 0, 
            "output": messages
        })
        
    if "total" in coverage_data:
        lines = coverage_data.get("total", {}).get("lines", {})
        pct = lines.get("pct", 0)
        total_lines, lines_covered, lines_skipped = (
            lines.get("total", 0),
            lines.get("covered", 0),
            lines.get("skipped", 0)
        )
        good_coverage = pct > CONFIG_COVERAGE_THRESHOLD_LINES
        coverage_status = "Good" if good_coverage else "Inadequate"
        coverage_output = "\n".join([
            f"Coverage percentage: {pct}%",
            f"Total Lines: {total_lines}",
            f"Lines Covered: {lines_covered}",
            f"Lines Skipped: {lines_skipped}",
        ])
        gradescope_tests.append({
            "name": f"Coverage Status: {coverage_status}",
            "max_score": CONFIG_COVERAGE_THRESHOLD_SCORE,
            "score": CONFIG_COVERAGE_THRESHOLD_SCORE if good_coverage else 0,
            "output": coverage_output
        })

    print("jest_data",json.dumps(jest_data, indent=2))
    print("assertions",json.dumps(assertions, indent=2))
    print("gradescope_tests",json.dumps(gradescope_tests, indent=2))
    print("coverage", json.dumps(coverage_data, indent=2))
    # TODO: Add in file integrity checks
    # TODO: Add in linter report
    # TODO: Add in check that the remote site does not 404

    if args.output != None:
      with open(args.output,'w') as json_data:
        json.dump({ "tests": gradescope_tests}, json_data,indent=2,sort_keys=True)


if __name__=="__main__":
  main()