# Prometheus exporter for SP500 rate from yahoo finance

## Installation
Just run 
```
kubectl apply -f kubernetes/sp500exporter.yml
```

You do not need to compile anything, image is already published. In Prometheus modify configuration to use
**prometheus/scrape-config.yml**

## Example output
```
kubectl exec -it busybox -- curl sp500exporter-service:9100/metrics
stock_price{stock="sp500"} 455.20001220703125
```
