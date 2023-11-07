package main

import (
	"log"
    "os/exec"
    "runtime/debug"
)

func main() {
    cmd := exec.Command("/bin/bash", "-c",  "echo \"sha: \"$(date +\"%Y%m%d%H%M%S\") > /workspace/kapp-marker.yaml;")
    stdout, err := cmd.Output()
    if err == nil {
        log.Println(string(stdout))
    } else {
        log.Fatal(err)
        debug.PrintStack()
    }
}