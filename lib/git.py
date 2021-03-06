import subprocess


def clone(url, repo_root):
    p = subprocess.run(['git', 'clone', url, repo_root],
                       capture_output=True)

    if p.returncode != 0:
        raise IOError(p.stderr.decode("utf8"))


def blame(file, repo_root):
    p = subprocess.run(["git", "blame", "--line-porcelain", file],
                       capture_output=True,
                       cwd=repo_root)

    if p.returncode != 0:
        raise IOError(p.stderr.decode("utf8"))
    return p.stdout.decode("utf8").split("\n")


def ls_files(repo_root, dir=None):
    args = ["git", "ls-files"]
    if dir is not None:
        args.append(dir)

    p = subprocess.run(args,
                       capture_output=True,
                       cwd=repo_root)

    if p.returncode != 0:
        raise IOError(p.stderr.decode("utf8"))
    return p.stdout.decode("utf8").split("\n")


def log(repo_root, rev_range):
    # TODO: improve format
    args = ["git", "log",
            "--format=%H (%s, %cs)",
            "--date=iso-strict", rev_range,
            "--reverse"]
            # ]
    p = subprocess.run(args,
                       capture_output=True,
                       cwd=repo_root)

    if p.returncode != 0:
        raise IOError(p.stderr.decode(("utf8")))
    return p.stdout.decode("utf8").split("\n")
