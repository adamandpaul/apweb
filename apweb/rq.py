# -*- coding:utf-8 -*-

import rq.cli
import sys


def run_worker(cmd_context):
    argv = [sys.argv[0]]
    argv.extend(cmd_context.args.worker_args)
    sys.argv = argv
    rq.cli.worker()


def cmd_configure(sub_commands):
    worker_parser = sub_commands.add_parser("rq-worker")
    worker_parser.add_argument("worker_args", nargs=argparse.REMAINDER)
