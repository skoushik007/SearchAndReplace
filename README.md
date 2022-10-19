# EfficientSearchAndReplace
simple and efficient Search and replace program that can search for multiple search strings and if matches are found replace it with replace string. 
It runs through the text string only once and uses constant memory buffer in the application level. 
So this program doesn't load whole file and then do the processing and hence suitable for stream processing along side with kafka(for eg:)

 
SearchReplace class runs though the text just once and hence the main processing runs in o(n) time with o(1) space.

Trie class does pre processing on the search and replace string given as the json file as a parameter to the main program. Pre processing takes o(n + m) time and o(n + m)space,
	n is the total number of characters in the search strings.
    m is the total number of characters in the replace strings.

Usage:

Python  main.py  <in_file> <search_replace_file in json>

in_file -> contains the text that will be processed.
search_replace_file->contains the search and replace in json format.