"""
Python utility to execute behave based tests in parallel mode
Usage:
python behave-parallel.py -p=<num_of_process> -t=<bdd_tag> -F=<features_location> -D <user_defined_key_value>

Default Values:
num_of_process = 5
features_location = reusable_bdd_api/tests/features/

if tags are not provided, all the features will be executed
if tags are provided, feature containing tagged scenarios will be executed
As of now, only feature level parallelization is supported and not scenario level.
"""
import shutil
from multiprocessing import Pool
from subprocess import call, Popen, PIPE
from glob import glob
import logging
import argparse
import json
from functools import partial
import os

logging.basicConfig(level=logging.INFO,
                    format="[%(levelname)-8s %(asctime)s] %(message)s")
logger = logging.getLogger(__name__)


def parse_arguments():
    """
    Parses commandline arguments
    :return: Parsed arguments
    """
    parser = argparse.ArgumentParser('Run Behave in parallel mode')
    parser.add_argument('--allure_reporting', help='If you want to generate allure reports or not', default="false")
    parser.add_argument('--junit_reporting', help='If you want to generate junit reports or not', default="false")
    parser.add_argument('--processes', '-p', type=int, help='Maximum number of processes. Default = 5', default=5)
    parser.add_argument('--junit', '-j', action='store_true', help='Junit report')
    parser.add_argument('--junit_directory', '-J', help='Junit report location', default='reports/')
    parser.add_argument('--tags', '-t', help='specify behave tags to run')
    parser.add_argument('--define', '-D', action='append',
                        help='Define user-specific data for the config.userdata dictionary')
    parser.add_argument('--features', '-F', help='specify feature or location. Default=tests/features/',
                        default='tests/features/*.feature')

    args = parser.parse_args()
    return args


def _run_parallel_feature(feature, tags=None, userdata=None, report_loc=None, args=None):
    """
    Runs features matching given tags and userdata
    :param feature: Feature that should be run
    :type feature: str
    :param tags: Tags features should contain
    :type tags: str
    :param userdata: Userdata for behave
    :type userdata: list
    :return: Feature and status
    """

    logger.info("Processing feature: {}".format(feature))
    params = ""
    if userdata:
        params = params + " -D {0} --no-capture".format(' -D '.join(userdata))
    if report_loc and str(args.junit_reporting).lower() == 'true':
        params = params + " --junit --junit-directory {}".format(report_loc)
    if str(args.allure_reporting).lower() == 'true':
        params = params + " -f allure_behave.formatter:AllureFormatter -o allure_reports/results"
    cmd = "behave {0} {1}".format(params, feature)
    logger.info("Behave command for parallel execution: {}".format(cmd))
    r = call(cmd, shell=True)
    status = 'ok' if r == 0 else 'failed'
    return feature, status


def run_sequential(args):
    """
    This uses to execute the test scenario sequentially
    """
    if os.path.exists("reports"):
        shutil.rmtree("reports")
    if os.path.exists("allure_reports"):
        shutil.rmtree("allure_reports")
    feature_path = "tests/features/"
    params = ""
    if args.define:
        params = params + " -D {0} --no-capture".format(' -D '.join(args.define))
    if str(args.junit_reporting).lower() == 'true' and args.junit_directory:
        params = params + " --junit --junit-directory {}".format(args.junit_directory)
    if str(args.allure_reporting).lower() == 'true':
        params = params + " -f allure_behave.formatter:AllureFormatter -o allure_reports/results"

    cmd = 'behave {0} {1}'.format(params, feature_path)
    logger.info("Executing scenarios in sequential mode: {}".format(cmd))
    r = call(cmd, shell=True)
    status = 'ok' if r == 0 else 'failed'
    print "Sequential Execution Status:" + status


def run_parallel(args, pool):
    """
    This uses to execute the features parallel
    """

    if os.path.exists("reports"):
        shutil.rmtree("reports")
    if os.path.exists("allure_reports"):
        shutil.rmtree("allure_reports")
    logger.info("Executing suite in parallel")
    if args.tags:
        p = Popen('behave {0} -d -f json --no-summary -t {1}'.format(args.features, args.tags),
                  stdout=PIPE, shell=True)
        out, err = p.communicate()
        j = json.loads(out.decode())
        features = [e['location'].replace(args.features, '')[:-2] for e in j if e['status'] == 'untested']
    else:
        feature_files = glob(args.features)
        features = feature_files
    run_feature = partial(_run_parallel_feature, tags=args.tags, userdata=args.define,
                          report_loc=args.junit_directory, args=args)
    logger.info("Found {} features".format(len(features)))
    logger.info(features)
    features = [f for f in features if 'aft' not in f]
    for feature, status in pool.map(run_feature, features):
        print("{0:50}: {1}!!".format(feature, status))


def main():
    """
    Runner
    """
    args = parse_arguments()
    pool = Pool(args.processes)

    if args.processes > 1:
        run_parallel(args, pool)
    elif args.processes == 1:
        run_sequential(args)

    if str(args.allure_reporting).lower() == 'true':
        cmd = 'allure generate allure_reports/results/ -o allure_reports/html_reports'
        logger.info("Generating allure reports by : {}".format(cmd))
        r = call(cmd, shell=True)
        status = 'ok' if r == 0 else 'failed'
        print "Allure Report Generation Status:" + status


if __name__ == '__main__':
    main()
