# ISD_Parse
Parser for Silicon Labs Network Analyzer capture logs.

.isd files are ZIP format.  This script reads event.log files
contained in .isd.  The .isd file should be unzipped.  In case of long
captures, there will be multiple number eventX.log files.

## Example usage:
<pre>
sh$ isd-parse -h
Usage: /home/bofh/bin/isd-parse [ options ] &lt;isd-log-file&gt;
Options:
     --supress-pti : suppress rendering of unexceptional data 
                -h : show this help                           
sh$ isd-parse --suppress-pti ../event.log 
0.398715: ['00', '25', 'FF', 'AA', 'AA', 'AA', 'AA', 'AA', 'AA', '7A', 'B4', 'B3', '51', '89', '63', 'AB', '23', '23', '02', '84', '18', '72', 'AA', '61', '2F', '3B', '51', 'A8', 'E5', '37', '49', 'FB', 'C9', 'CA', '0C', '18', '53', '2C', 'FD', '47', '84', '17'] CRC FAILURE
sh$ 
</pre>
