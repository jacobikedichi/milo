peak_finder.py:

Uses Google elevation API to calculate the highest elevation between 2 points.  
For additional help, do: 
```python
python peak_finder.py --help
```
Usage:
python peak_finder lat1,lon1 lat2,lon2 [@@ sample number]  

'@@' symbol is used to pass in optional argument

i.e. python peak_finder.py -3.184523,37.295864 -2.936312,37.446926 @@sample 50

Note that 'sample' is an optional argument and is not required to be passed in. If not passed in, it defaults to 100


#####Sample-Output:#####
```python
python peak_finder.py -3.184523,37.295864 -2.936312,37.446926 @@sample 77
5798.45849609
```

