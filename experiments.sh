#!/bin/sh
mkdir ../outputs/Test1/
mkdir ../outputs/Test1/Markdown
bsub -o "../outputs/Test1/Markdown/Test1_0.md" -J "Test1_0" -env MYARGS="-name Test1-0 -num 0" < submit_cpu.sh
