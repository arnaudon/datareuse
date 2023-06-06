# DataReuse
Tool to reuse saved computations with various file formats.

It can be used as follows:

```
    from datareuse import Reuse
    
    with Reuse("data.csv", index=False, index_col=1) as reuse:
        df = reuse(computation, *args, **kwargs)
```

At the moment, the following file formats are available:
- csv (pandas)
