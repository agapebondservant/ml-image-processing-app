## Deployment

### Deploy the API App

* Deploy the app:
```
tanzu apps workload create image-processor-api-kfp -f config/workload.yaml --yes
```

* Tail the logs:
```
tanzu apps workload tail image-processor-api-kfp --since 64h
```

* Once deployment succeeds, get the URL for the app:
```
tanzu apps workload get image-processor-api-kfp #should yield image-processor-api-kfp.default.<your-domain>
```

* To delete the app:
```
tanzu apps workload delete image-processor-api-kfp --yes
```
