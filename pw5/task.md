# Practical work 5: The Longest Path

- Use any MapReduce framework of your choice to implement
LongestPath toy project
  - Input: set of files, one for each of your laptops
    - Each line contain one full path of a file
    - find /
  - Output: longest path(s)
- Write a short report in LATEX:
  - Name it « 05.word.count.tex »
  - How your Mapper and Reducer work. Figure.
  - Who does what.
- Work in your group, in parallel
- Push your report to corresponding forked Github repository

## PLEASE RUN `find /` on your own linux computer

in fact do `find / >> file.txt` to archive it + use the result!

## WHAT EVEN IS longest path

is it the most nodes to go from a file to another?
like

```text
/a/b/c/d/e/f/g/h/j/i/k/k/l -> /w/e/r/t/y/u/i/o/p/a/s/d/f/g/h/j/k/l
-> ../../../../../../../../../../../../../w/e/r/t/y/u/i/o/p/a/s/d/f/g/h/j/k/l ????
```

or is it just pure `len()`?
