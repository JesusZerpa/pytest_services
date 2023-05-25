```
controller=Controller()
service=Service("service-1")
service.step("paso-1")

```

```
service=Service("service-1",contoller="127.0.0.1:5000")
service.check("paso-1",True)
```