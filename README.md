# okitpricing2mysql (WIP for integration)
moving okit pricing database from Oracle Autonomous DB(ADB) to a local MySQL container.
Currently, okit is deployed locally in your laptop and it retrieves pricing information from database running in Oracle cloud, which is managed by myself.
Plan is to have a local database running in docker to minimize latency. 

Now I am accessing Oracle ADB using ORDS(Oracle REST Data Services), I will do the same approach to minimize my code changes.

What is OKIT?
Please visit: https://github.com/oracle/oci-designer-toolkit

Quick demo access (not the latest version): http://okit.oci.cool/okit/designer

### Run REST API
```sh
python app.py
```

![](images/test.png)
