#!/usr/bin/env python3

import os
import subprocess
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def validate_schema(target, schema, prefix=""):
    for (key, value) in schema.items():
        if not key in target:
            raise ValueError("Expected to find '%s%s' value in config" % (prefix, key))

        if not type(value) == type(target[key]):
            raise ValueError("Expected '%s%s' to be %s, found %s" % (prefix, key, type(value).__name__, type(target[key]).__name__))

        if isinstance(value, dict):
            validate_schema(target[key], schema[key], "%s." % key)

def write_private_key(path, private_key):
    private_key_path = "%s/id_rsa" % path
    
    file = open(private_key_path, "w")
    file.write(private_key)
    file.close()

    os.chmod(private_key_path, 0o600)

    return private_key_path

def scpTo(user, host, port, private_key_path, path, files):
    return _scp(user, host, port, private_key_path, path, files, True)

def scpFrom(user, host, port, private_key_path, path, files):
    return _scp(user, host, port, private_key_path, path, files, False)

def _scp(user, host, port, private_key_path, path, files, toRemote):
    if not isinstance(files, dict):
        raise ValueError("Expected 'files' to be a dict, found %s" % type(files).__name__)

    for (source_file, destination_file) in files.items():
        source = "%s/%s" % (path, source_file) if toRemote else "%s@%s:%s" % (user, host, source_file)
        destination = "%s@%s:%s" % (user, host, destination_file) if toRemote else "%s/%s" % (path, destination_file)

        print(f"{source} -> {destination}")
        cmd = ["scp", "-oStrictHostKeyChecking=no", "-i", private_key_path, "-P", port, "-r", source, destination]
        print(" ".join(cmd))
        proc = subprocess.run(cmd, check=True, stdout=subprocess.PIPE)
        eprint(proc.stdout.decode("utf-8"))

def sshRun(user, host, port, private_key_path, commands):
    if not isinstance(commands, list):
        raise ValueError("Expected 'commands' to be a list, found %s" % type(commands).__name__)
    
    print(commands)
    cmd = ["ssh", "-oStrictHostKeyChecking=no", "-i", private_key_path, "%s@%s" % (user, host), "-p", port, "%s" % " && ".join(commands)]
    print(" ".join(cmd))
    proc = subprocess.run(cmd, check=True, stdout=subprocess.PIPE)
    eprint(proc.stdout.decode("utf-8"))
