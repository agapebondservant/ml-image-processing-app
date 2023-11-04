# ML Image Processing App

<img src="image.png"
alt="Markdown Monster icon"
style="float: left; margin-right: 10px;" />

## Pre-requisites

* Required installations:
  [ ] Kubernetes cluster
  [ ] Tanzu Application Platform
  [ ] MLflow Tracking Server
  [ ] Greenplum instance (Required for in-database pipeline)
  [ ] Postgres instance (Required for in-database pipeline)

* Set up a **pre-commit** Git hook which will take care of autogenerating OpenAPI docs:
```
tee -a .git/hooks/pre-commit <<FILE
echo "Generate OpenAPI schema docs................"
$(which python3) -c "from app.analytics import api; api.generate_schema()"
echo "OpenAPI schema docs generated."
echo "Adding OpenAPI schema to repo..."
git add app/analytics/static/openapi.json
FILE
```

* Install **kappgit** (community executable which will automatically add a new marker file on commit):
```
wget -O /usr/local/bin/kappgit https://raw.githubusercontent.com/agapebondservant/kappgit/main/kappgit
chmod +x /usr/local/bin/kappgit
kappgit
```

* Set up secrets:
```
source .env
tanzu secret registry delete registry-credentials -n default -y || true
tanzu secret registry add registry-credentials --username ${DATA_E2E_REGISTRY_USERNAME} --password ${DATA_E2E_REGISTRY_PASSWORD} --server https://index.docker.io/v1/ --export-to-all-namespaces --yes -ndefault
kubectl apply -f config/tap-rbac.yaml -ndefault
kubectl apply -f config/tap-rbac-2.yaml -ndefault
```

* Set up Argo Workflows (if not already setup):
```
source .env
kubectl create ns argo
kubectl apply -f config/argo-workflow.yaml -nargo
envsubst < config/argo-workflow-http-proxy.in.yaml > config/argo-workflow-http-proxy.yaml
kubectl apply -f config/argo-workflow-http-proxy.yaml -nargo
kubectl create rolebinding default-admin --clusterrole=admin --serviceaccount=argo:default -n argo
kubectl apply -f config/argo-workflow-rbac.yaml -nargo
```

* Login to Argo - copy the token from here:
```
kubectl -n argo exec $(kubectl get pod -n argo -l 'app=argo-server' -o jsonpath='{.items[0].metadata.name}') -- argo auth token
```

## Deploy the Analytics App

* Deploy the app:
```
source .env
envsubst < config/workload.in.yaml > config/workload.yaml
tanzu apps workload create image-processor -f config/workload.yaml --yes
```

* Tail the logs of the main app:
```
tanzu apps workload tail image-processor --since 64h
```

* Once deployment succeeds, get the URL for the main app:
```
tanzu apps workload get image-processor     #should yield image-processor.default.<your-domain>
```

* To delete the app:
```
tanzu apps workload delete image-processor --yes
```

## Deploy the Training Pipeline
* cd to </root/of/branch/directory/with/appropriate/model/stage> 
(Example: the **main** github branch represents the "main" environment, the **staging** github branch represents the "staging" environment, etc)

* Deploy the pipeline:
```
ytt -f config/cifar/pipeline_app.yaml -f config/cifar/values.yaml | kapp deploy -a image-procesor-pipeline-<THE PIPELINE ENVIRONMENT> --logs -y  -nargo -f -
```

* View progress:
```
kubectl get app ml-image-processing-pipeline-<THE PIPELINE ENVIRONMENT> -oyaml  -nargo
```

* View the pipeline in the browser by navigating to https://argo-workflows.<your-domain-name> -
access the Login token by running
```
kubectl -n argo exec $(kubectl get pod -n argo -l 'app=argo-server' -o jsonpath='{.items[0].metadata.name}') -- argo auth token
```

* To delete the pipeline:
```
kapp delete -a image-procesor-pipeline-<THE PIPELINE ENVIRONMENT> -y -nargo
```

## Deploy the Training Pipeline Templates
* cd to </root/of/branch/directory/with/appropriate/model/stage>
  (Example: the **main** github branch represents the "main" environment, the **staging** github branch represents the "staging" environment, etc)

* Deploy the pipeline templates:
```
ytt -f config/templates/ | kubectl apply -n argo -f -
```

* View progress:
```
watch kubectl get pods -nargo
```

* To delete the pipeline templates:
```
ytt -f config/templates/ | kubectl delete -n argo -f -
```
