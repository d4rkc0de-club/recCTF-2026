```
docker build -t helper-site-gta .
```

```bash
docker run -d \
  --name helper-site-gta \
  -p 127.0.0.1:3001:80 \
  helper-site-gta

```
