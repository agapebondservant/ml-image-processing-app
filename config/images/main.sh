#!/bin/bash
echo "sha: " | cat - /layers/paketo-buildpacks_git/git/env/REVISION.default > /layers/paketo-buildpacks_git/git/env/REVISION.patched
bash