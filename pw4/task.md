# Practical work 4: Word Count

- Create a new directory named «WordCount»
- Use any MapReduce framework of your choice to implement
Word Count example
  - Java is OK
  - C/C++ is still preferred
    - No MapReduce framework for C/C++ at the moment
    - Invent yourself
- Write a short report in LATEX:
  - Name it « 04.word.count.tex »
  - Why you chose your specific MapReduce implementation
  - How your Mapper and Reducer work. Figure.
  - Who does what.
- Work in your group, in parallel
- Push your report to corresponding forked Github repository

## the Word Count example

- The classic example for MapReduce
- Input: a large text file
- Output : number of occurrence of each word

YOU ARE SEEING ME IMPLEMENT THIS IN ONE LINE OF PYTHON
one line

```python
print(collections.Counter(r for r in re.split(r"\W+", pathlib.Path(sys.argv[1]).read_text("utf-8")) if r))
```

usage:

```pwsh
python map_reduce.py fuckass.txt
```
